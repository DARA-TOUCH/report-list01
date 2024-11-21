from django.shortcuts import render

def welcome(request):
    return render(request, template_name='welcome.html')


def my_personal_info(request):
    return render(request, 'my_personal_data.html')

def tool_menu(request):
    return render(request, 'tool_menu.html')

def web_list(request):
    return render(request, 'web_list.html')

def disclaimer(request):
    return render(request, 'disclaimer.html')

def copy_report(request):
    pass