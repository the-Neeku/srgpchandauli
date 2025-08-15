import os
from django.db import models
from datetime import date
from django.core.exceptions import ValidationError

# Create your models here.

# ==========================
# College slide-photo table
# ==========================
class college_photo(models.Model):
    photo=models.ImageField(upload_to='college-photo/')
    updated_at = models.DateTimeField(auto_now=True)
    
    def filename(self):
        return os.path.basename(self.photo.name)

# =========================
# College principal table
# =========================
class Principal(models.Model):
    name=models.CharField(max_length=50)
    photo=models.ImageField(upload_to='principal/',blank=True, null=True)
    post=models.CharField(max_length=100)
    sec_post=models.CharField(max_length=300,blank=True, null=True)
    from_date=models.DateField()
    to_date=models.DateField(null=True, blank=True)
    message=models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
    
    def filename(self):
        return os.path.basename(self.photo.name)

# ======================
# College events table
# ======================  
def event_upload_path(instance, filename):
    folder = instance.folder_name or 'uncategorized'
    return os.path.join('events',folder, filename)

class Event(models.Model):
    folder_name = models.CharField(max_length=100, help_text="Enter folder name (e.g. nature, prices, etc.)")
    events_photo=models.ImageField(upload_to=event_upload_path)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.folder_name}"
    
    def filename(self):
        return os.path.basename(self.events_photo.name)

# ======================
# College notice table
# ======================
class Notice(models.Model):
    notice_content=models.CharField(max_length=300)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.notice_content
    
# ======================
# College link table
# ======================
class Imp_link(models.Model):
    view_content=models.CharField(max_length=200)
    links=models.CharField(max_length=250)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.view_content

# =========================
# Importent persion table
# =========================
class Imp_person(models.Model):
    name=models.CharField(max_length=50)
    post=models.CharField(max_length=200)
    photo=models.ImageField(upload_to='imp_person/')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def filename(self):
        return os.path.basename(self.photo.name)
    
# ======================
# College about table
# ======================
class About(models.Model):
    title=models.CharField(max_length=100)
    desc=models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
# ========================
# Colllege contect table
# ========================
class Contact(models.Model):
    address=models.TextField()
    phone=models.CharField(max_length=15)
    email=models.EmailField(max_length=50)
    note=models.TextField(max_length=200,blank=True, null=True)
    map_link=models.CharField(max_length=300)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.address

# ==========================
# College facilities table
# ==========================
class Facility(models.Model):
    title=models.CharField(max_length=200)
    image=models.ImageField(upload_to='facility/')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def filename(self):
        return os.path.basename(self.image.name)
    
# ======================
# course details table
# ======================
class Course(models.Model):
    course_name=models.CharField(max_length=100)
    Duration = models.CharField(max_length=100)
    seats = models.IntegerField()
    Eligibility = models.CharField(max_length=100)
    syllabus=models.FileField(blank=True, upload_to='syllabus/')
    details=models.TextField(blank=True, null=True)
    course_desc=models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.course_name

# ====================
# review table
# ====================
class Review(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    review_type=models.CharField(max_length=50)
    description=models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
# ====================
# Student table
# ====================
class Student(models.Model):
    # 1. Basic Details
    enroll = models.CharField(max_length=20, primary_key=True)  # Unique Enrollment Number
    student_name = models.CharField(max_length=50)  # Full Name
    father_name = models.CharField(max_length=50)
    mother_name = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    dob = models.DateField(verbose_name="Date of Birth")
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='students/photos/', blank=True, null=True)

    # 2. Contact Details
    student_mobile = models.CharField(max_length=15, unique=True)
    parent_mobile = models.CharField(max_length=15)
    email = models.EmailField(max_length=50, unique=True)
    permanent_address = models.TextField()
    current_address = models.TextField(blank=True, null=True)

    # 3. Academic Details
    admission_year = models.PositiveIntegerField()
    branch = models.CharField(max_length=50, choices=[('CSE', 'CSE'), ('EC', 'EC'), ('IC','IC')])
    mode_of_admission = models.CharField(max_length=50, choices=[('Direct', 'Direct'), ('Entrance Exam', 'Entrance Exam')])
    admission_type = models.CharField(max_length=50, choices=[('Regular', 'Regular'), ('Lateral', 'Lateral')])

    # 4. Previous Education
    tenth_school = models.CharField(max_length=100)
    tenth_board = models.CharField(max_length=50)
    tenth_passing_year = models.PositiveIntegerField()
    tenth_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    ITI_or_Twelfth = models.CharField(max_length=100, blank=True, null=True)
    board = models.CharField(max_length=50, blank=True, null=True)
    passing_year = models.PositiveIntegerField(blank=True, null=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    # 5. Documents Upload
    aadhaar_number = models.CharField(max_length=12, unique=True)
    aadhaar_card = models.FileField(upload_to='students/docs/aadhaar/')
    caste_certificate = models.FileField(upload_to='students/docs/caste_certificate/', blank=True, null=True)
    domicile_certificate = models.FileField(upload_to='students/docs/domicile_certificate/', blank=True, null=True)
    transfer_certificate = models.FileField(upload_to='students/docs/transfer_certificate/')
    character_certificate = models.FileField(upload_to='students/docs/character_certificate/')
    marksheets = models.FileField(upload_to='students/docs/marksheets/')

    # 6. Guardian Details
    father_occupation = models.CharField(max_length=50)
    mother_occupation = models.CharField(max_length=50, blank=True, null=True)
    annual_income = models.DecimalField(max_digits=10, decimal_places=2)

    # 7. System Info
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.enroll} - {self.student_name}"

    def filename(self):
        return os.path.basename(self.profile_photo.name) if self.profile_photo else None

# =============================
# librery management table
# =============================
# -----------------------------
# 1. Book Table (General Info)
# -----------------------------
class Book(models.Model):
    book_name = models.CharField(max_length=100)
    publication = models.CharField(max_length=100)
    book_price = models.IntegerField()
    total_copies = models.IntegerField(default=1)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        # Existing copies count from BookCopy table
        existing_copies = BookCopy.objects.filter(book=self).count()
        
        if self.total_copies < existing_copies:
            raise ValidationError(
                f"Cannot reduce total books below existing {existing_copies} copies. "
                "Please delete excess book copies first."
            )

    def save(self, *args, **kwargs):
        self.full_clean()  # call validation before save
        super().save(*args, **kwargs)

    def __str__(self):
        return self.book_name


# -----------------------------------------
# 2. BookCopy Table (Every Physical Copy)
# -----------------------------------------
class BookCopy(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  # belongs to which book
    book_set_id = models.CharField(max_length=20, unique=False)  # unique ID per copy
    is_available = models.BooleanField(default=True)  # available or issued
    
    def clean(self):
        # Total allowed copies
        allowed_limit = self.book.total_copies

        # Already existing copies count
        existing_count = BookCopy.objects.filter(book=self.book).exclude(pk=self.pk).count()

        if existing_count >= allowed_limit:
            raise ValidationError(f"{self.book.book_name} ke liye {allowed_limit} se zyada copies allowed nahi hain.")

        # Optional: Prevent duplicate book_set_id for same book
        if BookCopy.objects.filter(book=self.book, book_set_id=self.book_set_id).exclude(pk=self.pk).exists():
            raise ValidationError(f"Copy number {self.book_set_id} already exists for {self.book.book_name}.")

    def save(self, *args, **kwargs):
        self.full_clean()  # call validation before save
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.book.book_name} - {self.book_set_id}"


# ------------------------------------------
# 3. Issue Table (Issue & Return table)
# -----------------------------------------
class Issue(models.Model):
    book_set = models.ForeignKey(BookCopy, on_delete=models.PROTECT)  # exactly which copy is issued
    student = models.ForeignKey('Student', on_delete=models.PROTECT, blank=True, null=True, to_field='enroll')
    teacher = models.ForeignKey('Teacher', on_delete=models.PROTECT, blank=True, null=True, to_field='teacher_id')

    issue_date = models.DateField(default=date.today)  # automatic today's date
    due_date = models.DateField()  # librarian manually sets
    return_date = models.DateField(blank=True, null=True)
    fine = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def clean(self):
        # Validate student/teacher selection
        if not self.student and not self.teacher:
            raise ValidationError("Please provide either a student or a teacher.")
        if self.student and self.teacher:
            raise ValidationError("Please provide only one: Student or Teacher.")

        # Prevent same subject book issue for same student/teacher
        subject = self.book_set.book  # Book object
        if self.student:
            if Issue.objects.filter(
                student=self.student,
                book_set__book=subject,
                return_date__isnull=True
            ).exclude(pk=self.pk).exists():
                raise ValidationError(f"{self.student} already has a book issued for {subject.book_name}.")
        elif self.teacher:
            if Issue.objects.filter(
                teacher=self.teacher,
                book_set__book=subject,
                return_date__isnull=True
            ).exclude(pk=self.pk).exists():
                raise ValidationError(f"{self.teacher} already has a book issued for {subject.book_name}.")

    def save(self, *args, **kwargs):
        self.full_clean()

        if self.pk:  # Update case
            old_issue = Issue.objects.get(pk=self.pk)
            if old_issue.book_set != self.book_set:
                # Old copy को available कर दो
                old_issue.book_set.is_available = True
                old_issue.book_set.save(update_fields=['is_available'])
                
                # New copy को unavailable कर दो
                if not self.book_set.is_available:
                    raise ValueError("This copy is already issued.")
                self.book_set.is_available = False
                self.book_set.save(update_fields=['is_available'])
        else:  # New issue
            if not self.book_set.is_available:
                raise ValueError("This copy is already issued.")
            self.book_set.is_available = False
            self.book_set.save(update_fields=['is_available'])

        super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        self.book_set.is_available = True
        self.book_set.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.book_set.book_set_id} issued"

# ======================
# College teacher table
# ======================
# -----------------------------------
# 1. Teacher basic details by admin
# -----------------------------------
class Teacher(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    post=models.CharField(max_length=200, choices=[
        ('Lecturer Computer', 'Lecturer Computer'),
        ('Lecturer Electronics', 'Lecturer Electronics'),
        ('Lecturer Instrumentation and Control','Lecturer Instrumentation and Control'),
        ('Lecturer (Applied Science and Humanities)','Lecturer (Applied Science and Humanities)'),
        ('Librarian','Librarian'),
        ('Workshop Instructor','Workshop Instructor'),
        ])
    Qualification=models.CharField(max_length=200)
    photo=models.ImageField(upload_to='teacher/')
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def filename(self):
        return os.path.basename(self.photo.name)

# -------------------------------------
# 1. Teacher signup details by teacher
# -------------------------------------
class TeacherSignup(models.Model):
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=128)  # hashed password
    teacher = models.OneToOneField(Teacher, on_delete=models.PROTECT)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


# ======================
# Study matarial table
# ======================
class Corner_content(models.Model):
    content_title=models.CharField(max_length=100)
    content_desc=models.TextField(null=True, blank=True)
    content_file = models.FileField(upload_to='stu_content/', blank=True, null=True)
    content_link = models.URLField(max_length=500, blank=True, null=True)
    content_type=models.CharField(max_length=20)
    to_branch=models.CharField(max_length=20)
    to_year=models.CharField(max_length=50)
    teacher=models.ForeignKey(Teacher, on_delete=models.PROTECT, to_field='teacher_id',)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content_title
    
    def filename(self):
        return os.path.basename(self.content_file.name)
