from rest_framework import serializers
from .models import Person,Anon,Response

class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model=Person
        fields=['id','first_name','email','admirer','image']
    




class ResSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ['id', 'response']

class AnonSerializer(serializers.ModelSerializer):
    responses = ResSerializer(many=True, read_only=True)

    class Meta:
        model = Anon
        fields = ['id', 'username', 'responses']