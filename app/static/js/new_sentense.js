$('#add_text_btn').on('click', function (e) {
    var newId = 1;
    if ($(".text_block"))
        newId = $(".text_block").length + 1;
    var html = ' <div class="form-group text_block"><label class="col-md-2 control-label">Text block '+newId+'&nbsp;</label><div class="col-md-10"><input class="form-control text_input" id="text'+newId+'" name="text"></div></div>';
    $("#sentense").append(html);
});

$('#add_blank_btn').on('click', function (e) {
    var s_id = $('#section').val();
    if(s_id == '__None')
        alert('First select a section');
    else{
        var newId = 1;
        if ($(".blank_block"))
            newId = $(".blank_block").length + 1;
        $.ajax({
                url: '/api/words/' + s_id,
                method: 'get',
                dataType: 'json',
                success: function (data) {
                    var html = '<div class="form-group blank_block"><label class="col-md-2 control-label">Right word '+newId+'&nbsp;</label><div class="col-md-10 right_word"><select class="form-control " data-allow-blank="1" data-role="select2" id="right_word'+newId+'"><option selected value="__None"></option>';
                    data.forEach(function(item, i, data) {
                            html += '<option value="'+item.id+'">'+item.enWord+'</option>';
                        });
                    html += '</select></div></div>';
                    $("#sentense").append(html);
                }
            });
    }
});

$("#create_form").submit(function (e) {
    var s_id = $('#section').val();
    var clicked_btn = $(this).find("input[type=submit]:focus" );
    if(s_id == '__None')
        alert('Select a section');
    var sentense_data = {
        s_id: s_id,
        btn: clicked_btn.val()
    }
    var items = $('.text_input');
    var texts = [];
    for (let i = 0; i < items.length; i++)
        texts.push(items[i].value);
    items = $('.right_word');
    var blanks = [];

    for (let i = 1; i < items.length + 1; i++){
        var val = $('#right_word' + i).val();
        if (val == '__None'){
            alert("You didn't choose word number " + i);
            return false;
        }
        else
            blanks.push($('#right_word' + i).val());
    }
    sentense_data['texts[]'] = texts;
    sentense_data['blanks[]'] = blanks;
    $.ajax({
        url: '/add_sentense',
        method: 'post',
        dataType: 'json',
        data: sentense_data,
        success: function (data) {
            if(data['status']==1)
                window.location.href = data.url;
            else{
                alter(data.error);
            }
        }
    });
    return false;
    });