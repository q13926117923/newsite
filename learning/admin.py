from django.contrib import admin
from .models import TopicType,Topic
# Register your models here.
@admin.register(TopicType)
class TopicTypeAdmin(admin.ModelAdmin):
	list_display= ('id','type_name')
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
	list_display= ('title','content','author','get_read_num','create_time','last_update_time')
'''@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
	list_display= ('topic','read_num')	'''

