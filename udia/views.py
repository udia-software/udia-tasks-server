from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

def index(request):
    return HttpResponse('API Server for UDIA (tasks).')

@api_view()
def null_view(request):
    return Response(status=status.HTTP_400_BAD_REQUEST)
