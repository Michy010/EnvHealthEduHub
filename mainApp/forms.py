# forms.py
from django import forms
from .models import Course, Education

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['education', 'course_name', 'course_code', 'course_credit', 'course_description', 'course_file']
        widgets = {
            'course_description': forms.Textarea(attrs={'rows': 4}),
            'course_name': forms.TextInput(attrs={'placeholder': 'Enter course name'}),
            'course_code': forms.TextInput(attrs={'placeholder': 'Enter course code'}),
            'course_credit': forms.TextInput(attrs={'placeholder': 'Enter course credits'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['education'].queryset = Education.objects.all()
        self.fields['education'].label = 'Education Level'