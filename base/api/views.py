from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer

@api_view(['GET'])
def getRoutes(request):
  routes=[
    "GET api/",
    "GET /api/rooms",
    "GET /api/rooms/:id"
  ]
  return  Response(routes)

@api_view(['GET'])
def getRooms(request):
  room=Room.objects.all()
  serializer_data=RoomSerializer(room,many=True) # many means it will return all if true
  return Response(serializer_data.data)


@api_view(['GET'])
def getRoom(request,pk):
  print(pk,"data")
  room=Room.objects.get(id=pk)
  serializer_data=RoomSerializer(room,many=False) # many means it will return all if false it return only one 
  return Response(serializer_data.data)


