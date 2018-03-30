---
layout: post
title: "Generate & Rate"
date: 2018-03-30 17:15:00 -0500
categories: journal
---
This week I implemented the first sentence rating mechanism, based on the bigram matrix calculation from last week.

It's pretty simple, and doesn't achieve great results yet.

## Design
Here's the strategy. It simply calculates a large markov matrix for an entire corpus. Then a pseudo-random sample is chosen from the corpus to construct a CFG from. Then 100 sentences are generated from the CFG. The probability of the bigrams present in the generated text are looked up in the markov transition matrix and summed for each sentence. The idea is that highest scoring sentence should be more "corpus-like" than the lowest scoring sentence.

The simple sum method rewards use of a bigram from the corpus, and doesn't reward new bigrams. The method is also biased toward long sentences, since there are just more bigrams to score from. As a simple check, I cut off sentences at 15 tokens.

## Output Sample
The output is not excellent. For some reason, this generator is URL-happy.

```
Sentence 1
https://t.co/v2yo6pSYoB 11,000,000 % RT #WeeklyAddress delivered to -
delivered made-up #AlwaysTrump From https://t.co/xiu9AUiSSD . ''

Sentence 2
as a new country https://t.co/q… GOOD ! , thing https://t.co/DNzRZiKxhd
11,000,000 @realDonaldTrump !

Sentence 3
in https://t.co/DNzRZiKxhd force 10,800,000 https://t.co/DNzRZiKxhd , the   
followers !

Sentence 4
by @TeamTrump rally https://t.co/sUTyXBzer9 illegal #Debates2016 ,  
unnecessary https://t.co/xiu9AUiSSD !

Sentence 5
https://t.co/sUTyXBzer9 https://t.co/Fsy1diPWjU 200,000 poison
```

## Tokenization
The Stanford CoreNLP does not seem to allow custom tokenization of text, which is a small problem for this project. Specifically, I'd like to control how URLs, emojis, and contractions are treated. I'm able to separate them with regular expression for the Markov transition matrix, but the CoreNLP tokenizer doesn't allow regular expression use for tokenization.

Maybe preprocessing can handle contractions.

## Next
Tuning the parameters will likely create better sentences. Alpha in the CFG generator controls how unlikely a rule is repeated in an expansion. A true length penalty will be helpful, and trigram probabilities may also help.

The size of the sample which is converted to a CFG will possibly make the biggest difference, though. A larger sample means more rules, which means more possibilities. But too many possibilities prevent a thought from staying consistent.

Maybe throwing out the additive scores and replacing them with a cosine similarity comparison would be better. We'll see.
