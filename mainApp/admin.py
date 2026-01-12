from django.contrib import admin
from . models import Education, Reply, Course, Question, Semister, RegulationKeyword, Regulation

# Register your models here.
admin.site.register(Education)
admin.site.register(Regulation)
admin.site.register(Reply)
admin.site.register(Course)
admin.site.register(Question)
admin.site.register(Semister)
admin.site.register(RegulationKeyword)