from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from dashboard.views import error_404_view, error_500_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout', auth_views.LogoutView.as_view(),name='logout'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('', include('dashboard.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


handler404 = error_404_view
handler500 = error_500_view
