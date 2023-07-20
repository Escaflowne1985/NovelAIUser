/*自定义js, 用于xadmin edit界面二级联动查询*/

(function($) {
    function linkage_query() {
        $("#id_navi_f").change(function (e) {
            var val = $(this).val();
            var url = "/forum_navi/?fid=" + val;
            getSecNavi(url, "id_navi_s");
        });

        function getSecNavi(url, id) {
            $.ajax({
                type: "get",
                url: url,
                async: true,
                beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", $.getCookie("csrftoken"));
                },
                success: function (data) {
                    console.log(data);
                    $('#'+id)[0].selectize.clearOptions(); //二级select清空选项
                    for (var i = 0; i < data.length; i++) {
                        $('#'+id)[0].selectize.addOption({text: data[i].name, value: data[i].id, $order: i + 1}); //添加数据
                    }
                },
                error: function (xhr, textStatus) {
                    console.log(xhr);
                    console.log(textStatus);
                }
            })
        }
    }
    linkage_query();
})(jQuery);