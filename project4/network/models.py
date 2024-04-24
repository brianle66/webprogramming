from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    def __str__(self) -> str:
        return f'Post {self.id} made by {self.author} on {self.date_posted}'

class Follow(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='following')
    follower = models.ForeignKey(User,on_delete=models.CASCADE, related_name='followers')

    def __str__(self) -> str:
        return f'{self.user} is being followed by {self.follower}'
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_like')

    def __str__(self) -> str:
        return f'{self.user} liked {self.post}'