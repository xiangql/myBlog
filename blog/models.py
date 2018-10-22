from django.db import models
# Create your models here.

#用户表
class User(models.Model):
    account = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20)
    petname = models.CharField(max_length=20)
    phone = models.CharField(max_length=15, null=True, unique=True)
    email = models.EmailField(null=True, unique=True)
    isDelete = models.BooleanField(False)
    def __str__(self):
        return self.account

#博客表
class Blog(models.Model):
    bid = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=200)
    btype = models.CharField(max_length=20)
    cDate = models.DateTimeField(auto_now_add=True)
    context = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    isDelete = models.BooleanField(False)
    def __str__(self):
        return self.title

#用户收藏表
class Collect(models.Model):
    uid = models.CharField(max_length=20)
    bid = models.CharField(max_length=20)
    isDelete = models.BooleanField(False)
    class Meta:
        unique_together = ('uid', 'bid',)

#评论表
class Comment(models.Model):
    cid = models.AutoField(primary_key=True)
    fUser = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    content = models.TextField()
    isDelete = models.BooleanField(False)
    def __str__(self):
        return self.cid







