from rest_framework import viewsets
from .serializers import Person,PersonSerializer,AnonSerializer,ResSerializer
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
import threading
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .models import Person,Anon,Anon_Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

class PersonViewset(viewsets.ModelViewSet):
    serializer_class=PersonSerializer
    queryset=Person.objects.all()

class AnonViewset(viewsets.ModelViewSet):
    serializer_class=AnonSerializer
    queryset=Anon.objects.all()


class ResViewset(viewsets.ModelViewSet):
    serializer_class=ResSerializer
    queryset=Anon_Response.objects.all()




@swagger_auto_schema()
@api_view(['POST'])
def send_link(request):
    if request.method == "POST":
        data = request.data
        
        try:
            obj = Person.create(
                first_name=data['first_name'],
                email=data['email'],
                admirer=data['admirer'],
                image=data['image'],
                speak_from_heart=data['speak_from_heart']
            )
            image_url = request.build_absolute_uri(obj.image.url)
            #id_url=request.build_absolute_uri(obj.id)
            content={
                'link': f"https://askcrushout.netlify.app/asking/{obj.id}",
                'image':image_url
            }
            return JsonResponse(data=content,status=status.HTTP_201_CREATED)
        except (IntegrityError, ValidationError) as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class HandleMail(threading.Thread):
    def __init__(self,subject,body,receipient):
        self.subject=subject
        self.body=body
        self.receipient=receipient
        threading.Thread.__init__(self)
    
    def run(self):
        mail=EmailMessage(
            subject=self.subject,
            body=self.body,
            from_email='kumideveloper@gmail.com',
            to=self.receipient
        )
        mail.send()
@api_view(['POST','GET'])
def send_message(request:Request,id:int):
    user=Person.objects.filter(id=id).first()
    serializer=PersonSerializer(user,many=False)
    text=f'Dear,{user.first_name},it\\\'s with with great heart that your crush,{user.admirer} has accepted your proposal but thread carefully'
    if request.data:
        HandleMail(
            subject=request.data['message'],
            receipient=['kumideveloper@gmail.com',user.email],
            body=request.data['message']
            ).start()
        return Response({
            'message':'mail sent'})
    
    return Response({
            'user':serializer.data})