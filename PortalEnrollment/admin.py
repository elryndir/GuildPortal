from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Enrollement)
admin.site.register(EnrollmentSettings)
admin.site.register(CommentEnrollment)
admin.site.register(EnrollmentVote)