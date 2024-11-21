from django.urls import path
from .views import welcome, my_personal_info, tool_menu, web_list, disclaimer


app_name = 'core'

urlpatterns = [
    path("", view=welcome, name='welcome'),
    path("personal info/", view=my_personal_info, name='my_personal_info'),
    path("Tool Menu/", view=tool_menu, name='tool_menu'),
    path("web list/", view=web_list, name='web_list'),
    path("disclaimer/", view=disclaimer, name='disclaimer'),
    ]