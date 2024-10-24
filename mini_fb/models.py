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
    
    def get_friends(self):
        '''Return all friends of profile1 // needs to return a LIST of friend profiles'''
        # all friends where profile1 is either profile1 or profile2 in the Friends model
        friends_as_profile1 = Friends.objects.filter(profile1=self)
        friends_as_profile2 = Friends.objects.filter(profile2=self)

        friends = list(friends_as_profile1.values_list('profile2', flat=True))  # get profile2 friends
        friends += list(friends_as_profile2.values_list('profile1', flat=True))  # get profile1 friends
        return Profile.objects.filter(id__in=friends)

    def add_friend(self, other):
        '''Create a friendship between this profile and another, if not a duplicate.'''
        if (other in self.get_friends()): # type: ignore
            return
        
        Friends.objects.create(profile1=self, profile2=other)


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


class Friends(models.Model):
    '''Attributes of a user profile'''
    profile1 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="friends_profile1")
    profile2 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="friends_profile2")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this Profile object.'''
        return f'{self.profile1.first_name} {self.profile1.last_name} & {self.profile2.first_name} {self.profile2.last_name}'

    def get_status_messages(self):
        '''Return all of the status messages for this profile, newest first.'''
        sms = StatusMessage.objects.filter(profile=self.profile1) | StatusMessage.objects.filter(profile=self.profile2)
        return sms.order_by('-timestamp')
    