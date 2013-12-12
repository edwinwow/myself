from django.http import HttpResponse
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
    

def room_for_rent_list(request):
  """
  list all the rooms for rent
  """
  
  if request.method == 'GET':
    room_for_rent = RoomForRent.objects.all
    serializer = RoomForRentSerializer(room_for_rent, many=True)
    return JSONResponse(serializer.data)
    
  elif request.method == 'POST':
    data = JSONParser().parse(request)
    serializer = RoomForRentSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      return JSONResponse(serializer.data, status=201)
    else:
      return JSONResponse(serializer.errors, status=400)
    
    
