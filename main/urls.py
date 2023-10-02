from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Token
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # noqa: E501

    # Api
    path('api/', include('api.urls', namespace='api')),

    # Doc
    path('swagger-ui/', TemplateView.as_view(
        template_name='pages/swaggerDoc.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
]
