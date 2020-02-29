import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from .models import ReadNum,ReadDetail

def read_statistics_once_read(request, obj):
	ct = ContentType.objects.get_for_model(obj)
	key = "%s_%s_read" %(ct.model,ct.pk)
	if not request.COOKIES.get(key):
		#总阅读数+1
		readnum, created = ReadNum.objects.get_or_create(content_type=ct,object_id=obj.pk)
		readnum.read_num +=1
		readnum.save()
		#当天阅读数+1
		date = timezone.now().date()
		readDetail, created = ReadDetail.objects.get_or_create(content_type=ct,object_id=obj.pk,date=date)
		readDetail.read_num +=1
		readDetail.save()
	return key	

def get_seven_days_read_data(content_type):
	today = timezone.now().date()
	dates = []
	read_nums = []
	for i in range(6,-1,-1):
		date = today - datetime.timedelta(days=i)
		dates.append(date.strftime('%m/%d'))   #格式转化
		read_details = ReadDetail.objects.filter(content_type=content_type,date=date)
		result = read_details.aggregate(read_num_sum=Sum('read_num')) #read_num_sum是键 Sum('read_num')的结果是值
		read_nums.append(result['read_num_sum']or 0)	
	return read_nums,dates

def get_today_hot_data(content_type):
	today = timezone.now().date()
	read_details = ReadDetail.objects.filter(content_type=content_type,date=today).order_by('-read_num')
	return read_details[:7]

def get_yesterday_hot_data(content_type):
	today = timezone.now().date()
	yesterday = today - datetime.timedelta(days=1)
	read_details = ReadDetail.objects.filter(content_type=content_type,date=yesterday).order_by('-read_num')
	return read_details[:7]	
