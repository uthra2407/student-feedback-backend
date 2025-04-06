from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class StudentManager(BaseUserManager):
    def create_user(self, name, regno, institution, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Students must have an email address")
        email = self.normalize_email(email)

        # Ensure the institution exists before creating a student
        try:
            institution_instance = Institution.objects.get(name=institution)
        except Institution.DoesNotExist:
            raise ValueError("Institution does not exist!")

        student = self.model(
            name=name,
            regno=regno,
            institution=institution_instance,  # Reference to Institution instance
            email=email,
            **extra_fields
        )
        student.set_password(password)  # Hash the password
        student.save(using=self._db)
        return student

    def create_superuser(self, name, regno, institution, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(name, regno, institution, email, password, **extra_fields)

# class Student(AbstractBaseUser, PermissionsMixin):
#     name = models.CharField(max_length=255)
#     regno = models.CharField(max_length=20, unique=True, null=True, blank=True)
    
#     # Updated ForeignKey Reference (String Reference to Avoid Circular Import)
#     institution = models.ForeignKey('feedback.Institution', on_delete=models.CASCADE)  
#     email = models.EmailField(unique=True)

#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)

#     objects = StudentManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['name', 'regno', 'institution']

#     def __str__(self):
#         return self.email

class Student(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    regno = models.CharField(max_length=20, unique=True, null=True, blank=True)
    
    #institution = models.ForeignKey('feedback.Institution', on_delete=models.CASCADE)  
    institution = models.ForeignKey('feedback.Institution', on_delete=models.CASCADE, null=True, blank=True)


    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='student_groups'  # ✅ Added related_name to avoid conflicts
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='student_permissions'  # ✅ Added related_name to avoid conflicts
    )

    objects = StudentManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'regno', 'institution']

    def __str__(self):
        return self.email


# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# # 🔹 Custom Manager for Institution
# class InstitutionManager(BaseUserManager):
#     def create_institution(self, name, location, email, password=None):
#         if not email:
#             raise ValueError("Institutions must have an email address")
        
#         institution = self.model(
#             name=name,
#             location=location,
#             email=self.normalize_email(email),
#             password=password  # Directly store the password as plain text
#         )
#         institution.set_password(password)  # Using set_password to avoid JWT issues
#         institution.save(using=self._db)
#         return institution

# 🔹 Institution Model
# class Institution(AbstractBaseUser, PermissionsMixin):
#     name = models.CharField(max_length=255)
#     location = models.CharField(max_length=255, null=True, blank=True)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=255)  # Directly store plain text password

#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)

#     objects = InstitutionManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['name', 'location']

#     groups = models.ManyToManyField(
#         'auth.Group',
#         related_name='institution_groups',
#         blank=True
#     )
    
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         related_name='institution_permissions',
#         blank=True
#     )

#     def __str__(self):
#         return self.name

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class InstitutionManager(BaseUserManager):
    def create_institution(self, name, location, email, password=None):
        if not email:
            raise ValueError("Institutions must have an email address")
        
        institution = self.model(
            name=name,
            location=location,
            email=self.normalize_email(email),
            password=password  # ✅ Plain text password (no hashing)
        )
        institution.save(using=self._db)
        return institution

class Institution(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # ✅ Plain Text Password

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='institution_groups'  # ✅ Avoids conflicts
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='institution_permissions'  # ✅ Avoids conflicts
    )

    objects = InstitutionManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'location']

    def __str__(self):
        return self.name






from django.db import models
from .models import Student, Institution

# Feedback Model with Course and Six Feedback Questions
class Feedback(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)

    course = models.CharField(max_length=255)  # Added course field

    teaching = models.TextField(null=True, blank=True)
    course_content = models.TextField(null=True, blank=True)
    library_facilities = models.TextField(null=True, blank=True)
    lab_work = models.TextField(null=True, blank=True)
    extracurricular = models.TextField(null=True, blank=True)
    examination = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Feedback by {self.student.name} for {self.institution.name}"

from django.db import models
from .models import Student, Institution

# View_Feedback Model for institutions with Six Feedback Questions
class View_Feedback(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    course = models.CharField(max_length=255,null=True,blank=True)  # Added course field
    
    teaching = models.TextField(null=True, blank=True)
    course_content = models.TextField(null=True, blank=True)
    library_facilities = models.TextField(null=True, blank=True)
    lab_work = models.TextField(null=True, blank=True)
    extracurricular = models.TextField(null=True, blank=True)
    examination = models.TextField(null=True, blank=True)
    

    def __str__(self):
        return f"Feedback by {self.student.name} for {self.institution.name}"
from django.db import models
from .models import Student, Institution

# 🌟 Model to manage feedback viewing for students (Optional)
class ViewFeedbackStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    
    teaching = models.TextField(null=True, blank=True)
    course_content = models.TextField(null=True, blank=True)
    library_facilities = models.TextField(null=True, blank=True)
    lab_work = models.TextField(null=True, blank=True)
    extracurricular = models.TextField(null=True, blank=True)
    examination = models.TextField(null=True, blank=True)
    
    viewed_at = models.DateTimeField(auto_now_add=True)  # When the feedback was viewed

    def __str__(self):
        return f"Feedback viewed by {self.student.name} for {self.institution.name}"

