from setuptools import setup

setup(
    name='Syneto',
    version='1.1.0',
    packages=[
        'src',
        'src.client',
        'src.daemon',
        'src.utils',
    ],
    url='',
    license='',
    author='Raul Maier',
    author_email='maierraul96@gmail.com',
    description='This is the test for Syneto interview',
    entry_points={
        'console_scripts': [
            'gtd=src.daemon.daemon_process:start_daemon',
            'gtranslate=src.client.client:main'
        ],
    },
    install_requires = [
        "setuptools~=51.0.0",
        "click~=8.0.4",
        "lockfile~=0.12.2",
        "google-cloud-translate~=3.7.1",
        "python-dotenv~=0.19.2",
        "ratemate~=0.1.0",
    ]
)
