from django.shortcuts import render
from rest_framework import views
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from api.models import Receipt
import subprocess

# Create your views here.
class Upload(views.APIView):
  parser_classes = (FormParser, MultiPartParser,)

  def put(self, request, filename="image.png", format=None):
    new_receipt = Receipt(image=request.data['file'])
    new_receipt.save()
    p = subprocess.Popen(['tesseract', new_receipt.image.path, 'stdout'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()[0]
    print(out)


    return Response(status=204)
  
