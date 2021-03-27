from django.contrib import admin
from .models import Subject, Course, Module,Completed,CourseRating
# Register your models here.

# register subject in the admin
@admin.register(Subject)
# contents information of the course to show admin
class SubjectAdmin(admin.ModelAdmin):
    pass

@admin.register(Module)
# contents information of the course to show admin
class ModuleAdmin(admin.ModelAdmin):
    pass

# register admin for course
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass

@admin.register(Completed)
class CompletedAdmin(admin.ModelAdmin):
    pass
@admin.register(CourseRating)
class CourseRatingAdmin(admin.ModelAdmin):
    pass