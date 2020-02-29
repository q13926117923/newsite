from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator 
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from .models import Topic,TopicType
from read_statistics.utils import read_statistics_once_read
from comment.models import Comment
from comment.forms import CommentForm
# Create your views here.
def get_topic_list_common_data(request,topics_all_list):
    paginator = Paginator(topics_all_list,settings.EACH_PAGE_TOPICS_NUMBER)#每each_page_blogs_number页分页
    page_num = request.GET.get("page",1)#获取Url的页面参数（GET请求）默认值1 
    page_of_topics = paginator.get_page(page_num)
    current_page_num = page_of_topics.number #獲取當前頁碼

    current_page_range = list(range(max(current_page_num-2,1),current_page_num))\
                    +list(range(current_page_num,min(current_page_num+2,paginator.num_pages)+1)) #页数range
    #加上首页               
    if current_page_range[0] != 1:
        current_page_range.insert(0,1)
        if current_page_range[1]-current_page_range[0]!=1:
            current_page_range.insert(1,'...')     #...span
    #加上尾页
    if current_page_range[-1] != paginator.num_pages:
        current_page_range.append(paginator.num_pages)
        if current_page_range[-1]-current_page_range[-2]!=1:
            current_page_range.insert(-1,'...')    #...span
    #获取主题分类的对应主题数量
    TopicType.objects.annotate(topic_count=Count('topic'))
    '''topic_types =  TopicType.objects.all()
    topic_types_list=[]
    for topic_type in topic_types:
        topic_type.topic_count = Topic.objects.filter(Topic_Type=topic_type).count()
        topic_types_list.append(topic_type)
    '''
    topic_dates = Topic.objects.dates('create_time','month',order='ASC')
    topic_dates_dict= {}
    for topic_date in topic_dates:
        topic_count = Topic.objects.filter(create_time__year=topic_date.year,
                                                create_time__month=topic_date.month).count()
        topic_dates_dict[topic_date] = topic_count  


    context = {}
    context['topics'] = Topic.objects.all()   #topics默认为所有博客
    context['page_of_topics'] = page_of_topics
    context['topic_types'] = TopicType.objects.annotate(topic_count=Count('topic'))
    context['current_page_range']= current_page_range
    context['topic_dates'] = topic_dates_dict
    return context

def topic_list(request):
    topics_all_list= Topic.objects.all()
    context = get_topic_list_common_data(request,topics_all_list)
    return render(request,'topic_list.html',context)

def topic_detail(request,topic_pk):
    topic = get_object_or_404(Topic,pk=topic_pk)
    read_cookie_key = read_statistics_once_read(request,topic)
    topic_content_type=ContentType.objects.get_for_model(topic)
    comments = Comment.objects.filter(content_type=topic_content_type,object_id=topic_pk)

    context = {}
    context['topic'] = topic
    context['previous_topic'] = Topic.objects.filter(create_time__gt=topic.create_time).last()
    context['next_topic'] = Topic.objects.filter(create_time__lt=topic.create_time).first()
    context['comment_form'] = CommentForm(initial={'content_type':topic_content_type.model,'object_id':topic_pk})
    context['comments'] = comments
    response = render(request,'topic_detail.html',context) #相应
    response.set_cookie(read_cookie_key,'true',max_age = 5)
    return response

def topics_with_type(request,Topic_Type_pk):

    topic_type = get_object_or_404(TopicType, pk=Topic_Type_pk)
    topics_all_list= Topic.objects.filter(Topic_Type=topic_type)
    context = get_topic_list_common_data(request,topics_all_list)
    context['topics_type']=topic_type
    context['topics'] = topics_all_list
    return render(request,'topic_with_type.html',context)
#先是 topic_type = get_object_or_404(TopicType, pk=Topic_Type_pk) 通过pk=Topic_Type_pk 取得博客类型 （例如类型1，2，3）
#再是 context['topics'] = Topic.objects.filter(Topic_Type=topic_type)  Topic_Type=“类型：1或2或3
#凭pk=Topic_Type_pk”取得类型符合的所有topics

def topics_with_date(request,year,month):

    topics_all_list= Topic.objects.filter(create_time__year = year,create_time__month = month)

    context = get_topic_list_common_data(request,topics_all_list)
    context['topic_with_date'] = '%s年%s月' % (year,month)
    context['topics'] = topics_all_list
    context['topic_types'] = TopicType.objects.all()
    context['topic_dates'] = Topic.objects.dates('create_time','month',order='ASC')

    return render(request,'topic_with_date.html',context)

    
