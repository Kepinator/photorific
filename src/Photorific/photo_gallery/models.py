from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from StringIO import StringIO
import os

# updateContent function is modified from http://tomcoote.co.uk
def updateContent(img, format="JPEG"):
    file = StringIO()
    img.save(file, format, quality=128)

def resize(img_stream, size):
    image = Image.open(img_stream)
    if image.mode not in ('L', 'RGB'):
        image = image.convert('RGB')
    return image.resize(size, Image.ANTIALIAS)

#when we add users and user-specific galleries, we need to check whether the user is logged in before serving content
#and otherwise redirect them to login.

class Album(models.Model):
    name = models.TextField()
    owner = models.ForeignKey(User)
    dateCreate = models.DateField(auto_now_add="true")
    dateModified = models.DateField(auto_now="true")
    coverPhoto = models.ForeignKey('Photo', related_name='CoverPhoto', null=True)
    
    
class Photo(models.Model):
    displayName = models.CharField(max_length=200)
    comments = models.TextField()
    album = models.ForeignKey(Album)
    photo = models.ImageField(upload_to='photos')
    thumbnail = models.ImageField(upload_to='thumbnails', blank=True, null=True, editable=False)
    owner = models.ForeignKey(User)
    dateCreated = models.DateField(auto_now_add="true")
    dateModified = models.DateField(auto_now="true")
    
    
    #credit where credit is due - this save() is modified from a function I found at:
    #http://stackoverflow.com/questions/1164930/image-resizing-with-django
    #keeps aspect ratios correct while resizing
    def save(self):
        size = (200,160)    #thumnail size, slightly wider than tall a la facebook since most pictures aren't square
        if not self.id and not self.photo:
            return

        try:
            old_obj = Photo.objects.get(pk=self.pk)
            old_path = old_obj.photo.path
        except:
            pass

        thumb_update = False
        if self.thumbnail:
            try:
                statinfo1 = os.stat(self.photo.path)
                statinfo2 = os.stat(self.thumbnail.path)
                if statinfo1 > statinfo2:
                    thumb_update = True
            except:
                thumb_update = True

        pw = self.photo.width
        ph = self.photo.height
        nw = size[0]
        nh = size[1]

        if self.photo and not self.thumbnail or thumb_update:
            # only do this if the image needs resizing
            if (pw, ph) != (nw, nh):
                self.photo.seek(0)
                image = Image.open(StringIO(self.photo.read()))
                pr = float(pw) / float(ph)
                nr = float(nw) / float(nh)

                if image.mode not in ('L', 'RGB'):
                    image = image.convert('RGB')

                if pr > nr:
                    # photo aspect is wider than destination ratio
                    tw = int(round(nh * pr))
                    image = image.resize((tw, nh), Image.ANTIALIAS)
                    l = int(round(( tw - nw ) / 2.0))
                    image = image.crop((l, 0, l + nw, nh))
                elif pr < nr:
                    # photo aspect is taller than destination ratio
                    th = int(round(nw / pr))
                    image = image.resize((nw, th), Image.ANTIALIAS)
                    t = int(round(( th - nh ) / 2.0))
                    image = image.crop((0, t, nw, t + nh))
                else:
                    # photo aspect matches the destination ratio
                    image = image.resize(size, Image.ANTIALIAS)

            image.save(self.get_thumbnail_path())
            (pth, name) = os.path.split(self.photo.name)
            self.thumbnail = pth + 'thumbnails/' + name
            super(Photo, self).save()
            try:
                os.remove(old_path)
                os.remove(self.get_old_thumbnail_path(old_path))
            except:
                pass

    def get_thumbnail_path(self):
        (head, tail) = os.path.split(self.photo.path)
        if not os.path.isdir(head + '/thumbnails'):
            os.mkdir(head + '/thumbnails')
        return head + '/thumbnails/' + tail

    def get_old_thumbnail_path(self, old_photo_path):
        (head, tail) = os.path.split(old_photo_path)
        return head + '/thumbnails/' + tail