from django.contrib import admin
from .models import JobDetails, ApplicantDetails

# Register the models you have created here
@admin.register(JobDetails)
class JobDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'job_title', 'company', 'recruiter_id', 'application_deadline')
    search_fields = ('job_title', 'company')
    list_filter = ('application_deadline',)

@admin.register(ApplicantDetails)
class ApplicantDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'job_id', 'job_title', 'company', 'applicant_id', 'applicant_name', 'applicant_email')
    search_fields = ('job_title', 'applicant_email')
    list_filter = ('company',)