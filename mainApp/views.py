from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from . models import Course, Question, QuestionTag, Reply, Education, Semister

# Create your views here.
def homeView (request):
    question_obj = Question.objects.all().prefetch_related(
        'questiontag_set',
        'answers__children',
    ).order_by('-date_time')

    paginator = Paginator(question_obj, 5)
    page_num = request.GET.get('page')
    question_object = paginator.get_page(page_num)

    context = {
        'question_obj': question_object
    }
        
    return render(request, 'mainApp/index.html', context)

@login_required
def reply_question(request):
    if request.method == 'POST':
        reply = request.POST.get('reply')
        question_id = request.POST.get('question')
        parent = request.POST.get('parent_id')
        
        print(f"Reply: {reply}")
        print(f"Question ID: {question_id}")
        print(f'Parent ID: {parent}')
        
        if not reply or not question_id:
            return JsonResponse({
                'success': False, 
                'message': 'Reply and question ID are required.'
            })
        
        try:
            # Create the reply
            Reply.objects.create(
                reply=reply,
                question_id=question_id,
                user=request.user,
                parent = parent if parent else None
            )
            
            return JsonResponse({
                'success': True, 
                'message': 'Reply submitted successfully.'
            })
            
        except Exception as e:
            print(f"Error creating reply: {e}")
            return JsonResponse({
                'success': False, 
                'message': 'An error occurred while submitting your reply.'
            })
    
    # If not POST request, redirect to home
    return redirect('mainApp:home')


def regulationView (request):
    return render (request, 'mainApp/regulations.html')


@login_required
def coursesView(request):
    if request.method == 'POST':
        # Get form data
        course_name = request.POST.get('course_name')
        course_code = request.POST.get('course_code')
        course_description = request.POST.get('course_description')
        course_file = request.FILES.get('course_file')
        education_level = request.POST.get('education_level')
        course_credit = request.POST.get('course_credit', '3')
        
        # Validate required fields
        if not all([course_name, course_code, course_description, education_level]):
            return JsonResponse({
                'success': False,
                'message': 'Please fill in all required fields'
            }, status=400)
        
        # Validate file
        if not course_file:
            return JsonResponse({
                'success': False,
                'message': 'Please upload a course file'
            }, status=400)
        
        # Check file size
        max_size = 10 * 1024 * 1024  # 10MB
        if course_file.size > max_size:
            return JsonResponse({
                'success': False,
                'message': 'File size exceeds 10MB limit'
            }, status=400)
        
        try:
            # Create the course
            course = Course.objects.create(
                education_level=education_level,
                course_name=course_name,
                course_code=course_code,
                course_description=course_description,
                course_credit=course_credit,
                course_file=course_file,
                uploaded_by=request.user
            )
            
            return JsonResponse({
                'success': True,
                'message': f'Course "{course_name}" has been added successfully!',
                'course_id': course.id
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error creating course: {str(e)}'
            }, status=500)
    
    # GET request - display all courses
    # Get all active courses
    all_courses = Course.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        all_courses = all_courses.filter(
            Q(course_name__icontains=search_query) |
            Q(course_code__icontains=search_query) |
            Q(course_description__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(all_courses, 12) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Filter by education level for the template sections
    context = {
        'courses': page_obj,
        'diploma_courses': all_courses.filter(education_level='Diploma'),
        'bachelor_courses': all_courses.filter(education_level='Degree'),
        'master_courses': all_courses.filter(education_level='Masters'),
        'other_courses': all_courses.filter(education_level='Other'),
        'search_query': search_query,
        'total_courses': all_courses.count(),
    }
    
    return render(request, 'mainApp/materials.html', context)


def questionView (request):
    if request.method == 'POST':
        question_title = request.POST.get('question_title')
        question = request.POST.get('question')
        question_category = request.POST.get('category')
        question_tags = request.POST.get('tag', '')

        print(question_category)

        user = request.user

        qn = Question.objects.create(
            user = user,
            question_title = question_title,
            category = question_category,
            description = question,
            view_flag = 1
        )

        """Creating python QuestionTag objects for each tag in question_tags list
            This reduces the database hit
        """
        tag_objects = []
        for tag in question_tags.strip().split(','):
            _tag = QuestionTag(question=qn, tag=tag)
            tag_objects.append(_tag)

        """Saving the objects in the database only once
            Hit database only once
        """
        QuestionTag.objects.bulk_create(tag_objects)

        return JsonResponse({
            'message': 'Question submitted successful',
            'status': 'successful'
        })
    
    question_obj = Question.objects.all().prefetch_related('questiontag_set')

    paginator = Paginator(question_obj, 5)
    page_num = request.GET.get('page')
    question_object = paginator.get_page(page_num)

    return render (request, 'mainApp/index.html', {'question_object':question_object})



# Check if user is admin
def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def admin_course_dashboard(request):
    """Admin dashboard for managing courses"""
    # Get all courses
    courses = Course.objects.all()
    
    # Filtering options
    education_level = request.GET.get('education_level', '')
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    # Apply filters
    if education_level:
        courses = courses.filter(education_level=education_level)
    
    if search_query:
        courses = courses.filter(
            Q(course_name__icontains=search_query) |
            Q(course_code__icontains=search_query) |
            Q(course_description__icontains=search_query)
        )
    
    if status_filter:
        if status_filter == 'active':
            courses = courses.filter(is_active=True)
        elif status_filter == 'inactive':
            courses = courses.filter(is_active=False)
    
    # Get counts by education level
    diploma_count = Course.objects.filter(education_level='Diploma').count()
    degree_count = Course.objects.filter(education_level='Degree').count()
    masters_count = Course.objects.filter(education_level='Masters').count()
    other_count = Course.objects.filter(education_level='Other').count()
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(courses.order_by('-created_at'), 20)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'courses': page_obj,
        'total_courses': Course.objects.count(),
        'diploma_count': diploma_count,
        'degree_count': degree_count,
        'masters_count': masters_count,
        'other_count': other_count,
        'active_courses': Course.objects.filter(is_active=True).count(),
        'inactive_courses': Course.objects.filter(is_active=False).count(),
        'education_level_filter': education_level,
        'search_query': search_query,
        'status_filter': status_filter,
        'education_levels': Course.EDUCATION_LEVELS,  # Get choices from model
    }
    return render(request, 'mainApp/admin_courses.html', context)

@login_required
@user_passes_test(is_admin)
def add_course(request):
    """Add a new course"""
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        course_code = request.POST.get('course_code')
        course_credit = request.POST.get('course_credit', '3')
        course_description = request.POST.get('course_description')
        education_level = request.POST.get('education_level')  # Changed from education_id
        course_file = request.FILES.get('course_file')
        
        # Validation
        if not all([course_name, course_code, course_description, education_level]):
            messages.error(request, 'Please fill in all required fields')
            return redirect('mainApp:admin_course_dashboard')
        
        if not course_file:
            messages.error(request, 'Please upload course materials')
            return redirect('mainApp:admin_course_dashboard')
        
        # Check file size
        max_size = 10 * 1024 * 1024  # 10MB
        if course_file.size > max_size:
            messages.error(request, 'File size exceeds 10MB limit')
            return redirect('mainApp:admin_course_dashboard')
        
        try:
            # Check if course code already exists
            if Course.objects.filter(course_code=course_code).exists():
                messages.warning(request, f'Course code "{course_code}" already exists')
                return redirect('mainApp:admin_course_dashboard')
            
            # Create course - NO education ForeignKey, use education_level directly
            course = Course.objects.create(
                education_level=education_level,
                course_name=course_name,
                course_code=course_code,
                course_credit=course_credit,
                course_description=course_description,
                course_file=course_file,
                uploaded_by=request.user
            )
            
            messages.success(request, f'Course "{course_name}" added successfully!')
            
        except Exception as e:
            messages.error(request, f'Error adding course: {str(e)}')
        
        return redirect('mainApp:admin_course_dashboard')
    
    # If GET request, redirect to dashboard
    return redirect('mainApp:admin_course_dashboard')

@login_required
@user_passes_test(is_admin)
def edit_course(request, course_id):
    """Edit an existing course"""
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        try:
            course.course_name = request.POST.get('course_name', course.course_name)
            course.course_code = request.POST.get('course_code', course.course_code)
            course.course_credit = request.POST.get('course_credit', course.course_credit)
            course.course_description = request.POST.get('course_description', course.course_description)
            
            # Update education_level instead of education ForeignKey
            education_level = request.POST.get('education_level')
            if education_level in dict(Course.EDUCATION_LEVELS).keys():
                course.education_level = education_level
            
            # Handle file upload
            if 'course_file' in request.FILES and request.FILES['course_file']:
                new_file = request.FILES['course_file']
                # Check file size
                max_size = 10 * 1024 * 1024
                if new_file.size > max_size:
                    return JsonResponse({
                        'success': False,
                        'message': 'File size exceeds 10MB limit'
                    })
                course.course_file = new_file
            
            course.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Course "{course.course_name}" updated successfully!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error updating course: {str(e)}'
            })
    
    # If GET request, return course data for editing
    return JsonResponse({
        'success': True,
        'data': {
            'id': course.id,
            'course_name': course.course_name,
            'course_code': course.course_code,
            'course_credit': course.course_credit,
            'course_description': course.course_description,
            'education_level': course.education_level,  
            'is_active': course.is_active,
            'created_at': course.created_at.strftime('%Y-%m-%d %H:%M'),
            'uploaded_by': course.uploaded_by.username if course.uploaded_by else 'Unknown',
            'file_url': course.course_file.url if course.course_file and course.course_file != 'No file' else None,
            'file_name': course.course_file.name.split('/')[-1] if course.course_file and course.course_file != 'No file' else 'No file',
        }
    })

@login_required
@user_passes_test(is_admin)
def delete_course(request, course_id):
    """Delete or deactivate a course"""
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        action = request.POST.get('action', 'deactivate')
        
        try:
            if action == 'delete':
                course_name = course.course_name
                course.delete()
                messages.success(request, f'Course "{course_name}" deleted permanently!')
            else:
                # Toggle active status
                course.is_active = not course.is_active
                course.save()
                status = "activated" if course.is_active else "deactivated"
                messages.success(request, f'Course "{course.course_name}" {status}!')
                
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return redirect('mainApp:admin_course_dashboard')

@login_required
@user_passes_test(is_admin)
def toggle_course_status(request, course_id):
    """Toggle course active status (AJAX version)"""
    if request.method == 'POST':
        course = get_object_or_404(Course, id=course_id)
        course.is_active = not course.is_active
        course.save()
        
        status = "activated" if course.is_active else "deactivated"
        return JsonResponse({
            'success': True,
            'message': f'Course {status} successfully',
            'is_active': course.is_active,
            'course_id': course.id
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required
@user_passes_test(is_admin)
def bulk_action_courses(request):
    """Handle bulk actions on courses"""
    if request.method == 'POST':
        action = request.POST.get('bulk_action')
        course_ids = request.POST.getlist('course_ids[]')
        
        if not course_ids:
            messages.error(request, 'No courses selected')
            return redirect('mainApp:admin_course_dashboard')
        
        courses = Course.objects.filter(id__in=course_ids)
        
        try:
            if action == 'activate':
                courses.update(is_active=True)
                count = courses.count()
                messages.success(request, f'{count} course(s) activated successfully!')
                
            elif action == 'deactivate':
                courses.update(is_active=False)
                count = courses.count()
                messages.success(request, f'{count} course(s) deactivated successfully!')
                
            elif action == 'delete':
                count = courses.count()
                course_names = [c.course_name for c in courses]
                courses.delete()
                messages.success(request, f'{count} course(s) deleted permanently!')
                
            else:
                messages.error(request, 'Invalid action selected')
                
        except Exception as e:
            messages.error(request, f'Error performing bulk action: {str(e)}')
    
    return redirect('mainApp:admin_course_dashboard')

@login_required
@user_passes_test(is_admin)
def course_statistics(request):
    """Get course statistics for dashboard"""
    from django.db.models import Count
    from datetime import datetime, timedelta
    
    # Get time-based statistics
    today = datetime.now().date()
    last_week = today - timedelta(days=7)
    last_month = today - timedelta(days=30)
    
    # Course counts by level
    level_stats = Course.objects.values('education_level').annotate(
        count=Count('id'),
        active_count=Count('id', filter=Q(is_active=True))
    ).order_by('education_level')
    
    # Recent activity
    recent_courses = Course.objects.filter(
        created_at__gte=last_month
    ).count()
    
    # Courses by uploader
    uploader_stats = Course.objects.values('uploaded_by__username').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    # Monthly course creation trend
    from django.db.models.functions import TruncMonth
    monthly_trend = Course.objects.annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')[:12]
    
    return JsonResponse({
        'success': True,
        'data': {
            'level_stats': list(level_stats),
            'recent_courses': recent_courses,
            'uploader_stats': list(uploader_stats),
            'monthly_trend': list(monthly_trend),
            'total_courses': Course.objects.count(),
            'active_courses': Course.objects.filter(is_active=True).count(),
            'diploma_courses': Course.objects.filter(education_level='Diploma').count(),
            'bachelor_courses': Course.objects.filter(education_level='Degree').count(),
            'master_courses': Course.objects.filter(education_level='Masters').count(),
        }
    })