import jieba, json, multiprocessing, threading, re, pymongo, sys
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
jieba.load_userdict('dictionary/dict.txt.big.txt')
jieba.load_userdict("dictionary/NameDict_Ch_v2")

class IDF(object):
    """docstring for IDF"""
    def __init__(self):
        self.queueLock = threading.Lock()
        self.corpus = []
        self.IdfList = []
        self.text = ''
        self.Collect = pymongo.MongoClient(None)['nlp']['idf']
        
    # 輸入一篇文章，計算出個字詞的tf-idf
    def tfidf(self, doc, num):
        vectorizer = CountVectorizer()
        doc = [' '.join(doc)]
        freq = vectorizer.fit_transform(doc).toarray()[0]
        tf = {key:freq[index] for key, index in vectorizer.vocabulary_.items()}
        result = {}
        for i in tf:
            cursor = self.Collect.find({'key':i}).limit(1)
            if cursor.count():
                result[i] = (1+math.log(tf[i])) * dict(list(cursor)[0])['value']
        return sorted(result.items(), key=lambda x:-x[1])[:num]

    # 用wiki文本建立個單字的idf
    def build(self, fileName):
        with open(fileName, 'r', encoding='utf-8') as f:
            self.text = f.read()
            self.text = re.findall(r'\<doc.+?>(.+?)\<\/doc\>', self.text, re.S)

        workers = [threading.Thread(target=self.sentenct2terms, name=str(i)) for i in range(multiprocessing.cpu_count())]
        for thread in workers:
           thread.start()
        # Wait for all threads to complete
        for thread in workers:
            thread.join()

        self.calIdf()
        self.insert2Mongo()

    def sentenct2terms(self):
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

    def calIdf(self):
        # calculate idf
        vectorizer = TfidfVectorizer()
        vectorizer.fit_transform(self.corpus)
        idf = vectorizer.idf_
        self.IdfList = [{'key':key, 'value':value} for key, value in zip(vectorizer.get_feature_names(), idf)]

    def insert2Mongo(self):
        # insert 2 mongoDB
        self.Collect.insert(self.IdfList)
        self.Collect.create_index([("key", pymongo.HASHED)])

    @staticmethod
    def findCommonParent(termA, termB):
        for term in [termA, termB]:
            cursor = self.Collect.find({'key':term}).limit(1)
            if not cursor.count():
                return []
                result[i] = (1+math.log(tf[i])) * dict(list(cursor)[0])['value']

        a, b = [], []
        while not set(a).intersection(set(b)):
            self.Collect.find({'key':term}).limit(1)
            a.append()

if __name__ == "__main__":  
    idf = IDF()
    idf.build(sys.argv[1])