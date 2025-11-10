import copy
import time

import pm4py
from joblib import Parallel, delayed



from src.interaction_properties import get_interaction_patterns
from src.identity_relation import check_relation_log
from multiprocessing import Pool

def get_log_abstraction(relations):

    timestats = {}
    start = time.time()
    div,con,rel,defi = get_interaction_patterns(relations)
    opt = {a:[ot for ot in rel[a] if relations[relations["ocel:type"]==ot]["ocel:oid"].nunique()
        > relations[(relations["ocel:type"]==ot) & (relations["ocel:activity"]==a)]["ocel:oid"].nunique()] for a in relations["ocel:activity"].unique()}
    timestats["Multiplicity"] = time.time() -start
    start = time.time()
    dfgs = {ot:pm4py.discover_dfg(relations[relations["ocel:type"] == ot],
        activity_key="ocel:activity",timestamp_key="ocel:timestamp",case_id_key="ocel:oid")   for ot in relations["ocel:type"].unique()}
    timestats["Control"] = time.time()-start
    start = time.time()
    types = relations["ocel:type"].unique()
    results = Parallel(n_jobs=-2, backend="loky")(
        delayed(check_relation_log)(
            ot1, ot2, relations[relations["ocel:type"].isin([ot1, ot2])]
        )
        for ot1 in types for ot2 in types if ot1 != ot2
    )
    ident = set(sum(results,[]))
    timestats["Identity"] = time.time()-start
    return (dfgs,rel,div,con,defi,opt,ident), timestats