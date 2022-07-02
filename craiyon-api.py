import requests
import base64
import io
from PIL import Image

def make_req(prompt):

    headers = {
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "pragma": "no-cache",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1",
        "Referer": "https://www.craiyon.com/",
        "Referrer-Policy": "strict-origin-when-cross-origin"
      }
    body = {'prompt': prompt}
    r = requests.post("https://backend.craiyon.com/generate", json=body, headers=headers )
    images = r.json()['images']
    ims = [Image.open(io.BytesIO(base64.b64decode(i))) for i in images]
    return ims

def make_grid(imgs):
    w, h = imgs[0].size
    grid = Image.new('RGB', size=(3*w, 3*h))
    for i, img in enumerate(imgs):
        grid.paste(img, box=(i%3*w, i//3*h))
    return grid


def generate(prompt):
    images = make_req(prompt)
    return make_grid(images)
