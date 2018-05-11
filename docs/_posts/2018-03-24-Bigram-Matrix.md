---
layout: post
title: "Bigram Matrix"
date: 2018-03-24 17:30:00 -0500
categories: journal
---
Last week I developed a function which will calculate the bigram frequencies for a given piece of text.

The bigram frequency data structure is based on a [Markov transition matrix](https://en.wikipedia.org/wiki/Stochastic_matrix), which is a matrix of dimensions M<sub>i,j</sub>, where `i` and `j` are equal and are the number of unique words in a text sample.

So for the sentence `The quick brown fox jumps over the quick black dog.`, we get:
```
        the  quick    brown    fox    jumps    over    black    dog    .
the  [[ 0.   1.       0.       0.     0.       0.      0.       0.     0. ]
quick [ 0.   0.       0.5      0.     0.       0.      0.5      0.     0. ]
brown [ 0.   0.       0.       1.     0.       0.      0.       0.     0. ]
fox   [ 0.   0.       0.       0.     1.       0.      0.       0.     0. ]
jumps [ 0.   0.       0.       0.     0.       1.      0.       0.     0. ]
over  [ 1.   0.       0.       0.     0.       0.      0.       0.     0. ]
black [ 0.   0.       0.       0.     0.       0.      0.       1.     0. ]
dog   [ 0.   0.       0.       0.     0.       0.      0.       0.     1. ]
.     [ 0.   0.       0.       0.     0.       0.      0.       0.     0. ]]
```

The probability of transitioning from the term at row index `i` to the term at column index `j` is the value `m[i][j]`. The only bigram without 1.0 transition probability here is `quick`. The text transitions from `quick` to both `brown` and `black`, so each of those terms get 0.5 probability.

Since this is such a small matrix, we can visually verify that the probabilities in each row sum to 1.

One point to note: `the` is present twice, but it's transition is the same both times. This results in a probability of 1.0, which is the same as other bigrams which are only present once. Transitions are not weighted according to frequency of use.

## What's the Point?
This little program will allow me to calculate transition probabilities for the training corpus of tweets. We can best compare the output of my generation program with the corpus using cosine similarity. This method will be the first attempt at rating the output, as discussed in the [Rating Function]({{ site.baseurl }}{% post_url 2018-03-16-Rating-Function %}) post.
