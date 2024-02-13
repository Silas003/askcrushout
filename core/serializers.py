from rest_framework import serializers
from .models import Person,Anon,Anon_Response

class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model=Person
        fields=['id','first_name','email','admirer','image','speak_from_heart']
    
    
    
    

class ResSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anon_Response
        fields = ['id', 'response']

class AnonSerializer(serializers.ModelSerializer):
    responses = ResSerializer(many=True, read_only=True)

    class Meta:
        model = Anon
        fields = ['id', 'username', 'responses']