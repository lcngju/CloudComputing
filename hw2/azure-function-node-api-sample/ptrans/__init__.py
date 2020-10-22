import logging
import azure.functions as func

from PIL import Image,ImageFilter
import base64
#import numpy as np
import io


def image_to_base64(img):
    output_buffer = io.BytesIO()
    imgB = io.BytesIO()
    img.save(imgB, format='png')
    imgC = imgB.getvalue()
    
    return imgC


def b64toImg(img):
    img_b64decode = base64.b64decode(img)
    img = io.BytesIO(img_b64decode)
    img = Image.open(img)
    return img
    



def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    #logging.info(req.content)
    img = req.params.get('file')
    if not img:
        try:
            req_body = req.get_json()
            #logging.info(req_body)
        except ValueError:
            pass
        else:
            img = req_body.get('file')

    
    if img:
        img = b64toImg(img)
        img2 = img.filter(ImageFilter.BLUR)
        s = image_to_base64(img2)
        b = base64.b64encode(s)
        c = b.decode('utf-8')

        return func.HttpResponse(body=b)



    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
