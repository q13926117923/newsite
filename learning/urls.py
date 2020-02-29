from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
	path('',views.topic_list,name='topic_list'),
	path('<int:topic_pk>',views.topic_detail,name="topic_detail"), 
	path('type/<int:Topic_Type_pk>',views.topics_with_type,name="topics_with_type"),
	path('date/<int:year>/<int:month>',views.topics_with_date,name="topics_with_date"),

]