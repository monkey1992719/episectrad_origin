from django.urls import path, include
from django.conf.urls import url
from django.contrib import admin
from episectrad import settings
from django.conf.urls.static import static

import dashboard.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('language/<language>/', views.switch_language),

    url(r"^", include(dashboard.urls)),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
