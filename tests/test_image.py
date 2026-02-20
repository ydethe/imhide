import base64
from pathlib import Path
from io import BytesIO

import requests

from PIL import Image
import pypccc
from struct import pack, unpack

from imhide.crypto import decrypt, generate_key, encrypt


def _load_image() -> bytes:
    url = "https://picsum.photos/seed/imhide/1024/768"
    response = requests.get(url)
    image_data = BytesIO(response.content)

    image = Image.open(image_data).convert("RGBA")
    data = image.tobytes()

    return data


def create_encoded_image(key: bytes, data: bytes, encoded_file_pth: Path):
    # (n=bin_token size)
    # n	K	R	C	C2	p	q	ratio
    # 3162914	4	1.461538462	3724	13868176	1862	1274	1.00543995

    p = 1862
    q = 1274
    token = encrypt(data, key)
    b64_token = base64.urlsafe_b64decode(token)
    n_tkn = len(b64_token)
    n_pad = 3162914 - n_tkn - 8
    bin_token = pack("<Q", n_tkn) + b64_token + b"\x00" * n_pad
    enc = pypccc.rs_encode(bin_token)

    image = Image.frombytes(mode="RGBA", data=enc, size=(p, q))

    with open(encoded_file_pth, "wb") as f:
        image.save(f)


def get_decoded_image(key: bytes, encoded_file_pth: Path):
    with open(encoded_file_pth, "rb") as f:
        image = Image.open(f).convert("RGBA")
    enc = image.tobytes()
    bin_token = pypccc.rs_decode(enc)
    n_tkn = unpack("<Q", bin_token[:8])[0]
    token = base64.urlsafe_b64encode(bin_token[8 : 8 + n_tkn])
    decoded_data = decrypt(token, key)
    return decoded_data


def test_image():
    img_pth = Path("output.png")
    key = generate_key()

    original = _load_image()
    create_encoded_image(key, original, encoded_file_pth=img_pth)
    print("Encoded image created")

    # new_img_pth = Path("decoded.png")
    # decoded = get_decoded_image(key, img_pth)

    # image = Image.fromarray(decoded.astype("uint8"), "RGB")

    # with open(new_img_pth, "wb") as f:
    #     image.save(f)
    # print("Decoded image created")


if __name__ == "__main__":
    test_image()
