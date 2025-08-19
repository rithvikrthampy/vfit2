# viewer/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),               # UI page
    path('viewer/', views.viewer_page, name='viewer'), # 3D viewer page
    path('api/shirts/', views.api_list_shirts),
    path('api/run/', views.api_run_pix2surf),          # ?img_id=0&pose_id=0&low_type=shorts
]
