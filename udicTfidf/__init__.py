import pymongo, math, os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from udicOpenData.stopwords import rmsw
from ngram import NGram

class TFIDF(object):
    """docstring for TFIDF"""
    def __init__(self, lang, uri=None):
        self.lang = lang
        self.IdfList = []
        self.Collect = pymongo.MongoClient(uri)['nlp_{}'.format(self.lang)]['idf']
        self.idfNgram = NGram((i['key'] for i in self.Collect.find({}, {'key':1, '_id':False})))
        
    # 輸入一篇文章，計算出個字詞的tf-idf
    def tfidf(self, doc, flag):
        vectorizer = CountVectorizer()
        doc = [' '.join((i[0] for i in rmsw(doc, flag=True) if i[1] == flag or not flag))]
        if not doc: return []
        try:
            freq = vectorizer.fit_transform(doc).toarray()[0]
        except ValueError as e:
            print(e)
            return []
        tfs = {key:freq[index] for key, index in vectorizer.vocabulary_.items()}
        result = {}
        for term in tfs:
            cursor = self.Collect.find({'key':term}).limit(1)
            if cursor.count():
                result[term] = (1+math.log(tfs[term])) * dict(cursor[0])['value']
            else:
                ngramTerm = self.idfNgram.find(term)
                if ngramTerm:
                    cursor = self.Collect.find({'key':ngramTerm}).limit(1)
                    if cursor.count():
                        result[term] = (1+math.log(tfs[term])) * dict(cursor[0])['value']
        return sorted(result.items(), key=lambda x:-x[1])

    # output字詞idf
    def idf(self, keyword):
        cursor = self.Collect.find({'key':keyword}, {'value':1, '_id':False}).limit(1)
        if cursor.count():
            return cursor[0]
        else:
            return {}

    # 用wiki文本建立個單字的idf
    def build(self):
        def calIdf():
            # calculate idf
            vectorizer = TfidfVectorizer()
            with open(os.path.join('Wikipedia', 'wiki_seg_{}.txt'.format(self.lang)), 'r') as f:
                corpus = [article.strip() for article in f]
            vectorizer.fit_transform(corpus)
            idf = vectorizer.idf_
            self.IdfList = [{'key':key, 'value':value} for key, value in zip(vectorizer.get_feature_names(), idf)]

        def insert2Mongo():
            # insert 2 mongoDB
            self.Collect.remove({})
            self.Collect.insert(self.IdfList)
            self.Collect.create_index([("key", pymongo.HASHED)])

        calIdf()
        insert2Mongo()