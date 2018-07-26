import hug
from helpers import requests_image
from models import Child
from facial_search import facial_search
import os

api = hug.API(__name__)
api.http.add_middleware(hug.middleware.CORSMiddleware(api, max_age=10))


@hug.post('/create-missing')
def create_missing(body):
    """accepts file uploads"""
    # <body> is a simple dictionary of {filename: b'content'}
    child = Child()
    child_id = Child.generate_id()
    child.phone_number = body["phoneNumber"]
    child.child_id = child_id
    child.image_url = body["imageUrl"]
    child.child_name = body["childName"]
    child.guardian_name = body["guardianName"]
    child.image_path = "images/" + str(child_id)
    requests_image(body["imageUrl"], "images/" + str(child_id))
    try:
        child.save()
    except Exception as e:
        print(e)
    return {'child_id': child_id}, 200


@hug.post('/find-missing')
def find_missing(body):
    known_image_url = body["imageUrl"]
    random_id = Child.generate_id()
    image_path = "temp/" + random_id
    requests_image(known_image_url, image_path)
    facial_search_result, status = facial_search(image_path)
    if os.path.exists(image_path):
        os.remove(image_path)
    else:
        print("The file does not exists")
    return {
        'status': status,
        'result': facial_search_result
    }


@hug.get('/missing-children/{page_number}')
def missing_children(page_number: int):
    children_data = []
    start = (page_number - 1) * 10
    end = page_number * 10
    next_page = '/missing_children/' + str(page_number + 1)
    children = Child.objects[start: end]
    for child in children:
        children_data.append({
            'child_id': child['child_id'],
            'child_name': child['child_name'],
            'age': child['age'],
            'place_of_missing': child['place_of_missing'],
            'guardian_name': child['guardian_name'],
            'image_url': child['image_url'],
            'phone_number': child['phone_number']
        })
    return {
        'children': children_data,
        'next': next_page
    }
