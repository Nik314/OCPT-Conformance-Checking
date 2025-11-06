import time

import pm4py

from src.interaction_properties import get_interaction_patterns
from src.identity_relation import check_relation_log


def get_log_abstraction(relations):

    timestats = {}
    start = time.time()
    div,con,rel,defi = get_interaction_patterns(relations)
    opt = {a:[ot for ot in rel[a] if relations[relations["ocel:type"]==ot]["ocel:oid"].nunique()
        > relations[(relations["ocel:type"]==ot) & (relations["ocel:activity"]==a)]["ocel:oid"].nunique()] for a in relations["ocel:activity"].unique()}
    print("Interaction Multiplicity Patterns Log Done")
    timestats["Multiplicity"] = time.time() -start
    start = time.time()
    dfgs = {ot:pm4py.discover_dfg(relations[relations["ocel:type"] == ot],
        activity_key="ocel:activity",timestamp_key="ocel:timestamp",case_id_key="ocel:oid")   for ot in relations["ocel:type"].unique()}
    print("Control Flow Patterns Log Done")
    timestats["Control"] = time.time()-start
    start = time.time()
    ident = set()
    types = relations["ocel:type"].unique()
    for a in rel.keys():
        for b in rel.keys():
            for ot1 in types:
                for ot2 in types:
                    if a != b and ot1 != ot2 and check_relation_log(ot1,ot2,a,b,relations):
                        ident.add((ot1,ot2,a,b))

    print("Identity Relation Patterns Log Done")
    timestats["Identity"] = time.time()-start
    return (dfgs,rel,div,con,defi,opt,ident), timestats