from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod,ReadDetail


# Create your models here.
class TopicType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name
      
class Topic(models.Model,ReadNumExpandMethod):
    title = models.CharField(max_length=50)
    Topic_Type = models.ForeignKey(TopicType,on_delete = models.DO_NOTHING)
    content = RichTextUploadingField()
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    read_details = GenericRelation(ReadDetail)
    create_time = models.DateTimeField(auto_now_add=True) 
    last_update_time = models.DateTimeField(auto_now_add=True)

    
        
    def __str__(self):
        return"<Blog: %s>"% self.title

    class Meta:
        ordering = ['-create_time']

'''
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    topic = models.OneToOneField(Topic,on_delete = models.DO_NOTHING)
    '''