import time
import pm4py

def determine_conformance(ocpn, relations,timeout):
    done_objects = 0
    for ot in relations["ocel:type"].unique():
        net = ocpn.nets[ot]
        log = relations[relations["ocel:type"] == ot]

        variants = pm4py.get_variants(log,activity_key="ocel:activity",timestamp_key="ocel:timestamp",case_id_key="ocel:oid")

        for variant,count in variants.items():
            sub_log = pm4py.filter_variants(log,[variant],retain=True,
                        activity_key="ocel:activity",timestamp_key="ocel:timestamp",case_id_key="ocel:oid")
            pm4py.fitness_alignments(sub_log, petri_net=net[0],initial_marking=net[1],final_marking=net[2],
                        activity_key="ocel:activity",timestamp_key="ocel:timestamp",case_id_key="ocel:oid")
            pm4py.precision_alignments(sub_log, petri_net=net[0],initial_marking=net[1],final_marking=net[2],
                        activity_key="ocel:activity",timestamp_key="ocel:timestamp",case_id_key="ocel:oid")
            done_objects += count
            if time.time() > timeout:
                break
        if time.time() > timeout:
            break

    return 1 - (done_objects / relations["ocel:oid"].nunique())



