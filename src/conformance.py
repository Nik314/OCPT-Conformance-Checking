import numpy
from src.log_abstraction import get_log_abstraction
from src.tree_abstraction import get_tree_abstraction
import time

def determine_conformance(ocpt, relations,timeout):

    tree_abstraction,timestat_tree = get_tree_abstraction(ocpt)
    log_abstraction,timestats_log = get_log_abstraction(relations)
    start = time.time()
    fit = get_fitness(log_abstraction,tree_abstraction)
    pre = get_precision(log_abstraction,tree_abstraction)
    end = time.time() - start
    print(fit)
    print(pre)

    total = {key:value+timestat_tree[key] for key,value in timestats_log.items()}
    total["Overhead"] = end
    total = {key:value/sum(total.values()) for key,value in total.items()}
    return 0.0,total



def get_patterns(log_abstraction,tree_abstraction):
    log_dfgs,log_rel,log_div,log_con,log_defi,log_opt,log_ident = log_abstraction
    tree_dfgs,tree_rel,tree_div,tree_con,tree_defi,tree_opt,tree_ident = tree_abstraction
    total_activities = list(log_rel.keys()) + list(tree_rel.keys())

    alphabet = set([a for a in log_rel.keys()] + [a for a in tree_rel.keys()])
    object_types = set([ot for ot in log_dfgs.keys()] +  [ot for ot in tree_dfgs.keys()])

    control_patterns_log = [ot in log_dfgs.keys() and (a,b) in log_dfgs[ot][0].keys() and log_dfgs[ot][0][(a,b)]> 0
                for a in alphabet for b in alphabet for ot in object_types]
    control_patterns_log += [ot in log_dfgs and a in log_dfgs[ot][1] and log_dfgs[ot][1][a]
                for a in alphabet for ot in object_types]
    control_patterns_log += [ot in log_dfgs and a in log_dfgs[ot][2] and log_dfgs[ot][2][a]
                for a in alphabet for ot in object_types]

    control_patterns_tree = [ot in tree_dfgs.keys() and (a,b) in tree_dfgs[ot][0].keys() and tree_dfgs[ot][0][(a,b)]> 0
                for a in alphabet for b in alphabet for ot in object_types]
    control_patterns_tree += [ot in tree_dfgs and a in tree_dfgs[ot][1] and tree_dfgs[ot][1][a]
                for a in alphabet for ot in object_types]
    control_patterns_tree += [ot in tree_dfgs and a in tree_dfgs[ot][2] and tree_dfgs[ot][2][a]
                for a in alphabet for ot in object_types]

    multiplicity_patterns_log = [a in (log_rel,log_div,log_defi,log_con,log_opt)[i] and
            ot in (log_rel,log_div,log_defi,log_con,log_opt)[i][a]
            for a in total_activities for ot in object_types for i in range(0,5)]

    identity_patterns_log = [not (ot1,ot2,a,b) in log_ident for a in total_activities
            for b in total_activities for ot1 in object_types for ot2 in object_types if a!=b and ot1 != ot2
            and ((a in log_rel.keys() and b in log_rel.keys() and ot1 in log_rel[a] and ot2 in log_rel[a]
                 and ot1 in log_rel[b] and ot2 in log_rel[b]) or
                             (a in tree_rel.keys() and ot1 in tree_rel[a] and ot2 in tree_rel[
                                 a] and b in tree_rel.keys()
                              and ot1 in tree_rel[b] and ot2 in tree_rel[b]))]

    multiplicity_patterns_tree = [a in (tree_rel,tree_div,tree_defi,tree_con,tree_opt)[i] and
            ot in (tree_rel,tree_div,tree_defi,tree_con,tree_opt)[i][a]
            for a in total_activities for ot in object_types for i in range(0,5)]

    identity_patterns_tree = [not (ot1,ot2,a,b) in tree_ident for a in total_activities
            for b in total_activities for ot1 in object_types for ot2 in object_types if a!=b and ot1 != ot2
                 and ((a in log_rel.keys() and b in log_rel.keys() and ot1 in log_rel[a] and ot2 in log_rel[a]
                       and ot1 in log_rel[b] and ot2 in log_rel[b]) or
                      (a in tree_rel.keys() and ot1 in tree_rel[a] and ot2 in tree_rel[
                          a] and b in tree_rel.keys()
                       and ot1 in tree_rel[b] and ot2 in tree_rel[b]))]

    return ((control_patterns_log,multiplicity_patterns_log,identity_patterns_log),
            (control_patterns_tree,multiplicity_patterns_tree,identity_patterns_tree))





def get_fitness(log_abstraction, tree_abstraction):

    pattern_value_log, pattern_value_tree = get_patterns(log_abstraction,tree_abstraction)
    result = []
    for i in range(len(pattern_value_log)):
        total, fitting = 0, 0
        log_value = pattern_value_log[i]
        tree_value = pattern_value_tree[i]
        for j in range(len(log_value)):
            if log_value[j]:
                total += 1
            if log_value[j] and tree_value[j]:
                fitting += 1
        result.append(fitting/total if total else 1.0)
    return result

def get_precision(log_abstraction, tree_abstraction):

    pattern_value_log, pattern_value_tree = get_patterns(log_abstraction,tree_abstraction)
    result = []
    for i in range(len(pattern_value_log)):
        total, precise = 0, 0
        log_value = pattern_value_log[i]
        tree_value = pattern_value_tree[i]
        for j in range(len(log_value)):
            if tree_value[j]:
                total += 1
            if log_value[j] and tree_value[j]:
                precise += 1
        result.append(precise/total if total else 1.0)
    return result