import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password, check_password
from MAIN_APP.models import *
from .forms import *
from django.utils import timezone
from datetime import date
from django.db.models import Q


# =================================
# Function to render the home page
# =================================
def index(request): 
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        review_type=request.POST.get('option')
        description=request.POST.get('description')
        try:
            data_review =Review(name=name, email=email, review_type=review_type,description=description)
            data_review.save()
            messages.success(request, f"<script>alert('Thank you, Dear {name} your {review_type} has been successfully submitted.');</script>")
        except Exception as e:
                messages.error(request, f"<script>alert('Error: Your {review_type} could not be submitted.');</script>")
        return redirect('/')
    data={
        'title': 'HOME',
        'notices': Notice.objects.all(),
        'links': Imp_link.objects.all(),
        'photos': college_photo.objects.all(),
        'principal_current': Principal.objects.last(),
        'person': Imp_person.objects.all(),
    }
    return render(request, "index.html",data)
# ========================================
# Function to render the principal's page
# ========================================
def our_principal(request):
    data={
        'title': 'PRINCIPAL',
        'active': 'home',
        'principal_current': Principal.objects.last(),
        'principal': Principal.objects.all(),
    }
    return render(request, "principal.html",data)
# =======================================
# Function to render the teacher's page
# =======================================
def our_teachers(request):
    data={
        'title': 'TEACHERS',
        'active': 'home',
        'cs': Teacher.objects.filter(post='Lecturer Computer'),
        'ec': Teacher.objects.filter(post='Lecturer Electronics'),
        'ic': Teacher.objects.filter(post='Lecturer Instrumentation and Control'),
        'gs': Teacher.objects.filter(post='Lecturer (Applied Science and Humanities)'),
        'lib': Teacher.objects.filter(post='Librarian'),
        'work': Teacher.objects.filter(post='Workshop Instructor'),

    }
    return render(request, "teachers.html",data)
# ===================================
# Function to render the events page
# ===================================
def our_events(request):
    images_by_folder = {}
    all_images = Event.objects.all()
    for img in all_images:
        folder = img.folder_name
        images_by_folder.setdefault(folder, []).append(img)
    data={
        'title': 'EVENTS',
        'active': 'home',
        'galleries': images_by_folder,
    }
    return render(request, "events.html",data)
# =========================================
# Function to render the facilities page
# =========================================
def our_facility(request):
    data={
        'title': 'FACILITY',
        'facility': Facility.objects.all(),
    }
    return render(request, "facility.html",data)

# ========================
# Student Signup View
# ========================
def student_signup(request):
    form = StudentSignupForm()

    # Determine which step is submitted
    step = request.POST.get('step') if request.method == "POST" else None

    if request.method == "POST":

        # --------- Step 1: Basic Details → Send OTP ---------
        if step == "basic":
            enroll = request.POST.get('enroll')
            name = request.POST.get('student_name')
            email = request.POST.get('email')

            # Duplicate check
            if Student.objects.filter(enroll=enroll).exists():
                messages.error(request, "Enrollment number already exists!")
                return render(request, 'student-signup.html', {'form': form})
            if Student.objects.filter(email=email).exists():
                messages.error(request, "Email already exists!")
                return render(request, 'student-signup.html', {'form': form})

            # Generate OTP and save in session
            otp = random.randint(100000, 999999)
            request.session['enroll'] = enroll
            request.session['student_name'] = name
            request.session['email'] = email
            request.session['otp'] = str(otp)

            # Send OTP email
            html_message = render_to_string('emails/otp_email.html', {'name': name, 'otp': otp})
            msg = EmailMessage(
                subject="Your OTP for Student Registration",
                body=html_message,
                from_email='SRGP <4833srgpchandauli@gmail.com>',
                to=[email]
            )
            msg.content_subtype = "html"
            msg.send()

            messages.info(request, f"OTP sent to {email}")
            return render(request, 'student-signup.html', {
                'otp_step': True,
                'form': form,
                'title': 'Student Registration',
                'active': 'Registration',
                })

        # --------- Step 2: OTP Verification ---------
        elif step == "otp":
            input_otp = request.POST.get('otp')
            session_otp = request.session.get('otp')

            if input_otp == session_otp:
                messages.success(request, "OTP verified! Please complete full registration.")
                # Show full registration form
                return render(request, 'student-signup.html', {
                    'full_reg': True,
                    'form': form,
                    'enroll': request.session.get('enroll'),
                    'name': request.session.get('student_name'),
                    'email': request.session.get('email')
                })
            else:
                messages.error(request, "Invalid OTP. Try again.")
                return render(request, 'student-signup.html', {
                    'otp_step': True,
                    'form': form,
                    'title': 'Student Registration',
                    'active': 'Registration',
                    })

        # --------- Step 3: Full Registration Submit ---------
        elif step == "full_reg":
            form = StudentSignupForm(request.POST, request.FILES)
            if form.is_valid():
                # Set the readonly fields from session
                form.instance.enroll = request.session.get('enroll')
                form.instance.student_name = request.session.get('student_name')
                form.instance.email = request.session.get('email')

                # Save to database
                form.save()

                # Clear session
                for key in ['enroll', 'student_name', 'email', 'otp']:
                    if key in request.session:
                        del request.session[key]

                messages.success(request, "Registration completed successfully!")
                return redirect('student_login') 
            else:
                messages.error(request, "Please correct the errors below.")
                return render(request, 'student-signup.html', {
                    'full_reg': True,
                    'form': form,
                    'enroll': request.session.get('enroll'),
                    'name': request.session.get('student_name'),
                    'email': request.session.get('email'),
                    'title': 'Student Registration',
                    'active': 'Registration',
                })
    # --------- Default GET request ---------
    return render(request, 'student-signup.html', {
        'form': form,
        'title': 'Student Registration',
        'active': 'Registration',
        })

# ========================
# Student login System
# ========================
def student_login(request):
    if request.method == "POST":
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            enrollment = form.cleaned_data['enrollment_no']
            dob = form.cleaned_data['dob']

            try:
                student = Student.objects.get(enroll=enrollment, dob=dob)
                # set session 
                request.session['student_id'] = student.enroll
                request.session['student_name'] = student.student_name
                request.session['user_type'] = 'student'
                return redirect('/student-dashboard/')

            except Student.DoesNotExist:
                messages.error(request, "Invalid Enrollment No or DOB")
    else:
        form = StudentLoginForm()
    data={
        'title': 'STUDENT LOGIN',
        'active': 'login',
        'form': form
    }
    return render(request, "student-login.html", data)
# ==========================
# login checkup for student
# ==========================
def student_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'student_id' in request.session:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('/student-login/')
    return wrapper

# ========================
# student dashboard
# ========================

@student_login_required
def student_dashboard(request):
    enroll = request.session.get('student_id')
    student_name = request.session.get('student_name')
    student = get_object_or_404(Student, enroll=enroll)

    # Calculate current year from admission_year
    year_num = date.today().year - student.admission_year + 1
    if year_num == 1:
        current_year = "1st Year"
    elif year_num == 2:
        current_year = "2nd Year"
    elif year_num == 3:
        current_year = "3rd Year"
    else:
        current_year = "All Year"

    # Filter content based on branch and year
    content = Corner_content.objects.filter(
        (Q(to_branch=student.branch) | Q(to_branch='All Branch')) &
        (Q(to_year=current_year) | Q(to_year='All Year'))
    ).order_by('-updated_at')  # optional ordering latest first
    data = {
        'name': student_name,
        'title': 'STUDENT LOGIN',
        'active': 'login',
        'content': content,
    }
    return render(request, "student-dashboard.html", data)

@student_login_required
def Student_profile(request):
    enroll = request.session.get('student_id')
    name = request.session.get('student_name')

    student = get_object_or_404(Student, enroll=enroll)
    data = {
        'student': student,
        'name': name,
        'title': 'Student Profile',
        'active': 'login'
    }
    return render(request, 'stu-profile.html', data)

# ========================
# student logout
# ========================
@student_login_required
def student_logout(request):
    request.session.flush()  # clear session
    return redirect('/student-login/')

# ========================
# Teacher Signup View
# ========================
def teacher_signup(request):
    form = TeacherSignupForm()  # <-- Always define it before

    if request.method == "POST":
        if 'otp' in request.POST:
            input_otp = request.POST.get('otp')
            session_otp = str(request.session.get('otp'))

            if input_otp == session_otp:
                teacher_name = request.session.get('teacher')
                username = request.session.get('username')
                email = request.session.get('email')
                password = make_password(request.session.get('password'))

                try:
                    teacher_instance = Teacher.objects.get(name=teacher_name)
                except Teacher.DoesNotExist:
                    messages.error(request, "Teacher not found.")
                    return redirect('teacher_signup')

                TeacherSignup.objects.create(
                    teacher=teacher_instance,
                    username=username,
                    email=email,
                    password=password
                )

                # Clear session
                for key in ['otp', 'teacher', 'username', 'email', 'password']:
                    request.session.pop(key, None)

                messages.success(request, "Signup successful! Please login.")
                return redirect('teacher_login')
            else:
                messages.error(request, "Invalid OTP.")
                return render(request, 'teacher_signup.html', {'otp_step': True, 'form': form})

        else:
            form = TeacherSignupForm(request.POST)
            if form.is_valid():
                teacher = form.cleaned_data['teacher']
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']

                if TeacherSignup.objects.filter(teacher=teacher).exists():
                    messages.error(request, "You have already signed up.")
                    return redirect('teacher_login')

                otp = random.randint(100000, 999999)

                request.session['teacher'] = str(teacher)
                request.session['username'] = username
                request.session['email'] = email
                request.session['password'] = password
                request.session['otp'] = str(otp)

                html_message = render_to_string('emails/otp_email.html', {
                    'name': teacher,
                    'otp': otp
                })

                email_msg = EmailMessage(
                    subject="Your OTP Code for Secure Verification – SRGP CHANDAULI",
                    body=html_message,
                    from_email='SRGP CHANDAULI <4833srgpchandauli@gmail.com>',
                    to=[email]
                )
                email_msg.content_subtype = "html"
                email_msg.send()

                messages.info(request, f"OTP sent to {email}")
                return render(request, 'teacher_signup.html', {'otp_step': True, 'form': form})

    return render(request, 'teacher_signup.html', {
        'form': form,
        'active': 'Registration',
        'title': 'Registration'
    })

# ========================
# institute login System
# ========================
def teacher_login(request):
    if request.method == "POST":
        form = InstituteLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                user = TeacherSignup.objects.get(username=username)
                if check_password(password, user.password):
                    # Set session
                    request.session['username'] = user.username
                    request.session['teacher_id'] = user.teacher.teacher_id if user.teacher else None
                    request.session['name'] = user.teacher.name if user.teacher else user.username
                    request.session['post'] = user.teacher.post if user.teacher else None
                    request.session['user_type'] = 'institute'

                    messages.success(request, "Login successful!")
                    # email setup
                    ip_address = get_client_ip(request)
                    browser = get_browser_info(request)
                    login_time = timezone.localtime().strftime("%d %b %Y, %I:%M %p")

                    html_message = render_to_string('emails/teacher_login.html', {
                        'name': user.teacher.name if user.teacher else user.username,
                        'login_time': login_time,
                        'ip_address': ip_address,
                        'browser': browser,
                        'site_name': 'srgpchandauli.ac.in'
                    })

                    email_msg = EmailMessage(
                        subject="Teacher Login Notification – SRGP CHANDAULI",
                        body=html_message,
                        from_email='SRGP CHANDAULI <4833srgpchandauli@gmail.com>',
                        to=[user.email]
                    )
                    email_msg.content_subtype = "html"
                    email_msg.send()
                    return redirect('teacher_dashboard')
                else:
                    messages.error(request, "Incorrect password.")
            except TeacherSignup.DoesNotExist:
                messages.error(request, "Username does not exist.")
    else:
        form = InstituteLoginForm()

    return render(request, 'teacher_login.html', {
        'form': form,
        'active': 'login'
        })
    
# ========================  
# Login checkup for teacher
# ========================    
def teacher_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'username' in request.session or 'teacher_id' in request.session:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('/institute-login/')
    return wrapper

# ========================
# Teacher Dashboard View
# ========================

@teacher_login_required
def teacher_dashboard(request):
    username = request.session['username']
    name = request.session.get('name')
    teacher_id = request.session.get('teacher_id')
    if request.method == "POST":
        form = CornerContentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Content added successfully!")
        else:
            messages.error(request, form.errors)
    return render(request, 'teacher-dashboard.html', {
        'username': username,
        'name': name,
        'post': request.session.get('post'),
        'data': Corner_content.objects.filter(teacher_id=teacher_id),
        'title': 'TEACHER DASHBOARD',
        'active': 'login'
    })

# ========================
# teacher update content
# ========================

@teacher_login_required
def update_content(request, id):
    obj = get_object_or_404(Corner_content, id=id)
    if request.method == "POST":
        form = CornerContentForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Content updated successfully!")
        else:
            messages.error(request, form.errors)
    return redirect('teacher_dashboard')

# ========================
# teacher delete content
# ========================

@teacher_login_required
def delete_content(request, id):
    content = get_object_or_404(Corner_content, id=id)
    content.delete()
    messages.success(request, "Content deleted successfully!")
    return redirect('teacher_dashboard')

# ========================
# teacher change password
# ========================

@teacher_login_required
def change_password(request):
    username = request.session['username']
    name = request.session.get('name')
    teacher_user = TeacherSignup.objects.get(username=username)
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            old = form.cleaned_data['old_password']
            new = form.cleaned_data['new_password']

            if check_password(old, teacher_user.password):
                teacher_user.password = make_password(new)
                teacher_user.save()
                messages.success(request, 'Your password was successfully updated!')
                return redirect('teacher_dashboard')
            else:
                messages.error(request, 'Old password is incorrect.')
    else:
        form = PasswordChangeForm()

    return render(request, 'change-password.html', {
        'form': form,
        'username': username,
        'name': name,
        'post': request.session.get('post'),
        'title': 'Change Password',
        'active': 'login'
    })


# ========================    
# teacher profile
# ========================

@teacher_login_required
def teacher_profile(request):
    username = request.session['username']
    name = request.session['name']

    try:
        # Get the TeacherSignup object and join Teacher using select_related
        profile = TeacherSignup.objects.select_related('teacher').get(username=username)
    except TeacherSignup.DoesNotExist:
        profile = None

    data = {
        'profile': profile,
        'username': username,
        'name': name,
        'post': request.session.get('post'),
        'title': 'Teacher Profile',
        'active': 'login'
    }
    return render(request, 'profile.html', data)


# ========================
# teacher Logout
# ========================

@teacher_login_required
def teacher_logout(request):
    request.session.flush()
    messages.success(request, "Logged out successfully.")
    return redirect('teacher_login')

# ========================
# Library management
# ========================
@teacher_login_required
def book_details(request):
    if request.method == "POST":
        form = BookDetailsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Book detail added successfully!")
        else:
            messages.error(request, form.errors)
    data = {
        'title': 'Library',
        'active': 'login',
        'name': request.session.get('name'),
        'post': request.session.get('post'),
        'data': Book.objects.all()
    }
    return render(request, "book-details.html", data)

def update_book_details(request, id):
    obj = get_object_or_404(Book, id=id)
    if request.method == "POST":
        form = BookDetailsForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "book details one record updated successfully!")
        else:
            messages.error(request, form.errors)
    return redirect('book_details')

@teacher_login_required
def delete_book_details(request, id):
    content = get_object_or_404(Book, id=id)
    content.delete()
    messages.success(request, "book details one record deleted successfully!")
    return redirect('book_details')

@teacher_login_required
def book_status(request):
    # Get all book copies and books for dropdown
    
    books = Book.objects.all()
    if request.method == "POST":
        form = BookStatusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Book details one record added successfully!")
        else:
            messages.error(request, form.errors)
    data = {
        'title': 'Library',
        'active': 'login',
        'name': request.session.get('name'),
        'post': request.session.get('post'),
        'data': BookCopy.objects.all(),
        'books': books         # dropdown ke liye
    }
    return render(request, "book-status.html", data)

def update_book_status(request, id):
    obj = get_object_or_404(BookCopy, id=id)
    if request.method == "POST":
        form = BookStatusForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "book status one record updated successfully!")
        else:
            messages.error(request, form.errors)
    return redirect('book_status')

@teacher_login_required
def delete_book_status(request, id):
    content = get_object_or_404(BookCopy, id=id)
    content.delete()
    messages.success(request, "book status one record deleted successfully!")
    return redirect('book_status')

@teacher_login_required
def book_issue(request):
    issues = Issue.objects.select_related('book_set', 'student', 'teacher').all()
    add_copies = BookCopy.objects.filter(is_available=True)
    update_copies =  BookCopy.objects.all()
    students = Student.objects.all()
    teachers = Teacher.objects.all()
    if request.method == "POST":
        form = BookIssueForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Book issued successfully!")
        else:
            messages.error(request, form.errors)
    data = {
        'title': 'Library',
        'active': 'login',
        'name': request.session.get('name'),
        'post': request.session.get('post'),
        'issues': issues,
        'add': add_copies,
        'update': update_copies,
        'students': students,
        'teachers': teachers,
        'today': date.today(),
    }
    return render(request, "book-issue.html", data)

@teacher_login_required
def update_book_issue(request, id):
    obj = get_object_or_404(Issue, id=id)
    if request.method == "POST":
        form = BookIssueForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "book issue one record updated successfully!")
        else:
            messages.error(request, form.errors)
    return redirect('book_issue')

@teacher_login_required
def delete_book_issue(request, id):
    content = get_object_or_404(Issue, id=id)
    book_copy = content.book_set
    book_copy.is_available = True
    book_copy.save(update_fields=['is_available'])
    content.delete()
    messages.success(request, "book issue one record deleted successfully!")
    return redirect('book_issue')

# =================================
# Function to render courses pages
# =================================
def cse(request):
    data={
        'title': 'CSE',
        'active': 'course',
        'course': Course.objects.filter(course_name='COMPUTER SCIENCE & ENGINEERING'),
    }
    return render(request, "courses.html",data)

def ece(request):
    data={
        'title': 'ECE',
        'active': 'course',
        'course': Course.objects.filter(course_name='ELECTRONICS ENGINEERING'),
    }
    return render(request, "courses.html",data)

def ice(request):
    data={
        'title': 'ICE',
        'active': 'course',
        'course': Course.objects.filter(course_name='INSTUMENTATION & CONTROL'),
    }
    return render(request, "courses.html",data)

# ====================================
# Function to render the contact page
# ====================================
def contact_us(request):
    data = {
        'title': 'CONTACT',
        'contact': Contact.objects.first,
    }
    return render(request, "contact.html", data)

# =================================
# Function to render the about page
# =================================
def about_us(request):
    data={
        'title': 'ABOUT',
        'about': About.objects.all(),
    }
    return render(request, "about.html",data)

#=========================
# external data facth...
#=========================
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0] 
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_browser_info(request):
    user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
    return user_agent
