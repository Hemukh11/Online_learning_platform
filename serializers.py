from rest_framework import serializers
from .models import Course, Lesson, Enrollment, Progress
from django.contrib.auth import get_user_model

User = get_user_model()

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id','title','content','order']

class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        fields = ['id','title','description','created_at','lessons']

class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), source='course', write_only=True)
    class Meta:
        model = Enrollment
        fields = ['id','course','course_id','enrolled_at']

class ProgressSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer(read_only=True)
    lesson_id = serializers.PrimaryKeyRelatedField(queryset=Lesson.objects.all(), source='lesson', write_only=True)
    class Meta:
        model = Progress
        fields = ['id','lesson','lesson_id','completed','updated_at']
