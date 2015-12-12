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

class Login(views.APIView):
  def post(self, request):
    user = authenticate(username = request.GET.get('username'), password = request.GET.get('password'))
    if user is not None:
        # the password verified for the user
        if user.is_active:
            return Response(status = 200)
        else:
            return Response(status = 401)
    else:
        # the authentication system was unable to verify the username and password
        return Response(status = 401)

  
