import json, multiprocessing, threading, re, pymongo, sys, math, jieba
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from udicOpenData.stopwords import rmsw

class TFIDF(object):
    """docstring for TFIDF"""
    def __init__(self, uri=None):
        self.queueLock = threading.Lock()
        self.corpus = []
        self.IdfList = []
        self.text = ''
        self.Collect = pymongo.MongoClient(uri)['nlp']['idf']
        
    # 輸入一篇文章，計算出個字詞的tf-idf
    def tfidf(self, doc):
        vectorizer = CountVectorizer()
        doc = [' '.join(rmsw(doc))]
        freq = vectorizer.fit_transform(doc).toarray()[0]
        tf = {key:freq[index] for key, index in vectorizer.vocabulary_.items()}
        result = {}
        for i in tf:
            cursor = self.Collect.find({'key':i}).limit(1)
            if cursor.count():
                result[i] = (1+math.log(tf[i])) * dict(list(cursor)[0])['value']
        return sorted(result.items(), key=lambda x:-x[1])

    # output字詞idf
    def idf(self, keyword):
        cursor = self.Collect.find({'key':keyword}, {'value':1, '_id':False}).limit(1)
        if cursor.count():
            return cursor[0]
        else:
            return {}

    # 用wiki文本建立個單字的idf
    def build(self, fileName):
        def sentenct2terms():
            tmpCorpus = []
            while True:
                self.queueLock.acquire()
                if self.text:
                    i = self.text.pop()
                    self.queueLock.release()                
                    tmpCorpus.append(' '.join(jieba.cut(i)))
                else:
                    self.queueLock.release()
                    break

            self.queueLock.acquire()
            self.corpus.extend(tmpCorpus)
            self.queueLock.release()

        def calIdf():
            # calculate idf
            vectorizer = TfidfVectorizer()
            vectorizer.fit_transform(self.corpus)
            idf = vectorizer.idf_
            self.IdfList = [{'key':key, 'value':value} for key, value in zip(vectorizer.get_feature_names(), idf)]

        def insert2Mongo():
            # insert 2 mongoDB
            self.Collect.insert(self.IdfList)
            self.Collect.create_index([("key", pymongo.HASHED)])

        with open(fileName, 'r', encoding='utf-8') as f:
            self.text = f.read()
            self.text = re.findall(r'\<doc.+?>(.+?)\<\/doc\>', self.text, re.S)

        workers = [threading.Thread(target=sentenct2terms, name=str(i)) for i in range(multiprocessing.cpu_count())]
        for thread in workers:
           thread.start()
        # Wait for all threads to complete
        for thread in workers:
            thread.join()

        calIdf()
        insert2Mongo()




if __name__ == '__main__':
    from wiki.__init__ import WikiKCEM
    from collections import defaultdict
    import pyprind
    idf = TFIDF()
    # idf.build(sys.argv[1])
    wiki = WikiKCEM()
    kcemTable = {}

    f = json.load(open('accessbility.json','r'))
    result = {}
    for d in f:
        try:
            tmp = dict(idf.tfidf(d['context'], 5))
            for i in tmp:
                result[i] = result.setdefault(i, 0) + 1
        except Exception as e:
            pass

    print(sorted(result.items(), key=lambda x:-x[1]))
    top5_before = defaultdict(list)
    top5_after = defaultdict(list)
    for key, value in list(sorted(result.items(), key=lambda x:-x[1]))[:5]:
        category = kcemTable.setdefault(key, wiki.findParent(key)['value'][0][0]) 
        top5_before[category].append(key)
    print(sorted(top5_before.items(), key=lambda x:-len(x[1])))

    print('----------------------------------------------------')    
    for key, value in result.items():
        category = kcemTable.setdefault(key, wiki.findParent(key)['value'][0][0])
        top5_after[category].append(key)
    print(sorted(top5_after.items(), key=lambda x:-len(x[1])))

    print('----------------------------------------------------')    
    print('all accessbility as one article and then show tfidf')
    f = json.load(open('accessbility.json','r'))
    context = ''.join(i['context'] for i in f)
    result = dict(idf.tfidf(context, 5))
    print(sorted(result.items(), key=lambda x:-x[1]))

    print('----------------------------------------------------')    
    print('all accessbility as one article and -> tfidf -> kcem')
    top5_before = defaultdict(list)
    for key, value in list(sorted(result.items(), key=lambda x:-x[1])):
        category = kcemTable.setdefault(key, wiki.findParent(key)['value'][0][0])
        top5_before[category].append(key)
    print(sorted(top5_before.items(), key=lambda x:-len(x[1])))

    print('----------------------------------------------------')    
    print('all accessbility as one article and -> kcem -> topK')
    top5_before = defaultdict(list)
    print(kcemTable)
    for key in pyprind.prog_bar(rmsw(context)):
        parent = kcemTable.setdefault(key, wiki.findParent(key)['value'][0][0] if wiki.findParent(key) else [])
        if parent:
            top5_before[parent].append(key)
    print(sorted(top5_before.items(), key=lambda x:-len(x[1])))
    top5_before = {k:len(v)for k,v in top5_before.items()}
    print(sorted(top5_before.items(), key=lambda x:-len(x[1])))