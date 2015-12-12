from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import views
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from api.models import Receipt
from decimal import Decimal

import subprocess, re


# Create your views here.
class Upload(views.APIView):
  parser_classes = (FormParser, MultiPartParser,)

  def put(self, request, filename="image.png", format=None):
    username = request.data['username']
    names_file = request.data['names_file']
    prices_file = request.data['prices_file']

    user = User.objects.get(username=username)
    new_receipt = user.receipt_set.create(
      names_image = names_file, 
      prices_image = prices_file
      )

    p1 = subprocess.Popen(['tesseract', new_receipt.names_image.path, 'stdout', '-psm', '6'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    names_file_ocr = p1.communicate()[0]

    p2 = subprocess.Popen(['tesseract', new_receipt.prices_image.path, 'stdout', '-psm', '6'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    prices_file_ocr = p2.communicate()[0]

    names_split = names_file_ocr.decode().split('\n')
    prices_split = prices_file_ocr.decode().split('\n')

    print(names_split)
    print(prices_split)

    non_decimal = re.compile(r'[^\d.]+')

    for i in range(0, len(names_split)):
      name = names_split[i]

      if (len(name) > 0):
        price = prices_split[i]

        new_receipt.receiptitem_set.create(
          name = name,
          price = Decimal(non_decimal.sub('', price))
        )

    return Response(status=204)
  
