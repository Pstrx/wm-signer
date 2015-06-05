import hashlib

from os.path import isfile
from random import randint
from struct import Struct, pack, error as StructException


class SignerException(Exception):
    pass


class Signer:

    power = None
    modulus = None

    def __init__(self, wmid, keys, passwd):
        if not wmid or not passwd:
            raise SignerException('WMID и/или пароль от файла ключей '
                                  'не задан.')

        self.wmid = wmid
        self.passwd = passwd

        if not isfile(keys):
            raise SignerException('Файл ключей не найден: %s' % keys)

        try:
            with open(keys, 'rb') as f:
                self.read_key_data(f.read())
        except IOError:
            raise SignerException('Ошибка чтения из файла ключей.')

    def sign(self, data):
        """
        Создание подписи для данных.
        """

        # Создание хэша для данных (16 байт)
        base = self.md4(data)

        # Добавим 40 рандомных байт
        for _ in range(0, 10):
            base += pack('<L', randint(0, 65535))

        # Добавляем длину базы (56 = 16 + 40) как первые 2 байта
        base = pack('<H', len(base)) + base

        # Модульное возведение в степень
        dec = pow(self.reverse_to_decimal(base), self.power, self.modulus)

        # Преобразование в шестнадцатеричное представление
        hexa = '{0:x}'.format(dec)

        # Заполнение пустых байтов нулями
        hexa = '0' * (132 - len(hexa)) + hexa

        # Отратный порядок байт
        hex_reversed = ''
        for i in range(0, len(hexa) // 4):
            mul = i * 4
            hex_reversed = hexa[mul:mul + 4] + hex_reversed

        return hex_reversed.lower()

    def read_key_data(self, binary):
        """
        Чтение данных из файла ключей.
        """

        size, data = self.unpack(binary, '< H H 16s L', without_size=False)
        payload = {
            'reversed': data[0],
            'signFlag': data[1],
            'hash': data[2],
            'length': data[3],
            'buffer': binary[size:]
        }

        data = self.read_key_buffer(payload)
        if data is None:
            raise SignerException('Проверка хэша не удалась. '
                                  'Возможно, файл ключей поврежден.')

        self.sign_vars(data)

    def sign_vars(self, buff):
        """
        Инициализация `power` и `modulus`.
        """

        _, power_len = self.unpack(buff, '< L H')
        _, _, power, mod_len = self.unpack(buff, '< L H %ds H' % power_len)
        _, _, _, _, modulus = self.unpack(buff, '< L H %ds H %ds'
                                          % (power_len, mod_len))

        self.power = self.reverse_to_decimal(power)
        self.modulus = self.reverse_to_decimal(modulus)

    def read_key_buffer(self, data):
        """
        Проверить и вернуть буфер ключей.
        """

        data['buffer'] = self.encrypt_key(data['buffer'])

        return data['buffer'] if self.verify_hash(data) else None

    def encrypt_key(self, buff):
        """
        Шифрование ключа, используя хэш WMID + PASSWD.
        """

        digest = self.md4(self.wmid + self.passwd)

        return self.xor_strings(list(buff), list(digest), 6)

    def verify_hash(self, data):
        """
        Проверка хэша ключа.
        """

        verify = pack('<H', data['reversed']) + pack('<H', 0) + \
                 pack('<4L', 0, 0, 0, 0) + pack('<L', data['length']) + \
                 data['buffer']

        return self.md4(verify) == data['hash']

    @staticmethod
    def xor_strings(subject, modifier, shift=0):
        """
        Операция XOR для двух строк.
        """

        i, j = shift, 0
        while len(subject) > i:
            subject[i] = subject[i] ^ modifier[j]
            i += 1
            j += 1
            if j >= len(modifier):
                j = 0

        return bytearray(subject)

    @staticmethod
    def reverse_to_decimal(value):
        """
        Преобразование двоичных данных в десятичную форму.
        """

        return int.from_bytes(value, byteorder='little')

    @staticmethod
    def md4(value):
        """
        Хэширование строки алгоритмом MD4, который содержится в модуле OpenSSL.
        """

        algorithm = hashlib.new('md4')

        if isinstance(value, bytes):
            algorithm.update(value)
        else:
            algorithm.update(str.encode(value))

        return algorithm.digest()

    @staticmethod
    def unpack(binary, fmt, without_size=True):
        """
        Получение данных из их бинарного представления.
        """

        s = Struct(fmt)

        try:
            unpacked = s.unpack(binary[:s.size])
        except StructException:
            raise SignerException('Ошибка при распаковке данных. '
                                  'Возможно файл ключей поврежден.')

        if without_size:
            return unpacked
        else:
            return s.size, unpacked
