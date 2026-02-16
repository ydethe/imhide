from imhide import logger
from imhide.ErrorCorrectingCode import ErrorCorrectingCode


def test_ecc():
    ecc = ErrorCorrectingCode()

    msg = b"hello world"
    enc = ecc.encode(msg)
    decoded_msg = ecc.decode(enc)
    assert decoded_msg == msg

    print(len(msg), len(enc))
    logger.debug("debug poney")


if __name__ == "__main__":
    test_ecc()
