from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
import json
from . models import Course, Question, QuestionTag, Reply, Education, Semister, Vote

# Create your views here.
def homeView(request):
    question_obj = Question.objects.all().prefetch_related(
        'questiontag_set',
        'answers__children',
        'answers__votes',
    ).order_by('-date_time')

    paginator = Paginator(question_obj, 5)
    page_num = request.GET.get('page')
    question_object = paginator.get_page(page_num)
    
    # Calculate dynamic stats for authenticated users
    if request.user.is_authenticated:
        questions_asked = Question.objects.filter(user=request.user).count()
        answers_provided = Reply.objects.filter(user=request.user).count()
        # Calculate total upvotes for user's answers
        user_answers = Reply.objects.filter(user=request.user)
        answer_likes = sum(answer.upvotes for answer in user_answers)
        
        # Annotate answers with user vote information
        for question in question_object:
            for answer in question.answers.all():
                user_vote = answer.votes.filter(user=request.user).first()
                if user_vote:
                    answer.user_vote = user_vote.vote_type
                else:
                    answer.user_vote = None
    else:
        questions_asked = 0
        answers_provided = 0
        answer_likes = 0

    context = {
        'question_obj': question_object,
        'questions_asked': questions_asked,
        'answers_provided': answers_provided,
        'materials_accessed': 42,  # Replace with actual calculation
        'works_published': 3,      # Replace with actual calculation
        'answer_likes': answer_likes,       
        'helpful_answers': 8,      # Replace with actual calculation
        'downloads': 156,          # Replace with actual calculation
        'profile_views': 89,       # Replace with actual calculation
    }
        
    return render(request, 'mainApp/index.html', context)

@login_required
def reply_question(request):
    if request.method == 'POST':
        reply_text = request.POST.get('reply')
        question_id = request.POST.get('question')
        parent_id = request.POST.get('parent_id')
        
        print(f"Reply: {reply_text}")
        print(f"Question ID: {question_id}")
        print(f'Parent ID: {parent_id}')
        
        if not reply_text or not question_id:
            return JsonResponse({
                'success': False, 
                'message': 'Reply and question ID are required.'
            })
        
        try:
            # Get the question
            question = Question.objects.get(id=question_id)
            
            # Handle parent reply if exists
            parent_reply = None
            if parent_id:
                try:
                    parent_reply = Reply.objects.get(id=parent_id)
                except Reply.DoesNotExist:
                    return JsonResponse({
                        'success': False,
                        'message': 'Parent reply not found.'
                    })
            
            # Create the reply
            Reply.objects.create(
                reply=reply_text,
                question=question,
                user=request.user,
                parent=parent_reply  # Pass the Reply instance, not ID
            )
            
            return JsonResponse({
                'success': True, 
                'message': 'Reply submitted successfully.'
            })
            
        except Question.DoesNotExist:
            return JsonResponse({
                'success': False, 
                'message': 'Question not found.'
            })
        except Exception as e:
            print(f"Error creating reply: {e}")
            return JsonResponse({
                'success': False, 
                'message': f'An error occurred while submitting your reply: {str(e)}'
            })
    
    # If not POST request, redirect to home
    return redirect('mainApp:home')


def regulationView(request):
    return render(request, 'mainApp/regulations.html')

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

def questionView(request):
    if request.method == 'POST':
        question_title = request.POST.get('question_title')
        question = request.POST.get('question')
        question_category = request.POST.get('category')
        question_tags = request.POST.get('tag', '')

        user = request.user

        qn = Question.objects.create(
            user=user,
            question_title=question_title,
            category=question_category,
            description=question,
            view_flag=1
        )

        # Create QuestionTag objects
        tag_objects = []
        for tag in question_tags.strip().split(','):
            tag = tag.strip()
            if tag:  # Only add non-empty tags
                tag_objects.append(QuestionTag(question=qn, tag=tag))

        if tag_objects:
            QuestionTag.objects.bulk_create(tag_objects)

        return JsonResponse({
            'message': 'Question submitted successfully',
            'status': 'successful'
        })
    
    question_obj = Question.objects.all().prefetch_related('questiontag_set')
    paginator = Paginator(question_obj, 5)
    page_num = request.GET.get('page')
    question_object = paginator.get_page(page_num)

    return render(request, 'mainApp/index.html', {'question_object': question_object})

# Check if user is admin
def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def admin_course_dashboard(request):
    """Admin dashboard for managing courses"""
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
        'education_levels': Course.EDUCATION_LEVELS,
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
        education_level = request.POST.get('education_level')
        course_file = request.FILES.get('course_file')
        
        # Validation
        if not all([course_name, course_code, course_description, education_level]):
            messages.error(request, 'Please fill in all required fields')
            return redirect('mainApp:admin_course_dashboard')
        
        if not course_file:
            messages.error(request, 'Please upload course materials')
            return redirect('mainApp:admin_course_dashboard')
        
        # Check file size
        max_size = 10 * 1024 * 1024
        if course_file.size > max_size:
            messages.error(request, 'File size exceeds 10MB limit')
            return redirect('mainApp:admin_course_dashboard')
        
        try:
            # Check if course code already exists
            if Course.objects.filter(course_code=course_code).exists():
                messages.warning(request, f'Course code "{course_code}" already exists')
                return redirect('mainApp:admin_course_dashboard')
            
            # Create course
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
            
            # Update education_level
            education_level = request.POST.get('education_level')
            if education_level in dict(Course.EDUCATION_LEVELS).keys():
                course.education_level = education_level
            
            # Handle file upload
            if 'course_file' in request.FILES and request.FILES['course_file']:
                new_file = request.FILES['course_file']
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

def load_more_answers(request):
    question_id = request.GET.get('question')
    offset = int(request.GET.get('offset', 0))
    limit = 5
    
    try:
        question = Question.objects.get(id=question_id)
        # Get top-level answers only (parent=None)
        answers = question.answers.filter(parent=None).order_by('-date_time')[offset:offset + limit]
        
        html = render_to_string('mainApp/answer_tree.html', {
            'answers': answers
        }, request=request)
        
        return JsonResponse({
            'success': True,
            'html': html,
            'has_more': question.answers.filter(parent=None).count() > offset + limit
        })
        
    except Question.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Question not found.'
        })

@login_required

def rate_answer(request):
    try:
        data = json.loads(request.body)
        answer_id = data.get('answer_id')
        vote_type = data.get('type')  # 'up' or 'down'
        
        if not answer_id or vote_type not in ['up', 'down']:
            return JsonResponse({
                'success': False,
                'message': 'Invalid request data'
            })
        
        try:
            answer = Reply.objects.get(id=answer_id)
        except Reply.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Answer not found'
            })
        
        # Check if user already voted
        existing_vote = Vote.objects.filter(user=request.user, reply=answer).first()
        
        if existing_vote:
            # User is changing their vote
            if existing_vote.vote_type == vote_type:
                # User is removing their vote
                existing_vote.delete()
                if vote_type == 'up':
                    answer.upvotes = max(0, answer.upvotes - 1)
                else:
                    answer.downvotes = max(0, answer.downvotes - 1)
            else:
                # User is changing vote type
                if existing_vote.vote_type == 'up':
                    answer.upvotes = max(0, answer.upvotes - 1)
                    answer.downvotes += 1
                else:
                    answer.downvotes = max(0, answer.downvotes - 1)
                    answer.upvotes += 1
                existing_vote.vote_type = vote_type
                existing_vote.save()
        else:
            # New vote
            Vote.objects.create(
                user=request.user,
                reply=answer,
                vote_type=vote_type
            )
            if vote_type == 'up':
                answer.upvotes += 1
            else:
                answer.downvotes += 1
        
        answer.save()
        
        # Check if user has already voted
        user_vote = None
        if request.user.is_authenticated:
            user_vote_obj = Vote.objects.filter(user=request.user, reply=answer).first()
            if user_vote_obj:
                user_vote = user_vote_obj.vote_type
        
        return JsonResponse({
            'success': True,
            'upvotes': answer.upvotes,
            'downvotes': answer.downvotes,
            'rating_score': answer.rating_score,
            'user_vote': user_vote,
            'message': 'Vote submitted successfully'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        })