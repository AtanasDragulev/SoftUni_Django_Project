from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('online_store.apps.frontend.urls')),
    path('', include('online_store.apps.core.urls')),
    path('', include('online_store.apps.cart.urls')),
    path('user/', include('online_store.apps.accounts.urls')),
    path('backoffice/', include('online_store.apps.backoffice.urls')),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
