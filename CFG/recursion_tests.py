"""
Test harness for recursion.py

For each alpha value between 0.01 and 0.90 with a step of 0.01, gives the
average length of 100 sentences for each alpha value.

Uses the test grammar defined in rules.

For generation of graph: average sentence length vs. alpha
"""
import recursion

rules = {
    'S': [
        ('S', 'NP'),       # recursive
        ('S', 'S', 'VP'),  # recursive
        ('NP', 'VP'),      # non-recursive
    ],
    'NP': [
        ('NN',),          # non-recursive
        ('ADJ', 'NP'),    # recursive
        ('blue', 'NP'),   # recursive
        ('green', 'NP'),  # recursive
    ],
    'VP': [('V',)],  # non-recursive
    'NN': [('I',)],  # non-recursive
    'V': [('am',)]   # non-recursive
}

symbol = 'S'

# alpha 0.0 -> 0.90 step == 0.01
for a in range(1, 100):
    sentence_lengths = []

    # Average of 100 runs
    for x in range(100):
        sentence_lengths.append(
            len(recursion.expand(symbol, rules, alpha=a/100)))

    # Write average of 100 runs to file
    with open('avg_sentence_length.txt', mode='a', encoding='utf-8') as f:
        f.write(str(sum(sentence_lengths) / len(sentence_lengths)) + '\n')
