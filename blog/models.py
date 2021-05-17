import datetime
from django.urls import reverse
from django.conf import settings
from django.core.files import File
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from io import BytesIO
import ntpath
import os
from PIL import Image


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def user_upload_path(instance, filename):
    return "blog/{}-{}/{}".format(instance.user.username, instance.slug, path_leaf(filename))

# Image in form of BytesIO, so we need this helper function
def saveEditedImage(img):
    """Get original compressed image (667x500 from device in form of BytesIO). Create original image and one thumbnail image (300x200)"""
    
    #In case mobile compression not succedeed then compress here
    image = Image.open(BytesIO(img.read()))
    maxDimen = 750 
    if img.width > img.height:
        width = maxDimen
        height = img.height/img.width * width
    else:
        height = maxDimen
        width = img.width/img.height * height
    output = BytesIO()
    image.thumbnail((width, height), Image.ANTIALIAS)
    image.save(output, format='JPEG', quality=70)
    output.seek(0)

    maxDimen = 300 
    if img.width > img.height:
        width = maxDimen
        height = img.height/img.width * width
    else:
        height = maxDimen
        width = img.width/img.height * height

    output2 = BytesIO()
    image.thumbnail((width, height), Image.ANTIALIAS)
    image.save(output2, format='JPEG', quality=70)
    output2.seek(0)
    return img, output, output2

# Helping function end here
def get_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return get_slug(instance, new_slug)
    return slug

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="posts", default=1, on_delete=models.SET_DEFAULT)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to= user_upload_path,
        null=True,
        blank=True,height_field = 'height_field',
        width_field = 'width_field')
    height_field = models.IntegerField(default=0, blank=True, null=True)
    width_field = models.IntegerField(default=0, blank=True, null=True)
    content = models.TextField()
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('blog:retrieve', kwargs={ 'slug' : self.slug, })
    def save(self, *args, **kwargs):
        """Using `pillow` resize and compress image(s)."""
        try:
            this = Post.objects.get(id=self.id)
            # Delete old file if new file assigned
            if self.image and this.image and this.image != self.image:
                print('Deleting old file on uploading new one')
                this.image.delete(save=False)
                # Save new one
                img, output, output2 = saveEditedImage(self.image)
                self.image = File(output, img.name)
        except:
            if self.image: # No older file exists so add new one
                img, output, output2 = saveEditedImage(self.image)
                self.image = File(output, img.name)
                # self.thumb = File(output2, img.name.replace('.jpg', '_thumb.jpg'))

        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-created',)

@receiver(pre_save, sender=Post)
def my_handler(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = get_slug(instance)

# 1. Delete all files associated with model when object deleted
@receiver(models.signals.post_delete)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding object is deleted.
    """
    list_of_models = ('Inspection',) #('Place', 'Slide', 'AboutUs')
    if sender.__name__ in list_of_models: # this is the dynamic part you want
        if instance.image1 and os.path.isfile(instance.image1.path):
            os.remove(instance.image1.path)
            os.remove(instance.thumb1.path)
        if instance.image2 and os.path.isfile(instance.image2.path):
            os.remove(instance.image2.path)
            os.remove(instance.thumb2.path)
        if instance.image3 and os.path.isfile(instance.image3.path):
            os.remove(instance.image3.path)
            os.remove(instance.thumb3.path)