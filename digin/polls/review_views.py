import pke
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import collections
import os
from .wordCloud import wordCloud
from background_task import background

# define the set of valid Part-of-Speeches
pos = {'ADJ'}
@background(schedule=10)
def generate_wordcloud(place_id, reviews):
	
	freq = collections.defaultdict(float)
	for review in reviews:
		if len(review) <= 10:
			continue
		print(review)
		# 1. create a TextRank extractor.
		extractor = pke.unsupervised.TextRank()

		# 2. load the content of the document.
		extractor.load_document(input=review,
		                        language='en',
		                        normalization=None)

		# 3. build the graph representation of the document and rank the words.
		#    Keyphrase candidates are composed from the 33-percent
		#    highest-ranked words.
		extractor.candidate_weighting(window=10,
									  pos=pos,
		                              top_percent=1)

		# 4. get the 10-highest scored candidates as keyphrases
		keyphrases = extractor.get_n_best(n=10)
		for keyphrase in keyphrases:
			freq[keyphrase[0].lower()] += 1
	print(keyphrases)
	filename = str(place_id) + ".png"
	if len(freq) == 0:
		os.system("cp /home/yi/Documents/School/CS411/cs411-digin/digin/digin/static-asset/nowords.png " + "/home/yi/Documents/School/CS411/cs411-digin/digin/digin/static-asset/"+filename)
		return filename
	
	wordcloud = wordCloud().get_wordCloud(freq)
	wordcloud2 = WordCloud().generate_from_frequencies(freq)
	filename2 = str(place_id) + "2.png"
	plt.imsave("digin/static-asset/" + filename, wordcloud)
	plt.imsave("digin/static-asset/" + filename2, wordcloud2)
	# plt.imsave(filename, wordcloud)
	

	return filename

