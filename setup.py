from distutils.core import setup

setup(
    name = 'Tfidf',
    packages=['Tfidf'],
    package_dir={'Tfidf':'Tfidf'},
    package_data={'Tfidf':['management/commands/*']},
    version = '0.1',
    description = 'A django App for Tfidf',
    author = ['davidtnfsh'],
    author_email = 'davidtnfsh@gmail.com',
    url = 'https://github.com/udicatnchu/tf-idf',
    download_url = 'https://github.com/udicatnchu/tf-idf',
    keywords = ['Tfidf', 'tf-idf'],
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
