### WebMoney Signer `0.2`

https://wiki.wmtransfer.com/projects/webmoney/wiki/WMSigner

*Python 2/3*

#### Example

```python
from wm_signer.signer import Signer

if __name__ == '__main__':
    signer = Signer(wmid='000000000000',
                    keys='./data/000000000000.kwm',
                    passwd='************')

    signature = signer.sign('data')
    print(signature)
```