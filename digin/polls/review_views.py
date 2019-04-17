import pke
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import collections

# dummy_reviews = [
# "Outstanding sushi / Japanese with a Korean twist cuisine in a beautifully decorated restaurant space.  The produce and food served here are top quality. Service is also uniformly excellent.  This place gets busy at lunch so expect to wait, but it's worth it! The sake don I had was amazing with sushi grade salmon and sushi rice, veggies, seaweed, salmon roe, served with a miso soup. Everyone in my lunch group was very impressed with this restaurant. We will be back!",
# "Been to a few Japanese restaurants in the region and Sakanaya is certainly the one that takes the cake according to to my taste buds. It's a small place, but well worth the wait to experience some tasty fireworks.",
# "The standard for ramen/rolls/sushi in Chambana. It's hard to find this level of quality even in Chicago. Pricey, sure, but there's a reason the place is still always packed. Food = top notch. Service = fantastic. The only downside would be the long lines during peak hours.",
# "The sushi here is awesome, probably the best in Urbana-Champaign",
# "I love coming here for dinner, I have come here many times with friends or on dates. It's always busy since it is so small, so make sure to come early, but it is certainly worth the wait. I love the sushi and the ramen, especially the spider Maki which I order every time. The seaweed salad and miso soup are also really good. Servers are nice.",
# "Best place on Campus town for sushi! Waiters are super friendly and explain all dishes very well. Their ramen is really light and tasty as well.A nice ambience for a classy dinner or date",
# "Sakanaya is the only legitimate sushi and ramen restaurant on campus. It is affordable, on green street, and worth every penny! If you haven't been to Sakanaya, you haven't been to Urbana-Champaign.",
# "If you want some good sushi in Champaign that’s affordable, definitely the place to go!! It’s on campus so it’s super accessible too.",
# "Great place to eat sushi. Fresh and delicious",
# "My husband and I love sushi and are from Wisconsin and crossed our fingers going in because we had never been to this restaurant. The service the moment we walked in was amazing ! We ordered 4 different rolls to share and within 25 minutes we had gotten all our rolls and were able to continue our trip! Highly recommended !",
# 	]

# define the set of valid Part-of-Speeches
pos = {'ADJ'}



def generate_wordcloud(place_id, reviews):
	print(place_id)
	print(reviews)
	freq = collections.defaultdict(float)
	for review in reviews:
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
