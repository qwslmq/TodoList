#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from . import models

admin.site.register(models.User)
admin.site.register(models.TodoItem)
# Register your models here.
