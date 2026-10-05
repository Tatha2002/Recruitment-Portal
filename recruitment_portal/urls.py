from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from accounts import views
from dashboard import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('accounts.urls')),
    path('candidates/', include('candidates.urls')),
    # path('interviews/', include('interviews.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('', views.dashboard, name='dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)