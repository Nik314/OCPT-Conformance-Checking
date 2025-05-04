import os
import pandas
import pm4py
import time
import liss.localocpa.objects.log.importer.ocel.factory as factory
from src import df2_miner_apply, convert_ocpt_to_ocpn
from liss.main import *

result = pandas.DataFrame(columns=["Log", "align_time","align_percent","context_time","context_percent",
                "perspective_time","perspective_percent","abstraction_time"])

for file_name in os.listdir("data"):

    print(file_name)
    ocpt = df2_miner_apply("data/"+file_name)
    ocpn = convert_ocpt_to_ocpn(ocpt)
    print("Model Mined & Translated")
    budget = 3600


    try:
        log = pm4py.read_ocel2("data/"+file_name)
    except:
        log = pm4py.read_ocel("data/"+file_name)

    from src.conformance import determine_conformance
    start = time.time()
    timeouts = determine_conformance(ocpt,log.relations,(start+budget))
    runtime_me = min(time.time() -start,budget)
    timeout_me = timeouts
    print("Abstraction-Based Done In "+str(runtime_me) +" Seconds With Timeout On " +str(timeout_me) +" Of Events")



    pm4py.write_ocel_json(log,"temp/"+file_name.split(".")[0] +".jsonocel")
    defacto_ocel = factory.apply("temp/"+file_name.split(".")[0] +".jsonocel")
    start = time.time()
    timeouts = calculate_oc_alignments(defacto_ocel, ocpn,start+budget)
    runtime_liss = min(time.time() -start,budget)
    timeout_liss = timeouts
    print("Perspective-Based Done In "+str(runtime_liss) +" Seconds With Timeout On " +str(timeout_liss) +" Of Executions")


    from park.conformance import determine_conformance
    start = time.time()
    timeouts = determine_conformance(ocpn,log.relations,(start+budget))
    runtime_park = min(time.time() -start,budget)
    timeout_park = timeouts
    print("Perspective-Based Done In "+str(runtime_park) +" Seconds With Timeout On " +str(timeout_park) +" Of Events")

    from adams.conformance import determine_conformance
    start = time.time()
    timeouts = determine_conformance(ocpn,log.relations,(start+budget))
    runtime_adams = min(time.time() -start,budget)
    timeout_adams = timeouts
    print("Context-Based Done In "+str(runtime_adams) +" Seconds With Timeout On " +str(timeout_adams) +" Of Events")


    continue

#result.to_csv("results.csv")


