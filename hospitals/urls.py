from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path
from . import views

schema_view = get_schema_view(
   openapi.Info(
      title='OMOP API',
      default_version='v1',
      description='health tracking api',
      terms_of_service='https://github.com/withyeah',
      contact=openapi.Contact(email='yerang.dev@gmail.com'),
      license=openapi.License(name='BSD License'),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('patients/', views.patients_list),
    path('visits/', views.visits_list),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
]
