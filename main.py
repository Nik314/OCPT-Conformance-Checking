import os
import pandas
import pm4py
import time
import numpy
from src.log_abstraction import get_log_abstraction
from src.tree_abstraction import get_tree_abstraction
from src.conformance import get_fitness, get_precision
from pm4py.algo.transformation.log_to_features.variants.trace_based import times_from_first_occurrence_activity_case

import liss.localocpa.objects.log.importer.ocel.factory as factory
from src import df2_miner_apply, convert_ocpt_to_ocpn
from liss.main import *




def compare_values():
    result = pandas.DataFrame(columns=["log", "Fit Abstraction", "Fit Perspective", "Prec Abstraction", "PRec Perspective"])
    for file_name in os.listdir("data"):
        if "08" in file_name:
            continue
        print(file_name)
        ocpt = df2_miner_apply("data/" + file_name)
        ocpn = convert_ocpt_to_ocpn(ocpt)
        print("Model Mined & Translated")

        try:
            log = pm4py.read_ocel2("data/" + file_name)
        except:
            log = pm4py.read_ocel("data/" + file_name)

        log_abstraction = get_log_abstraction(log.relations)
        tree_abstraction = get_tree_abstraction(ocpt)
        fit_abstract = get_fitness(log_abstraction, tree_abstraction)
        prec_abstract = get_precision(log_abstraction, tree_abstraction)

        fit_perspective, prec_perspective = [],[]
        for ot in log.relations["ocel:type"].unique():
            net = ocpn.nets[ot]
            sub_log = log.relations[log.relations["ocel:type"] == ot]

            fit_perspective.append(pm4py.fitness_alignments(sub_log, petri_net=net[0], initial_marking=net[1], final_marking=net[2],
                                     activity_key="ocel:activity", timestamp_key="ocel:timestamp",
                                     case_id_key="ocel:oid")["averageFitness"])

            prec_perspective.append(pm4py.precision_alignments(sub_log, petri_net=net[0], initial_marking=net[1], final_marking=net[2],
                                       activity_key="ocel:activity", timestamp_key="ocel:timestamp",
                                       case_id_key="ocel:oid"))


        result.loc[result.shape[0]] = file_name, fit_abstract, numpy.mean(fit_perspective), prec_abstract, numpy.mean(prec_perspective)
        result.to_csv("comparison.csv")



def run_abstractions(budget):
    result = pandas.DataFrame(columns=["log", "time","percentage"])
    for file_name in os.listdir("data"):

        print(file_name)
        ocpt = df2_miner_apply("data/"+file_name)
        ocpn = convert_ocpt_to_ocpn(ocpt)
        print("Model Mined & Translated")

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
        result.loc[result.shape[0]] = file_name,runtime_me,timeout_me
    result.to_csv("result_abstraction.csv")


def run_perspective(budget):

    result = pandas.DataFrame(columns=["log", "time", "percentage"])
    for file_name in os.listdir("data"):

        print(file_name)
        ocpt = df2_miner_apply("data/" + file_name)
        ocpn = convert_ocpt_to_ocpn(ocpt)
        print("Model Mined & Translated")

        try:
            log = pm4py.read_ocel2("data/" + file_name)
        except:
            log = pm4py.read_ocel("data/" + file_name)

        from park.conformance import determine_conformance
        start = time.time()
        timeouts = determine_conformance(ocpn,log.relations,(start+budget))
        runtime_park = min(time.time() -start,budget)
        timeout_park = timeouts
        print("Perspective-Based Done In "+str(runtime_park) +" Seconds With Timeout On " +str(timeout_park) +" Of Objects")
        result.loc[result.shape[0]] = file_name,runtime_park,timeout_park
    result.to_csv("result_perspective.csv")



def run_context(budget):

    result = pandas.DataFrame(columns=["log", "time", "percentage"])
    for file_name in os.listdir("data"):

        print(file_name)
        ocpt = df2_miner_apply("data/" + file_name)
        ocpn = convert_ocpt_to_ocpn(ocpt)
        print("Model Mined & Translated")

        try:
            log = pm4py.read_ocel2("data/" + file_name)
        except:
            log = pm4py.read_ocel("data/" + file_name)

        from adams.conformance import determine_conformance
        start = time.time()
        timeouts = determine_conformance(ocpn,log.relations,(start+budget))
        runtime_adams = min(time.time() -start,budget)
        timeout_adams = timeouts
        print("Context-Based Done In "+str(runtime_adams) +" Seconds With Timeout On " +str(timeout_adams) +" Of Events")
        result.loc[result.shape[0]] = file_name,runtime_adams,timeout_adams
    result.to_csv("result_context.csv")




def run_alignment(budget):

    result = pandas.DataFrame(columns=["log", "time", "percentage"])
    for file_name in os.listdir("data"):

        print(file_name)
        ocpt = df2_miner_apply("data/" + file_name)
        ocpn = convert_ocpt_to_ocpn(ocpt)
        print("Model Mined & Translated")

        try:
            log = pm4py.read_ocel2("data/" + file_name)
        except:
            log = pm4py.read_ocel("data/" + file_name)

        pm4py.write_ocel_json(log,"temp/"+file_name.split(".")[0] +".jsonocel")
        defacto_ocel = factory.apply("temp/"+file_name.split(".")[0] +".jsonocel")
        start = time.time()
        timeouts = calculate_oc_alignments(defacto_ocel, ocpn,start+budget)
        runtime_liss = min(time.time() -start,budget)
        timeout_liss = timeouts
        print("Alignment-Based Done In "+str(runtime_liss) +" Seconds With Timeout On " +str(timeout_liss) +" Of Executions")
        result.loc[result.shape[0]] = file_name,runtime_liss,timeout_liss
        result.to_csv("result_alignment.csv")


budget = 3600
#run_abstractions(budget)
#run_perspective(budget)
#run_context(budget)
#run_alignment(budget)
compare_values()


