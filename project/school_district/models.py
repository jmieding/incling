from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models

class School(models.Model):
  name = models.CharField(max_length=100)

  def __str__(self):
    return self.name

class Classroom(models.Model):
  number = models.CharField(max_length=50)
  school = models.ForeignKey(School, on_delete=models.CASCADE)

  def clean(self):
    try:
      if Classroom.objects.get(number=self.number, school=self.school):
        raise ValidationError(
          'Classroom {0} already exists at {1}. '\
          .format(self.number, self.school)
          )
    except ObjectDoesNotExist:
      pass

  def save(self, *args, **kwargs):
    try:
      if Classroom.objects.get(number=self.number, school=self.school):
        raise ValidationError(
          'Classroom {0} already exists at {1}. '\
          .format(self.number, self.school)
          )
    except ObjectDoesNotExist:
      pass
    super(Classroom, self).save(*args, **kwargs)
  # Different schools can have rooms with the same number, but duplicate 
  # numbers within the same school are not permitted.

  def __str__(self):
    return self.number

class Student(models.Model):
  name = models.CharField(max_length=100)
  school = models.ForeignKey(School)
  classroom = models.ForeignKey(Classroom)
  # Classrooms and schools can have multiple students with the same name 
  # (e.g. "John Smith"), so there is no uniqueness requirement.

  def clean(self, *args, **kwargs):
    if self.classroom.school != self.school:
      try:
        self.classroom = Classroom.objects.get(
          school=self.school, 
          number=self.classroom,
        )
      except ObjectDoesNotExist:
        raise ValidationError(
          'Classroom {0} does not exist at School {1}. '\
          'If you meant to do this, either add a new school or a new'\
          'classroom.'\
          .format(self.classroom, self.school)
          )
  # If the admin tries to use the classroom instance that doesn't belong to 
  # the selected school, the clean method overrides the selection and 
  # chooses the classroom that does belong to that school. If there is 
  # no classroom with that number at the selected school, an validation error
  # is thrown.
    
  def save(self, *args, **kwargs):
    if self.classroom.school != self.school:
      try:
        self.classroom = Classroom.objects.get(
          school=self.school, 
          number=self.classroom,
        )
      except ObjectDoesNotExist:
        raise ValidationError(
          'Classroom {0} does not exist at School {1}. '\
          'If you meant to do this, either add a new school or a new'\
          'classroom.'\
          .format(self.classroom, self.school)
          )
    super(Student, self).save(*args, **kwargs)
  # Same functionality as the clean method, except 

  def __str__(self):
    return self.name