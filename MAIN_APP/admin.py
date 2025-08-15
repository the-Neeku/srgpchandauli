from django.contrib import admin
from .models import *
from django.utils.html import format_html
from .utils import get_existing_folders

# Register your models here.

class PrincipalAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Photo', 'Post', 'Sec. Post', 'From Date', 'display_to_date', 'Massage')

    def display_to_date(self, obj):
        return obj.to_date or "Present"
    display_to_date.short_description = "To Date"
    
class EventFolderAdmin(admin.ModelAdmin,):
    readonly_fields = ('existing_folders_list','updated_at')

    def existing_folders_list(self, obj):
        folders = get_existing_folders('media/events/')
        return format_html('<br>'.join(folders))

    existing_folders_list.short_description = "Existing Event Folders"
    
class baseAdmin(admin.ModelAdmin):
    readonly_fields = ('updated_at',)

class TeacherSignupAdmin(admin.ModelAdmin):
    readonly_fields = ('username','updated_at')
    exclude = ('password',)

class ReviewAdmin(admin.ModelAdmin):
    readonly_fields=('name','email','review_type','description')

class CornerContentAdmin(admin.ModelAdmin):
    readonly_fields=('teacher_id', 'content_title', 'content_type', 'content_file', 'content_desc', 'to_branch', 'to_year', 'updated_at')

class BookAdmin(admin.ModelAdmin):
    readonly_fields=('book_name','publication','total_copies','updated_at')    

class BookcopyAdmin(admin.ModelAdmin):
    readonly_fields=('book','book_set_id','is_available')    

class IssueAdmin(admin.ModelAdmin):
    readonly_fields=('book_set','student','teacher','issue_date','due_date','return_date','fine')    

admin.site.register(Principal, baseAdmin)
admin.site.register(Teacher, baseAdmin)
admin.site.register(Event, EventFolderAdmin)
admin.site.register(Notice, baseAdmin)
admin.site.register(Imp_link, baseAdmin)
admin.site.register(Imp_person, baseAdmin)
admin.site.register(About, baseAdmin)
admin.site.register(Contact, baseAdmin)
admin.site.register(Facility, baseAdmin)
admin.site.register(Course, baseAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Student, baseAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookCopy, BookcopyAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Corner_content, CornerContentAdmin)
admin.site.register(college_photo, baseAdmin)
admin.site.register(TeacherSignup, TeacherSignupAdmin)