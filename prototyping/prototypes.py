import os
import sys
# این ماژول را به عنوان ماژول تنظیمات معرفی می کنیم.
os.environ["DJANGO_SETTINGS_MODULE"]=__name__
SECRET_KEY = '(ain*0-al(%h347@dqj$#952s+izs#2rt&&xn-w--k0dn1xmu+'


# اگر با export DEBUG=off حالت دیباگ را غیر فعال کرده باشند آن را اعمال می کنیم.
DEBUG = os.environ.get('DEBUG', 'on') == 'on'

# با تنظیم ALLOWED_HOSTS می توانیم درستی درخواست HTTP HOST دریافتی را ارزیابی کنیم.
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')


MIDDLEWARE_CLASSES = ()

BASE_DIR = os.path.dirname(__file__)


ROOT_URLCONF='sitebuilder.urls'


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sitebuilder',
)


STATIC_URL = '/static/'

SITE_PAGES_DIRECTORY = os.path.join(BASE_DIR, 'pages')
SITE_OUTPUT_DIRECTORY = os.path.join(BASE_DIR, '_build')
STATIC_ROOT = os.path.join(BASE_DIR, '_build', 'static')

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


