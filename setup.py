from distutils.core import setup

setup(
    name='wm-signer',
    version='0.1',
    description='WebMoney Signer',
    author='Egor Smolyakov',
    author_email='egorsmkv@gmail.com',
    license='MIT',
    url='https://github.com/eg0r/wm-signer',
    packages=['wm_signer'],
    install_requires=['passlib'],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

