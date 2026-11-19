import base64
import random


class RSAKeyGenerator:
    __p = 0
    __q = 0
    __n = 0
    __euler = 0
    __pub_exp = 0
    __pr_exp = 0

    def __is_prime(self, n: int) -> bool:
        """Возвращает True, если n — простое число."""
        if n < 2:
            return False
        if n < 4:
            return True
        if n % 2 == 0:
            return False
        d = 3
        while d * d <= n:
            if n % d == 0:
                return False
            d += 2
        return True

    def __check_size(self, a: int, b: int) -> None:
        if a.bit_length() != b.bit_length():
            raise ValueError("Числа p и q должны быть одного размера")

    def __init__(self, p: int, q: int) -> None:
        self.__check_size(p, q)
        self.p = p
        self.q = q
        self.n = self.p * self.q

    @property
    def p(self) -> int:
        return self.__p

    @p.setter
    def p(self, new_p: int):
        if not self.__is_prime(new_p):
            raise ValueError("Число p должно быть простым!")
        self.__p = new_p

    @property
    def q(self) -> int:
        return self.__q

    @q.setter
    def q(self, new_q: int):
        if not self.__is_prime(new_q):
            raise ValueError("Число q должно быть простым!")
        self.__q = new_q

    @property
    def n(self) -> int:
        return self.__n

    @n.setter
    def n(self, new_n: int) -> None:
        self.__n = new_n

    def __calculate_euler(self) -> None:
        self.__euler = (self.p - 1) * (self.q - 1)

    @staticmethod
    def are_numbers_coprime(a: int, b: int) -> bool:
        while b:
            a, b = b, a % b
        return a == 1

    @staticmethod
    def __extended_gcd(a: int, b: int):
        """Расширенный алгоритм Евклида: возвращает (g, x, y), где a*x + b*y = g."""
        if b == 0:
            return a, 1, 0
        g, x1, y1 = RSAKeyGenerator.__extended_gcd(b, a % b)
        return g, y1, x1 - (a // b) * y1

    def __generate_public_key(self):
        self.__calculate_euler()
        while True:
            candidate = random.randrange(2, self.__euler)
            if not self.are_numbers_coprime(candidate, self.__euler):
                continue
            if (candidate * candidate) % self.__euler == 1:
                continue
            self.__pub_exp = candidate
            return

    def __generate_private_key(self):
        if self.__pub_exp == 0:
            raise ValueError("Сначала нужно задать public_key")

        g, x, _ = self.__extended_gcd(self.__pub_exp, self.__euler)
        if g != 1:
            raise ValueError("e и euler(n) не взаимно просты")

        self.__pr_exp = x % self.__euler

    def public_key(self):
        self.__generate_public_key()
        return self.__pub_exp, self.__n

    def private_key(self):
        self.__generate_private_key()
        return self.__pr_exp, self.__n

    def encrypt(self, m: int) -> int:
        if not (0 <= m < self.__n):
            raise ValueError("Сообщение должно быть в диапазоне [0, n)")
        return pow(m, self.__pub_exp, self.__n)

    def decrypt(self, c: int) -> int:
        return pow(c, self.__pr_exp, self.__n)

    def encrypt_message(self, message: str) -> str:
        encrypted_msg = "".join([chr(self.encrypt(ord(c))) for c in message])
        return base64.b64encode(encrypted_msg.encode("utf-8")).decode("ascii")

    def decrypt_message(self, encrypted_message: str) -> str:
        decoded_msg = base64.b64decode(encrypted_message).decode("utf-8")
        return "".join([chr(self.decrypt(ord(c))) for c in decoded_msg])
