import numpy as np
from commpy.channelcoding import Trellis, turbo


class ErrorCorrectingCode(object):
    def __init__(self):
        memory = np.array([2])  # constraint length = 3
        g_matrix = np.array([[7, 5]])  # generator polynomials (octal)

        self.__trellis = Trellis(memory, g_matrix)

    def encode(self, data: bytes) -> bytes:
        N = len(data)
        interleaver = np.random.permutation(N)
        arr = np.frombuffer(data, dtype=np.uint8)
        print(arr.shape)

        sys_bits, parity1, parity2 = turbo.turbo_encode(
            arr, self.__trellis, self.__trellis, interleaver
        )
        coded_bits = np.concatenate([sys_bits, parity1, parity2])

        return coded_bits

    def decode(self, enc: bytes, num_iter: int = 6) -> bytes:
        N = len(enc)
        rx_sys = enc[0:N]
        rx_par1 = enc[N : 2 * N]
        rx_par2 = enc[2 * N : 3 * N]

        decoded_bits = turbo.turbo_decode(
            rx_sys, rx_par1, rx_par2, self.__trellis, self.__trellis, num_iter, self.__interleave
        )

        decoded_bits = decoded_bits.astype(int)

        return decoded_bits
