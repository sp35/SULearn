from django.apps import AppConfig


class CourseConfig(AppConfig):
    name = 'course'
    def ready(self):
        import course.signals