from imhide.crypto import generate_key, encrypt, decrypt


def test_crypto():
    key = generate_key()
    raw = b"Hello, world!"
    token = encrypt(raw, key)
    data = decrypt(token, key)

    assert data == raw


if __name__ == "__main__":
    test_crypto()
