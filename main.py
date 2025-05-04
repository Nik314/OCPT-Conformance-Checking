import os
import pandas
import pm4py
import time
import liss.localocpa.objects.log.importer.ocel.factory as factory
from src import df2_miner_apply, convert_ocpt_to_ocpn
from liss.main import *

result = pandas.DataFrame(columns=["Log", "Runtime","Sync", "Imp (Ordered)", "Imp (Concurrent)"])

for file_name in os.listdir("data"):
    print(file_name)
    ocpt = df2_miner_apply("data/"+file_name)
    ocpn = convert_ocpt_to_ocpn(ocpt)
    print("Model Mined & Translated")
    budget = 120


    try:
        log = pm4py.read_ocel2("data/"+file_name).relations
    except:
        log = pm4py.read_ocel("data/"+file_name).relations


    from park.conformance import determine_conformance
    start = time.time()
    timeouts = determine_conformance(ocpn,log,(start+budget))
    runtime_park = min(time.time() -start,budget)
    timeout_park = timeouts
    print("Perspective-Based Done In "+str(runtime_park) +" Seconds With Timeout On " +str(timeout_park) +" Of Events")

    from adams.conformance import determine_conformance
    start = time.time()
    timeouts = determine_conformance(ocpn,log,(start+budget))
    runtime_adams = min(time.time() -start,budget)
    timeout_adams = timeouts
    print("Context-Based Done In "+str(runtime_adams) +" Seconds With Timeout On " +str(timeout_adams) +" Of Events")


    continue
    defacto_ocel = factory.apply("data/"+file_name)
    t = timeit.Timer(lambda:  calculate_oc_alignments(defacto_ocel, dejure_ocpn))

#result.to_csv("results.csv")


