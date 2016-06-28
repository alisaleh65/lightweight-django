import os
import hashlib
import sys
# این ماژول را به عنوان ماژول تنظیمات معرفی می کنیم.
os.environ["DJANGO_SETTINGS_MODULE"]=__name__
SECRET_KEY = '(ain*0-al(%h347@dqj$#952s+izs#2rt&&xn-w--k0dn1xmu+'


# اگر با export DEBUG=off حالت دیباگ را غیر فعال کرده باشند آن را اعمال می کنیم.
DEBUG = os.environ.get('DEBUG', 'on') == 'on'
print("debug is ", DEBUG)

# با تنظیم ALLOWED_HOSTS می توانیم درستی درخواست HTTP HOST دریافتی را ارزیابی کنیم.
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')


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

BASE_DIR = os.path.dirname(__file__)

INSTALLED_APPS = (
    'django.contrib.staticfiles',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_URL = '/static/'

# همین ماژول را به عنوان ماژول تنظیمات url مشخص میکنیم.

ROOT_URLCONF=__name__


# تجربه نشان داد که اگر قبل این import ها تنظیمات انجام نشود ، دیگر انجام نخواهد شد :))

from io import BytesIO
from PIL import Image, ImageDraw
from django import forms
from django.conf.urls import url
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import etag
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.core.wsgi import get_wsgi_application




# با این متد کار view را انجام می دهیم.
def index(request):
    example = reverse('placeholder', kwargs={'width':50, 'height':50})
    context = {
        'example': request.build_absolute_uri(example)
    }
    
    return render(request, 'home.html', context)
    

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


    
# مزیت استفاده از etag در مقایسه با cache این است که مرورگر خود کار cache سمت سرور را انجام می دهد، ولی استفاده از آن دقت می خواهد.
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
        

# set WSGI
application = get_wsgi_application()

urlpatterns = (
    url(r'^placeholder/(?P<width>[0-9]+)x(?P<height>[0-9]+)/$', placeholder,  name='placeholder'),
    url(r'^$', index, name='homepage'),
)


if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

