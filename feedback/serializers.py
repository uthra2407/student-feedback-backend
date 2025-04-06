from rest_framework import serializers
from .models import Feedback
from .models import Student
from .models import Institution

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
#class StudentSerializer(serializers.ModelSerializer):
 #   class Meta:
  #      model = Student
   #     fields = '__all__'
from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'regno', 'institution', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        student = Student.objects.create_student(
            name=validated_data['name'],
            regno=validated_data['regno'],
            institution=validated_data['institution'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return student


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = '__all__'


from rest_framework import serializers
from .models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'

