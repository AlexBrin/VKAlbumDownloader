import re
import json
import urllib.request
import httplib2
import sys
import os

def req(groupId, albumId):
    data = ["v=5.73", "owner_id=" + groupId, "album_id=" + albumId,\
            "photo_sizes=1", "count=1000"]
    data = "&".join(data)
    
    h = httplib2.Http(".cache")
    url = "https://api.vk.com/method/photos.get?" + data
    res, content = h.request("https://api.vk.com/method/photos.get?" + data, "GET")
    return json.loads(content.decode("utf8"))

def savePhoto(url, path):
    file = url.split('/').pop()
    h = httplib2.Http('.cache')
    response, content = h.request(url)
    file = open(path + "/" + file, 'wb')
    file.write(content)
    file.close()

def findMaxSize(sizes):
    m = 0
    current = False
    for photo in sizes:
        if photo['width'] >= m:
            m = photo['width']
            current = photo['src']
    return current


if len(sys.argv) < 3:
    print("Нужно использовать 2 аргумента: ссылка на альбом и название")
    exit(0)

url = sys.argv[1]
path = sys.argv[2]

os.mkdir(path)
print("Создал директорию. Начинаю загрузку...")

url = re.search("album([\-\d]+)_(\d+)", url)
groupId = url.group(1)
albumId = url.group(2)

photos = req(groupId, albumId)
for photo in photos['response']['items']:
    urlPhoto = findMaxSize(photo['sizes'])
    savePhoto(urlPhoto, path)

print("Загружено")
