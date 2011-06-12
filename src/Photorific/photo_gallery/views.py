from django.http import HttpResponse, HttpResponseRedirect
from photo_gallery.models import Photo, Album
from photo_gallery.forms import AddPhotoForm, AddAlbumForm, RegisterUserForm
from PIL import Image
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

@login_required
def albums(request):
    user = request.user
    album_list = Album.objects.filter(owner=user)
    return render_to_response('photo_gallery/albums.html', {'albums' : album_list})

@login_required
def add_album(request):
    form = AddAlbumForm()
    return render_to_response('photo_gallery/addalbum_ajax.html', {'form' : form})

def save_album(request):
    if request.method == 'POST':
        form = AddAlbumForm(request.POST)
        if form.is_valid():
            album = Album()
            album.name = form.cleaned_data.get('name')
            album.owner = request.user
            album.save()
            return HttpResponseRedirect('/gallery/' + str(album.id) + '/')

@login_required
def gallery(request, album_id, page_length=25):   #the view to see an album, or all photos if no album_id provided
    user = request.user
    album = Album.objects.get(pk=album_id)
    if album.owner == user:
        thumbnail_list = Photo.objects.filter(owner=user).filter(album=album_id)
        return render_to_response('photo_gallery/gallery.html', {'thumbnails' : thumbnail_list, 'album': album})
    else:
        return render_to_response('photo_gallery/login.html')

@login_required
def photo(request, photo_id):
    the_photo = get_object_or_404(Photo, pk=photo_id)
    return render_to_response('photo_gallery/photo_ajax.html', {'photo' : the_photo})

@login_required
def add_photo(request, album_id):
    form = AddPhotoForm()
    return render_to_response('photo_gallery/addphoto_ajax.html', {'form' : form, 'album_id' : album_id})

@login_required
def save_photo(request, album_id):
    if request.method == 'POST':
        form = AddPhotoForm(request.POST, request.FILES) # A form bound to the POST data
        if form.is_valid():
            the_photo = Photo()
            the_photo.displayName = form.cleaned_data.get('photo_name')
            the_photo.comments = form.cleaned_data.get('comments')
            the_photo.owner = request.user
            
            try:
                album = Album.objects.get(pk=album_id)
            except:
                return render_to_response('photo_gallery/addphoto', {'form' : form})
            the_photo.album = album
            the_photo.photo = form.cleaned_data.get('photo')
            the_photo.save()
            return HttpResponseRedirect('/gallery/' + str(album_id) + '/')
        else:
            return render_to_response('photo_gallery/addphoto', {'form' : form})
    else:
        form = AddPhotoForm()
        return render_to_response('photo_gallery/addphoto.html', {'form' : form})

@login_required
def delete_photo(request, photo_id):
    photo = Photo.objects.get(pk=photo_id)

    if request.user == photo.owner:
        album = photo.album
        photo.delete()
        thumbnail_list = Photo.objects.filter(owner=request.user).filter(album=album.id)
        return render_to_response('photo_gallery/thumbnails.html', {'thumbnails' : thumbnail_list})
    else:
        return HttpResponseRedirect('/albums/')    #they're trying to do something they shouldn't
    
def set_coverphoto(request, photo_id):
    photo = Photo.objects.get(pk=photo_id)
    
    if request.user == photo.owner:
        album = photo.album
        album.coverPhoto = photo
        album.save()
    return HttpResponse

def register_user(request):
    form = RegisterUserForm()
    return render_to_response('photo_gallery/register_ajax.html', {'form' : form})

def add_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            fname = form.cleaned_data.get('fname')
            lname = form.cleaned_data.get('lname')
            
            from django.contrib.auth.models import User 
            user = User.objects.create_user(username=uname, password=pwd, email=email)
            user.first_name = fname
            user.last_name = lname
            user.save()
            user = authenticate(username=uname, password=pwd)
            if user.is_authenticated():
                login(request=request, user=user)
            return HttpResponseRedirect('/albums/')    #if for some reason authentication fails, 
                                                        #user will be automagically redirected to login page
        else:
            return render_to_response('photo_gallery/register.html', {'form' : form})

            
            
