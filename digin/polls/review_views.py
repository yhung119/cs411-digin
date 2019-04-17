import pke
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import collections

# define the set of valid Part-of-Speeches
pos = {'ADJ'}



def generate_wordcloud(place_id, reviews):
	
	freq = collections.defaultdict(float)
	for review in reviews:
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
			freq[keyphrase[0]] += 1

	wordcloud = WordCloud().generate_from_frequencies(freq)
	filename = str(place_id) + ".png"
	plt.imsave("digin/static-asset/" + filename, wordcloud)
	# plt.imsave(filename, wordcloud)

	return filename
