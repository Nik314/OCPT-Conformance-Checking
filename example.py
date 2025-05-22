import pandas
import datetime

import pm4py

from src.log_abstraction import get_log_abstraction
from src.oc_process_trees import OperatorNode,LeafNode,Operator
from src.tree_abstraction import get_tree_abstraction
from src.conformance import determine_conformance


#construct example event log from the paper
relations = pandas.DataFrame(columns=["ocel:timestamp","ocel:eid","ocel:activity","ocel:oid","ocel:type"])
events = [("place",["c_11","o_21","i_31","i_32"]), ("pack",["o_21","i_32","e_41"]),
          ("place",["c_11","o_22","i_33","i_34"]), ("pay",["c_11","o_21","i_31","i_32"]),
          ("pickup",["c_11","o_21","i_32","e_41"]), ("pay",["c_11","o_22","i_33","i_34"]),
          ("pack",["o_21","o_22","i_31","i_33","e_41"]), ("place",["c_11","o_23","i_35"]),
          ("pack",["o_22","i_34","e_41","e_42"]), ("pickup",["c_11","o_22","i_34","e_41"]),
          ("pay",["c_11","o_23","i_35"]), ("pack",["o_23","i_35","e_41"]),
          ("pickup",["c_11","o_21","o_22","i_31","i_33"]), ("refund",["o_23","i_35","e_41"])]


timestamp = datetime.datetime.now()
for i in range(len(events)):
    activity = events[i][0]
    for object in events[i][1]:
        relations.loc[relations.shape[0]] = (timestamp + i*datetime.timedelta(seconds=i)), i, activity, object.split("_")[1], object.split("_")[0]



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


print("Log Abstraction")
dfgs,rel,div,con,defi,opt = get_log_abstraction(relations)
print(rel)
print(div)
print(con)
print(defi)
print(opt)
for dfg in dfgs.values():
    pm4py.view_dfg(*dfg)

print("Tree Abstraction")
dfgs,rel,div,con,defi,opt = get_tree_abstraction(ocpt)
print(rel)
print(div)
print(con)
print(defi)
print(opt)
for dfg in dfgs.values():
    pm4py.view_dfg(*dfg)


print(determine_conformance(ocpt,relations,10))


