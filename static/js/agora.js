(function ($) {
    // Handle showing the login popup
    var handleLoginLink = function () {
        var loginLink = $('.login-link');

        if (loginLink.length) {
            loginLink.click(function () {
                $('#login-popup').show();

                return false;
            });

            $('#login-popup').click(function (event) {
                // Only catch events in the outer, overlay div
                if (event.target === this) {
                    $(this).hide();
                }
            });
        }
    };

    $(document).ready(function () {
        handleLoginLink();

        // Add in the line numbers (no JS fallback unfortunately)
        if ($('.snippet').length) {
            var counter = 1;

            $('.code-lines').children().each(function () {
                // Set the top offset to be the same as that of the line
                var div = '<p style="top: ' + this.offsetTop + 'px">' +
                    '<a href="#l' + counter + '">' + counter + '</a></p>';
                counter++;
                $('.line-counters').append(div);
            });
        }
    });
})(jQuery);
