from wordCloud import wordCloud
test_data = {
    "friendly": 7,
    "more": 6,
    "prompt": 5,
    "great": 4,
    "least": 3,
    "clean": 1,
    "able": 2,
    "bad": 2,
    "pre-order":2,
    "disappointed":2,
    "high":2,
    "helpful":2,
    "expenseive":2,
    "grumpy":2,
    "mad":22,
}
wordCloud = wordCloud()
import time

start = time.time()
wordCloud.get_wordCloud(test_data).show()
end = time.time()
print("time:{}".format(end - start))
