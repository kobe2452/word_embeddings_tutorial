#!/usr/bin/env python
# -*- coding: utf-8 -*-

# script to visualize word embeddings of given model with PCA dimensionality reduction
# creates image with matplotlib
# https://raw.githubusercontent.com/devmount/GermanWordEmbeddings/master/visualize.py
# 
# @author: Andreas Mueller
# @see: Bachelor Thesis 'Analyse von Wort-Vektoren deutscher Textkorpora'
# Contributors:
# Michael Egger <michael.egger@tsn.at>
#
# MODIFIED FOR INTRO TO NLP COURSE USE
# BY TONG LIU, CECILIA O. ALM
#
# @usage: python visualize.py

import gensim
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# configuration

# pair1 = ['quiet', 'quieter']
# pair2 = ['loud', 'louder']
# pair3 = ['light', 'lighter']
# pair4 = ['dark', 'darker']
# pair5 = ['soft', 'softer']
# pair6 = ['strong', 'stronger']

words = ['light', 'lighter', 'dark', 'darker']

# words = ['quiet', 'quieter', 'loud', 'louder', 'light', 'lighter', 'dark', 'darker', 'soft', 'softer', 'strong', 'stronger']

def draw_words(model, words, pca=False, alternate=True, arrows=True, x1=3, x2=3, y1=3, y2=3, filename=''):
    """
    Reduces dimensionality of vectors of given words either with PCA or with t-SNE and draws the words into a diagram.

    :param model: to visualize vectors from
    :param words: list of word strings to visualize
    :param pca: use PCA (True) or t-SNE (False) to reduce dimensionality
    :param alternate: use different color and label align for every second word
    :param arrows: use arrows to connect related words (items that are next to each other in list)
    :param x1: x axis range (from)
    :param x2: x axis range (to)
    :param y1: y axis range (from)
    :param y2: y axis range (to)
    :param filename: for diagram
    :return: None
    """
    # get vectors for given words from model
    vectors = [model[word] for word in words]

    if pca:
        # http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html
        pca = PCA(n_components=2, whiten=True)
        vectors2d = pca.fit(vectors).transform(vectors)
    else:
        # http://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html
        tsne = TSNE(n_components=2, random_state=0)
        vectors2d = tsne.fit_transform(vectors)

    # draw image
    plt.clf()
    plt.figure(figsize=(7, 7))
    if pca:
        plt.axis([x1, x2, y1, y2])

    first = True  # color alternation to divide given groups
    for point, word in zip(vectors2d, words):
        # plot points
        plt.scatter(point[0], point[1], c='r' if first else 'g')
        # plot word annotations
        plt.annotate(
            word, 
            xy=(point[0], point[1]),
            xytext=(-7, -6) if first else (7, -6),
            textcoords='offset points',
            ha='right' if first else 'left',
            va='bottom',
            size="x-large"
        )
        first = not first if alternate else first

    # draw arrows
    if arrows:
        for i in range(0, len(words)-1, 2):
            a = vectors2d[i][0] + 0.04
            b = vectors2d[i][1]
            c = vectors2d[i+1][0] - 0.04
            d = vectors2d[i+1][1]
            plt.arrow(
                a, b, c-a, d-b,
                shape='full',
                lw=0.1,
                edgecolor='#bbbbbb',
                facecolor='#bbbbbb',
                length_includes_head=True,
                head_width=0.08,
                width=0.01
            )

    plt.savefig(filename, bbox_inches="tight")

def main():

    # get trained model
    trained_model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin.gz', binary=True)

    # draw pca plots
    draw_words(trained_model, words, True, True, True, -3, 3, -2, 2.2, 'word_embeddings_gensim_PCA.png')
    draw_words(trained_model, words, False, True, True, -3, 3, -2, 2.2, 'word_embeddings_gensim_tSNE.png')

if __name__ == '__main__':
    main()