import pandas
import datetime

import pm4py

from src.log_abstraction import get_log_abstraction
from src.oc_process_trees import OperatorNode,LeafNode,Operator
from src.tree_abstraction import get_tree_abstraction
from src.conformance import determine_conformance


#construct example event log from the paper
relations = pandas.DataFrame(columns=["ocel:timestamp","ocel:eid","ocel:activity","ocel:oid","ocel:type"])
events = [("place",["c_11","o_21","i_31","i_32"]),
          ("pay",["c_11","o_21","i_31","i_32"]),
          ("pack",["i_31"]),
          ("place",["c_11","o_22","i_33"]),
          ("pack",["o_21","o_22","i_32","i_33"]),
          ("pay",["c_11","o_22","i_33"]),
          ("pickup",["c_11","o_21","o_22","i_32","i_33"]),
          ("refund",["c_11","o_21","i_31"])]


timestamp = datetime.datetime.now()
for i in range(len(events)):
    activity = events[i][0]
    for object in events[i][1]:
        relations.loc[relations.shape[0]] = (timestamp + i*datetime.timedelta(seconds=i)), i, activity, object.split("_")[1], object.split("_")[0]



#construct example process tree from the paper
place = LeafNode(activity="place",related={"c","o","i"},divergent={"c"},convergent={"i"},deficient=set())
pay = LeafNode(activity="pay",related={"c","o","i"},divergent={"c"},convergent={"i"},deficient=set())
pack = LeafNode(activity="pack",related={"o","i"},divergent=set(),convergent={"i"},deficient=set())
refund = LeafNode(activity="refund",related={"c","o","i"},divergent={"c"},convergent={"i"},deficient=set())
pickup = LeafNode(activity="pickup",related={"c","o","i"},divergent={"c"},convergent={"i"},deficient=set())

ocpt = OperatorNode(Operator.SEQUENCE,[
    place,
    OperatorNode(Operator.PARALLEL,[pay,pack]),
    OperatorNode(Operator.XOR,[refund,pickup])
])

#determine_conformance(OperatorNode(Operator.PARALLEL,[pay,pack]),relations[relations["ocel:activity"].isin(["pay","pack"])],10)
#determine_conformance(OperatorNode(Operator.XOR,[pickup,refund]),relations[relations["ocel:activity"].isin(["pickup","refund"])],10)
timeout,stats = determine_conformance(ocpt,relations,10)
print(stats)






