from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Stadium


class StadiumList(APIView):
    def get(self, request, format=None):
        stadiums = Stadium.objects.all()  
        return Response(stadiums)
