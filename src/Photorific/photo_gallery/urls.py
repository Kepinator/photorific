from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('photo_gallery.views',
    url(r'^$', 'albums'),    #site "root"
    url(r'^albums/$', 'albums'),
    url(r'^gallery/(?P<album_id>\d+)/', 'gallery'),
    url(r'^photo/(?P<photo_id>\d+)/', 'photo'),
    url(r'^addalbum/$', 'add_album'),
    url(r'^savealbum/$', 'save_album'),
    url(r'^addphoto/(?P<album_id>\d+)/', 'add_photo'),
    url(r'^savephoto/(?P<album_id>\d+)/', 'save_photo'),
    url(r'^deletephoto/(?P<photo_id>\d+)/', 'delete_photo'),
    url(r'^coverphoto/(?P<photo_id>\d+)/', 'set_coverphoto')
    # Examples:
    # url(r'^$', 'Photorific.views.home', name='home'),
    # url(r'^Photorific/', include('Photorific.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
