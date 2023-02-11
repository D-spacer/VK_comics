import requests
import random
import os
from dotenv import load_dotenv


def check_vk_response(response):
    decoded_response = response.json()
    if 'error' in decoded_response:
        raise ConnectionError(f'Возникла ошибка {decoded_response["error"]["error_msg"]}')


def get_random_comic_number():
    last_comic_response = requests.get('https://xkcd.com/info.0.json')
    last_comic_response.raise_for_status()
    decoded_last_comics_data_response = last_comic_response.json()
    image_number = int(decoded_last_comics_data_response['num'])
    image_number_to_post = random.randint(1, image_number)
    return image_number_to_post


def download_comic(image_number_to_post):
    image_details_response = requests.get(f'https://xkcd.com/{image_number_to_post}/info.0.json')
    image_details_response.raise_for_status()
    decoded_image_details_response = image_details_response.json()
    image_download_response = requests.get(decoded_image_details_response['img'])
    image_download_response.raise_for_status()
    with open(f'image_{image_number_to_post}.png', 'wb') as file:
        file.write(image_download_response.content)
    return decoded_image_details_response['alt']


def get_link_to_upload(group_id, access_token, api_version=5.131):
    server_parameters = {
        'access_token': access_token,
        'group_id': group_id,
        'v': api_version
    }
    server_details_response = requests.get('http://api.vk.com/method/photos.getWallUploadServer',
                                           params=server_parameters)
    check_vk_response(server_details_response)
    decoded_server_details_response = server_details_response.json()
    return decoded_server_details_response['response']['upload_url']


def upload_image(image_number_to_post, upload_link):
    with open(f'image_{image_number_to_post}.png', 'rb') as file:
        url = upload_link
        files = {
            'photo': file
        }
        image_upload_response = requests.post(url, files=files)
    check_vk_response(image_upload_response)
    decoded_image_upload_response = image_upload_response.json()
    return decoded_image_upload_response['server'], decoded_image_upload_response['photo'], \
           decoded_image_upload_response['hash']


def save_image(server, photo, hash_, group_id, access_token, api_version=5.131):
    image_parameters = {
        'access_token': access_token,
        'server': server,
        'photo': photo,
        'hash': hash_,
        'group_id': group_id,
        'v': api_version

    }
    image_save_response = requests.post(
        'http://api.vk.com/method/photos.saveWallPhoto',
        params=image_parameters)
    check_vk_response(image_save_response)
    decoded_image_save_response = image_save_response.json()
    return decoded_image_save_response["response"][0]["owner_id"], decoded_image_save_response["response"][0]["id"]


def post_image(owner_id, id_, group_id, comment, access_token, api_version=5.131):
    image_post_parameters = {
        'access_token': access_token,
        'owner_id': f'-{group_id}',
        'from_group': 1,
        'message': comment,
        'attachments': f'photo{owner_id}_'
                       f'{id_}',
        'v': api_version
    }
    check_vk_response(requests.post('http://api.vk.com/method/wall.post',
                  params=image_post_parameters))


def main():
    load_dotenv()
    access_token = os.environ['VK_ACCESS_TOKEN']
    group_id = os.environ['VK_GROUP_ID']
    try:
        image_number_to_post = get_random_comic_number()
        comment = download_comic(image_number_to_post)
        upload_link = get_link_to_upload(group_id, access_token)
        server, photo, hash_ = upload_image(image_number_to_post, upload_link)
        owner_id, id_ = save_image(server, photo, hash_, group_id, access_token)
        post_image(owner_id, id_, group_id, comment, access_token)
    finally:
        os.remove(f'image_{image_number_to_post}.png')


if __name__ == "__main__":
    main()
