import pandas
import datetime
from src.log_abstraction import get_log_abstraction
from src.oc_process_trees import OperatorNode,LeafNode,Operator
from src.tree_abstraction import get_tree_abstraction
from src.conformance import determine_conformance


#construct example event log from the paper
relations = pandas.DataFrame(columns=["ocel:timestamp","ocel:eid","ocel:activity","ocel:oid","ocel:type"])
events = [("place",["c_1","o_1","i_1","i_2"]), ("pack",["o_1","i_2","e_1"]),
          ("place",["c_1","o_2","i_3","i_4"]), ("pay",["c_1","o_1","i_1","i_2"]),
          ("pickup",["c_1","o_1","i_2","e_1"]), ("pay",["c_1","o_2","i_3","i_4"]),
          ("pack",["o_1","o_2","i_1","i_3","e_1"]), ("place",["c_1","o_3","i_5"]),
          ("pack",["o_2","i_4","e_1","e_2"]), ("pickup",["c_1","o_2","i_4","e_1"]),
          ("pay",["c_1","o_3","i_5"]), ("pack",["o_3","i_5","e_1"]),
          ("pickup",["c_1","o_1","o_2","i_1","i_3"]), ("refund",["o_3","i_5","e_1"])]


timestamp = datetime.datetime.now()
for i in range(len(events)):
    activity = events[i][0]
    for object in events[i][1]:
        relations.loc[relations.shape[0]] = (timestamp + i*datetime.timedelta(seconds=i)), i, activity, object.split("_")[1], object.split("_")[0]
print(relations)



#construct example process tree from the paper
place = LeafNode(activity="place",related={"c","o","i"},divergent={"c"},convergent={"i"},deficient=set())
pay = LeafNode(activity="pay",related={"c","o","i"},divergent={"c"},convergent={"i"},deficient=set())
pack = LeafNode(activity="pack",related={"o","i","e"},divergent={"o","e"},convergent={"i"},deficient=set())
refund = LeafNode(activity="refund",related={"o","i","e"},divergent={"o","e"},convergent={"i"},deficient=set())
pickup = LeafNode(activity="pickup",related={"c","o","i","e"},divergent={"c","e"},convergent={"i"},deficient={"e"})

ocpt = OperatorNode(Operator.SEQUENCE,[
    place,
    OperatorNode(Operator.PARALLEL,[pay,pack]),
    OperatorNode(Operator.XOR,[refund,pickup])
])


print(str(ocpt))

dfgs,rel,div,con,defi,opt = get_log_abstraction(relations)
print(rel)
print(div)
print(con)
print(defi)
print(opt)


dfgs,rel,div,con,defi,opt = get_tree_abstraction(ocpt)
print(rel)
print(div)
print(con)
print(defi)
print(opt)


print(determine_conformance(ocpt,relations,10))


