import copy
import random


def expand(symbol, rules, alpha=0.25):
    """
    Initialize a dict which will contain weights for each production used at
    each level of recursion. rule_weights is passed by shallow copy between 
    levels of recursion to avoid mutating an upper level's weights.

    Args:
        symbol (str): The symbol from which to begin expansion. Must be 
        contained in rules

        rules (dict): Nonterminal symbols and their expansion possibilities
            key: str
            value: list of tuples

            ex. rules = {
                    'S': [('S', 'NP'),       # Possible expansions
                          ('S', 'S', 'VP'),  # ...
                          ('NP', 'VP')],     # ...
                    'NP': [...],
                    ...}
        
        alpha (float): Penalization parameter for repeated expansions. Alpha 
            is multiplied by the previous probability of a chosen expansion, so 
            probability of repeated expansion decreases as value decreases. 
                
                P = alpha ** N

                where P is probability of expansion being chosen
                      N is number of times the rule has been expanded in the 
                        current depth-first traversal.
                      0 < alpha < 1.0
    
    Returns:
        tuple of str: A grammatical sentence according to CFG
    """

    # Initialize dict values to 1.0
    rule_weights = {}

    def recurse(symbol, rule_weights):
        sentence = ()

        # Initialize nonterminal expansion weights
        if symbol not in rule_weights:
            rule_weights[symbol] = [1.0,] * len(rules[symbol])
        # else, they're already set in an upper recursion level

        random_expansion = random.choices(population=rules[symbol], 
                                          weights=rule_weights[symbol],
                                          k=1)[0]  # NOTE 
                                                   # Assumes len(list) == 1
        
        # Decrease future probability of chosen rule
        # NOTE Assumes only one match of random_expansion in rules[symbol]
        rule_weights[symbol][rules[symbol].index(random_expansion)] *= alpha  

        for rhs_symbol in random_expansion:
            if rhs_symbol in rules:  # nonterminal symbol
                sentence += recurse(rhs_symbol, copy.copy(rule_weights))

            else:  # terminal symbol
                sentence += (rhs_symbol,)

        return sentence

    return recurse(symbol, rule_weights)   
