from django.urls import path
from . import views

app_name = 'mainApp'

urlpatterns = [
    path('', views.homeView, name='home'),
    path('material/', views.coursesView, name='material'),
    path('regulation/', views.regulationView, name='regulation'),
    path('submit_question/', views.questionView, name='question'),
    path('reply_qn/', views.reply_question, name='reply'),

    # Course management URLs
    path('admin-access/courses/', views.admin_course_dashboard, name='admin_course_dashboard'),
    path('admin-access/courses/add/', views.add_course, name='add_course'),
    path('admin-access/courses/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('admin-access/courses/<int:course_id>/delete/', views.delete_course, name='delete_course'),
    path('admin-access/courses/<int:course_id>/toggle-status/', views.toggle_course_status, name='toggle_course_status'),
    path('admin-access/courses/bulk-action/', views.bulk_action_courses, name='bulk_action_courses'),
    path('admin-access/courses/statistics/', views.course_statistics, name='course_statistics'),

    # Public courses URL (for students)
    path('courses/', views.coursesView, name='courses'),
    
]
