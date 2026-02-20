import base64
from struct import pack, unpack
from typing import Tuple
from pathlib import Path

import pypccc
from PIL import Image

from .crypto import encrypt, decrypt


def compute_encoded_size(target_bin_token: int) -> Tuple[int, int]:
    # (n=bin_token size)
    # n	K	R	C	C2	p	q
    # 3162914	4	1.461538462	3724	13868176	1862	1274
    # 5266	4	1.461538462	152	23104	76	52
    # 403430	4	1,46153846153846	1330	1768900	665	455

    p = -1
    q = -1
    if target_bin_token == 3162914:
        p = 1862
        q = 1274
    elif target_bin_token == 5266:
        p = 76
        q = 52
    elif target_bin_token == 403430:
        p = 665
        q = 455
    else:
        ValueError(target_bin_token)
    return p, q


def encode_payload(key: bytes, data: bytes, nbytes: int) -> bytes:
    token = encrypt(data, key)
    b64_token = base64.urlsafe_b64decode(token)
    n_tkn = len(b64_token)
    n_pad = nbytes - n_tkn - 8
    bin_token = pack("<Q", n_tkn) + b64_token + b"\x00" * n_pad
    enc = pypccc.rs_encode(bin_token)
    return enc


def decode_payload(key: bytes, enc: bytes) -> bytes:
    bin_token = pypccc.rs_decode(enc)

    n_tkn = unpack("<Q", bin_token[:8])[0]

    token = base64.urlsafe_b64encode(bin_token[8 : 8 + n_tkn])

    decoded_data = decrypt(token, key)

    return decoded_data


def create_encoded_image(key: bytes, data: bytes, encoded_file_pth: Path, target_bin_token: int):

    # p = 1862
    # q = 1274
    enc = encode_payload(key, data, nbytes=target_bin_token)

    p, q = compute_encoded_size(target_bin_token)
    image = Image.frombytes(mode="RGBA", data=enc, size=(p, q))

    with open(encoded_file_pth, "wb") as f:
        image.save(f)


def get_decoded_image(key: bytes, encoded_file_pth: Path):
    with open(encoded_file_pth, "rb") as f:
        image = Image.open(f).convert("RGBA")
    enc = image.tobytes()

    decoded_data = decode_payload(key, enc)

    return decoded_data
