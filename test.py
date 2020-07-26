import base64
import requests

URL = 'https://8f80b27ydg.execute-api.us-east-1.amazonaws.com/dev/find'


def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')


def upload_image(base64image):
    r = requests.post(URL, data={'image_blob': base64image})
    return r


if __name__ == '__main__':
    image1 = get_base64_encoded_image('./snake1.jpg')
    response1 = upload_image(image1)
    if 'snake' in response1.text.lower():
        print(response1.text)
    else:
        print('no snek1')

    image2 = get_base64_encoded_image('./snake2.jpg')
    response2 = upload_image(image2)
    if 'snake' in response2.text.lower():
        print(response2.text)
    else:
        print('no snek2')
