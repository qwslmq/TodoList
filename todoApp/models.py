#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models

class User(models.Model):

    gender = (
        ('male', "男"),
        ('female', "女"),
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default="男")
    c_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"

class TodoItem(models.Model):
    name = models.ForeignKey(User)
    task = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now_add=True,blank=True)
    complete =models.BooleanField(default=False)
    def __unicode__(self):
        return self.task

