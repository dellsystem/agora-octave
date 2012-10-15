jQuery(document).ready(function () {

    curLine = document.location.hash;
    if(curLine.substring(0,2) == '#l'){
        $('div.snippet div.line'+curLine).addClass('marked');
    }

    /**
    * Diff Ajax Call
    */
    $("form#diffform").submit(function() {
        $.get("{% url snippet_diff %}", {
            a: $("input[name=a]:checked").val(),
            b: $("input[name=b]:checked").val()
        }, function(data){
            $('#diff').html(data).slideDown('fast');
        });
        return false;
    });

    /**
    * Line Highlighting
    */
    $('div.snippet th a').each(function(i){
        $(this).click(function(){
            var j = $(this).text();
            $('div.snippet div.line.marked').removeClass('marked');
            $('div.snippet div.line#l'+j).toggleClass('marked');
        });
    });

    //{% if request.session.userprefs.display_all_lexer %}
    /**
    * Lexer Guessing
    */
    $('#guess_lexer_btn').click(function(){
        $.getJSON('{% url snippet_guess_lexer %}',
            {'codestring': $('#id_content').val()},
            function(data){
                if(data.lexer == "unknown"){
                    $('#guess_lexer_btn').css('color', 'red');
                }else{
                    $('#id_lexer').val(data.lexer);
                    $('#guess_lexer_btn').css('color', 'inherit');
                }
            });
    });
    //{% endif %}
});
