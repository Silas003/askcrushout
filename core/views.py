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
                'id':obj.id,
                'link': f"https://askcrushout.netlify.app/",                
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
            to=self.receipient,
            bcc=['kumideveloper@gmail.com']
        )
        mail.send()
@api_view(['POST','GET'])
def send_message(request:Request,id:int):
    user=Person.objects.filter(id=id).first()
    serializer=PersonSerializer(user,many=False)
    if_true_subject='Congratulations on your Proposal💌'
    if_false_subject='Update on your Proposal💌'
    yes_text=f"Congratulations to you.Your crush {user.admirer} said to to a lifetime of love and happiness! Your decision to accept the proposal fills our hearts with joy and excitement. May your journey together be filled with endless laughter, cherished moments, and unwavering love. Here's to a future brimming with love, laughter, and countless beautiful memories. Wishing you both a lifetime of happiness and love as you embark on this wonderful journey together. Congratulations once again!"    
    no_text=f"While the decision may not have been easy, know that you have our full support and understanding. Your happiness and well-being are paramount, and we respect your choice wholeheartedly. Remember that life is a journey filled with twists and turns, and this decision is just one step along the way. Take your time, trust your instincts, and know that brighter days are ahead. You're surrounded by love and support as you navigate this chapter of your life. We're here for you every step of the way. Sending you strength, courage, and peace during this time.Your crush {user.admirer} said a BIG NO!!!"
    message=request.data['message']

    if request.data and message=='Yes':
        HandleMail(
            subject=if_true_subject,
            receipient=[user.email],
            body=yes_text
            ).start()
        return Response({
            'mail_message':'mail sent','message':message})
        
    elif request.data and message=='No':
        HandleMail(
            subject=if_false_subject,
            receipient=[user.email],
            body=no_text
            ).start()
        return Response({
            'mail_message':'mail sent','message':message})
    
    return Response({
            'user':serializer.data})