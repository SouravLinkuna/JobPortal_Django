from rest_framework import generics, authentication, permissions, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.settings import api_settings
from rest_framework.response import Response
from user.models import UserDetails
from .serializers import JobDetailsSerializer, ApplicantDetailsSerializer
from user.serializers import UserSerializer
from .models import ApplicantDetails, JobDetails
from user.permissions import IsRecruiter, IsSeeker
from django.db.models import F, Q
from datetime import datetime
# Method to post a job
# className ---> JobPostView 

# Method to view the recruiter job posts
# className --->  MyPostsView

# Method to view the job status
# className --->  JobStatusView

# Method to view seeker profile
# className --->  ViewProfileView

# Method to update and delete a job
# className --->  JobUpdateDeleteView
# Create a permission to allow recruiters to edit only their own job post details

# Method to list all the jobs
# className --->  JobListView

# Method to filter jobs
# className --->  JobFiltersView

# Method to apply for a job
# className --->  JobApplyView

# Method to view seeker applied jobs
# className --->  JobAppliedView

class PostJob(generics.CreateAPIView):
    queryset = UserDetails.objects.all()
    serializer_class = JobDetailsSerializer
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            job_title = serializer.validated_data.get('job_title')
            description = serializer.validated_data.get('description')
            experience = serializer.validated_data.get('experience')
            work_location = serializer.validated_data.get('work_location')
            employment_type = serializer.validated_data.get('employment_type')
            qualification = serializer.validated_data.get('qualification')
            openings = serializer.validated_data.get('openings')
            application_deadline = serializer.validated_data.get('application_deadline')

            recruiter_id = UserDetails.objects.get(pk=request.user.id)
            company = recruiter_id.company
            about_company = recruiter_id.about_company
            website = recruiter_id.website

            job = JobDetails(job_title=job_title, description=description, experience=experience, work_location=work_location, employment_type=employment_type, qualification=qualification, openings=openings, application_deadline=application_deadline, company=company, recruiter_id=recruiter_id, about_company=about_company, website=website)
            job.save()

            return Response({'message': 'job details have been posted successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class MyPosts(generics.ListAPIView):
    queryset = JobDetails.objects.all()
    serializer_class = JobDetailsSerializer
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]

    def get(self, request, *args, **kwargs):
        user = UserDetails.objects.get(pk=request.user.id)
        my_jobs = JobDetails.objects.filter(recruiter_id=user).order_by("id")
        response = []
        for job in my_jobs:
            a = {
                "id": job.id,
                "job_title": job.job_title,
                "company": job.company,
                "description": job.description,
                "experience": job.experience,
                "work_location": job.work_location,
                "employment_type": job.employment_type,
                "qualification": job.qualification,
                "about_company": job.about_company,
                "website": job.website,
                "openings": job.openings,
                "no_of_applicants": job.no_of_applicants,
                "application_deadline": (job.application_deadline).strftime("%Y-%m-%d")
                }
            response.append(a)
        return Response(response, status=status.HTTP_200_OK)

class JobStatus(generics.RetrieveAPIView):
    queryset = JobDetails.objects.all()
    serializer_class = JobDetailsSerializer
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]

    def get(self, request, job_id, *args, **kwargs):
        jobdetails = JobDetails.objects.get(pk=job_id)
        if jobdetails.recruiter_id != request.user:
            return Response({
                    "message": "You do not have permission to perform this action"
                }, status=status.HTTP_403_FORBIDDEN)
        else:
            myjobs = ApplicantDetails.objects.filter(job_id=jobdetails)
            response = []
            for job in myjobs:
                a = {
                    "job_id": job.job_id.id,
                    "job_title": job.job_title,
                    "company": job.company,
                    "applicant_id": job.applicant_id.id,
                    "applicant_name": job.applicant_name,
                    "applicant_email": job.applicant_email
                    }
                response.append(a)
            return Response(response, status=status.HTTP_200_OK)

class ViewProfile(generics.RetrieveAPIView):
    queryset = UserDetails.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]

    def get(self, request, pk, *args, **kwargs):
        try:
            user = UserDetails.objects.get(pk=pk)
        except UserDetails.DoesNotExist:
            return Response({
                "detail": "Not found."
            }, status=status.HTTP_404_NOT_FOUND)
        response = {
            "name": user.name,
            "email": user.email,
            "date_of_birth": (user.date_of_birth).strftime("%Y-%m-%d"),
            "gender": user.gender,
            "mobile_number": user.mobile_number,
            "address": user.address,
            "course": user.course,
            "specialization": user.specialization,
            "course_type": user.course_type,
            "college": user.college,
            "percentage": str(user.percentage),
            "year_of_passing": user.year_of_passing,
            "skills": user.skills,
            "summary": user.summary,
            "experience_level": user.experience_level,
            "designation":user.designation,
            "responsibilities": user.responsibilities,
            "company": user.company,
            "location": user.location,
            "worked_from": user.worked_from,
            "to": user.to,
            }
        return Response(response, status=status.HTTP_200_OK)

class UpdateJob(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobDetails.objects.all()
    serializer_class = JobDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk, *args, **kwargs):
        try:
            jobdetails = JobDetails.objects.get(pk=pk)
        except JobDetails.DoesNotExist:
            return Response({
                "detail": "Not found."
            }, status=status.HTTP_404_NOT_FOUND)
        if (jobdetails.recruiter_id != request.user) and request.user.is_staff:
            return Response({
                    "detail": "You do not have permission to perform this action."
                }, status=status.HTTP_403_FORBIDDEN)
        elif not request.user.is_staff:
            return Response({
                    "message": "You need recruiter privileges to perform this action"
                }, status=status.HTTP_403_FORBIDDEN)
        else:
            data = request.data.get('openings')
            jobdetails.openings = data
            jobdetails.save()
            return Response({
                    "message": "job details have been updated successfully"
                }, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk, *args, **kwargs):
        try:
            jobdetails = JobDetails.objects.get(pk=pk)
        except JobDetails.DoesNotExist:
            return Response({
                "detail": "Not found."
            }, status=status.HTTP_404_NOT_FOUND)
        
        if jobdetails.recruiter_id != request.user:
            return Response({
                "detail": "You do not have permission to perform this action."
            }, status=status.HTTP_403_FORBIDDEN)
        elif not request.user.is_staff:
            return Response({
                    "message": "You need recruiter privileges to perform this action"
                }, status=status.HTTP_403_FORBIDDEN)
        
        jobdetails.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)

class ListJob(generics.ListAPIView):
	queryset = JobDetails.objects.all()
	serializer_class = JobDetailsSerializer

	def get(self, request, *args, **kwargs):
		open_jobs = JobDetails.objects.filter(application_deadline__lte=datetime.now().date())
		response = []
		for job in open_jobs:
			a = {
				"id": job.id,
				"job_title": job.job_title,
				"company": job.company,
				"description": job.description,
				"experience": job.experience,
				"work_location": job.work_location,
				"employment_type": job.employment_type,
				"qualification": job.qualification,
				"about_company": job.about_company,
				"website": job.website,
				"openings": job.openings,
				"no_of_applicants": job.no_of_applicants,
				"application_deadline": (job.application_deadline).strftime("%Y-%m-%d")
			}
			response.append(a)
		return Response(response, status=status.HTTP_200_OK)

class FilterJob(generics.ListAPIView):
	queryset = JobDetails.objects.all()
	serializer_class = JobDetailsSerializer

	def get(self, request, *args, **kwargs):
		search_query = request.query_params.get('search', '')
		search_terms = search_query.split()
		query = Q()
		for term in search_terms:
			query |= Q(job_title__icontains=term) | Q(work_location__icontains=term) | Q(company__icontains=term) | Q(description__icontains=term)
		open_jobs = JobDetails.objects.filter(query, application_deadline__lte=datetime.now().date())
		response = []
		for job in open_jobs:
			a = {
				"id": job.id,
				"job_title": job.job_title,
				"company": job.company,
				"description": job.description,
				"experience": job.experience,
				"work_location": job.work_location,
				"employment_type": job.employment_type,
				"qualification": job.qualification,
				"about_company": job.about_company,
				"website": job.website,
				"openings": job.openings,
				"no_of_applicants": job.no_of_applicants,
				"application_deadline": (job.application_deadline).strftime("%Y-%m-%d")
			}
			response.append(a)
		return Response(response, status=status.HTTP_200_OK)

class ApplyJob(generics.CreateAPIView):
    queryset = ApplicantDetails.objects.all()
    serializer_class = ApplicantDetailsSerializer
    permission_classes = [permissions.IsAuthenticated, IsSeeker]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            job_id = serializer.validated_data.get('job_id')
            user = UserDetails.objects.get(pk=request.user.id)
            chk_appjobs = ApplicantDetails.objects.filter(job_id=job_id, applicant_id=user).count()
            if chk_appjobs > 0:
                return Response({
                    "message": "You have already applied for this job"
                }, status=status.HTTP_406_NOT_ACCEPTABLE)
            
            jobdetails = JobDetails.objects.get(pk=job_id.id)
            
            applicant = ApplicantDetails(job_id=job_id, job_title=jobdetails.job_title, company=jobdetails.company, applicant_id=user, applicant_name=user.name, applicant_email=user.email)
            applicant.save()

            jobdetails.no_of_applicants += 1
            jobdetails.save()
            
            return Response({
                    "message": "You have successfully applied for this job"
                }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class AppliedJobs(generics.ListAPIView):
    queryset = ApplicantDetails.objects.all()
    serializer_class = ApplicantDetailsSerializer
    permission_classes = [permissions.IsAuthenticated, IsSeeker]

    def get(self, request, *args, **kwargs):
        user = UserDetails.objects.get(pk=request.user.id)
        aaplied_jobs = ApplicantDetails.objects.filter(applicant_id=user).order_by("id")
        response = []
        for job in aaplied_jobs:
            jobdetails = JobDetails.objects.get(pk=job.id)
            a = {
                "job_id": job.id,
                "job_title": jobdetails.job_title,
                "company": jobdetails.company,
                "applicant_id": user.id,
                "applicant_name": user.name,
                "applicant_email": user.email
                }
            response.append(a)
        return Response(response, status=status.HTTP_200_OK)