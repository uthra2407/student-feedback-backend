# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import AllowAny
# from .models import Student
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import AllowAny
# from .models import Student, Institution

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register_student(request):
#     data = request.data.copy()

#     email = data.get('email')
#     password = data.get('password')

#     if not password:
#         return Response({"error": "Password is required."}, status=status.HTTP_400_BAD_REQUEST)
    
#     if Student.objects.filter(email=email).exists():
#         return Response({"error": "Email already exists. Please use a different email address."}, status=status.HTTP_400_BAD_REQUEST)

#     # 🔹 Check if institution exists
#     try:
#         institution = Institution.objects.get(name=data.get('institution'))
#     except Institution.DoesNotExist:
#         return Response({"error": "Institution does not exist!"}, status=status.HTTP_400_BAD_REQUEST)

#     # 🔹 Create a new student
#     student = Student.objects.create_user(
#         name=data.get('name'),
#         regno=data.get('regno'),
#         institution=institution,  # Pass Institution instance instead of string
#         email=email,
#         password=password
#     )
    
#     return Response({"message": "Student registered successfully!"}, status=status.HTTP_201_CREATED)


# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import AllowAny
# from rest_framework_simplejwt.tokens import RefreshToken
# from .models import Student

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def login_student(request):
#     email = request.data.get('email')
#     password = request.data.get('password')

#     try:
#         student = Student.objects.get(email=email)
        
#         # Check password manually
#         if student.check_password(password):
#             # Generate JWT tokens properly
#             refresh = RefreshToken.for_user(student)
#             return Response({
#                 "message": "Login successful!",
#                 "access_token": str(refresh.access_token),
#                 "refresh_token": str(refresh),
#                 "student_id": student.id
#             }, status=status.HTTP_200_OK)
#         else:
#             return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

#     except Student.DoesNotExist:
#         return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from django.contrib.auth.password_validation import validate_password

from .models import Student, Institution

# 🔹 Student Registration View
@api_view(['POST'])
@permission_classes([AllowAny])
def register_student(request):
    data = request.data.copy()
    
    email = data.get('email')
    password = data.get('password')

    if not password:
        return Response({"error": "Password is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Validate email format
        EmailValidator()(email)
    except ValidationError:
        return Response({"error": "Invalid email format."}, status=status.HTTP_400_BAD_REQUEST)

    # Validate password strength
    try:
        validate_password(password)
    except ValidationError as e:
        return Response({"error": e.messages}, status=status.HTTP_400_BAD_REQUEST)

    if Student.objects.filter(email=email).exists():
        return Response({"error": "Email already exists. Please use a different email address."}, status=status.HTTP_400_BAD_REQUEST)

    # 🔹 Get Institution (404 if not found)
    institution = get_object_or_404(Institution, name=data.get('institution'))

    # 🔹 Create Student
    student = Student.objects.create_user(
        name=data.get('name'),
        regno=data.get('regno'),
        institution=institution,
        email=email,
        password=password
    )

    return Response({"message": "Student registered successfully!"}, status=status.HTTP_201_CREATED)


# 🔹 Student Login View
@api_view(['POST'])
@permission_classes([AllowAny])
def login_student(request):
    email = request.data.get('email')
    password = request.data.get('password')

    student = Student.objects.filter(email=email).first()

    if student and check_password(password, student.password):
        refresh = RefreshToken.for_user(student)
        return Response({
            "message": "Login successful!",
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "student_id": student.id
        }, status=status.HTTP_200_OK)

    return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Institution

# 🔹 Institution Registration API
@api_view(['POST'])
@permission_classes([AllowAny])
def register_institution(request):
    data = request.data.copy()

    email = data.get('email')
    password = data.get('password')

    if not password:
        return Response({"error": "Password is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    if Institution.objects.filter(email=email).exists():
        return Response({"error": "Email already exists. Please use a different email address."}, status=status.HTTP_400_BAD_REQUEST)

    # Create a new institution with plain text password
    institution = Institution.objects.create(
        name=data.get('name'),
        location=data.get('location'),
        email=email,
        password=password  # Store plain text password directly
    )
    
    print(f"Registered Institution: {institution.email}, Password: {institution.password}")
    return Response({"message": "Institution registered successfully!"}, status=status.HTTP_201_CREATED)



# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import AllowAny
# from rest_framework_simplejwt.tokens import RefreshToken
# from .models import Institution

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def login_institution(request):
#     email = request.data.get('email')
#     password = request.data.get('password')

#     print(f"Attempting login with Email: {email}, Password: {password}")

#     try:
#         institution = Institution.objects.get(email=email)
#         print(f"Stored Password: {institution.password}")

#         # Directly compare plain text password
#         if institution.password == password:
#              # Manually create JWT token without using RefreshToken.for_user
#             refresh = RefreshToken()
#             refresh['email'] = institution.email
#             refresh['role'] = 'institution'  # Adding custom claim if needed
            
#             print("Login successful! Generating tokens...")
#             return Response({
#                 "message": "Institution login successful!",
#                 "access_token": str(refresh.access_token),
#                 "refresh_token": str(refresh)
#             }, status=status.HTTP_200_OK)
#         else:
#             print("Invalid credentials: Password does not match.")
#             return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

#     except Institution.DoesNotExist:
#          print("Institution not found.")
#          return Response({"error": "Institution not found"}, status=status.HTTP_404_NOT_FOUND)

# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import AllowAny
# from .models import Institution

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def login_institution(request):
#     email = request.data.get('email')
#     password = request.data.get('password')

#     try:
#         institution = Institution.objects.get(email=email)
        
#         if institution.password == password:  # Plaintext password comparison
#             # 🔹 Store Institution ID in Session
#             request.session['institution_id'] = institution.id
#             return Response({
#                 "message": "Institution login successful!",
#                 "institution_id": institution.id
#             }, status=status.HTTP_200_OK)
#         else:
#             return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

#     except Institution.DoesNotExist:
#         return Response({"error": "Institution not found"}, status=status.HTTP_404_NOT_FOUND)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Institution, Feedback
from .serializers import FeedbackSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from .models import Institution

# # 🔹 Institution Login without `RefreshToken.for_user()`
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def login_institution(request):
#     email = request.data.get('email')
#     password = request.data.get('password')

#     try:
#         institution = Institution.objects.get(email=email)

#         # ✅ Direct password comparison (No Hashing)
#         if institution.password == password:
#             # 🔹 Manually create JWT tokens (Since RefreshToken.for_user() fails)
#             refresh = RefreshToken()
#             refresh['email'] = institution.email
#             refresh['role'] = 'institution'

#             access_token = str(refresh.access_token)

#             return Response({
#                 "message": "Institution login successful!",
#                 "institution_id": institution.id,
#                 "access_token": access_token,
#                 "refresh_token": str(refresh)
#             }, status=status.HTTP_200_OK)
#         else:
#             return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

#     except Institution.DoesNotExist:
#         return Response({"error": "Institution not found"}, status=status.HTTP_404_NOT_FOUND)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Institution

@api_view(['POST'])
@permission_classes([AllowAny])
def login_institution(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        institution = Institution.objects.get(email=email)

        if institution.password == password:  # ✅ Direct password check
            # 🔥 Custom Token Generation (Instead of for_user)
            refresh = RefreshToken()
            refresh['institution_id'] = institution.id  # ✅ Add institution_id to the token

            return Response({
                "message": "Institution login successful!",
                "institution_id": institution.id,
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    except Institution.DoesNotExist:
        return Response({"error": "Institution not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_feedback(request):
    institution = request.user  # ✅ Custom Authentication now sets `request.user`

    try:
        feedbacks = Feedback.objects.filter(institution=institution)
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Feedback.DoesNotExist:
        return Response({"message": "No feedback found for this institution."}, status=status.HTTP_404_NOT_FOUND)



# # 🔹 Institution View Feedback
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def view_feedback(request):
#     institution = request.user
#     print(f"Logged-in Institution ID: {institution.id}")  # Debugging statement

#     try:
#         feedbacks = Feedback.objects.filter(institution=institution)
#         print(f"Feedback Records Found: {feedbacks}")  # Debugging statement
#         serializer = FeedbackSerializer(feedbacks, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     except Feedback.DoesNotExist:
#         return Response({"message": "No feedback found for this institution."}, status=status.HTTP_404_NOT_FOUND)
















from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Feedback, Student, Institution
from .serializers import FeedbackSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# 🔹 Submit Feedback API (Student can submit feedback)
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # JWT token required
def submit_feedback(request):
    student_id = request.data.get('student_id')
    institution_name = request.data.get('institution_name')

    # Validate Student
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return Response({"error": "Student not found. Please check the student ID."}, status=status.HTTP_404_NOT_FOUND)

    # Validate Institution
    try:
        institution = Institution.objects.get(name=institution_name)
    except Institution.DoesNotExist:
        return Response({"error": "Institution not found. Please check the institution name."}, status=status.HTTP_404_NOT_FOUND)

    # Collect Feedback Data
    feedback_data = {
        "student": student.id,
        "institution": institution.id,
        "course": request.data.get("course"),
        "teaching": request.data.get("teaching"),
        "course_content": request.data.get("course_content"),
        "examination": request.data.get("examination"),
        "lab_work": request.data.get("lab_work"),
        "library_facilities": request.data.get("library_facilities"),
        "extracurricular": request.data.get("extracurricular")
    }

    # Serialize and Save Feedback
    serializer = FeedbackSerializer(data=feedback_data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Feedback submitted successfully!"}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def view_feedback(request):
#     institution = request.user  # Assuming institution login logic is similar
#     print(f"Logged-in Institution ID: {institution.id}")  # Debugging statement

#     try:
#         feedbacks = Feedback.objects.filter(institution=institution)
#         print(f"Feedback Records Found: {feedbacks}")  # Debugging statement
        
#         # Custom serialization to include student name and course
#         feedback_data = []
#         for feedback in feedbacks:
#             feedback_data.append({
#                 "student_name": feedback.student.name,
#                 "student_course": feedback.student.course,
#                 "feedback_details": FeedbackSerializer(feedback).data
#             })

#         return Response(feedback_data, status=status.HTTP_200_OK)
#     except Feedback.DoesNotExist:
#         return Response({"message": "No feedback found for this institution."}, status=status.HTTP_404_NOT_FOUND)

# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# from .models import Feedback, Institution
# from .serializers import FeedbackSerializer

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def view_feedback(request):
#     institution_id = request.session.get('institution_id')

#     if not institution_id:
#         return Response({"error": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

#     try:
#         institution = Institution.objects.get(id=institution_id)

#         feedbacks = Feedback.objects.filter(institution=institution)
#         serializer = FeedbackSerializer(feedbacks, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     except Institution.DoesNotExist:
#         return Response({"error": "Institution not found"}, status=status.HTTP_404_NOT_FOUND)
#     except Feedback.DoesNotExist:
#         return Response({"message": "No feedback found for this institution."}, status=status.HTTP_404_NOT_FOUND)






@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])  # Ensure only authenticated users can access this view
def my_protected_view(request):
    return Response({"message": "You are authenticated!"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_student_feedback(request):
    student = request.user  
    print(f"Logged-in Student ID: {student.id}")  # Debugging statement

    try:
        feedbacks = Feedback.objects.filter(student=student)
        print(f"Feedback Records Found: {feedbacks}")  # Debugging statement
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Feedback.DoesNotExist:
        return Response({"message": "No feedback found for this student."}, status=status.HTTP_404_NOT_FOUND)

# import os
# import pickle
# from django.conf import settings
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework import status
# from sklearn.svm import SVC
# import numpy as np

# # Load the model and vectorizer
# model_path = os.path.join(settings.BASE_DIR, 'feedback', 'models', 'svm_best_model.pkl')
# vectorizer_path = os.path.join(settings.BASE_DIR, 'feedback', 'models', 'tfidf_vectorizer.pkl')

# with open(model_path, 'rb') as model_file:
#     svm_model = pickle.load(model_file)

# with open(vectorizer_path, 'rb') as vectorizer_file:
#     tfidf_vectorizer = pickle.load(vectorizer_file)

# from .models import Feedback
# from django.db.models import Q

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def predict_sentiment(request):
#     student_id = request.data.get('student_id')
#     institution_name = request.data.get('institution_name')

#     # Fetch Feedback from Database
#     try:
#         feedback = Feedback.objects.get(
#             Q(student__id=student_id) & Q(institution__name=institution_name)
#         )
#     except Feedback.DoesNotExist:
#         return Response({"error": "Feedback not found for this student and institution."}, 
#                         status=status.HTTP_404_NOT_FOUND)

#     # Combine all feedback fields into one text
#     combined_feedback = " ".join(filter(None, [
#         feedback.teaching,
#         feedback.course_content,
#         feedback.library_facilities,
#         feedback.lab_work,
#         feedback.examination,
#         feedback.extracurricular
#     ])).strip()

#     if not combined_feedback:
#         return Response({"error": "No valid feedback text available for sentiment prediction."}, 
#                         status=status.HTTP_400_BAD_REQUEST)

#     # Preprocess and Predict
#     cleaned_text = combined_feedback.lower()
#     transformed_text = tfidf_vectorizer.transform([cleaned_text])
#     prediction = svm_model.predict(transformed_text)[0]

#     # Map prediction to labels
#     label_mapping = {1: 'positive', 0: 'neutral', -1: 'negative'}
#     predicted_sentiment = label_mapping.get(prediction, 'unknown')

#     # Return prediction result
#     return Response({
#         "student_id": student_id,
#         "institution_name": institution_name,
#         "predicted_sentiment": predicted_sentiment
#     }, status=status.HTTP_200_OK)

# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# from .models import Feedback

# # 🔹 Overall Sentiment Analysis API
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def institution_overall_sentiment(request):
#     # Count Sentiments from Feedback
#     positive_count = Feedback.objects.filter(teaching__icontains='positive').count() + \
#                      Feedback.objects.filter(course_content__icontains='positive').count() + \
#                      Feedback.objects.filter(examination__icontains='positive').count() + \
#                      Feedback.objects.filter(lab_work__icontains='positive').count() + \
#                      Feedback.objects.filter(library_facilities__icontains='positive').count() + \
#                      Feedback.objects.filter(extracurricular__icontains='positive').count()

#     negative_count = Feedback.objects.filter(teaching__icontains='negative').count() + \
#                      Feedback.objects.filter(course_content__icontains='negative').count() + \
#                      Feedback.objects.filter(examination__icontains='negative').count() + \
#                      Feedback.objects.filter(lab_work__icontains='negative').count() + \
#                      Feedback.objects.filter(library_facilities__icontains='negative').count() + \
#                      Feedback.objects.filter(extracurricular__icontains='negative').count()

#     neutral_count = Feedback.objects.all().count() - (positive_count + negative_count)

#     return Response({
#         "positive": positive_count,
#         "neutral": neutral_count,
#         "negative": negative_count
#     }, status=status.HTTP_200_OK)
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def category_wise_sentiment(request):
#     categories = [
#         'teaching', 'course_content', 'examination',
#         'lab_work', 'library_facilities', 'extracurricular'
#     ]

#     category_sentiment = {category: {"positive": 0, "neutral": 0, "negative": 0} for category in categories}

#     feedbacks = Feedback.objects.all()

#     for feedback in feedbacks:
#         for category in categories:
#             category_text = getattr(feedback, category, "")

#             if category_text:
#                 cleaned_text = category_text.lower()
#                 transformed_text = tfidf_vectorizer.transform([cleaned_text])
#                 prediction = svm_model.predict(transformed_text)[0]

#                 label_mapping = {1: 'positive', 0: 'neutral', -1: 'negative'}
#                 predicted_sentiment = label_mapping.get(prediction, 'unknown')

#                 category_sentiment[category][predicted_sentiment] += 1

#     return Response(category_sentiment, status=status.HTTP_200_OK)
# # 🔹 Student-Wise Sentiment Distribution API
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def student_sentiment_distribution(request):
#     student_id = request.data.get('student_id')
#     institution_name = request.data.get('institution_name')

#     # Validate Student
#     try:
#         student = Student.objects.get(id=student_id)
#     except Student.DoesNotExist:
#         return Response({"error": "Student not found. Please check the student ID."}, status=status.HTTP_404_NOT_FOUND)

#     # Validate Institution
#     try:
#         institution = Institution.objects.get(name=institution_name)
#     except Institution.DoesNotExist:
#         return Response({"error": "Institution not found. Please check the institution name."}, status=status.HTTP_404_NOT_FOUND)

#     # Get feedback data
#     feedbacks = Feedback.objects.filter(student=student, institution=institution)

#     if not feedbacks.exists():
#         return Response({"message": "No feedback found for this student and institution."}, status=status.HTTP_404_NOT_FOUND)

#     # Sentiment Distribution Data
#     sentiment_count = {"positive": 0, "neutral": 0, "negative": 0}

#     for feedback in feedbacks:
#         combined_text = ' '.join([
#             feedback.teaching or '',
#             feedback.course_content or '',
#             feedback.examination or '',
#             feedback.lab_work or '',
#             feedback.library_facilities or '',
#             feedback.extracurricular or ''
#         ]).strip()

#         if combined_text:
#             cleaned_text = combined_text.lower()
#             transformed_text = tfidf_vectorizer.transform([cleaned_text])
#             prediction = svm_model.predict(transformed_text)[0]

#             # Map numeric prediction to sentiment labels
#             label_mapping = {1: 'positive', 0: 'neutral', -1: 'negative'}
#             predicted_sentiment = label_mapping.get(prediction, 'unknown')

#             if predicted_sentiment in sentiment_count:
#                 sentiment_count[predicted_sentiment] += 1

#     return Response({
#         "student_name": student.name,
#         "institution_name": institution.name,
#         "sentiment_distribution": sentiment_count
#     }, status=status.HTTP_200_OK)

import pickle
import os
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Feedback, Student, Institution
from django.db.models import Q

# Load the model and vectorizer
model_path = os.path.join(settings.BASE_DIR, 'feedback', 'models', 'svm_best_model.pkl')
vectorizer_path = os.path.join(settings.BASE_DIR, 'feedback', 'models', 'tfidf_vectorizer.pkl')

with open(model_path, 'rb') as model_file:
    svm_model = pickle.load(model_file)

with open(vectorizer_path, 'rb') as vectorizer_file:
    tfidf_vectorizer = pickle.load(vectorizer_file)

# 🔹 Common Function for Sentiment Prediction
def predict_sentiment(text):
    if not text.strip():
        return "neutral"  # Default to neutral if text is empty

    cleaned_text = text.lower().strip()
    transformed_text = tfidf_vectorizer.transform([cleaned_text])
    prediction = svm_model.predict(transformed_text)[0]

    label_mapping = {1: 'positive', 0: 'neutral', -1: 'negative'}
    return label_mapping.get(prediction, 'neutral')

# 🔹 Overall Sentiment Analysis API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def institution_overall_sentiment(request):
    feedbacks = Feedback.objects.all()

    sentiment_count = {"positive": 0, "neutral": 0, "negative": 0}

    for feedback in feedbacks:
        combined_text = " ".join(filter(None, [
            feedback.teaching,
            feedback.course_content,
            feedback.library_facilities,
            feedback.lab_work,
            feedback.examination,
            feedback.extracurricular
        ])).strip()

        predicted_sentiment = predict_sentiment(combined_text)
        sentiment_count[predicted_sentiment] += 1

    return Response(sentiment_count, status=status.HTTP_200_OK)

# 🔹 Student-Wise Sentiment Distribution API
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def student_sentiment_distribution(request):
    student_id = request.data.get('student_id')
    institution_name = request.data.get('institution_name')

    # Validate Student
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return Response({"error": "Student not found. Please check the student ID."}, 
                        status=status.HTTP_404_NOT_FOUND)

    # Validate Institution
    try:
        institution = Institution.objects.get(name=institution_name)
    except Institution.DoesNotExist:
        return Response({"error": "Institution not found. Please check the institution name."}, 
                        status=status.HTTP_404_NOT_FOUND)

    # Get feedback data
    feedbacks = Feedback.objects.filter(student=student, institution=institution)

    if not feedbacks.exists():
        return Response({"message": "No feedback found for this student and institution."}, 
                        status=status.HTTP_404_NOT_FOUND)

    # Sentiment Distribution Data
    sentiment_count = {"positive": 0, "neutral": 0, "negative": 0}

    for feedback in feedbacks:
        combined_text = ' '.join([ 
            feedback.teaching or '',
            feedback.course_content or '',
            feedback.examination or '',
            feedback.lab_work or '',
            feedback.library_facilities or '',
            feedback.extracurricular or ''
        ]).strip()

        predicted_sentiment = predict_sentiment(combined_text)
        sentiment_count[predicted_sentiment] += 1

    return Response({
        "student_name": student.name,
        "institution_name": institution.name,
        "sentiment_distribution": sentiment_count
    }, status=status.HTTP_200_OK)

# 🔹 Category-Wise Sentiment Distribution API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category_wise_sentiment(request):
    categories = [
        'teaching', 'course_content', 'examination',
        'lab_work', 'library_facilities', 'extracurricular'
    ]

    category_sentiment = {category: {"positive": 0, "neutral": 0, "negative": 0} for category in categories}

    feedbacks = Feedback.objects.all()

    for feedback in feedbacks:
        for category in categories:
            category_text = getattr(feedback, category, "")

            predicted_sentiment = predict_sentiment(category_text)
            category_sentiment[category][predicted_sentiment] += 1

    return Response(category_sentiment, status=status.HTTP_200_OK)




