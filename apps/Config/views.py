from django.shortcuts import render


def bad_request(request, exception, template_name='400.html'):
    return render(request, template_name)


def permission_denied(request, exception, template_name='403.html'):
    return render(request, template_name)


def page_not_found(request, exception, template_name='404.html'):
    return render(request, template_name)


# 注意这里没有 exception 参数
def server_error(request, template_name='500.html'):
    return render(request, template_name)