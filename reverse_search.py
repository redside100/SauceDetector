import webbrowser
import requests
import uuid
import base64
import os

with open('client_id', 'r+') as f:
    client_id = f.readlines()

upload_api_url = 'https://api.imgur.com/3/upload'
google_rev = 'https://images.google.com/searchbyimage?image_url={}'


def crop_and_upload(img, region, overlay):
    overlay.clicking = True
    face_img_cropped = img.crop(
        (region[0], region[1], region[0] + region[2], region[1] + region[3]))
    temp_id = uuid.uuid4()
    face_img_cropped.save("temp-{}.jpg".format(temp_id), "JPEG")

    with open("temp-{}.jpg".format(temp_id), "rb") as f:
        image_data = f.read()

    b64_image = base64.standard_b64encode(image_data)
    header = {
        "Authorization": "Client-ID {}".format(client_id)
    }
    form_data = {
        'image': b64_image,
        'type': 'base64'
    }
    res = requests.post(upload_api_url, data=form_data, headers=header)
    if res.ok and res.json()['status'] == 200:
        link = res.json()['data']['link']
        webbrowser.open_new_tab(google_rev.format(link))

    os.remove('./temp-{}.jpg'.format(temp_id))
    overlay.clicking = False

