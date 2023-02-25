from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    dateCreated = models.DateField(auto_created=True, auto_now_add=True, editable=True)
    content = models.CharField(max_length=1000, default='Content', editable=True)
    userKey = models.ForeignKey(User, on_delete=models.CASCADE, related_name='postCreatedByUser')

class Like(models.Model):
    id = models.AutoField(primary_key=True)
    dateCreated = models.DateField(auto_created=True, auto_now_add=True, editable=True)
    userKey = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likeCreatedByUser')
    postKey = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likeLinkedToPost')

class Follow(models.Model):
    id = models.AutoField(primary_key=True)
    dateCreated = models.DateField(auto_created=True, auto_now_add=True, editable=True)
    createdByUserKey = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followCreatedByUser')  
    followingUserKey = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followLinkedToUser')

'''
related_name: 
This allows you to do a reverse lookup. Suppose you have a specific user object. You can do
specific_user.followCreatedBy.all() 
to get all the follows created by that user
'''