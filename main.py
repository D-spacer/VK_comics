import requests
import random
import os
from dotenv import load_dotenv
from vkbottle import VKAPIError


def check_vk_response(response):
	try:
		await response
	except VKAPIError as e:
		print("Возникла ошибка", e.code)


def get_random_image(access_token, group_id):
	last_comics_data_response = requests.get('https://xkcd.com/info.0.json')
	decoded_last_comics_data_response = last_comics_data_response.json()
	image_number = int(decoded_last_comics_data_response['num'])
	image_number_to_post = random.randint(1, image_number)
	return image_number_to_post
	

def download_image(image_number_to_post):
	image_details_response = requests.get(f'https://xkcd.com/{image_number_to_post}/info.0.json')
	image_details_response.raise_for_status()
	decoded_image_details_response = image_details_response.json()
	image_download_response = requests.get(decoded_image_details_response['img'])
	image_download_response.raise_for_status()
	with open(f'image_{image_number_to_post}.png', 'wb') as file:
		file.write(image_download_response.content)
		return decoded_image_details_response['alt']


def get_link_to_upload(group_id, access_token, image_number_to_post, api_version=5.131):
	server_parameters = {
		'access_token': access_token,
        'group_id': group_id,
		'v': api_version
    }
	server_details_response = requests.get('http://api.vk.com/method/photos.getWallUploadServer', params=server_parameters)
    check_vk_response(server_details_response)
	server_details_response.raise_for_status()
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
	image_upload_response.raise_for_status()
	decoded_image_upload_response = image_upload_response.json()
	return decoded_image_upload_response


def save_image(decoded_image_upload_response, group_id, access_token, api_version=5.131):
	image_parameters = {
		'access_token': access_token,
        'server': decoded_image_upload_response['server'],
        'photo': decoded_image_upload_response['photo'],
        'hash': decoded_image_upload_response['hash'],
        'group_id': group_id,
		'v': api_version
		
    }
	image_save_response = requests.post(
        'http://api.vk.com/method/photos.saveWallPhoto',
        params=image_parameters)
	check_vk_response(image_save_response)
	image_save_response.raise_for_status()
	decoded_image_save_response = image_save_response.json()
	return decoded_image_save_response["response"][0]["owner_id"], decoded_image_save_response["response"][0]["id"]


def post_image(owner_id, id, group_id, comment, access_token, image_number_to_post, api_version=5.131):
    image_post_parameters = {
		'access_token': access_token,
        'owner_id': f'-{group_id}',
        'from_group': 1,
        'message': comment,
        'attachments': f'photo{owner_id}_'
                       f'{id}',
		'v': api_version
    }
    requests.post('http://api.vk.com/method/wall.post',
                  params=image_post_parameters)
    os.remove(f'image_{image_number_to_post}.png')


def main():
	load_dotenv()
	access_token = os.environ['VK_ACCESS_TOKEN']
	group_id = os.environ['VK_GROUP_ID']
	image_number_to_post = get_random_image()
	comment = download_image(image_number_to_post)
	upload_link = get_link_to_upload(group_id, access_token, image_number_to_post)
	upload_data = upload_image(image_number_to_post, upload_link)
	owner_id, id = save_image(upload_data, group_id, access_token)
	post_image(owner_id, id, group_id, comment, access_token, image_number_to_post)


if __name__ == "__main__":
    main()
