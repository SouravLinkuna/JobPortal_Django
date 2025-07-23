from rest_framework import generics, authentication, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.response import Response
from .models import UserDetails
from .serializers import UserSerializer, LoginSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .permissions import IsRecruiter, IsSeeker
from rest_framework.views import APIView
import re
from django.contrib.auth import get_user_model
# Method to signup a recruiter
# className --->  RecruiterSignupView

# Method to signup a seeker
# className --->  SeekerSignupView

# Method to login recruiter and seeker
# className --->  LoginView
# recruiter and seeker should pass auth token in headers along with any request.

# Method to view, update and delete a recruiter profile
# className --->  RecruiterProfileView

# Method to view, update and delete a seeker profile
# className --->  SeekerProfileView

# Method to recruiter and seeker
# className --->  LogoutView
      
class RecruiterSignup(generics.CreateAPIView):
    queryset = UserDetails.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        name = request.data.get('name')
        if not re.match(r'^[a-zA-Z]+$', name):
            return Response({'name': ['Enter a valid name']}, status=status.HTTP_400_BAD_REQUEST)
        designation = request.data.get('designation')
        company = request.data.get('company')
        email = request.data.get('email')
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return Response({'email': ['Enter a valid email']}, status=status.HTTP_400_BAD_REQUEST)
        date_of_birth = request.data.get('date_of_birth')
        gender = request.data.get('gender')
        mobile_number = request.data.get('mobile_number')
        if not re.match(r'^[7-9]\d{9}$', str(mobile_number)):
            return Response({'mobile_number': ['Enter a valid number']}, status=status.HTTP_400_BAD_REQUEST)
        about_company = request.data.get('about_company')
        website = request.data.get('website')

        password = request.data.get("password")
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$', password):
            return Response({'password': ['Enter a valid password']}, status=status.HTTP_400_BAD_REQUEST)
        
        user_model = get_user_model()
        if user_model.objects.filter(email=email).count() > 0:
            return Response({'email': ['user details with this email already exists.']}, status=status.HTTP_400_BAD_REQUEST)
        if user_model.objects.filter(mobile_number=mobile_number).count() > 0:
            return Response({'mobile_number': ['user details with this mobile number already exists.']}, status=status.HTTP_400_BAD_REQUEST)
        user_model.objects.create_admin(email=email, password=password, name=name, designation=designation, company=company, date_of_birth=date_of_birth, gender=gender, mobile_number=mobile_number, about_company=about_company, website=website)

        return Response({'message': 'Your account has been created successfully'}, status=status.HTTP_201_CREATED)

class SeekerSignup(generics.CreateAPIView):
    queryset = UserDetails.objects.all()
    serializer_class = UserSerializer
    
    def post(self, request):
        name = request.data.get('name')
        if not re.match(r'^[a-zA-Z]+$', name):
            return Response({'name': ['Enter a valid name']}, status=status.HTTP_400_BAD_REQUEST)
        email = request.data.get('email')
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return Response({'email': ['Enter a valid email']}, status=status.HTTP_400_BAD_REQUEST)
        date_of_birth = request.data.get('date_of_birth')
        gender = request.data.get('gender')
        mobile_number = request.data.get('mobile_number')
        if not re.match(r'^[7-9]\d{9}$', str(mobile_number)):
            return Response({'mobile_number': ['Enter a valid number']}, status=status.HTTP_400_BAD_REQUEST)
        address = request.data.get('address')
        course = request.data.get('course')
        specialization = request.data.get('specialization')
        course_type = request.data.get('course_type')
        college = request.data.get('college')
        percentage = request.data.get('percentage')
        year_of_passing = request.data.get('year_of_passing')
        skills = request.data.get('skills')
        summary = request.data.get('summary')
        experience_level = request.data.get('experience_level')
        designation = request.data.get('designation')
        responsibilities = request.data.get('responsibilities')
        company = request.data.get('company')
        location = request.data.get('location')
        worked_from = request.data.get('worked_from')
        to = request.data.get('to')

        password = request.data.get("password")
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$', password):
            return Response({'password': ['Enter a valid password']}, status=status.HTTP_400_BAD_REQUEST)
        
        user_model = get_user_model()
        if user_model.objects.filter(email=email).count() > 0:
            return Response({'email': ['user details with this email already exists.']}, status=status.HTTP_400_BAD_REQUEST)
        if user_model.objects.filter(mobile_number=mobile_number).count() > 0:
            return Response({'mobile_number': ['user details with this mobile number already exists.']}, status=status.HTTP_400_BAD_REQUEST)
        user_model.objects.create_user(email=email, password=password, name=name, designation=designation, company=company, date_of_birth=date_of_birth, gender=gender, mobile_number=mobile_number, address=address, course=course, specialization=specialization, course_type=course_type, college=college, percentage=percentage, year_of_passing=year_of_passing, skills=skills, summary=summary, experience_level=experience_level, responsibilities=responsibilities, location=location, worked_from=worked_from, to=to)

        return Response({'message': 'Your account has been created successfully'}, status=status.HTTP_201_CREATED)

class Login(APIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            # Your authentication logic here
            if email is None or password is None:
                return Response({'error': 'Please provide both email and password'}, status=status.HTTP_400_BAD_REQUEST)
            
            user = authenticate(email=email, password=password)
            
            if not user:
                return Response({"non_field_errors": ["Unable to authenticate with provided credentials"]}, status=status.HTTP_400_BAD_REQUEST)
            
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'message': 'Login successful'
                }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecruiterProfile(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserDetails.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]

    def get(self, request):
        user = request.user
        user_details = UserDetails.objects.get(pk=user.id)
        response = {
            "name": user_details.name,
            "designation": user_details.designation,
            "company": user_details.company,
            "email": user_details.email,
            "date_of_birth": (user_details.date_of_birth).strftime("%Y-%m-%d"),
            "gender":user_details.gender,
            "mobile_number": user_details.mobile_number, 
            "about_company": user_details.about_company,
            "website":user_details.website
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def destroy(self, request):
        user = request.user
        user_details = UserDetails.objects.get(pk=user.id)
        user_details.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request, *args, **kwargs):
        mobile_number = request.data.get("mobile_number")
        userdetail = UserDetails.objects.get(pk=request.user.id)
        userdetail.mobile_number = mobile_number
        userdetail.save()
        
        response = {
            "name": userdetail.name,
            "designation": userdetail.designation,
            "company": userdetail.company,
            "email": userdetail.email,
            "date_of_birth": (userdetail.date_of_birth).strftime("%Y-%m-%d"),
            "gender":userdetail.gender,
            "mobile_number": userdetail.mobile_number, 
            "about_company": userdetail.about_company,
            "website":userdetail.website
        }
        return Response(response, status=status.HTTP_200_OK)

class SeekerProfile(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserDetails.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        user_details = UserDetails.objects.get(pk=user.id)
        response = {
            "name": user_details.name,
            "email": user_details.email,
            "date_of_birth": (user_details.date_of_birth).strftime("%Y-%m-%d"),
            "mobile_number": user_details.mobile_number,
            "address": user_details.address,
            "specialization": user_details.specialization,
            "course_type": user_details.course_type,
            "college": user_details.college,
            "percentage": str(user_details.percentage),
            "year_of_passing": user_details.year_of_passing,
            "skills": user_details.skills,
            "summary": user_details.summary,
            "experience_level":user_details.experience_level,
            "designation": user_details.designation,
            "responsibilities":user_details.responsibilities,
            "company":user_details.company,
            "location":user_details.location,
            "worked_from":user_details.worked_from,
            "to":user_details.to,
            "gender":user_details.gender,
            "course":user_details.course,
        }
        print("hjhfg", response)
        return Response(response, status=status.HTTP_200_OK)
    
    def destroy(self, request):
        user = request.user
        user_details = UserDetails.objects.get(pk=user.id)
        user_details.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request, *args, **kwargs):
        skills = request.data.get("skills")
        userdetail = UserDetails.objects.get(pk=request.user.id)
        userdetail.skills = skills
        userdetail.save()
        
        response = {
            "name": userdetail.name,
            "email": userdetail.email,
            "date_of_birth": (userdetail.date_of_birth).strftime("%Y-%m-%d"),
            "mobile_number": userdetail.mobile_number,
            "address": userdetail.address,
            "specialization": userdetail.specialization,
            "course_type": userdetail.course_type,
            "college": userdetail.college,
            "percentage": str(userdetail.percentage),
            "year_of_passing": userdetail.year_of_passing,
            "skills": userdetail.skills,
            "summary": userdetail.summary,
            "experience_level":userdetail.experience_level,
            "designation": userdetail.designation,
            "responsibilities":userdetail.responsibilities,
            "company":userdetail.company,
            "location":userdetail.location,
            "worked_from":userdetail.worked_from,
            "to":userdetail.to,
            "gender":userdetail.gender,
            "course":userdetail.course,
        }
        return Response(response, status=status.HTTP_200_OK)

class Logout(generics.CreateAPIView):
    def get(self, request):
        try:
            # Get the token associated with the user
            token = Token.objects.get(user=request.user)
        except Token.DoesNotExist:
            # Token not found, the user is already logged out
            return Response({'detail': 'User is already logged out.'}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the token
        token.delete()

        return Response({"message": "You've been logged out successfully"}, status=status.HTTP_200_OK)