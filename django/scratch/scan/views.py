from django.shortcuts import render
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import tempfile
import time
import math
import json
from io import BufferedWriter, FileIO

import sys
import json
from PIL import Image, ImageDraw

from scan.detection import *

@csrf_exempt
def handle_upload(request):
    upload = request.FILES['file']

    fh = tempfile.NamedTemporaryFile(delete=True)
    extension = upload.name.split(".")[1]
    filename = "{}.{}".format(fh.name, extension)

    with BufferedWriter(FileIO(filename, "w")) as dest:
        for c in upload.chunks():
            dest.write(c)

    img = Image.open(filename).convert('RGB')
    detect(filename, False)
    return JsonResponse(json.dumps(''), safe=False)
