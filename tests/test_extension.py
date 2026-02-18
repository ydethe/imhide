from imhide import logger
from imhide.ErrorCorrectingCode import ErrorCorrectingCode


def test_ecc():
    ecc = ErrorCorrectingCode()

    msg = b"hello world"
    enc = ecc.encode(msg)
    enc[5] = ord("w")

    decoded_msg = ecc.decode(enc)
    print(decoded_msg)

    assert decoded_msg == msg

    print(len(msg), len(enc))
    logger.debug("debug poney")


if __name__ == "__main__":
    test_ecc()
