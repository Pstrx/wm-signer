### WebMoney Signer `0.1`

Модуль, который создаёт подписи с использованием файла ключей WebMoney Keeper Classic.

> Предназначен для взаимодействия с программными [X-интерфейсами](http://www.webmoney.ru/rus/developers/api.shtml) WebMoney,
> [XML-интерфейсами](http://wm.exchanger.ru/asp/rules_xml.asp) WebMoney Exchanger и др.

*На данный момент поддерживается третья версия Python.*

#### Пример использования

```python
from wm_signer.signer import Signer

if __name__ == '__main__':
    signer = Signer(wmid='000000000000',
                    keys='./data/000000000000.kwm',
                    passwd='************')

    signature = signer.sign('Данные, которые будут подписаны.')
    print(signature)
```

#### Установка

* Через **pip**:
  ```shell
  [sudo] pip install wm-signer
  ```

* Из репозитория:

  ```shell
  git clone https://github.com/eg0r/wm-signer
  cd wm-signer-master
  [sudo] python setup.py install
  ```

**Файл ключей должен быть резервным, а не основным.**

#### Ошибки

Пожалуйста, сообщите, если обнаружите ошибку в библиотеке.