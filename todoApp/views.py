#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from todoApp import models,forms,serializers
import hashlib

#hash函数
def hash_code(password, salt='todoList'):
    hashcode = hashlib.sha256()
    password += salt
    hashcode.update(password.encode())
    return hashcode.hexdigest()

#主页
def index(request):
    pass
    return render(request, 'todoApp/index.html')

#登录页面
def login(request):
    if request.session.get('is_login', None):
        return redirect("/index/")
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == hash_code(password):  # 哈希值和数据库内的值进行比对
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'todoApp/login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'todoApp/login.html', locals())

#注册页面
def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册
        return redirect("/index/")
    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'todoApp/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'todoApp/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'todoApp/register.html', locals())

                # 当一切都OK的情况下，创建新用户
                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)  # 使用加密密码
                new_user.email = email
                new_user.save()
                message = "用户注册成功"
                return redirect('/login/',locals())  # 自动跳转到登录页面

    register_form = forms.RegisterForm()
    return render(request, 'todoApp/register.html', locals())

#登出
def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/index/")
    request.session.flush()
    return redirect("/login/")

@csrf_exempt
def todoItems(request):
    if request.session.get('is_login', None):
        if request.method == 'GET':
            user = models.User.objects.get(name=request.session['user_name'])
            serializer = serializers.TodoItemSerializer(user.todoitem_set.all(), many=True)
            return JsonResponse(serializer.data, safe=False)

        elif request.method == 'POST':
            option = request.POST.get("option", None)
            if option =="complete":
                id = request.POST.get("id",None)
                if id :
                        todoItem = models.TodoItem.objects.get(id=id )
                        if todoItem.name==models.User.objects.get(name=request.session['user_name']):
                            todoItem.complete = False if todoItem.complete else True
                            todoItem.save()
                            serializer = serializers.TodoItemSerializer(todoItem)
                            return JsonResponse(serializer.data, safe=False)
            if option =="delete":
                id = request.POST.get("id",None)
                if id :
                    todoItem = models.TodoItem.objects.get(id=id)
                    if todoItem.name==models.User.objects.get(name=request.session['user_name']):
                        todoItem.delete()
                        return HttpResponse("删除成功")
            if option =="add":
                task = request.POST.get("task",None)
                if task and len(task)<200:
                    user = models.User.objects.get(name=request.session['user_name'])
                    todoItem = models.TodoItem(name=user,task=task)
                    todoItem.save()
                    serializer = serializers.TodoItemSerializer(todoItem)
                    return JsonResponse(serializer.data, safe=False)
            return HttpResponse("Please try again",status_code=300)
