from setuptools import setup

setup(
    name='Syneto',
    version='1.0.0',
    packages=['syneto_translate'],
    url='',
    license='',
    author='Raul Maier',
    author_email='maierraul96@gmail.com',
    description='This is the test for Syneto interview',
    entry_points = {
        'console_scripts': [
            'gtd=syneto_translate.daemon_process:main',
            'gtranslate=syneto_translate.client:main'
        ],
    }
)
