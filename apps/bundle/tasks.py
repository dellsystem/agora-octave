import mimetypes
import os

import archive
import magic
from celery import task

from apps.bundle.models import Bundle, BundleFile


mimetypes.add_type('application/x-gzip', '.tgz')
mimetypes.add_type('application/x-bzip2', '.tz2')
archive_extensions = ('.zip', '.tgz', '.tar', '.tz2')


def process_files_in_dir(bundle, dir_name, parent_dir):
    """
    Go through all the subdirectories and files (in that order) in this
    directory.
    """
    dir_contents = [os.path.join(dir_name, f) for f in os.listdir(dir_name)]
    dirs = filter(os.path.isdir, dir_contents)
    files = filter(os.path.isfile, dir_contents)
    print "Directories: %s" % ", ".join(dirs)
    print "Files: %s" % ", ".join(files)

    for file_path in sorted(dirs) + sorted(files):
        filename = os.path.basename(file_path)
        full_path = file_path[len(bundle.get_temp_path()) + 1:]
        bundle_file = BundleFile(bundle=bundle, name=filename,
            parent=parent_dir, full_path=full_path)

        if file_path in files:
            bundle_file.is_dir = False
            bundle_file.file_size = os.path.getsize(file_path)

            # Only highlight the file contents if it's plain text
            mime_type = magic.from_file(file_path, mime=True)
            if mime_type.startswith('text/'):
                with open(file_path, 'rt') as file:
                    # Store the contents of the file in the code field
                    bundle_file.save_file_contents(file)

            bundle_file.save()
        else:
            # It's a directory - call this function on it recursively
            bundle_file.is_dir = True
            bundle_file.save()
            process_files_in_dir(bundle, file_path, bundle_file)

@task()
def handle_bundle_upload(bundle_id):
    bundle = Bundle.objects.get(pk=bundle_id)
    file = bundle.get_temp_path()

    # Figure out the most likely mime-type
    mime_type = magic.from_file(file, mime=True)
    extension = mimetypes.guess_extension(mime_type)

    print "mime type: %s" % mime_type
    print "extension: %s" % extension

    if extension in archive_extensions:
        new_path = file + extension
        # Treat it as an archive. Rename it to that, then extract
        os.rename(file, new_path)

        try:
            # Extract it to a directory, same path as the filename
            archive.extract(new_path, to_path=file)

            # Now go through the extracted files, make BundleFiles from them
            process_files_in_dir(bundle, file, None)
        except archive.ArchiveException:
            print "Archive exception"
            pass
    elif mime_type.startswith('text/'):
        # Should be a plain text file - create a CodeFile for it
        bundle_file = BundleFile(bundle=bundle, name=bundle.file_name,
            full_path=bundle.file_name, file_size=os.path.getsize(file))
        bundle_file.save_file_contents(open(file, 'rt'),
            original_filename=bundle.file_name)

    print "Done uploading!"
    bundle.done_uploading = True
    bundle.save()
