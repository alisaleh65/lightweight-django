import os
import hashlib
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", __name__)
from django.conf import settings

DEBUG = os.environ.get('DEBUG', 'on') == 'on'
print("debug is ", DEBUG)

SECRET_KEY = os.environ.get('SECRET_KET', '(ain*0-al(%h347@dqj$#952s+izs#2rt&&xn-w--k0dn1xmu+')

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')


ROOT_URLCONF=__name__


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)


from django.conf.urls import url
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import etag

from django import forms


from io import BytesIO

from PIL import Image, ImageDraw


class ImageForm(forms.Form):
    ''' form to validate requested placeholder image.'''
    
    height = forms.IntegerField(min_value=1, max_value=2000)
    width = forms.IntegerField(min_value=1, max_value=2000)
    
    def generate(self, image_format='PNG'):
        height = self.cleaned_data['height']
        width = self.cleaned_data['width']
        
        key = '{}.{}.{}'.format(width, height, image_format)
        
        content = cache.get(key)
        
        if content is None:
            print("miss")
            image = Image.new('RGB', (width, height))
            draw = ImageDraw.Draw(image)
            text = '{}x{}'.format(width, height)
            textwidth, textheight = draw.textsize(text)
            if textwidth < width and textheight < height:
                texttop = (height - textheight)//2
                textleft = (width - textwidth)//2
                draw.text((textleft, texttop), text, fill=(255,255,255) )
            content = BytesIO()
            image.save(content, image_format)
            content.seek(0)
            cache.set(key , content , 60*60)
        else:
            print("hit")
        return content
    

def index(request):
    return HttpResponse("Hello World")
    
    
def generate_etag(request, width, height):
    content = 'Placeholder: {0}x{1}'.format(width, height)
    return hashlib.sha1(content.encode('utf-8')).hexdigest()
    
    
@etag(generate_etag)    
def placeholder(request, width, height):
    form = ImageForm({'height':height, 'width':width})
    if form.is_valid():
        height = form.cleaned_data['height']
        width = form.cleaned_data['width']
        image = form.generate()
        return HttpResponse(image, content_type='image/png')
    else:
        return HttpResponse("Invalid Image request.")
  
urlpatterns = (
    url(r'^image/(?P<width>[0-9]+)x(?P<height>[0-9]+)/$', placeholder,  name='placeholder'),
    url(r'^$', index, name='homepage'),
)

# set WSGI

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()



if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)















