from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Course, Lesson, Enrollment, Progress
from .serializers import CourseSerializer, LessonSerializer, EnrollmentSerializer, ProgressSerializer
from django.shortcuts import get_object_or_404

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        course_id = self.request.query_params.get('course')
        qs = super().get_queryset()
        if course_id:
            qs = qs.filter(course_id=course_id)
        return qs

class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Enrollment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ProgressViewSet(viewsets.ModelViewSet):
    serializer_class = ProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Progress.objects.filter(enrollment__user=self.request.user)

    @action(detail=False, methods=['post'])
    def mark(self, request):
        enrollment_id = request.data.get('enrollment_id')
        lesson_id = request.data.get('lesson_id')
        completed = request.data.get('completed', True)
        enrollment = get_object_or_404(Enrollment, id=enrollment_id, user=request.user)
        progress, created = Progress.objects.get_or_create(enrollment=enrollment, lesson_id=lesson_id)
        progress.completed = completed
        progress.save()
        return Response(ProgressSerializer(progress).data)
