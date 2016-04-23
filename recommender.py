import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import EnglishStemmer
import re
import math
import numpy
class Recommender:
    def __init__(self):
        self.p=[]
        self.q=""
        
    
    def refineproject(self,eachpro):
        return self.stemming(self.unstopped(self.tokenize(eachpro)))
         
    
    def addproject(self,pro):
        self.p+=pro
    
    def addquery(self,q):
        
        self.q+=self.stemming(q)
    
    def tokenize(self,p):
        tokenizer = RegexpTokenizer('\w+')
        words=p.lower().split()
        words=map(lambda s:s.decode(encoding='UTF-8',errors='ignore'),words)
        words=" ".join(words)
        tokenized_doc=" ".join(tokenizer.tokenize(words))
        return tokenized_doc
    
    def unstopped(self,p):
        tokenizer = RegexpTokenizer('\w+')
        stop=tokenizer.tokenize(open('english.txt').read())
        pattern = re.compile(r'\b(' + r'|'.join(stop) + r')\b\s*')
        unstopped_text = pattern.sub('', p)
        return unstopped_text
    
    def stemming(self,p):
        stemobj=EnglishStemmer()
        stemmed_text=map(stemobj.stem,p.split())
        stemmed_text=" ".join(stemmed_text)
        return stemmed_text
        
    

    def termFrequency(self,term, document):
        normalizeDocument = document.lower().split()
        return normalizeDocument.count(term.lower()) / float(len(normalizeDocument))  
    
    
    def inverseDocumentFrequency(self,term, allDocuments):
        numDocumentsWithThisTerm = 0
        for doc in range (len(allDocuments)):

            if term.lower() in allDocuments[doc].lower().split():

                numDocumentsWithThisTerm = numDocumentsWithThisTerm + 1

        if numDocumentsWithThisTerm > 0:
            return 1.0 + math.log(float(len(allDocuments)) / numDocumentsWithThisTerm)
        else:
            return 1.0
        
        
    def docvectorizer(self,document,query):
        query=query.lower().split()
        vector=[]
        for term in query:
            tfidf=self.termFrequency(term,document)*self.inverseDocumentFrequency(term,map(lambda s:s[1],self.p))
            vector.append(tfidf)
        return vector

    def queryvectorizer(self,query):
        querytokens=query.lower().split()

        vector=[]
        for term in querytokens:
            tfidf=self.termFrequency(term,query)*self.inverseDocumentFrequency(term,map(lambda s:s[1],self.p))
            vector.append(tfidf)
        return vector


    def computesimilarity(self,query,document):
        queryvector = self.queryvectorizer(query)
        documentvector = self.docvectorizer(document,query)

        return numpy.dot(queryvector,documentvector)
    
    def recommendation(self,query):
        ans=[]
        for eachpro in self.p:
            ans.append((self.computesimilarity(query,eachpro[1]),eachpro[0]))
        ans=sorted(set(ans),reverse=True)
        print ans
        return map(lambda s:s,ans[:6])