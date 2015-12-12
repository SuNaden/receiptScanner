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
    names_file = request.data['names_file'];
    prices_file = request.data['prices_file']

    new_receipt = Receipt(names_image=names_file, prices_image=prices_file)
    new_receipt.save()

    p = subprocess.Popen(['tesseract', new_receipt.names_image.path, 'stdout'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    names_file_ocr = p.communicate()[0]

    p = subprocess.Popen(['tesseract', new_receipt.prices_image.path, 'stdout'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    prices_file_ocr = p.communicate()[0]

    print(names_file_ocr)
    print(prices_file_ocr)

    return Response(status=204)
  
