from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

app_name = 'api'

urlpatterns = [
    path('admin/', admin.site.urls),

    # Token
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # noqa: E501

    # Api
    path('api/', include('api.urls', namespace='api')),

    # Doc
    path('', TemplateView.as_view(
        template_name='pages/doc.html',
        extra_context={'schema_url': 'api/schema-swagger'}
    ), name='swagger-ui'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
