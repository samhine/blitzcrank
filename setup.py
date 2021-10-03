from setuptools import setup, find_packages

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='blitzcrank',
    packages=find_packages(),
    version='0.0.3',
    license='MIT',
    description='The Riot API in Python, made easy.',
    author='Samuel Hine',
    author_email='sam.hine27@gmail.com',
    url='https://github.com/samhine/blitzcrank',
    download_url='https://github.com/samhine/blitzcrank/archive/refs/tags/0.0.3.tar.gz',
    keywords=['PYTHON', 'RIOT', 'API'],
    install_requires=[
        'responses',
        'requests',
        'roleml',
        'pandas',
        'ratelimit'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
    long_description_content_type='text/markdown',
    long_description=long_description,
)
