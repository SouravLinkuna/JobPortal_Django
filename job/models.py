from django.db import models

from user.models import UserDetails


class JobDetails(models.Model):
    job_title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    description = models.TextField()
    experience = models.CharField(max_length=100, null=True)
    work_location = models.CharField(max_length=255, null=True)
    employment_type = models.CharField(max_length=100, null=True)
    qualification = models.CharField(max_length=255, null=True)
    about_company = models.TextField()
    website = models.URLField()
    openings = models.IntegerField(null=True)
    no_of_applicants = models.IntegerField(default=0)
    application_deadline = models.DateField(null=True)
    recruiter_id = models.ForeignKey(UserDetails, on_delete=models.CASCADE)

    def __str__(self):
        return self.job_title

class ApplicantDetails(models.Model):
    job_id = models.ForeignKey(JobDetails, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    applicant_id = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    applicant_name = models.CharField(max_length=255)
    applicant_email = models.EmailField(max_length=255)