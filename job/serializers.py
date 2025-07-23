from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

# Method Name 'JobSerializer'
# Method Name 'ApplicantSerializer'

from rest_framework.authtoken.models import Token
from .models import JobDetails, ApplicantDetails
class JobDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDetails
        fields = ('job_title','description','experience','work_location','employment_type','qualification','openings','application_deadline',)

class ApplicantDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicantDetails
        fields = ('job_id',)