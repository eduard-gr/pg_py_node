
# Create a Grammar Class to define your language
from pyleri import Grammar, Regex, Keyword, Sequence

# Returns properties of a node object as a dictionary:
def node_props(node, children):
    return {
        'start': node.start,
        'end': node.end,
        'name': node.element.name if hasattr(node.element, 'name') else None,
        'element': node.element.__class__.__name__,
        'string': node.string,
        'children': children}


# Recursive method to get the children of a node object:
def get_children(children):
    return [node_props(c, get_children(c.children)) for c in children]


# View the parse tree:
def view_parse_tree(res):
    start = res.tree.children[0] \
        if res.tree.children else res.tree
    return node_props(start, get_children(start.children))

class MyGrammar(Grammar):
    r_name = Regex('(?:"(?:[^"]*)")+')
    k_hi = Keyword('hi')
    START = Sequence(k_hi, r_name)

# Compile your grammar by creating an instance of the Grammar Class.
my_grammar = MyGrammar()

# Use the compiled grammar to parse 'strings'
print(view_parse_tree(my_grammar.parse('hi "Iris"'))) # => True
#print(my_grammar.parse('bye "Iris"').is_valid) # => False
#print(my_grammar.parse('bye "Iris"').as_str()) # => error at position 0, expecting: hi