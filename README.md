# udicTfidf

A TF-IDF model using Wikipedia corpus

## Installing

* (Recommended): Use [docker-compose](https://github.com/udicatnchu/udic-nlp-api) to install

## Manually Install

If you want to integrate `udicTfidf` into your own django project, use manually install.

* `pip install udicTfidf`

### Config

1. add django app `udicTfidf` in `settings.py`：

  ```
  INSTALLED_APPS = [
      'udicTfidf'
       ...
  ]
  ```
2. add url patterns of udicTfidf into `urls.py`：

  ```
  import udicTfidf.urls
  urlpatterns += [
      url(r'^tfidf/', include(udicTfidf.urls))
  ]
  ```
3. use `python3 manage.py buildTfidf --lang <lang, e.g., zh or en or th> ` to build model of kcm.

4. fire `python manage.py runserver` and go `127.0.0.1:8000/` to check whether the config is all ok.

## API

1. get idf：_`/tfidf/idf`_
  - keyword
  - example：[http://udiclab.cs.nchu.edu.tw/tfidf/idf?keyword=中興大學](http://udiclab.cs.nchu.edu.tw/tfidf/idf?keyword=中興大學)

  ```
  {
    value: 9.857856840334222
  }
  ```

2. calculate tf-idf of an article：_`/tfidf/tfidf`_
  - flag: You can specify specific part of speech. (default will return all kind of part of speech)
  - example： 
  ```
  import requests
  doc = '''
  正義聯盟🦇⚡️
  這部期待已久的年度大片不專業影評來啦
  特地等這部片上映將近兩週才發影評～相信大部分的人都已經看過啦～所以接下來就專心被我爆雷和我一起討論吧
  畢竟這是年度大片！所以以下影評將會非常的長篇大論在討論這部電影～請耐心的看完喲
  以下有超級重雷 請小心服用'''
  requests.post("http://udiclab.cs.nchu.edu.tw/tfidf/tfidf?flag=n", {"doc":doc}).json()
  ```

    ```
    [
      ["影評", 17.310233324173833  ],
      ["重雷", 14.0846905856024  ],
      ["這部", 13.02391863750646  ],
      ["爆雷", 12.986078296934291  ],
      ["大片", 12.11062567904188  ],
      ["長篇大論", 11.064265699458039  ],
      ["期待已久", 10.618954682802675  ],
      ["正義聯盟", 10.041639317767851  ],
      ["討論", 9.2563143039489  ],
    ]
    ```

## Built With

python3.5

## Contributors
* __張泰瑋__ [david](https://github.com/david30907d)

## License

This package use `GPL3.0` License.