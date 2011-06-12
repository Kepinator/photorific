from django.conf.urls.defaults import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += patterns('',
    url(r'^register/$', 'photo_gallery.views.register_user'),
    url(r'^adduser/$', 'photo_gallery.views.add_user'),
    url(r'^', include('photo_gallery.urls')),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'photo_gallery/login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login')
#   url(r'^/admin/', include(admin.site.urls))

    # Examples:
    # url(r'^$', 'Photorific.views.home', name='home'),
    # url(r'^Photorific/', include('Photorific.foo.urls')),

)


