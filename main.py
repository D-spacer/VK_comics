import requests
import random
import os
from dotenv import load_dotenv


def post_comics(access_token, group_id):
    response_last_comics = requests.get('https://xkcd.com/info.0.json')
    decoded_last_comics = response_last_comics.json()
    image_number = int(decoded_last_comics['num'])
    image_to_post = random.randint(1, image_number)

    response_image_details = requests.get(f'https://xkcd.com/{image_to_post}/info.0.json')
    response_image_details.raise_for_status()
    decoded_response_image_details = response_image_details.json()

    response_image_download = requests.get(decoded_response_image_details['img'])
    response_image_download.raise_for_status()
    with open(f'image_{image_to_post}.png', 'wb') as file:
        file.write(response_image_download.content)

    parameters_server_details = {
        'group_id': group_id
    }
    response_link = requests.get(f'http://api.vk.com/method/photos.getWallUploadServer?access_token={access_token}&v=5.131',
                                 params=parameters_server_details)
    response_link.raise_for_status()
    decoded_response_link = response_link.json()

    with open(f'image_{image_to_post}.png', 'rb') as file:
        url = decoded_response_link['response']['upload_url']
        files = {
            'photo': file
        }
        response_image_upload = requests.post(url, files=files)
        response_image_upload.raise_for_status()
        decoded_response_image_upload = response_image_upload.json()

    parameters_image = {
        'server': decoded_response_image_upload['server'],
        'photo': decoded_response_image_upload['photo'],
        'hash': decoded_response_image_upload['hash'],
        'group_id': group_id
    }
    response_image_save = requests.post(
        f'http://api.vk.com/method/photos.saveWallPhoto?access_token={access_token}&v=5.131',
        params=parameters_image)
    response_image_save.raise_for_status()
    decoded_response_image_save = response_image_save.json()

    parameters_image_post = {
        'owner_id': f'-{group_id}',
        'from_group': 1,
        'message': decoded_response_image_details['alt'],
        'attachments': f'photo{decoded_response_image_save["response"][0]["owner_id"]}_'
                       f'{decoded_response_image_save["response"][0]["id"]}'
    }

    requests.post(f'http://api.vk.com/method/wall.post?access_token={access_token}&v=5.131',
                  params=parameters_image_post)

    os.remove(f'image_{image_to_post}.png')


def main():
    load_dotenv()
    access_token = os.environ['ACCESS_TOKEN']
    group_id = os.environ['GROUP_ID']
    post_comics(access_token, group_id)


if __name__ == "__main__":
    main()