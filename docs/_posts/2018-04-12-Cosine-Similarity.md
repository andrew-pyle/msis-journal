---
layout: post
title: "Cosine Similarity"
date: 2018-04-12 09:41:00 -0500
categories: journal
---
*Long article this week*

We've got two things to discuss in this post: design changes and a new rating function.

## Design Change
After a discussion with my adviser, Dr. Charles Romney, it seems that the rating function has too much responsibility in the current design.

Conceptually, the rating function must evaluate both the sentence structure and the imitation of the original corpus. Sentences with 15 verb phrases are not typical English, so they should be rated poorly. But sentences with a normal number of verb phrase which have words about hot-air balloons should also be rated poorly.

This means the rating function is doing too much.

### Partition the Evaluation
To combat this issue, I have offloaded the sentence structure part of the evaluation process back to the generation model. I did this by simplifying the language generation model: Rather than expanding from the 'ROOT' nonterminal via a random walk to terminal symbols, the generation system now expands only the lowest level of nonterminal symbols to terminal symbols. The figure below shows the new starting point circled in red.

![]({{ site.baseurl }}/assets/quickfoxparse.png)

Expanding from these nonterminal symbols has the effect of taking sentence structures directly from the original corpus but limits the flexibility of the CFG generation model. That tradeoff results in more realistic sentences before the imitation rating ever takes place.

## New Rating Method
Now that we have sentences with better grammar to evaluate, we can rate them.

To avoid the [length bias]({{ site.baseurl }}{% post_url 2018-03-30-Generate-&-Rate %}) with the previous rating method (sum of bigram frequency values), I implemented a cosine-similarity-based rating function for generated sentences.

The text of all sentences in the corpus is tokenized as unigrams, bigrams, trigrams, or even quadrigrams. That's a document. Then each generated sentence is tokenized in the same way. Those are the other documents.

The tokens are transformed into a term-document matrix, and cosine similarity comparison can be done between the whole corpus (document 1) and each generated sentence (documents 1 - *N*). ([Scikit-learn](http://scikit-learn.org/stable/) has a great package for Python.)
```
Corpus · Doc 1 = score 1
Corpus · Doc 2 = score 2
...
Corpus · Doc N = score N
```
It seems that quadrigrams are too infrequent between a generated sentence and the corpus (as we'd expect), and trigram scores tend to cluster at the same few values. That seems to indicate that the same few trigrams are being scored in each sentence. Bigrams have a wider range of score values, so I think that bigrams may be the most specific token which is broadly applicable.

Maybe we can tie all this together next week.

### Sample Generated Sentences
**Unigram-Based Cosine Similarity**

| Score | Sentence |
|-------|----------|
| 0.384333 | anti-Trump and @usairforce think kneeling more If The manner.The , and my parents demand YOU ? .@POTUS |
| 0.379415 | GREAT But A.M. are taking larger FOR the Rocket , plus our clips am you ? Year |

**Bigram-Based Cosine Similarity**

| Score | Sentence |
|-------|----------|
| 0.065988 | careful & research Am bringing stronger of The Administration , and his echoes kneel I ! relief |
| 0.060698 | Little or PR continue noticing more of the honor , and their odds 'RE He ! help |

**Trigram-Based Cosine Similarity**

| Score | Sentence |
|-------|----------|
| 0.008517 | Courageous & economy demand getting stronger By The @USCGSoutheast , plus our crews tune him ! player |
| 0.008517 | good & luncheon commend analyzing tougher by that #FEMA , and our @KellyannePolls am you ! tomorrow |

**Quadrigram-Based Cosine Similarity**

| Score | Sentence |
|-------|----------|
| 0.004711 | Courageous & economy demand getting stronger By The @USCGSoutheast , plus our crews tune him ! player |
| 0.000000 | Great But recruitment INSPIRE analyzing longer despite no @GOPChairwoman , and My Democrats demand She ! COS |
