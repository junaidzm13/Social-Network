from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts")
    content = models.CharField(max_length=300)
    num_likes = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "content": self.content,
            "likes": self.num_likes,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }

class Fpost(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="fposts")
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="f_posts")

class Follower(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers")
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following")
    
class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=128)

class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="liked")
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="likes")


