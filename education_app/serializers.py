from rest_framework import serializers

from education_app.models import Product, Lesson


class ProductSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = ('author', 'name', 'start_at', 'cost', 'lessons_count')


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('name', 'link_to_video')


class ProductLessonsSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('name', 'lessons')
