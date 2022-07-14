from rest_framework.decorators import api_view
from rest_framework.response import Response
 #input data to jason data 
from base.models import Room
from .serializers import  RoomSerializer
from base.api import serializers

# from django.http import JsonResponse

@api_view(['GET']) #decorator for working with function based views.
def getRoutes(request):
    routes =[
        'GET/api',
        'GET /api/rooms', #get the api rooms
        'GET /api/room/:id' #which room
    
    ]
    return Response(routes)




@api_view(['GET'])

def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many = True)
    return Response(serializer.data) #converts the objects to json format 


@api_view(['GET'])

def getRoom(request, pk):
    rooms = Room.objects.get(id= pk)
    serializer = RoomSerializer(rooms, many = False )
    return Response(serializer.data)

