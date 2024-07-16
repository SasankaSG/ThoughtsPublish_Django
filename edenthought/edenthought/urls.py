
from django.contrib import admin
from django.urls import path, include

#create a unique url to access our media files
from django.conf import settings
#we can access media root media url in setting.py

from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('journal.urls'))
]
#custom url to access media urls and static urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)