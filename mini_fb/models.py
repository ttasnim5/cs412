from django.db import models

class Profile(models.Model):
    '''Attributes of a user profile'''
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)
    image_url = models.URLField(blank=True)  # image as a string
    
    def __str__(self):
        '''Return a string representation of this Profile object.'''
        return f'{self.first_name} {self.last_name}'
   
    def get_status_messages(self):
        '''Return all of the status messages for this profile, newest first.'''
        return self.statusmessage_set.order_by('-timestamp')


class StatusMessage(models.Model):    
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    message = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        '''Return a string representation of this status message object.'''
        return f'{self.message}'
    
    def get_status_images(self):
        '''Return all of the images for this message, newest first.'''
        return self.image_set.order_by('-timestamp')


class Image(models.Model):    
    message = models.ForeignKey("StatusMessage", on_delete=models.CASCADE)  # Linking image to StatusMessage
    image_file = models.ImageField(blank=False)  # actual image, not url
    timestamp = models.DateTimeField(auto_now=True)  
    
    def __str__(self):
        '''Return a string representation of this image.'''
        return f'Image for status: {self.message.message}'
