from distutils.core import setup

setup(
    name = 'udicTfidf',
    packages=['udicTfidf'],
    package_dir={'udicTfidf':'udicTfidf'},
    package_data={'udicTfidf':['management/commands/*']},
    version = '1.1',
    description = 'A django App for udicTfidf',
    author = ['davidtnfsh'],
    author_email = 'davidtnfsh@gmail.com',
    url = 'https://github.com/udicatnchu/tf-idf',
    download_url = 'https://github.com/udicatnchu/tf-idf',
    keywords = ['udicTfidf', 'tf-idf'],
    classifiers = [],
    license='GPL3.0',
    install_requires=[
        'sklearn',
        'numpy',
        'scipy',
        'pymongo',
        'udicOpenData',
        'jieba'
    ],
    zip_safe=True,
)
