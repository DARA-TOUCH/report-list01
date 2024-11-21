from django.urls import path
# from .views import List01ViewSet
from .views import List01View, SalakabattDataView, DownloadSalakabattDataView, ListCleanUp, List01MakeUpView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import View

app_name = 'list01'


urlpatterns = [
    path('', List01View.as_view(), name='create_list01'),
    path('salakabatt-data', SalakabattDataView.as_view(), name='salakabatt_data'),
    path('download-salakabatt-data', DownloadSalakabattDataView.as_view(), name='download_salakabatt_data'),
    path('cleanup', ListCleanUp.as_view(), name='cleanup'),
    path('makeup-list01-template', List01MakeUpView.as_view(), name='makeup_list01_template'),
]