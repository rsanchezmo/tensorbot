from setuptools import setup, find_packages


setup(
    name='tensorbot',
    version='1.0.0',
    description='A bot to send Tensorboard training or testing plots to Telegram',
    url='https://github.com/rsanchezmo/tensorbot',
    author='Rodrigo Sanchez Molina',
    author_email='rsanchezm98@gmail.com',
    license='Apache 2.0',
    install_requires=[
            "requests",
            "matplotlib",
            "tbparse"
    ]
)
