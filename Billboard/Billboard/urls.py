from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework import routers

from bboard.views import UserViewSet, AdvertisementViewSet, ReactionViewSet, CategoryViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'advertisements', AdvertisementViewSet)
router.register(r'reactions', ReactionViewSet)

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('bboard.urls')),
    path('swagger-ui/', TemplateView.as_view(template_name='swagger-ui.html')),
    path('swagger/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
