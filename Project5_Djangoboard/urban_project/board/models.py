from django.db import models
from django.contrib.auth.models import User
DEFAULT = 'img/default.jpg'
class Advertisement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(upload_to='img', null=True, default=DEFAULT)
    '''Задача №5-6. Добавление лайков и дизлайков к объявлениям'''
    likes = models.ManyToManyField(User, related_name='Advertisement.post+')
    dislikes = models.ManyToManyField(User, related_name='Advertisement.post+')
    def total_posts(self):
        return self.objects.count()
    def total_likes(self):
        return self.likes.count()
    def total_dislikes(self):
        return self.dislikes.count()
    def __str__(self):
        return self.title

class Comment(models.Model):
    advertisement = models.ForeignKey(Advertisement, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.advertisement}'
