from django.urls import path
from .views import RecruiterSignup, SeekerSignup, Login, RecruiterProfile, SeekerProfile, Logout


urlpatterns = [
   # recruiter/signup/
   # seeker/signup/
   # login/
   # recruiterprofile/
   # seekerprofile/
   # logout/
   path('recruiter/signup/', RecruiterSignup.as_view(), name='recruiter_signup'),
   path('seeker/signup/', SeekerSignup.as_view(), name='seeker_signup'),
   path('login/', Login.as_view(), name='login'),
   path('recruiterprofile/', RecruiterProfile.as_view(), name='recruiter_profile'),
   path('seekerprofile/', SeekerProfile.as_view(), name='seeker_profile'),
   path('logout/', Logout.as_view(), name='logout'),
]