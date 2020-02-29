import datetime
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from django.core.cache import cache
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from read_statistics.utils import get_seven_days_read_data,  get_today_hot_data, get_yesterday_hot_data
from learning.models import Topic
from .forms import LoginForm,RegForm

def get_7_days_hot_data():
    today = timezone.now().date()   
    date = today - datetime.timedelta(days=7)
    topics = Topic.objects\
                            .filter(read_details__date__lt=today, read_details__date__gte=date)\
                            .values('id','title')\
                            .annotate(read_num_sum = Sum('read_details__read_num'))\
                            .order_by('-read_details__read_num')
    return topics[:7]
def base(request):
    topic_content_type = ContentType.objects.get_for_model(Topic)
    read_nums,dates = get_seven_days_read_data(topic_content_type)

    # 获取7天热门博客的缓存数据
    hot_data_for_7_days = cache.get('hot_data_for_7_days')
    if hot_data_for_7_days is None :
        hot_data_for_7_days = get_7_days_hot_data()
        cache.set('hot_data_for_7_days',hot_data_for_7_days,3600)
        print('calc')
    else:
        print('use cache')

    context={}
    context['dates']= dates
    context['read_nums'] = read_nums
    context['yesterday_hot_data'] = get_yesterday_hot_data(topic_content_type)
    context['today_hot_data'] = get_today_hot_data(topic_content_type)
    context['hot_data_for_7_days'] = get_7_days_hot_data()
    return render(request,'index.html',context)

def login(request):
    '''username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = auth.authenticate(request, username=username, password=password)
    referer = request.META.get('HTTP_REFERER',reverse('base'))#根据request获取当前网址url，若无则跳转首页
                                            #reverse解析url别名
    if user is not None:
        auth.login(request, user)
        return redirect(referer)
        ...
    else:
        return render(request,'error.html',{'massage':'不存在 错误'})'''

    if request.method =='POST':         #如果请求是POST 执行
        login_form = LoginForm(request.POST) #实例化LoginForm，参数是请求里的POST数据，并在forms.py处理数据
        if login_form.is_valid():       #如果数据可用（验证通过），进行登录
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from',reverse('base')))#from是参数能获取到网页?from=xxx的路径，
                                                                     #如果获取不到就返回首页
    else:
        login_form = LoginForm()

    context={}
    context['login_form'] = login_form   
    return render(request,'login.html',context)

def register(request):
    if request.method =='POST':         #如果请求是POST 执行
        reg_form = RegForm(request.POST) #实例化LoginForm，参数是请求里的POST数据，并在forms.py处理数据
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            password = reg_form.cleaned_data['password']
            email = reg_form.cleaned_data['email']
            #创建用户
            user = User.objects.create_user(username,email,password)
            user.save()
            #登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from',reverse('base')))
    else:
        reg_form = RegForm()

    context={}
    context['reg_form'] = reg_form   
    return render(request,'register.html',context)