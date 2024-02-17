# from django.db import models
# import random
# from string import digits

# randomize=random.SystemRandom()
# id="".join(randomize.choice(digits) for i in range(5))

# class Person(models.Model):
#     id=models.CharField(
#         default=id,
#         primary_key=True,
#         unique=True,
#         max_length=6)
#     first_name=models.CharField(max_length=100)
#     admirer=models.CharField(max_length=50)
#     email=models.EmailField(unique=True)
#     response=models.CharField(max_length=50)

#     def create(self,**validated_data):
#         if Person.objects.filter(id==validated_data['id']):
#             id="".join(randomize.choice(digits) for i in range(5))
#             new=Person.objects.create(
#                 id=id,
#                 first_name=validated_data['first_name'],
#                 email=validated_data['email'],
#                 admirer=validated_data['admirer']
#             )
#             new.save()
from django.db import models
import random
from string import digits

randomize = random.SystemRandom()

class Person(models.Model):
    id = models.CharField(
        primary_key=True,
        unique=True,
        max_length=6
    )
    first_name = models.CharField(max_length=100)
    admirer = models.CharField(max_length=50)
    email = models.EmailField()
    response = models.CharField(max_length=50)
    speak_from_heart=models.TextField()

    @classmethod
    def generate_id(cls):
        return "".join(randomize.choice(digits) for i in range(5))

    @classmethod
    def create(cls, **validated_data):
        validated_data['id'] = cls.generate_id()
        return cls.objects.create(**validated_data)
    
    
class Anon(models.Model):
    username=models.CharField(max_length=25)

    def __str__(self) -> str:
        return self.username
    
class Anon_Response(models.Model):
    user=models.ForeignKey(Anon,on_delete=models.CASCADE,related_name='responses')
    response=models.TextField()
    
    def __str__(self) -> str:
        return f"{self.user}"