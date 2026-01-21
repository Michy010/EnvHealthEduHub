from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.utils import timezone

# Create your models here.

User = get_user_model()

# Get or create a deleted user
def get_deleted_user():
    try:
        return User.objects.get(username='deleted_user')
    except User.DoesNotExist:
        # Create a deleted user placeholder
        deleted_user = User.objects.create_user(
            username='deleted_user',
            email='deleted@example.com',
            password='deleted_user_password_123',
            first_name='Deleted',
            last_name='User'
        )
        deleted_user.is_active = False
        deleted_user.save()
        return deleted_user

class Question(models.Model):
    question_category = (
        ('Regulations and Laws', 'Regulations and Laws'),
        ('Methodology', 'Methodology'),
        ('Learning Resources', 'Learning Resources'),
        ('Career Advice', 'Career Advice'),
        ('Technical', 'Technical Issues'),
    )
    user = models.ForeignKey(User, on_delete=models.SET(get_deleted_user))
    question_title = models.CharField(max_length=100)
    
    description = models.TextField()
    save_flag = models.BooleanField(default=False)
    category = models.CharField(max_length=30, choices=question_category)
    view_flag = models.PositiveIntegerField(default=0)
    date_time = models.DateTimeField(auto_now_add=True)

    @property
    def top_answers(self):
        return self.answers.filter(parent=None)

    def __str__(self):
        return self.question_title
    
class QuestionTag(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    tag = models.CharField(max_length=200)

    def __str__(self):
        return f'#{self.tag} - {self.question.question_title}'

class Reply(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    reply = models.TextField()
    date_time = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    user = models.ForeignKey(User, on_delete=models.SET(get_deleted_user))
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    is_best_answer = models.BooleanField(default=False)
    
    def __str__(self):
        return self.reply[:50]
    
    class Meta:
        ordering = ['-date_time']
    
    @property
    def rating_score(self):
        return self.upvotes - self.downvotes

class Vote(models.Model):
    VOTE_TYPES = (
        ('up', 'Upvote'),
        ('down', 'Downvote'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, related_name='votes')
    vote_type = models.CharField(max_length=4, choices=VOTE_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'reply']
    
    def __str__(self):
        return f"{self.user.username} - {self.vote_type} on Answer {self.reply.id}"

class Education(models.Model):
    edu_level = (
        ('Diploma', 'Diploma'),
        ('Degree', 'Degree'),
        ('Masters', 'Masters'),
        ('Other', 'Other')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='education')
    education_level = models.CharField(max_length=15, choices=edu_level)
    institution = models.CharField(max_length=100, default='Not included')

    def __str__(self):
        return f'{self.education_level}'

class Semister(models.Model):
    semester_choices = (
        ('First', 'First'),
        ('Second', 'Second'),
        ('Third', 'Third'),
        ('Fourth', 'Fourth'),
        ('Fifth', 'Fifth'),
        ('Sixth', 'Sixth'),
        ('Seventh', 'Seventh'),
        ('Eighth', 'Eighth'),
    )
    education = models.ForeignKey(Education, on_delete=models.CASCADE, related_name='semesters')
    semester = models.CharField(max_length=15, choices=semester_choices)

    def __str__(self):
        return f'{self.semester} Semester - {self.education.education_level}'

class Course(models.Model):
    EDUCATION_LEVELS = (
        ('Diploma', 'Diploma'),
        ('Degree', 'Degree'),
        ('Masters', 'Masters'),
        ('Other', 'Other')
    )
    
    education_level = models.CharField(
        max_length=15, 
        choices=EDUCATION_LEVELS,
        default='Degree'
    )
    
    course_name = models.CharField(max_length=150)
    course_code = models.CharField(max_length=150)
    course_credit = models.CharField(max_length=150, default='3')
    course_description = models.TextField()
    course_file = models.FileField(
        upload_to='documents/courses/',
        validators=[FileExtensionValidator(['pdf', 'docx', 'doc', 'ppt', 'pptx'])], 
        blank=True,
        null=True
    )
    
    uploaded_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='uploaded_courses'
    )
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.course_name} - {self.education_level}'
    
    class Meta:
        ordering = ['education_level', 'course_code']
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
    
class Regulation(models.Model):
    Categories = (
        ('water supply', 'Water supply'),
    )
    File_format = (
        ('pdf', 'PDF'),
        ('docx', 'DOCX'),
    )
    category = models.CharField(max_length=12, choices=Categories)
    regulation_name = models.CharField(max_length=200)
    regulation_file = models.FileField(upload_to='documents/regulations/', default='No file')
    updated_at = models.DateTimeField(auto_now=timezone.now)
    file_format = models.CharField(max_length=12, choices=File_format)

    def __str__(self):
        return self.regulation_name
    
class RegulationKeyword(models.Model):
    regulation = models.ForeignKey(Regulation, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.keyword} - {self.regulation.regulation_name}'