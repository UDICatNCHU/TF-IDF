# udicTfidf
用Wikipedia所有語料所計算出來的TF-IDF自動化腳本，變成django app放在實驗室的api上供大家query

## Get Started

### Prerequisities

Ubuntu需要先安裝：

`sudo pip install virtualenv`

## Installing

1. `pip install udicTfidf`

## Run
#### Building the model  
必須先用wikiExtract取得wiki文檔

> 1. 必須先用wikiExtract取得wiki文檔： `wikiExtract.py ...`
> 2. Build：`python3 manage.py buildTfidf --file wiki.txt.trad `

1. command:
```
usage: manage.py buildTfidf  [--file file]
```
* args:
  * file: wiki文檔 or Other文檔

#### Usage of udicTfidf class  
因為udicTfidf是一個django的函式庫，所以需要設定urls.py以及vies.py  
並且在settings.py INSTALLED_APPS 新增udicTfidf喔

1. settings.py：
  ```
  INSTALLED_APPS = [
      'udicTfidf'
       ...
  ]
  ```
2. urls.py：  
在專案的urls.py引入函式庫的urls.py即可使用該api  
  ```
  import udicTfidf.urls
  urlpatterns += [
      url(r'^tfidf/', include(udicTfidf.urls))
  ]
  ```


## API
1. 取得字的idf：_`/tfidf/idf`_
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