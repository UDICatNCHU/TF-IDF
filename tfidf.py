import jieba, json, multiprocessing, threading, re, pymongo
from sklearn.feature_extraction.text import TfidfTransformer  
from sklearn.feature_extraction.text import CountVectorizer  
from sklearn.feature_extraction.text import TfidfVectorizer  
jieba.load_userdict('dictionary/dict.txt.big.txt')
jieba.load_userdict("dictionary/NameDict_Ch_v2")
queueLock = threading.Lock()
result = []
with open('wiki.txt.trad', 'r', encoding='utf-8') as f:
    text = f.read()
    text = re.findall(r'\<doc.+?>(.+?)\<\/doc\>', text, re.S)
         
def sentenct2terms():
    tmp = []
    while True:
        queueLock.acquire()
        if text:
            i = text.pop()
            queueLock.release()                
        else:
            queueLock.release()
            break

        tmp.append(jieba.lcut(i))

    queueLock.acquire()
    result.extend(tmp)
    queueLock.release()
if __name__ == "__main__":  
    workers = [threading.Thread(target=sentenct2terms, name=str(i)) for i in range(multiprocessing.cpu_count())]
    for thread in workers:
       thread.start()

    # Wait for all threads to complete
    for thread in workers:
        thread.join()

    with open('wiki.json', 'w') as f:
        corpus = []
        for i in result:
            tmp = ''
            for j in i:
                tmp += j + ' '
            corpus.append(tmp)
        json.dump(corpus, f)
    
    # calculate idf
    X = vectorizer.fit_transform(corpus)
    idf = vectorizer.idf_
    result = [{'key':key, 'value':value} for key, value in zip(vectorizer.get_feature_names(), idf)]

    # insert 2 mongoDB
    client = pymongo.MongoClient(None)['nlp']
    Collect = client['idf']
    Collect.insert(result)
    Collect.create_index([("key", pymongo.HASHED)])