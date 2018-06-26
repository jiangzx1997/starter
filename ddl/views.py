from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse # 此处有改动
from django.contrib.auth.decorators import login_required
from django.db import models

from .models import Topic, Entry
from .forms import EntryForm, GroupTaskForm
from datetime import datetime

from users.models import Group

# Create your views here.
def index(request):
    """学习笔记的主页"""
    return render(request, 'ddl/index.html')

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
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data = request.POST)
        if form.is_valid():
            new_entry = form.save(commit = False)
            new_entry.owner = request.user
            new_entry.date_ended = datetime(new_entry.YYYY, new_entry.MM, new_entry.DD)
            new_entry.save()
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

@login_required
def new_group_task(request, group_id):
    """在特定的主题中添加新条目"""
    group = Group.objects.get(id = group_id)
    
    if group.leader != request.user:
        raise Http404
    
    if request.method != 'POST':
        form = GroupTaskForm()
    else:
        form = GroupTaskForm(data = request.POST)
        if form.is_valid():
            new_entry = form.save(commit = False)
            new_entry.owner = request.user
            new_entry.group = group
            new_entry.date_ended = datetime(new_entry.YYYY, new_entry.MM, new_entry.DD)
            new_entry.save()
            return HttpResponseRedirect(reverse('users:group_info', args=[group_id]))
    context = {'group':group, 'form':form}
    return render(request, 'ddl/new_group_task.html', context)
