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
    });
})(jQuery);
