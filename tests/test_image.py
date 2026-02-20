from pathlib import Path
from io import BytesIO

import requests
from PIL import Image

from imhide.crypto import generate_key
from imhide.image_codec import create_encoded_image, get_decoded_image


def _load_image(w: int, h: int) -> bytes:
    url = f"https://picsum.photos/seed/imhide/{w}/{h}"
    response = requests.get(url)
    image_data = BytesIO(response.content)

    image = Image.open(image_data).convert("RGBA")
    data = image.tobytes()

    return data


def test_simple():
    key = generate_key()
    img_pth = Path("simple.png")

    w = 42
    h = 30
    original = _load_image(w, h)
    create_encoded_image(key, original, encoded_file_pth=img_pth, target_bin_token=5266)
    print("Encoded image created")

    new_img_pth = Path("decoded.png")
    decoded = get_decoded_image(key, img_pth)

    image = Image.frombytes(mode="RGBA", data=decoded, size=(w, h))

    with open(new_img_pth, "wb") as f:
        image.save(f)
    print("Decoded image created")


def test_medium():
    key = generate_key()
    img_pth = Path("medium.png")

    w = 400
    h = 250
    original = _load_image(w, h)
    create_encoded_image(key, original, encoded_file_pth=img_pth, target_bin_token=403430)
    print("Encoded image created")

    new_img_pth = Path("decoded.png")
    decoded = get_decoded_image(key, img_pth)

    image = Image.frombytes(mode="RGBA", data=decoded, size=(w, h))

    with open(new_img_pth, "wb") as f:
        image.save(f)
    print("Decoded image created")


def test_big():
    key = generate_key()
    img_pth = Path("big.png")

    w = 1024
    h = 768
    original = _load_image(w, h)
    create_encoded_image(key, original, encoded_file_pth=img_pth, target_bin_token=3162914)
    print("Encoded image created")

    new_img_pth = Path("decoded.png")
    decoded = get_decoded_image(key, img_pth)

    image = Image.frombytes(mode="RGBA", data=decoded, size=(w, h))

    with open(new_img_pth, "wb") as f:
        image.save(f)
    print("Decoded image created")


if __name__ == "__main__":
    # test_big()
    test_medium()
    # test_simple()
