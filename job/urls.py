from django.urls import path
from .views import PostJob, MyPosts, JobStatus, ViewProfile, UpdateJob, ListJob, FilterJob, ApplyJob, AppliedJobs



urlpatterns = [
    # postjob/
    # myposts/
    # jobstatus/<job_id>
    # viewprofile/<applicant_id>
    # updatejob/<pk>
    # listjob/
    # filterjob/
    # applyjob/
    # appliedjobs/  
    path('postjob/', PostJob.as_view(), name='post_job'),
    path('myposts/', MyPosts.as_view(), name='my_posts'),
    path('jobstatus/<int:job_id>', JobStatus.as_view(), name='job_status'),
    path('viewprofile/<int:pk>', ViewProfile.as_view(), name='view_profile'),
    path('updatejob/<int:pk>', UpdateJob.as_view(), name='update_job'),
    path('listjob/', ListJob.as_view(), name='list_job'),
    path('filterjob/', FilterJob.as_view(), name='filter_job'),
    path('applyjob/', ApplyJob.as_view(), name='apply_job'),
    path('appliedjobs/', AppliedJobs.as_view(), name='applied_jobs'), 
]


