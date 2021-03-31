$(document).ready(function() {

});

$('#section_select').on('change', function (e) {
        var s_id = $('#section_select').val();
        if (s_id) {
            $.ajax({
                url: '/api/tasks/' + s_id,
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
                            html += '<label class="col-md-2 control-label"></label><li class="col-md-10 control-label"><h3>';
                            console.log(item.taskType);
                            switch(item.type) {
                              case 1:
                                html += 'Theory</h3></li>';
                                break;
                              case 2:
                                html += 'Translate from EN to RU</h3></li>';
                                break;
                              case 3:
                                html += 'Translate from RU to EN</h3></li>';
                                break;
                            }

                        });
                        html += '</ol></div>';
                        $("#content").html(html);
                    }
                }
            });
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
                        window.location.reload(true);
                }
            });
    }
    else{
        alert("Choose task's type");
    }
});