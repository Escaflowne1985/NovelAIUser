$('#id_industry').change(function () {
    var id = $('#id_industry').find('option:selected').val(); //获取父级选中值
    $('#id_job')[0].selectize.clearOptions();// 清空子级
    $.ajax({
        type: 'get',
        url: 'select_industry_job?industry_id=' + id,
        data: '',
        async: true,
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}')
        },
        success: function (data) {
            data = JSON.parse(data.title)//将JSON转换
            for (var i = 0; i < data.length; i++) {
                var test = {text: data[i].fields.title, value: data[i].pk, $order: i + 1}; //遍历数据,拼凑出selectize需要的格式
                console.log(test)
                $('#id_job')[0].selectize.addOption(test); //添加数据
            }
        },
        error: function (xhr, textStatus, data) {
            console.log('error')
        }
    })
})

$('#id_industry1').change(function () {
    var id = $('#id_industry1').find('option:selected').val(); //获取父级选中值
    $('#id_job1')[0].selectize.clearOptions();// 清空子级
    $.ajax({
        type: 'get',
        url: 'select_industry_job?industry_id=' + id,
        data: '',
        async: true,
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}')
        },
        success: function (data) {
            data = JSON.parse(data.title)//将JSON转换
            for (var i = 0; i < data.length; i++) {
                var test = {text: data[i].fields.title, value: data[i].pk, $order: i + 1}; //遍历数据,拼凑出selectize需要的格式
                console.log(test)
                $('#id_job1')[0].selectize.addOption(test); //添加数据
            }
        },
        error: function (xhr, textStatus, data) {
            console.log('error')
        }
    })
})

$('#id_industry2').change(function () {
    var id = $('#id_industry2').find('option:selected').val(); //获取父级选中值
    $('#id_job2')[0].selectize.clearOptions();// 清空子级
    $.ajax({
        type: 'get',
        url: 'select_industry_job?industry_id=' + id,
        data: '',
        async: true,
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}')
        },
        success: function (data) {
            data = JSON.parse(data.title)//将JSON转换
            for (var i = 0; i < data.length; i++) {
                var test = {text: data[i].fields.title, value: data[i].pk, $order: i + 1}; //遍历数据,拼凑出selectize需要的格式
                console.log(test)
                $('#id_job2')[0].selectize.addOption(test); //添加数据
            }
        },
        error: function (xhr, textStatus, data) {
            console.log('error')
        }
    })
})

$('#id_industry3').change(function () {
    var id = $('#id_industry3').find('option:selected').val(); //获取父级选中值
    $('#id_job3')[0].selectize.clearOptions();// 清空子级
    $.ajax({
        type: 'get',
        url: 'select_industry_job?industry_id=' + id,
        data: '',
        async: true,
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}')
        },
        success: function (data) {
            data = JSON.parse(data.title)//将JSON转换
            for (var i = 0; i < data.length; i++) {
                var test = {text: data[i].fields.title, value: data[i].pk, $order: i + 1}; //遍历数据,拼凑出selectize需要的格式
                console.log(test)
                $('#id_job3')[0].selectize.addOption(test); //添加数据
            }
        },
        error: function (xhr, textStatus, data) {
            console.log('error')
        }
    })
})

$('#id_industry4').change(function () {
    var id = $('#id_industry4').find('option:selected').val(); //获取父级选中值
    $('#id_job4')[0].selectize.clearOptions();// 清空子级
    $.ajax({
        type: 'get',
        url: 'select_industry_job?industry_id=' + id,
        data: '',
        async: true,
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}')
        },
        success: function (data) {
            data = JSON.parse(data.title)//将JSON转换
            for (var i = 0; i < data.length; i++) {
                var test = {text: data[i].fields.title, value: data[i].pk, $order: i + 1}; //遍历数据,拼凑出selectize需要的格式
                console.log(test)
                $('#id_job4')[0].selectize.addOption(test); //添加数据
            }
        },
        error: function (xhr, textStatus, data) {
            console.log('error')
        }
    })
})