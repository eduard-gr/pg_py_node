import pyparsing as pp

class FieldNode(pp.ParseResults):
    def __init__(self, tokens):
        super().__init__(tokens)

    def test(self):
        return "OK"

ident = pp.Word(pp.alphas)
num = pp.Word(pp.nums)

term = ident | num

LEFT_PARENTHESIS, RIGHT_PARENTHESIS, LEFT_BRACE, RIGHT_BRACE, LEFT_BRACKET, RIGHT_BRACKET, COLON = map(pp.Suppress, "(){}[]:")

expr = pp.Group(COLON + ident + term)


func = pp.Dict(LEFT_BRACE + expr + RIGHT_BRACE)
func.setResultsName("blabl")
#func.setParseAction(FieldNode)

res = func.parse_string("{:fn 123}")

#print(res.dump())
print(res.dump())
print(res.getName())
#print(res.asDict())
#print(res['fn'])