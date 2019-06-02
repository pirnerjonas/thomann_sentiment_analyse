import nltk
import numpy as np
from itertools import chain
import matplotlib.pyplot as plt
import pandas as pd
import re
from wordcloud import WordCloud
import random
from sklearn.decomposition import PCA
from scipy import interp
from itertools import cycle
from sklearn.metrics import roc_curve, auc, roc_auc_score



def dist_word(word, data):
    """ dise Funktion plottet für ein gegebens Wort die Wahrscheinlichkeit innerhalb der Klasse """
    _ = data[data["stars_gesamt"]==100]["tokenWord_pp_neg"]
    # collapse sublists to one list (this way you dont have to iterate over the rows)
    fdist_five = nltk.FreqDist(chain.from_iterable(_))
    _ = data[data["stars_gesamt"]==80]["tokenWord_pp_neg"]
    # collapse sublists to one list (this way you dont have to iterate over the rows)
    fdist_four = nltk.FreqDist(chain.from_iterable(_))
    _ = data[data["stars_gesamt"]==60]["tokenWord_pp_neg"]
    # collapse sublists to one list (this way you dont have to iterate over the rows)
    fdist_three = nltk.FreqDist(chain.from_iterable(_))
    _ = data[data["stars_gesamt"]==40]["tokenWord_pp_neg"]
    # collapse sublists to one list (this way you dont have to iterate over the rows)
    fdist_two = nltk.FreqDist(chain.from_iterable(_))
    _ = data[data["stars_gesamt"]==20]["tokenWord_pp_neg"]
    # collapse sublists to one list (this way you dont have to iterate over the rows)
    fdist_one = nltk.FreqDist(chain.from_iterable(_))

    f5 = fdist_five[word]/fdist_five.N()
    f4 = fdist_four[word]/fdist_four.N()
    f3 = fdist_three[word]/fdist_three.N()
    f2 = fdist_two[word]/fdist_two.N()
    f1 = fdist_one[word]/fdist_one.N()

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

def generate_POS_wordcloud(data, column, POS, stars=0):
    """ Nimmt Dataframe Spalte im Tokenformat [(Das, ART)...] entgegen und plottet für 
    ein POS-Tag die entsprechende Häufigkeit. POS kann im Regex Format angegeben werden.
    """
    # color wird nach stars vergeben
    color = stars*3
    def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
        return "hsl({}, 80%%, %d%%)".format(color) % random.randint(40, 100)

    if stars != 0:
        data = data[data["stars_gesamt"]==stars]
        data = data.reset_index(drop=True)

    n = len(data)
    words = [[word for word, tag in data[column][i] if re.match(POS,tag)] for i, _ in enumerate(data)]

    wordcloud = WordCloud().generate(' '.join(list(chain.from_iterable(words))))

    # Display the generated image:
    default_colors = wordcloud.to_array()
    plt.title("Häufigste {} für {} Sterne Bewertungen (n={})".format(str(POS), str(stars), str(n)))
    plt.imshow(wordcloud.recolor(color_func=grey_color_func, random_state=3), interpolation="bilinear")
    plt.axis("off")
    plt.figure()

def bigram_wordcould(data, stars, word1=".+", word2=".+", pos1=".+", pos2=".+"):
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

    default_colors = wordcloud.to_array()
    plt.figure( figsize=(20,10))
    plt.imshow(wordcloud.recolor(color_func=grey_color_func, random_state=3), interpolation="bilinear")
    plt.title("Sterne: {}".format(str(stars/20)), fontsize=18)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.figure()
    wordcloud.to_file("wordcloud{}.png".format(str(stars/20)))

def word2vec_pca(model, words):
    """ model ist word2vec model"""
    _ = [model.wv[word] for word in words]
    pca_df = pd.DataFrame(_)

    pca = PCA(n_components=2)
    principalComponents = pca.fit_transform(pca_df)
    pca_df = pd.DataFrame(data = principalComponents, columns = ['PC1', 'PC2'])

    pca_df = pd.concat([pca_df, pd.Series(words)], axis=1)

    fig, ax = plt.subplots()
    ax.scatter(pca_df["PC1"], pca_df["PC2"])
    for i, word in enumerate(words):
        ax.annotate(word, (pca_df.loc[i,"PC1"], pca_df.loc[i,"PC2"]))
    plt.show()

def roc_plot(y_test, pred, num_class, model):
    n_classes = num_class

    fpr = dict()
    tpr = dict()
    roc_auc = dict()
        
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(np.array(pd.get_dummies(y_test))[:, i], np.array(pd.get_dummies(pred))[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])

    all_fpr = np.unique(np.concatenate([fpr[i] for i in range(n_classes)]))

    mean_tpr = np.zeros_like(all_fpr)
    for i in range(n_classes):
        mean_tpr += interp(all_fpr, fpr[i], tpr[i])

    mean_tpr /= n_classes

    fpr["macro"] = all_fpr
    tpr["macro"] = mean_tpr
    roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])

    lw=2
    
    plt.plot(fpr["macro"], tpr["macro"],
            label='macro-average ROC curve (area = {0:0.2f})'
                ''.format(roc_auc["macro"]),
            color='black', linestyle=':', linewidth=4)

    colors = cycle(['deepskyblue', 'orange', 'lime', 'tomato', 'magenta'])
    for i, color in zip(range(n_classes), colors):
        plt.plot(fpr[i], tpr[i], color=color, lw=lw,
                label='ROC curve of class {0} (area = {1:0.2f})'
                ''.format(i+1, roc_auc[i]))

    plt.plot([0, 1], [0, 1], 'k--', lw=lw)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic for {}'.format(model))
    plt.legend(loc="lower right")
    plt.show()