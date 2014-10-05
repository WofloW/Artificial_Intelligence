import argparse,string,sys,os,math,heapq
import cPickle as pickle
from os.path import join


stopword = ['a', 'about', 'above', 'above', 'across', 'after', 'afterwards', 'again', 'against', 'all', 'almost', 'alone', 'along', 'already', 'also','although','always','am','among', 'amongst', 'amoungst', 'amount',  'an', 'and', 'another', 'any','anyhow','anyone','anything','anyway', 'anywhere', 'are', 'around', 'as',  'at', 'back','be','became', 'because','become','becomes', 'becoming', 'been', 'before', 'beforehand', 'behind', 'being', 'below', 'beside', 'besides', 'between', 'beyond', 'bill', 'both', 'bottom','but', 'by', 'call', 'can', 'cannot', 'cant', 'co', 'con', 'could', 'couldnt', 'cry', 'de', 'describe', 'detail', 'do', 'done', 'down', 'due', 'during', 'each', 'eg', 'eight', 'either', 'eleven','else', 'elsewhere', 'empty', 'enough', 'etc', 'even', 'ever', 'every', 'everyone', 'everything', 'everywhere', 'except', 'few', 'fifteen', 'fify', 'fill', 'find', 'fire', 'first', 'five', 'for', 'former', 'formerly', 'forty', 'found', 'four', 'from', 'front', 'full', 'further', 'get', 'give', 'go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her', 'here', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'however', 'hundred', 'ie', 'if', 'in', 'inc', 'indeed', 'interest', 'into', 'is', 'it', 'its', 'itself', 'keep', 'last', 'latter', 'latterly', 'least', 'less', 'ltd', 'made', 'many', 'may', 'me', 'meanwhile', 'might', 'mill', 'mine', 'more', 'moreover', 'most', 'mostly', 'move', 'much', 'must', 'my', 'myself', 'name', 'namely', 'neither', 'never', 'nevertheless', 'next', 'nine', 'no', 'nobody', 'none', 'noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'of', 'off', 'often', 'on', 'once', 'one', 'only', 'onto', 'or', 'other', 'others', 'otherwise', 'our', 'ours', 'ourselves', 'out', 'over', 'own','part', 'per', 'perhaps', 'please', 'put', 'rather', 're', 'same', 'see', 'seem', 'seemed', 'seeming', 'seems', 'serious', 'several', 'she', 'should', 'show', 'side', 'since', 'sincere', 'six', 'sixty', 'so', 'some', 'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhere', 'still', 'such', 'system', 'take', 'ten', 'than', 'that', 'the', 'their', 'them', 'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby', 'therefore', 'therein', 'thereupon', 'these', 'they', 'thickv', 'thin', 'third', 'this', 'those', 'though', 'three', 'through', 'throughout', 'thru', 'thus', 'to', 'together', 'too', 'top', 'toward', 'towards', 'twelve', 'twenty', 'two', 'un', 'under', 'until', 'up', 'upon', 'us', 'very', 'via', 'was', 'we', 'well', 'were', 'what', 'whatever', 'when', 'whence', 'whenever', 'where', 'whereafter', 'whereas', 'whereby', 'wherein', 'whereupon', 'wherever', 'whether', 'which', 'while', 'whither', 'who', 'whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with', 'within', 'without', 'would', 'yet', 'you', 'your', 'yours', 'yourself', 'yourselves', 'the'];

class article:
	def __init__(self, filename=None, category=None, raw_text=None,dict_TF={}):
		self.filename = filename
		self.category = category
		self.raw_text = raw_text
		self.dict_TFIDF = {}
		self.dict_TF = dict_TF
	def __repr__(self) :
		return '%s' % self.filename
	def computeTFIDF(self,DF,D):
		for word in self.dict_TF:
			if word not in DF:
				DF[word] = 1
			self.dict_TFIDF[word]=self.dict_TF[word]*math.log(D/DF[word])


		# print word,self.dict_TFIDF[word],self.dict_TF[word],dict_DF[word]
	def load_and_TF(self,path):
		dict_TF={}
		raw_text=open(path).read()
		text=raw_text.lower()
		text=text.split()
		for word in text:
			word = word.strip(string.punctuation)
			if word not in stopword:
				if word not in dict_TF:
					self.dict_TF[word]=1
				else:
					self.dict_TF[word]+=1


class newsgroup:
	def __init__(self, category):
		self.category = category
		self.articles=[]
		self.dict_TFIDF={}
		self.dict_DF={}

	def __repr__(self) :
		return '%s' % self.category

	def computeDocumentFrequency(self,category,directory):
		category_directory=join(directory,category)
		filenames=os.listdir(category_directory)
		self.dict_DF={}

		for filename in filenames:
			if '.' not in filename:
				dict_TF={}
				raw_text=open(join(category_directory,filename)).read()
				text=raw_text.lower()
				text=text.split()
				for word in text:
					word = word.strip(string.punctuation)
					if word not in stopword:
						if word not in dict_TF:
							dict_TF[word]=1
							if word not in self.dict_DF:
								self.dict_DF[word]=1
							else:
								self.dict_DF[word]+=1
						else:
							dict_TF[word]+=1
				self.articles.append(article(filename,category,raw_text,dict_TF))

	def computeTFIDFCategory(self):
		print "computeTFIDFCategory: %s" %self.category
		dict_TFIDF_sorted=heapq.nlargest(1000,self.dict_TFIDF,key=self.dict_TFIDF.__getitem__)
		new_TFIDF={}
		for word in dict_TFIDF_sorted:
			new_TFIDF[word]=self.dict_TFIDF[word]
		self.dict_TFIDF=new_TFIDF
		# print self.dict_TFIDF
		
class corpus:
	def __init__(self,list_dirnames=None,directory=None):
		self.newsgroups=[]
		self.DF={}
		self.D = 0

		for category in list_dirnames:
			print 'loading category: %s' % category
			newsgroup_inst=newsgroup(category)
			newsgroup_inst.computeDocumentFrequency(category,directory)
			self.D += len(newsgroup_inst.articles)
			for word in newsgroup_inst.dict_DF:
				if word not in self.DF:
					self.DF[word]=newsgroup_inst.dict_DF[word]
				else:
					self.DF[word]+=newsgroup_inst.dict_DF[word]
			self.newsgroups.append(newsgroup_inst)
		for i in range(len(self.newsgroups)):
			for j in range(len(self.newsgroups[i].articles)):
				self.newsgroups[i].articles[j].computeTFIDF(self.DF,self.D)
				# print self.newsgroups[i].articles[j].dict_TFIDF
				for word in self.newsgroups[i].dict_DF:
					if word in self.newsgroups[i].articles[j].dict_TF:
						if word not in self.newsgroups[i].dict_TFIDF:
							self.newsgroups[i].dict_TFIDF[word]=self.newsgroups[i].articles[j].dict_TFIDF[word]
						else:
							self.newsgroups[i].dict_TFIDF[word]+=self.newsgroups[i].articles[j].dict_TFIDF[word]
			self.newsgroups[i].computeTFIDFCategory()
		# print self.newsgroups[0].dict_DF
		# print self.DF,self.D
		# print self.newsgroups[0].articles[0].dict_TF
		# print self.newsgroups[0].dict_TFIDF
		# print self.newsgroups
	def pickle_dict(self):
		dict_temp={}
		for category in self.newsgroups:
			dict_temp[category.category] = category.dict_TFIDF 
		pickle.dump(dict_temp, open('20category' , 'wb'))
		pickle.dump([self.DF,self.D],open('DFandD','wb'))

def cosineSimilarity(dict1,dict2):
	numerator = 0
	denominator = 0
	denominator1 = 0
	denominator2 = 0

	for word in dict1:
		if word in dict2:
			numerator+=dict1[word]*dict2[word]
		denominator1 += dict1[word]*dict1[word]
	denominator1 = math.sqrt(denominator1)
	for word in dict2:
		denominator2 += dict2[word]*dict2[word]
	denominator2 = math.sqrt(denominator2)
	denominator = denominator1 * denominator2
	return numerator/denominator

def classify(article, category20):
	max_similarity = 0
	similar_category = None
	for category in category20:
		temp=cosineSimilarity(article.dict_TFIDF, category20[category])
		# print category,temp
		if temp >max_similarity:
			max_similarity = temp
			similar_category = category
	return similar_category





if __name__ == '__main__':
	# directory = "/home/wfang2/Downloads/20_newsgroups"
	# directory = "/home/wfang2/Downloads/1"
	directory = "D:/usf/20_newsgroups"
	for (dirpath, dirnames, filenames) in os.walk(directory):
		list_dirnames=dirnames
		break
	corpus_inst=corpus(list_dirnames,directory)
	corpus_inst.pickle_dict()
	# pickle.dump(corpus_inst,open('corpus','wb'))
	# print corpus_inst.newsgroups[0].articles
	# a=corpus_inst.newsgroups[0].articles[0].dict_TFIDF
	# b=corpus_inst.newsgroups[1].dict_TFIDF
	# c=corpus_inst.newsgroups[0].articles[1].dict_TFIDF
	# print cosineSimilarity(a,c)
	


		

    
