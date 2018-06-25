from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse # 此处有改动
from django.contrib.auth.decorators import login_required
from django.db import models

from .models import Topic, Entry
from .forms import EntryForm
from datetime import datetime

# Create your views here.
def index(request):
    """学习笔记的主页"""
    return render(request, 'ddl/index.html')

'''
@login_required
def topics(request):
    """显示所有的主题"""
    topics = Topic.objects.filter(owner = request.user).order_by('date_added')
    context = {'topics__':topics}
    return render(request, 'ddl/topics.html', context)
'''


@login_required
def topic(request):
    """显示单个主题及其所有的条目"""
#    topic = Topic.objects.get(id = topic_id)
    # 确认请求的主题属于当前用户
#    if topic.owner != request.user:
#        raise Http404
    todos = Entry.objects.filter(owner = request.user, tag = False).order_by('date_ended')
    finisheds = Entry.objects.filter(owner = request.user, tag = True).order_by('date_ended')
    context = {'todos':todos, 'finisheds':finisheds}
    return render(request, 'ddl/topic.html', context)

'''
@login_required   
def new_topic(request):
    """添加新主题"""
    if request.method != 'POST':
        # 未提交数据：创建一个新表单
        form = TopicForm()
    else:
        # POST提交的数据，对数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit = False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('ddl:topics'))
    context = {'form':form}
    return render(request, 'ddl/new_topic.html', context)
'''

def date_to_string(YYYY, MM, DD):
    date = str(YYYY) + '-'
    if MM < 10:
        date += '0'
    date += str(MM) + '-'
    if DD < 10:
        date += '0'
    date += str(DD)

@login_required
def new_entry(request):
    """在特定的主题中添加新条目"""
#    topic = Topic.objects.get(id = topic_id)
    if request.method != 'POST':
        # 未提交数据, 创建一个空表单
        form = EntryForm()
    else:
        # POST提交的数据, 对数据进行处理
        form = EntryForm(data = request.POST)
        if form.is_valid():
            new_entry = form.save(commit = False)
            new_entry.owner = request.user
            #new_entry.date_ended = date_to_string(new_entry.YYYY, new_entry.MM, new_entry.DD)
            new_entry.date_ended = datetime(new_entry.YYYY, new_entry.MM, new_entry.DD)
            #new_entry.date_ended = "2018-02-01"
            new_entry.save()
            #new_entry.objects.fliter(owner = request.user).update(
            #    date_ended = models.DateTimeField(new_entry.YYYY, new_entry.MM, new_entry.DD))
            return HttpResponseRedirect(reverse('ddl:topic'))
    context = {'form':form}
    return render(request, 'ddl/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """编辑既有条目"""
    entry = Entry.objects.get(id = entry_id)
#    topic = entry.topic
    
    if entry.owner != request.user:
        raise Http404
    
    if request.method != 'POST':
        # 初次请求, 使用当前条目填充表单
        form = EntryForm(instance = entry)

    else:
        # POST提交的数据, 对数据进行处理
        form = EntryForm(instance = entry, data = request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('ddl:topic'))
            
    context = {'entry':entry, 'topic':topic, 'form':form}
    return render(request, 'ddl/edit_entry.html', context)

@login_required
def delete_entry(request, entry_id):
    """删除既有条目"""
    entry = Entry.objects.get(id = entry_id)

    if entry.owner != request.user:
        raise Http404

    Entry.objects.filter(id = entry_id).delete()
    return HttpResponseRedirect(reverse('ddl:topic'))

@login_required
def finish_entry(request, entry_id):
    """完成既有条目"""
    entry = Entry.objects.get(id = entry_id)

    if entry.owner != request.user:
        raise Http404

    Entry.objects.filter(id = entry_id).update(tag=True)
    return HttpResponseRedirect(reverse('ddl:topic'))
    
