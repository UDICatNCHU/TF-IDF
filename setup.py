from distutils.core import setup

setup(
    name = 'tfidf',
    packages=['tfidf'],
    package_dir={'tfidf':'tfidf'},
    package_data={'tfidf':['management/commands/*']},
    version = '0.1',
    description = 'A django App for tfidf',
    author = ['davidtnfsh'],
    author_email = 'davidtnfsh@gmail.com',
    url = 'https://github.com/udicatnchu/tf-idf',
    download_url = 'https://github.com/udicatnchu/tf-idf',
    keywords = ['tfidf', 'tf-idf'],
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
