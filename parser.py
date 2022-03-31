import pyparsing as pp

from inspect import getmembers
from pprint import pprint


#https://pyparsing-docs.readthedocs.io/en/latest/HowToUsePyparsing.html#parseresults

pp.ParserElement.enable_left_recursion()


class FieldNode(object):

    def __init__(self, tokens):
        self._tokens = tokens
        self._name, self._value, *self._datum = tokens[0]

    def _get_value(self):
        if type(self._value) == bool:
            if self._value == True:
                return 'true'

            if self._value == False:
                return 'false'

        if self._value == None:
            return '<>'

        return self._value

    def __len__(self):
        print("__len__ OK")
        return len(self._tokens)

    def __getitem__(self, i):
        print("__getitem__ OK")
        return self._tokens[i]

    def __contains__(self, k):
        print("__contains__ OK")
        return k in self._tokens

    def __str__(self):
        print("__str__ OK")
        return self._value

    def __getattr__(self, name):
        print("__getattr__ OK")
        return self._value[name]

    def serialize(self):
        return ":{} {}".format(self._name, self._get_value())

class ArrayNode(object):
    def __init__(self, tokens):
        self._list = tokens[0]

    def serialize(self):
        return "({})".format(" ".join([item.serialize() for item in self._list]))

class ObjectNode(object):

    def __init__(self, tokens):
        self._type, self._properties = tokens[0]

    def __getattr__(self, name):
        #return self._properties[0]
        return self._properties.get(name)

    def serialize(self):
        return "{{{} {}}}".format(self._type, " ".join([property.serialize() for property in self._properties]))

#source = """{PLANNEDSTMT :commandType 1 :queryId 0 :hasReturning false :hasModifyingCTE false :canSetTag true :transientPlan false :dependsOnRole false :parallelModeNeeded false :jitFlags 0 :planTree {RESULT :startup_cost 0.00 :total_cost 0.01 :plan_rows 1 :plan_width 4 :parallel_aware false :parallel_safe false :async_capable false :plan_node_id 0 :targetlist ({TARGETENTRY :expr {CONST :consttype 23 :consttypmod -1 :constcollid 0 :constlen 4 :constbyval true :constisnull false :location 7 :constvalue 4 [ 1 0 0 0 0 0 0 0 ]} :resno 1 :resname ?column? :ressortgroupref 0 :resorigtbl 0 :resorigcol 0 :resjunk false}) :qual <> :lefttree <> :righttree <> :initPlan <> :extParam (b) :allParam (b) :resconstantqual <>} :rtable ({RTE :alias <> :eref {ALIAS :aliasname *RESULT* :colnames <>} :rtekind 8 :lateral false :inh false :inFromCl false :requiredPerms 0 :checkAsUser 0 :selectedCols (b) :insertedCols (b) :updatedCols (b) :extraUpdatedCols (b) :securityQuals <>}) :resultRelations <> :appendRelations <> :subplans <> :rewindPlanIDs (b) :rowMarks <> :relationOids <> :invalItems <> :paramExecTypes <> :utilityStmt <> :stmt_location 0 :stmt_len 9}"""
source1 = """{PLANNEDSTMT :commandType 1 :queryId 0}"""


def make_keyword(kwd_str, kwd_value):
    return pp.Keyword(kwd_str).setParseAction(pp.replaceWith(kwd_value))

TRUE = make_keyword("true", True)
FALSE = make_keyword("false", False)
NULL = make_keyword("<>", None)

LEFT_PARENTHESIS, RIGHT_PARENTHESIS, LEFT_BRACE, RIGHT_BRACE, LEFT_BRACKET, RIGHT_BRACKET, COLON = map(pp.Suppress, "(){}[]:")

string = pp.Word(pp.alphas+"?*")
number = pp.pyparsing_common.number()

numbers = pp.Forward()
numbers <<= numbers + number | number

node_object = pp.Forward()
node_array = pp.Forward()

node_value = (TRUE | FALSE | NULL | string | number | node_object | node_array)

node_array << pp.Group(
    LEFT_PARENTHESIS + pp.Optional(pp.delimitedList(node_value)) + RIGHT_PARENTHESIS
)

node_datum = pp.Forward()
node_datum << LEFT_BRACKET + numbers + RIGHT_BRACKET

node_field = pp.Group(
    COLON + pp.Word(pp.alphas+"_-") + node_value + pp.Optional(node_datum)
)
#node_field.setParseAction(FieldNode)

node_fields = pp.Forward()
node_fields <<= node_fields + node_field | node_field

node_object << pp.Group(
    LEFT_BRACE + pp.Word(pp.alphas) + pp.Dict(node_fields) + RIGHT_BRACE
)

result = node_object.parseString(source1)

print(result[0].queryId, type(result[0].queryId))
#result[0].queryId = 123
#print(result[0].queryId, type(result[0].queryId))

#print(result[0].serialize())

#print(result[0][1])

#print(result.dump())
#print("data keys=", list(result.keys()))
#print("data keys=", list(result.keys()))
#print("data['min']=", result["min"])
# print("sum(data['min']) =", sum(result["min"]))
# print("data.max =", result.max)
# print("sum(data.max) =", sum(result.max))
#

#node_array.setParseAction(ArrayNode)

#node_object.setParseAction(ObjectNode)
