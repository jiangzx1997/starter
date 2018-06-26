from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import MyUser

# Create your views here.

def logout_view(request):
    """注销用户"""
    logout(request)
    return HttpResponseRedirect(reverse('ddl:index'))

def register(request):
    if request.method != 'POST':
        print('method = get')
        form = RegistrationForm()
    else:
        print('method = post')
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password1'],
                email = form.cleaned_data['email'],
            )
            new_user = MyUser()
            new_user.user = user
            new_user.number = form.cleaned_data['number']
            new_user.name = form.cleaned_data['name']
            new_user.save()
            authenticate_user = authenticate(username = user.username, password = request.POST['password1'])
            login(request, authenticate_user)
            return HttpResponseRedirect('/')
        else:
            print('valid is not acceptable')
    context = {'form' : form}
    return render(request, 'users/register.html', context)

@login_required
def group(request):
    groups = request.user.group_set.all()
    context = {'groups':groups}
    return render(request, 'users/group.html', context)

@login_required
def new_group(request):
    if request.method != 'POST':
        # 未提交数据, 创建一个空表单
        form = GroupForm()
    else:
        # POST提交的数据, 对数据进行处理
        form = GroupForm(request.POST)
        if form.is_valid():
            new_group = form.save(commit = False)
            new_group.leader = request.user
            new_group.save()
            new_group.member.add(request.user)
            new_group.save()
            return HttpResponseRedirect(reverse('users:change_member', args=[new_group.id, 0]))
    context = {'group':group, 'form':form}
    return render(request, 'users/new_group.html', context)

@login_required
def change_group_name(request, group_id, to_id):
    group = Group.objects.get(id = group_id)
    if request.method != 'POST':
        # 未提交数据, 创建一个空表单
        form = GroupForm(instance = group)
    else:
        # POST提交的数据, 对数据进行处理
        form = GroupForm(instance = group, data = request.POST)
        if form.is_valid():
            form.save()
            if (to_id == '0'):
                return HttpResponseRedirect(reverse('users:change_member', args=[group_id, to_id]))
            else:
                return HttpResponseRedirect(reverse('users:group_info', args=[group_id]))
    context = {'group':group, 'form':form, 'to_id':to_id}
    return render(request, 'users/change_group_name.html', context)


@login_required
def add_member(request, group_id, to_id):

    group = Group.objects.get(id = group_id)
    if group.leader != request.user:
        raise Http404
    
    if request.method != 'POST':
        form = MemberIDForm()
        context = {'group':group, 'form':form, 'to_id': to_id}
        return render(request, 'users/change_member.html', context) 
    else:
        form = MemberIDForm(request.POST)
        if form.is_valid():
            type = form.cleaned_data['key']
            aim = request.user
            for user in User.objects.all():
                if form.cleaned_data['userID'] == user.myuser.number:
                    aim = user
                    break
            findflag = 0
            for user in group.member.all():
                if user == aim:
                    findflag = 1
                    break
            if type == 'act1':
                if not findflag:
                    group.member.add(aim)
            return HttpResponseRedirect(reverse('users:change_member', args=[group_id, to_id]))
    context = {'group':group, 'form':form, 'to_id': to_id}
    return render(request, 'users/change_member.html', context)

@login_required
def del_member(request, group_id, to_id, user_number):

    group = Group.objects.get(id = group_id)
    if group.leader != request.user:
        raise Http404
    
    aim = request.user
    for user in group.member.all():
        if str(user_number) == user.myuser.number:
            aim = user
            break
    group.member.remove(aim)
    return HttpResponseRedirect(reverse('users:change_member', args=[group_id, to_id]))

@login_required
def group_info(request, group_id):
    """管理既有小组"""
    group = Group.objects.get(id = group_id)
    
    if not request.user in group.member.all():
        raise Http404
    
    LeadFlag = True
    if group.leader != request.user:
        LeadFlag = False
    
    todos = group.grouptask_set.filter(tag = False).order_by('date_ended')
    finisheds = group.grouptask_set.filter(tag = True).order_by('date_ended')
    
    context = {'group':group, 'LeadFlag':LeadFlag, 'todos':todos, 'finisheds':finisheds}
    return render(request, 'users/group_info.html', context)

@login_required
def del_group(request, group_id):

    group = Group.objects.get(id = group_id)
    if group.leader != request.user:
        raise Http404
    group.delete()
    return HttpResponseRedirect(reverse('users:group',))

'''
def register(request):
    """注册新用户"""
    if request.method != 'POST':
        # 显示空的注册表单
        form = UserCreationForm()
    else:
        # 处理填写好的表单
        form = UserCreationForm(data = request.POST)
        
        if form.is_valid():
            new_user = form.save()
            # 让用户自动登陆, 再重定向到主页
            authenticate_user = authenticate(username = new_user.username, password = request.POST['password1'])
            login(request, authenticate_user)
            return HttpResponseRedirect(reverse('ddl:index'))
    
    context = {'form':form}
    return render(request, 'users/register.html', context)
'''