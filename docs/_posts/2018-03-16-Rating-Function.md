---
layout: post
title: "Rating Function"
date: 2018-03-16 15:15:00 -0500
categories: journal
---
It's been a few weeks since my last post; I've been busy with other projects. The next few weeks should show some progress.

# Rating the Output
Technical problems aside, we are able to generate some text based on a custom CFG implementation which is defined from a snippet of tweet text. This is great, but it's noisy. Each new snippet generated is highly likely to be gibberish, since there's nothing but randomness guiding the walk down the rule tree.

Now we need to create some criteria for rating the output. In other words, how can we pick the least gibberish-like output, or at least pick one with an acceptably small amount of gibberish?

## Bigram & Trigrams
The proposed design will use bigram and/or trigram frequencies. The original text corpus has certain frequencies with which any given word follows every other word in the corpus. The frequency for all pairs is the bigram frequency, and the frequency for 3-word sequences is trigram frequency.

### Bigram
`"the dog" : 0.1`
`"man dog" : 0.02`

### Trigram
`"the big dog" : 0.2`
`"the man dog" : 0.003`

These frequencies can be calculated for a large corpus of the same source as the input to the CFG, which will allow us to calculate a score for the generated sentence. Basically, we want to measure the divergence between a generated sentence and the corpus.

One strategy would be to sum the bigram frequencies for all bigrams in the generated sentence found in larger corpus. But that's just my first thought. Many other calculations are possible.

Whatever calculation is developed, a generated sentence score threshold can be established by human evaluation, allowing the definition of a successful generated sentence, which can be kept as output.

I'll be working on these possibilities next week. Stay tuned.
