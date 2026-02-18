import requests
from io import BytesIO

from PIL import Image
from pyturbocode.TurboCodec import TurboCodec
from imhide.crypto import generate_key, encrypt


def _load_image() -> bytes:
    url = "https://picsum.photos/seed/imhide/1024/768"
    response = requests.get(url)
    image_data = BytesIO(response.content)

    # with open("output.jpg", "wb") as f:
    #     f.write(image_data.getbuffer())

    image = Image.open(image_data).convert("RGBA")
    data = image.tobytes()

    return data


def test_image():
    key = generate_key()
    codec = TurboCodec()

    data = _load_image()

    token = encrypt(data, key)
    enc = codec.encode(token)
    print(len(enc))


if __name__ == "__main__":
    test_image()
