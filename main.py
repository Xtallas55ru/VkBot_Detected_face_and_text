#|==========================|
#|Developer: Xtallas55ru    |
#|version: 1.0              |
#|vk: https://vk.com/xtallas|
#|==========================|

import boto3    # Amazon cloud
import time     # Time
import vk_api   # Vk_api
import urllib.request # Urllib
import requests
import json

from PIL import Image, ImageDraw  

login, password = '', '' # Login and password variable
values = {"out": 0,"count": 100, "time_offset": 60}


img_name  = 'img.jpg'

Width_default = 1280
Height_default = 1024

owner_id = 371446566

client = boto3.client('rekognition')

vk = vk_api.VkApi(login, password)
vk.auth()
vk_session = vk.get_api()

def main():
    response = vk.method("messages.get", values)
    if response["items"]:
        values["last_message_id"] = response["items"][0]["id"]
        vk.method("messages.markAsRead", {"message_ids": values["last_message_id"]})
        global user_id
        user_id = response["items"][0]["user_id"] 
        photo_c = len(response["items"][0]["attachments"][0]['photo'])
        if photo_c == 14:
            save_photo(response["items"][0]["attachments"][0]['photo']['photo_2560'])
        elif photo_c == 13:
            save_photo(response["items"][0]["attachments"][0]['photo']['photo_1280'])
        else:
            save_photo(response["items"][0]["attachments"][0]['photo']['photo_604'])
    time.sleep(1)

def save_photo(img):
    resource = urllib.request.urlopen(img)
    out = open(img_name, 'wb') 
    out.write(resource.read())
    out.close()
    detect_and_crop_face()
    
def detect_and_crop_face():
    #Open images for readbytes
    with open(img_name, 'rb') as image:
        #Detected Face
        value = client.detect_faces(
            Image = {'Bytes': image.read()}
        )
        #Image close
        image.close()
    #Checking count face
    if len(value['FaceDetails']) != 0:
        #Detacted text
        with open(img_name, 'rb') as image:
            response = client.detect_text(
                Image = {'Bytes': image.read()}
            )
        #Image close
        image.close()
        #For text detected and search "FABLAB_UTMN"
        for text in response['TextDetections']: 
            if text['DetectedText'] == 'FABLAB_UTMN':
                send_messages('','# - ' + text['DetectedText'] + ' был найден')
    else:
        send_messages('','Не удалось найти лицо!')
                
def bot_on():
    vk.method('messages.send', {
        'user_id': owner_id,
        'message':     ''' ********************************* 
        * Developed by Vladimir Makarov 
        * Bot: Detect_Face_Bot by python3.6.5
        * Contacts: vk.com/xtallas
        * Version: 1.0 
        **********************************''',
    })

def send_messages(attachment, massages = ' '):
    vk.method('messages.send', {
        'user_id': user_id,
        'message': massages,
        'attachment': attachment
    })
    
if __name__ == '__main__':
    bot_on()
    while(True):
        try:
            main()
        except Exception as e:
            vk.method('messages.send', {
                'user_id': owner_id,
                'message': 'Ошибка ' + str(e),
            })