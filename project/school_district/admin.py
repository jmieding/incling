from django.contrib import admin

from .models import School, Classroom, Student

class SchoolAdmin(admin.ModelAdmin):
  model = School

class ClassroomAdmin(admin.ModelAdmin):
  model = Classroom

class StudentAdmin(admin.ModelAdmin):
  model = Student

admin.site.register(School, SchoolAdmin)
admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(Student, StudentAdmin)