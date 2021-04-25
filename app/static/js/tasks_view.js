function update_tasks_on_screen(section_id){
    $.ajax({
                url: '/api/tasks/' + section_id,
                method: 'get',
                dataType: 'json',
                success: function (data) {
                    $('#content-title').css("display", "block");
                    $('#add_task_block').css("display", "block");
                    if(data.length == 0){
                        $("#content").html('<div class="form-group"><label class="col-md-2 control-label"></label><h2 class="col-md-10 control-label">This section is empty yet</h2></div>')
                    }
                    else{
                        var html = '<div class="form-group"><label class="col-md-12 control-label"></label><ol>';
                        data.forEach(function(item, i, data) {
                            html += '<label class="col-md-2 control-label"></label><li class="col-md-10 control-label"><div class="li_flex"><h3>';
                            switch(item.type) {
                              case 1:
                                html += 'WORDS: Theory';
                                break;
                              case 2:
                                html += 'WORDS: Translate from EN to RU';
                                break;
                              case 3:
                                html += 'WORDS: Translate from RU to EN';
                                break;
                              case 4:
                                html += 'WORDS: Choose by definition';
                                break;
                              case 5:
                                html += 'WORDS: Make a word from letters'; break;
                              case 6:
                                html += 'WORDS: Choose by audio'; break;
                              case 7:
                                html += 'WORDS: Write by audio'; break;
                              case 8:
                                html += 'COLLOCATIONS: Theory'; break;
                              case 9:
                                html += 'COLLOCATIONS: Translate from EN to RU'; break;
                              case 10:
                                html += 'COLLOCATIONS: Translate from RU to EN'; break;
                              case 11:
                                html += 'COLLOCATIONS: Match beginning and end'; break;
                              case 11:
                                html += 'SENTENSES: Insert missing word'; break;
                            }
                            html += '</h3><button type="button" class="x_btn" onclick="confirm(\'Delete this task?\') ? delete_task(' + item.id +') : \'\'">x</button></div></li>';
                        });
                        html += '</ol></div>';
                        $("#content").html(html);
                    }
                }
            });
}

$('#section_select').on('change', function (e) {
        var s_id = $('#section_select').val();
        if (s_id) {
            update_tasks_on_screen(s_id);
        }
    });

$('#add_task_btn').on('click', function (e) {
    var s_id = $('#section_select').val();
    var t_id = $('#new_task_type').val();
    if(t_id){
        $.ajax({
                url: '/add_task',
                method: 'post',
                dataType: 'json',
                data: {'s_id': s_id, 't_id': t_id},
                success: function (data) {
                    if(data.status == 'ok')
                        //window.location.reload(true);
                        update_tasks_on_screen(s_id);
                }
            });
    }
    else{
        alert("Choose task's type");
    }
});

function delete_task(task_id){
    var s_id = $('#section_select').val();
    $.ajax({
        url: '/delete_task/' + task_id,
        method: 'post',
        dataType: 'json',
        success: function (data) {
            update_tasks_on_screen(s_id);
        }
    });
}