from dotenv import load_dotenv
import requests
import os
import list_util

# Access secret keys saved in .env file
load_dotenv()
CAT_API_KEY = os.getenv('CAT_API_KEY')

def get_cats(breed, no_of_photos, is_gif):
    breed = '' if breed == 'all' else breed
    mime_types = 'gif' if is_gif else 'jpg,png'
    return requests.get(f'https://api.thecatapi.com/v1/images/search?api_key{CAT_API_KEY}&limit={no_of_photos}&breed_id={breed}&mime_types={mime_types}').json()

def get_cat_breeds():
    return requests.get(f'https://api.thecatapi.com/v1/breeds?api_key{CAT_API_KEY}').json()

def get_cat_breed_id_from_name(name):
    if (name == 'All of them!'):
        return 'all'

    cat_breeds_json = get_cat_breeds()
    cat_breed_name_list = list(map(lambda cat_breed_object : cat_breed_object['name'], cat_breeds_json))
    cat_index = list_util.binary_search(name, cat_breed_name_list)
    return cat_breeds_json[cat_index]['id']

def get_cat_breed_from_breed_id(breed_id):
    if (breed_id == 'all'):
        return 'All of them!'

    cat = get_cats(breed_id, '1', False)
    return cat[0]['breeds']['name']
