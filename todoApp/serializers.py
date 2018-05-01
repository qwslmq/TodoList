from rest_framework import serializers
from .models import TodoItem

class TodoItemSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    task=serializers.CharField(required=True,max_length=200)
    complete=serializers.BooleanField(required=False)

    def create(self, validated_data):
        return TodoItem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.task = validated_data.get("task",instance.task)
        instance.complete=validated_data.get("complete",instance.complete)
        return instance