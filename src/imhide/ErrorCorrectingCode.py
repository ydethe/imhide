import typing as T
from reedsolo import RSCodec


class ErrorCorrectingCode(object):
    def __init__(self):
        self.__rsc = RSCodec(10)  # 10 ecc symbols

    def encode(self, data: bytes) -> bytes:
        enc = self.__rsc.encode(data)
        return enc

    def decode(self, enc: bytes) -> bytes:
        decoded_msg, decoded_msgecc, errata_pos = self.__rsc.decode(enc)
        return decoded_msg
