from django.conf.urls import include, url
from django.contrib import admin
from material.frontend import urls as frontend_urls
from django.shortcuts import render
def index(request):
    return render(request, 'test.html', None)
    
urlpatterns = [
    # Examples:
    # url(r'^$', 'test_material.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'', include(frontend_urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index),
]
