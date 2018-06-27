![image](https://user-images.githubusercontent.com/119648/41982937-5a0daf54-7a35-11e8-83cc-c8f920919af0.png)
# Introduction
This application is about **disambiguating** terms in social media using the **Naive Bayes** algorithm, which is a powerful and surprisingly simple algorithm. The model which we're going to make is a baseline for text mining which can work reasonably well for a variety of datasets.

Usually extracting information from text datasets isn't an easy task because of its _unstructured_ format. The data is mostly highly connected, with lots of mentions and cross-references and in order to gain the information we need to interpret for context.

One major problem is the disambiguation in certain words depends on the main context. For example, if we run into the **Android** word, that has its literal meaning [a robot that looks like human] or the context is about the android operating system by Google.

Now, imagine we have some restriction for the count of words or characters which we could have for our text, as twitter which has 140(recently 280) character limitation for each tweet. Even by having options like hashtags to denote the topic of the tweet but still, we need an intelligent approach to evaluate the context by resolving disambiguated phrases.

# Tutorial & Usage
After cloning the repository, you'll need to sign up for a Twitter account and **create a new App** in [https://apps.twitter.com/](https://apps.twitter.com/)

Then rename the **config.example.py** to **config.py** and set all the credential values by copying them from your application page in twitter.

**NOTE:** Before running the scripts make sure you have read/write permission for the directory consists of the repository.

* First, running the _fetch_tweets_ method from the main script:
user _-p_ to define the phrase and _-c_ for the number of tweets you want to fetch.

`python main.py fetch_tweets -p android -c 50`

By running above command, the script makes an output file consisting of phrase in filename under the _output/data_ directory.

* In the second step, try to set the relevance of the tweet to the topic which we're looking for. For instance, in the case of android phrase, we want to distinguish between tweet related to operating system and others.

`python main.py label_tweets -p android`

Consider the _-p_ option which we used with the same phrase as first step, which means, we're going to set labels for the tweets consist of android phrase.

You need to choose option **0** or **1** based on relevance or not relevance respectively for each represented tweet in the console. 

**NOTE:** setting label could be paused and resume later if it was a long list of tweets to define the labels. You can easily break the script and call it again later and it will resume from the tweets which you left off.

* Once, you set the labels for all downloaded tweets, you can build and train the model by calling following command:

`python main.py build_model -p android` 

It will show the score of the model in the console, Go back and collect more data and you will find that the results increase!

By running above command, the script makes an export of model and saves in disk in the _output/models_ directory.

* If you need to know which words in collected tweets have more importance in classification of the labels, you can call the _list_top_words_ as shown below:

`python main.py list_top_words -p android`

Now, we are ready to use our classifier model for predecting label for tweets which are not collected earlier:

`python main.py predict -p android -c 10`

We call the method with _-p_ for the phrase in new tweets and _-c_ for the number of tweets which we want to make prediction on.

