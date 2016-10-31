from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static

from rest_framework import routers
from sensorsiestaserver.views import UserViewSet, GroupViewSet
from sensorsiestaserver.settings import STATIC_URL, STATIC_ROOT

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

print 'STATIC ROOT = ', STATIC_ROOT

urlpatterns = [
    #url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^api/', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
] + static(STATIC_URL, document_root=STATIC_ROOT)
