from django import forms
from .models import *
from django.core.validators import RegexValidator
# ------------------------
# Validator
# ------------------------
enroll_validator = RegexValidator(
    regex=r'^E\d{2}4833(355|389|330|338|380)\d{5}$',
    message='Enter the valid enrollment number!'
)

# ------------------------
# Student Login Form
# ------------------------
class StudentLoginForm(forms.Form):
    enrollment_no = forms.CharField(
        label="Enrollment No",
        validators=[enroll_validator],
        widget=forms.TextInput(attrs={'placeholder': 'Enter Enrollment No'})
    )
    dob = forms.DateField(
        label="Date of Birth",
        widget=forms.DateInput(attrs={'type': 'date'})
    )

# ---------------------
# Student Signup Form 
# ---------------------
class StudentSignupForm(forms.ModelForm):
    enroll = forms.CharField(
        label="Enrollment Number",
        validators=[enroll_validator],
        widget=forms.TextInput(attrs={'placeholder': 'Enter Enrollment Number'})
    )
    dob = forms.DateField(
        label="Date of Birth",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    admission_year = forms.IntegerField(
        label="Addmission Year",
        widget=forms.NumberInput(attrs={'min': 2000, 'max': 2100})
    )

    class Meta:
        model = Student
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # colon add after label
            field.label = f"{field.label}:"
            # lable change
            self.fields['tenth_board'].label = "Board:"
            self.fields['tenth_passing_year'].label = "Passing Year:"
            self.fields['tenth_percentage'].label = "Percentage:"
            # add Placeholder
            if 'placeholder' not in field.widget.attrs:
                field.widget.attrs['placeholder'] = f"Enter {field.label.replace(':','')}"
            
# ------------------------
# institute login form
# ------------------------  
class InstituteLoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=25)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

# ------------------------
# institute signup form
# ------------------------
class TeacherSignupForm(forms.Form):
    teacher = forms.ModelChoiceField(
        queryset=Teacher.objects.filter(teachersignup__isnull=True),  # Only unregistered teachers
        label="Select Your Name (Teacher)",
        empty_label="Select Teacher"
    )
    username = forms.CharField(max_length=25, label="Username")
    email = forms.EmailField(max_length=50, label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    

# ------------------------
# change password form
# ------------------------
class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new = cleaned_data.get('new_password')
        confirm = cleaned_data.get('confirm_password')
        if new != confirm:
            raise forms.ValidationError("New password and confirm password do not match.")
        return cleaned_data
    
# ------------------------
# corner content form
# ------------------------    
class CornerContentForm(forms.ModelForm):
    class Meta:
        model = Corner_content
        fields = ['content_title', 'content_desc', 'content_file', 'content_link', 'content_type', 'to_branch', 'to_year']

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get("content_file")
        link = cleaned_data.get("content_link")

        # Validation rules
        if not file and not link:
            raise forms.ValidationError("Please provide either a file or a link.")
        if file and link:
            raise forms.ValidationError("Please provide only one: file or link.")

        return cleaned_data

# ------------------------
# library management form
# ------------------------ 
class BookDetailsForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['book_name', 'publication', 'book_price', 'total_copies']
        
class BookStatusForm(forms.ModelForm):
    class Meta:
        model = BookCopy
        fields = ['book', 'book_set_id', 'is_available']
        
class BookIssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['book_set', 'student', 'teacher', 'issue_date', 'due_date', 'return_date', 'fine']
        