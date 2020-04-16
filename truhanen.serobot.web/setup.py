
from setuptools import setup, find_namespace_packages


# TODO Build the web frontend


setup(
    name='truhanen.serobot.web',
    version='0.1.0',
    author='Tuukka Ruhanen',
    author_email='tuukka.t.ruhanen@gmail.com',
    description='Web server & UI for controlling a Raspberry Pi robot.',
    install_requires=[
        # Serobot API
        'truhanen.serobot.api',
        # Web server
        'aiohttp',
        'aiohttp_security',
        'aiohttp_session',
        'cryptography',
    ],
    packages=find_namespace_packages(),
    scripts=[
        'scripts/start_serobot_server',
    ],
    zip_safe=False,
)
