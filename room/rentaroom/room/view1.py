from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import RoomForRent
from .serializers import RoomForRentSerializer

class JSONResponse(HttpResponse):
  
  """
  An HttpResponse that renders its content into JSON.
  """
  
  def __init__(self, data, **kwargs):
    content = JSONRenderer().render(data)
    kwargs['content_type'] = 'application/json'
    super(JSONResponse, self).__init__(content, **kwargs)
    
@api_view(['GET', 'POST'])
def room_for_rent_list(request):
  """
  list all the rooms for rent
  """
  
  if request.method == 'GET':
    room_for_rent = RoomForRent.objects.all
    serializer = RoomForRentSerializer(room_for_rent, many=True)
    return Response(serializer.data)
    
  elif request.method == 'POST':
    data = JSONParser().parse(request)
    serializer = RoomForRentSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])     
def room_for_rent_detail(request, pk):
  
  """
  Retrieve, update or delete a code room for rent.
  """
  try:
    room_for_rent = RoomForRent.objects.get(pk=pk)
  except Response(status=status.HTTP_404_NOT_FOUND)
    
    
  if request.method == 'GET':
    serializer = RoomForRentSerializer(room_for_rent)
    return Response(serializer.data)
    
  elif request.method == 'PUT':
    data = JSONParser().parse(request)
    serializer = RoomForRentSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST
      
    
  elif request.method == 'DELETE':
    room_for_rent.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET', 'POST'])
def rental_contract_list(request):
  """
  list all the rental contract under a person
  """
  
  if request.method == 'GET':
    room_for_rent = RoomForRent.objects.all(room_owner=request.user)
    serializer = RoomForRentSerializer(room_for_rent, many=True)
    return Response(serializer.data)
    
  elif request.method == 'POST':
    data = JSONParser().parse(request)
    serializer = RoomForRentSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
@api_view(['GET', 'POST'])
def rental_contract_list_for_renter(request):
  
  """
  list all the rental contract under a renter
  
  """
  
  if request.method == 'GET':
    room_for_rent = RoomForRent.objects.filter(room_renter=request.user)
    serializer = RoomForRentSerializer(room_for_rent, many=True)
    return Response(serializer.data)
    
    
  
    
    
  
  
    
    
    
    
    
