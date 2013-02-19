from __future__ import with_statement

import mimetypes
import os

import archive
import magic
from celery import task

from apps.bundle.models import Bundle, BundleFile, BundleVersion


mimetypes.add_type('application/x-gzip', '.tgz')
mimetypes.add_type('application/x-bzip2', '.tz2')
archive_extensions = ('.zip', '.tgz', '.tar', '.tz2')
text_mimetypes = (
    'application/xml',
)


def process_files_in_dir(bundle, dir_name, parent_dir):
    """
    Go through all the subdirectories and files (in that order) in this
    directory.
    """
    dir_contents = [os.path.join(dir_name, f) for f in os.listdir(dir_name)]
    dirs = filter(os.path.isdir, dir_contents)
    files = filter(os.path.isfile, dir_contents)

    for file_path in sorted(dirs) + sorted(files):
        filename = os.path.basename(file_path)
        full_path = file_path[len(bundle.get_temp_path()) + 1:]
        bundle_file = BundleFile(bundle=bundle, name=filename,
            parent=parent_dir, full_path=full_path,
            version=bundle.latest_version)

        if file_path in files:
            is_desc = False
            bundle_file.is_dir = False
            bundle_file.file_size = os.path.getsize(file_path)

            # Only highlight the file contents if it's plain text
            mime_type = magic.from_file(file_path, mime=True)
            if mime_type.startswith('text/') or mime_type in text_mimetypes:
                with open(file_path, 'rt') as file:
                    # Store the contents of the file in the code field
                    bundle_file.save_file_contents(file)

                    # DESCRIPTION file should be at most 1 level deep
                    single_parent = (parent_dir is not None or
                        '/' not in parent_dir)
                    is_desc = single_parent and filename == 'DESCRIPTION'

            # Check if this is the description file (if no description exists)
            if bundle.octave_format and bundle.description == '' and is_desc:
                bundle.description_file = bundle_file
                bundle.save()

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

    if extension in archive_extensions:
        new_path = file + extension
        # Save the new file name (needed for the BundleVersion)

        new_file_name = os.path.basename(new_path)
        # Treat it as an archive. Rename it to that, then extract
        os.rename(file, new_path)

        try:
            # Extract it to a directory, same path as the filename
            archive.extract(new_path, to_path=file)

            # Now go through the extracted files, make BundleFiles from them
            process_files_in_dir(bundle, file, None)
        except archive.ArchiveException:
            pass
    elif mime_type.startswith('text/'):
        # Should be a plain text file - create a CodeFile for it
        bundle_file = BundleFile(bundle=bundle, name=bundle.file_name,
            full_path=bundle.file_name, file_size=os.path.getsize(file),
            version=bundle.latest_version)
        bundle_file.save_file_contents(open(file, 'rt'),
            original_filename=bundle.file_name)
        new_file_name = os.path.basename(file)

    # Create the new BundleVersion
    BundleVersion.objects.create(bundle=bundle, file_name=new_file_name,
        version=bundle.latest_version)

    bundle.done_uploading = True
    bundle.save()
