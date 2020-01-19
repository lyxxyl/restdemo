from django.db import models

# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=32)
    price = models.IntegerField()
    pub_date = models.DateField()
    publish = models.ForeignKey('Publish')
    authors = models.ManyToManyField('Author')
    def __str__(self):
        return self.title

class Publish(models.Model):
    name = models.CharField(max_length=32)
    email = models.EmailField()
    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField()
    def __str__(self):
        return self.name



class member(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=100)
    type = models.IntegerField()
    def __str__(self):
        return self.username


class member_token(models.Model):
    user = models.OneToOneField(to=member)
    token = models.CharField(max_length=64)
    def __str__(self):
        return self.token



