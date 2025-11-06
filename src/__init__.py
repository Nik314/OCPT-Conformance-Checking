import pm4py
import time
import pandas
import warnings
warnings.simplefilter(action="ignore", category=pandas.errors.SettingWithCopyWarning)
from src.interaction_properties import get_interaction_patterns
from src.divergence_free_graph import get_divergence_free_graph
from src.oc_process_trees import load_from_pt, OperatorNode
from src.identity_relation import get_extended_ocpt
from src.ocpn_conversion import convert_ocpt_to_ocpn



def df2_miner_apply(log_path,ident=False):

    try:
        input_log = pm4py.read_ocel2(log_path).relations
    except:
        input_log = pm4py.read_ocel(log_path).relations

    div, con, rel, defi = get_interaction_patterns(input_log)
    print("Interacting Properties Done")
    df2_graph = get_divergence_free_graph(input_log,div,rel)
    print("DF2 Graph Done")
    process_tree = pm4py.discover_process_tree_inductive(df2_graph, noise_threshold=0.2)
    print("Traditional Process Tree Done")
    ocpt = load_from_pt(process_tree,rel,div,con,defi)
    print("Object-Centric Process Tree Done")
    if ident:
        extended_ocpt = get_extended_ocpt(ocpt, input_log)
        print("Identity Relations Done")
        format_tree = reformat_tree(extended_ocpt)
        return format_tree
    return ocpt


def reformat_tree(eocpt):
    if isinstance(eocpt,OperatorNode) and len(eocpt.subtrees) == 1:

        ot1 = eval(" ".join(eocpt.operator.split(" With ")[0].split(" ")[1:]))
        ot2 = eval(" ".join(eocpt.operator.split(" With ")[1].split(" ")[:-1]))
        operator = eocpt.operator.split(" ")[0]

        if operator.lower() == "imp":
            pairs = [(ot1_sub, ot2_sub) for ot1_sub in ot1 for ot2_sub in ot2]
        else:
            pairs = ([(ot1_sub, ot2_sub) for ot1_sub in ot1 for ot2_sub in ot2]
                + [(ot2_sub, ot1_sub) for ot1_sub in ot1 for ot2_sub in ot2])

        result = OperatorNode(operator=pairs.pop(0), subtrees=[])
        og_node = result
        while pairs:
            result.subtrees.append(OperatorNode(operator=pairs.pop(0), subtrees=[]))
            result = result.subtrees[0]
        result.subtrees.append(reformat_tree(eocpt.subtrees[0]))
        return og_node

    elif isinstance(eocpt,OperatorNode) and len(eocpt.subtrees) > 1:
        return OperatorNode(eocpt.operator,subtrees=[reformat_tree(sub) for sub in eocpt.subtrees])
    else:
        return eocpt


