from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import views
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from api.models import Receipt
from decimal import Decimal
from django.contrib.auth import authenticate

import subprocess, re
from pusher import Pusher

# Create your views here.
class Upload(views.APIView):
  parser_classes = (FormParser, MultiPartParser,)

  def put(self, request, filename="image.png", format=None):
    pusher = Pusher(app_id=u'160687', key=u'0eb2780d9a8a875c0727', secret=u'b45f1f052cd3359c9ceb')

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

        pusher.trigger(u'receipt_channel', u'new_receipt', { "test": "testdata" })

    return Response(status=204)

class Login(views.APIView):
  def post(self, request):
    user = authenticate(username = request.POST.get('username'), password = request.POST.get('password'))
    if user is not None:
        # the password verified for the user
        if user.is_active:
            return Response(status = 200)
        else:
            return Response(status = 401)
    else:
        # the authentication system was unable to verify the username and password
        return Response(status = 401)

  
