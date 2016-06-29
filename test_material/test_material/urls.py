from django.conf.urls import include, url
from django.contrib import admin
from material.frontend import urls as frontend_urls
from django.shortcuts import render
def index(request):
    a = '''
    {% include 'material/includes/material_css.html' %}
    <script src="{% static 'material/js/jquery-2.2.0.js' %}"></script>
    {% include 'material/includes/material_js.html' %}
    {% load material_form %} 
    <form method="POST">
        {% csrf_token %}
        {% form form=form %}{% endform %}
        <button type="submit" name="_submit" class="btn">Submit</button>
    </form>

    '''
    return render(request, 'test.html', None)
urlpatterns = [
    # Examples:
    # url(r'^$', 'test_material.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index),
]
