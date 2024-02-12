from rest_framework import routers
from .views import PersonViewset,send_link,send_message,ResViewset,AnonViewset
from django.urls import path
router=routers.DefaultRouter()

router.register('person',PersonViewset,basename='person')
router.register('anon',AnonViewset,basename='anon')
router.register('res',ResViewset,basename='res')

urlpatterns = [
    path('send-link/',send_link,name='send=link'),
    path('message/<int:id>',send_message,name='message')
]
urlpatterns+=router.urls
