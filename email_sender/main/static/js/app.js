$(document).ready( function () {

    $('#submit').on({
        'click': function () {

            $.ajax({
                'type': 'POST',
                'url': '/post_msg',
                'dataType': 'json',
                'data': $('#form').serialize(),
                success: function (msg) {
                    console.log(msg);
                    $('#fail').hide();
                    $('#success').show();
                },
                error: function (response) {
                    let responseJson = JSON.parse(response.responseText);
                    console.log(responseJson);
                    console.log(responseJson.error);
                    $(".error_msg").text(responseJson.error);
                    $('#success').hide();
                    $('#fail').show();
                }
            });
        }
    });
});