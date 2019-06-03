import random
import re
from itertools import chain, cycle

import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
from scipy import interp
from wordcloud import WordCloud


def dist_word(word, data):
    """ plottet für ein gegebens Wort die jeweiligen Wahrscheinlichkeiten in den Bewertungsklassen.
    
    Arguments:
        word {str} -- das Wort, welches untersucht werden soll
        data {dataframe} -- das zugehörige DataFrame
    """
    
    # frequency distribution für die unterschiedlichen Klassen speichern
    _ = data[data["stars_gesamt"]==100]["tokenWord_pp_neg"]
    fdist_five = nltk.FreqDist(chain.from_iterable(_))
    _ = data[data["stars_gesamt"]==80]["tokenWord_pp_neg"]
    fdist_four = nltk.FreqDist(chain.from_iterable(_))
    _ = data[data["stars_gesamt"]==60]["tokenWord_pp_neg"]
    fdist_three = nltk.FreqDist(chain.from_iterable(_))
    _ = data[data["stars_gesamt"]==40]["tokenWord_pp_neg"]
    fdist_two = nltk.FreqDist(chain.from_iterable(_))
    _ = data[data["stars_gesamt"]==20]["tokenWord_pp_neg"]
    fdist_one = nltk.FreqDist(chain.from_iterable(_))

    # Anteil des Worts je Klasse
    f5 = fdist_five[word]/fdist_five.N()
    f4 = fdist_four[word]/fdist_four.N()
    f3 = fdist_three[word]/fdist_three.N()
    f2 = fdist_two[word]/fdist_two.N()
    f1 = fdist_one[word]/fdist_one.N()

    # Plotten der Häufigkeit je Klasse
    plt.plot([1,2,3,4,5],[f1,f2,f3,f4,f5])
    plt.plot(1, f1,'bo')
    plt.plot(2, f2,'bo')
    plt.plot(3, f3,'bo')
    plt.plot(4, f4,'bo')
    plt.plot(5, f5,'bo')
    plt.xlabel("Anzahl der Sterne")
    plt.ylabel("rel. Häufigkeit")
    plt.title("%s" % word)
    plt.savefig('dist_word_{}.png'.format(word))
    plt.show()


def bigram_wordcould(data, stars, word1=".+", word2=".+", pos1=".+", pos2=".+"):
    """plottet bigrams wordclouds für eine bestimmte Anzahl von Sternen. Für die bigrams kann nach Wortart und Wort gefiltert werden. 
    Dafür stehen die entsprechenden Parameter word1 und word2 für das erste und zweite Wort, und die Parameter pos1 und pos2 für die 
    Part-of-Speech Tags.
    
    Arguments:
        data {dataframe} -- das zugehörige DataFrame
        stars {int} -- Sterne, Angabe in Prozentzahl (1 Stern = 20, 2 Stern = 40 ...)
    
    Keyword Arguments:
        word1 {str} -- erstes Wort des bigrams (default: {".+"})
        word2 {str} -- zweites Wort des bigrams (default: {".+"})
        pos1 {str} -- erste Wortart des bigrams (default: {".+"})
        pos2 {str} -- zweite Wortart  des bigrams (default: {".+"})
    
    Returns:
        plot -- gibt den entsprechenden plot aus
    """
    data = data[data["stars_gesamt"]==stars]

    # color wird nach stars vergeben
    color = stars*3
    def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
        return "hsl({}, 80%%, %d%%)".format(color) % random.randint(40, 100)

    # hier wird die Einschränkung nach Worten und Wortart vorgenommen
    def topic_sent(tagged_review_words):
        word_tag_pairs = nltk.bigrams(tagged_review_words)
        matched_pairs = [(a[0], b[0]) for (a, b) in word_tag_pairs if re.match(word1, a[0]) and re.match(word2, b[0]) and re.match(pos1,a[1]) and re.match(pos2,b[1])]
        return matched_pairs

    # anwenden der Hilfsfunktion
    _ = [topic_sent(review) for review in data["taggedWords_neg"]]

    # umwandeln in dict, dass von generate_from_frequencies verarbeitet werden kann
    dist = dict(nltk.FreqDist(chain.from_iterable(_)))
    keys = [str(key) for key in dist.keys()]
    keys = [re.sub("[^\w ]","", key) for key in keys]
    values = [float(value) for value in dist.values()]
    wordcloud = WordCloud(background_color='grey', width=1600, height=800, max_words=40).generate_from_frequencies(dict(zip(keys,values)))

    plt.figure( figsize=(20,10))
    plt.imshow(wordcloud.recolor(color_func=grey_color_func, random_state=3), interpolation="bilinear")
    plt.title("Sterne: {}".format(str(stars/20)), fontsize=18)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.figure()
    wordcloud.to_file("wordcloud{}.png".format(str(stars/20)))
