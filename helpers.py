import requests
from io import open as iopen
from urllib.parse import urlsplit


def requests_image(file_url, file_name):
    suffix_list = ['jpg', 'gif', 'png', 'tif', 'svg']
    try:
        file_suffix = urlsplit(file_url)[2].split('/')[-1].split('.')[1]
    except IndexError:
        file_suffix = 'jpg'
    i = requests.get(file_url)
    file_name = file_name + "." + file_suffix
    if file_suffix in suffix_list and i.status_code == requests.codes.ok:
        with iopen(file_name, 'wb') as file:
            file.write(i.content)
    else:
        print("land")
        return False
