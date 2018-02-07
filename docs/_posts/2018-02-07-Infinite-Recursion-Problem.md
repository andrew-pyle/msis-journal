---
layout: post
title: "Infinite Recursion Problem"
date: 2018-02-07 12:00:00 -0600
categories: journal
---
# Constituency Parsing
Constituency parsing software is installed!
- [Stanford CoreNLP 3.8.0](https://stanfordnlp.github.io/CoreNLP/history.html)
- [Shift-Reduce Parser](https://nlp.stanford.edu/software/srparser.html)
- [Python client for CoreNLP server](https://github.com/Lynten/stanford-corenlp)

Next I'll need to create a CFG from parsed sentences. I'll save that problem until I'm able to implement my CFG in code. That way I can make CFG design issues on its needs, not based on a parsed sentence string format.

# Generation Algorithm
Next I'll need to solve the infinite recursion problem with random sentence generation from a CFG.

## CFG
```
Nonterminal symbols:
S -> NP VP
NP -> NN
NP -> ADJ NP
VP -> V
VP -> V DT DO

Terminal symbols:
V -> run | walk | am | is
NN -> boy | dog | ball | lady
ADJ -> small | good
DO -> dog
DT -> the
```

## Algorithm Idea
The algorithm needs to randomly generate a sentence from all allowable sentences stored in the CFG. This process entails starting with a root symbol (S above), and repeatedly expanding symbols until all nonterminal symbols have become one of their possible terminal symbols.

The issue is in the recursive structure of the CFG (e.g. `NP` is expandable to `ADJ NP`). Since recursive definitions are allowable, infinite expansion is possible.

- `NP` is expanded to `ADJ NP`
- `NP` in the expansion is itself expanded to `ADJ NP`
- And so on to infinity

| Nonterminal | Expansion | Current State |
| -- | -- | -- |
| `S` | `NP VP` | `NP VP` |
| `NP` | `ADJ NP` | `ADJ NP VP` |
| `ADJ` | `small` | `small NP VP` |
| `NP` | `ADJ NP` | `small good NP VP` |
| ∞ | ∞ | ∞ |

[Eli Bendersky](https://eli.thegreenplace.net/2010/01/28/generating-random-sentences-from-a-context-free-grammar) developed an algorithm ([and released the Python code into the public domain](https://eli.thegreenplace.net/pages/about)) to solve the problem by lowering each chosen expansion's future probability of being chosen again.

The idea seems like it will work for me; I am discussing my possible implementation with Dr. Nitin Agarwal.

I've summarized the algorithm's basic idea below.

## Algorithm Example Output
set p(`all rules`) = 1.0
`Sentence = S`

**Recursive Call # 1**
`S` expanded to `NP VP`
p(`S -> NP VP`) decreased
`Sentence = NP VP`

**Recursive Call # 2**
`NP` expanded to `ADJ NP`
p(NP -> ADJ NP) decreased
`Sentence = ADJ NP VP`

**Recursive Call # 3**
`ADJ` expanded to `small`
p(`ADJ -> small`) decreased
`Sentence = small NP VP`

**Recursive Call # 4**
now p(`NP -> ADJ NP`) < p(`NP -> NN`) so `NP -> NN` chosen
`NP` expanded to `NN`
p(`NP -> NN`) decreased
`Sentence = small NN VP`

**Recursive Call # 5**
`NN` expanded to `ball`
p(`NN -> ball`) decreased
`Sentence = small ball VP`

**Recursive Call # 6**
`VP` expanded to `V`
p(`VP -> V`) decreased
`Sentence = small ball V`

**Recursive Call # 7**
`V` expanded to `run`
p(`V -> run`) decreased
`Sentence = small ball run`

All symbols are terminal (base case of recursion), so all calls return.
