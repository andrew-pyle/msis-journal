---
layout: post
title: "Python Programming"
date: 2018-02-22 12:40:00 -0600
categories: journal
---
This week I have succeeded in completing a test pipeline:  

↓ Python `str`  
↓ Stanford CoreNLP Shift-Reduce Parser  
↓ Python CoreNLP wrapper API  
↓ `CFG` class  
↓ `CFG.expand()`  
↓ Grammatical Sentence  
```python
('Republicans','to','want','the','popular','Tax','Cuts',',','away','because',
'of','the','Dems','want','away','take','away','.')
```
🎉 Celebrate! 🎉

## Problems
Stanford CoreNLP outputs the constituency parse as a string, which creates some limitations for this project.

### CoreNLP Output
Parsing of the string is not simple. I have not found a way to obtain a structured output from CoreNLP, so a new algorithm would be needed to load the defined rules into our Python data types.
```python
"(ROOT
  (S
    (NP (DT The) (JJ quick) (JJ brown) (NN fox))
    (VP (VBD jumped)
      (PP (IN over)
        (NP (DT the) (JJ lazy) (NN dog))))
    (. .)))"
```
NLTK has a function to import this type of string structure: `Tree.fromstring()`, so for now, the project will use NLTK's method and add a hack to transfer the data to the project's custom (read: lightweight) `CFG` class.
```python
# Hack #1
list_o_rules = [tuple(str(rule).replace("'", '').split(' -> ')) for
                    rule in nltk.Tree.productions()]
```

### Nonterminal Class Needed
This hack removes the NLTK distinction between terminal and nonterminal symbols. In the project's `CFG` class, I made the assumption that this lack of distinction would not be a problem. It is. CoreNLP sometimes defines a nonterminal character as the exact same terminal character. For example, `.` can be the symbol for a punctuation nonterminal.
```python
"(. .)"
"(. !)"
"(. ?)"
```
Now there is infinite expansion because `expand()` relies on hitting a terminal symbol to return a result. It interprets `.` the terminal as `.` the nonterminal, and recurses forever. So we get another hack. Hack #1 can be adjusted to retain NLTK's `Nonterminal` class on nonterminal symbols.
```python
# Hack #2
list_o_rules = [(rule.lhs(), rule.rhs()) for rule in nltk.Tree.productions()]
```
Now, nonterminal rules have their own class and terminal symbols are `str`.
```python
rules = {Nonterminal(.) : '.'}
rhs_symbol = '.' # type(.) == Nonterminal
rhs_symbol in rules # False  
```

`expand()` no longer thinks `.` terminal is the same as `Nonterminal(.)` in the rules list. Hack #2 is successful for now.
