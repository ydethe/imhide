from reedsolo import RSCodec


class ErrorCorrectingCode(object):
    def __init__(self):
        self.__rsc = RSCodec(
            nsym=10, nsize=255, fcr=0, prim=0x11D, generator=2, c_exp=8, single_gen=True
        )

    def encode(self, data: bytes) -> bytes:
        enc = self.__rsc.encode(data)
        return enc

    def decode(self, enc: bytes) -> bytes:
        decoded_msg, decoded_msgecc, errata_pos = self.__rsc.decode(enc)
        return decoded_msg
