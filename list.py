import pyparsing as pp
pp.ParserElement.enable_left_recursion()


class VariableNode(object):
    def __init__(self, tokens):
        self._tokens = tokens
        self._name, self._value = self._tokens[0]

    def getName(self):
        return self._name

    def getValue(self):
        return self._value

    def __repr__(self):
        return ":{} {}".format(self.getName(), self.getValue())


def make_keyword(kwd_str, kwd_value):
    return pp.Keyword(kwd_str).setParseAction(pp.replaceWith(kwd_value))

TRUE = make_keyword("true", True)
FALSE = make_keyword("false", False)
NULL = make_keyword("<>", None)

LEFT_BRACKET, RIGHT_BRACKET, LEFT_BRACE, RIGHT_BRACE, COLON, SPACE = map(pp.Suppress, "(){}: ")


pg_string = pp.dblQuotedString().setParseAction(pp.removeQuotes)
pg_number = pp.pyparsing_common.number().setName("pg_number")
pg_object = pp.Forward().setName("pg_object")

pg_value = pp.Forward().setName("pg_value")
pg_value << (pg_string | pg_number | pg_object | TRUE | FALSE | NULL)

pg_variable = pp.Forward().setName("pg_variable")
pg_variable << pp.Group(
    COLON + pp.Word(pp.alphas) + pg_value
)
pg_variable.addParseAction(VariableNode)

result = pg_variable.parseString(""":commandType 1""")
print(result.dump())
print(result[0])

pg_variable_list = pp.Forward()
pg_variable_list <<= pg_variable_list + pg_variable | pg_variable
#print(pg_variable_list.parseString(""":commandType 1 :queryId 0 :hasReturning false :hasModifyingCTE false""").dump())

pg_object << LEFT_BRACE + pp.Word(pp.alphas) + pp.Group(pg_variable_list) + RIGHT_BRACE

#print(pg_object.parseString("""{PLANNEDSTMT :commandType 1 :hasModifyingCTE {PLANNEDSTMT :commandType 1 }}""").dump())
#print(pg_object.parseString("""{PLANNEDSTMT :commandType 1 :hasModifyingCTE {PLANNEDSTMT :commandType 1 }}""").asDict())

