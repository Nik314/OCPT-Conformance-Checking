import hashlib
import time
from src.oc_process_trees import LeafNode,OperatorNode
import hashlib
import fast_hash
import pandas


def check_relation_log(ot1, ot2, relations):

    activities = relations["ocel:activity"].unique()
    result = []
    activity_groups = {act: relations[relations["ocel:activity"] == act] for act in activities}

    for a in activities:
        for b in activities:
            if a == b:
                continue
            subrelations = pandas.concat([activity_groups[a], activity_groups[b]], ignore_index=True)
            #hash_map = relations.groupby("ocel:eid").apply(lambda frame:
            #    int(hashlib.md5(str(sorted(frame["ocel:oid"].unique())).encode("utf_8")).hexdigest(), 16)).to_dict()
            hash_map = fast_hash.compute_hash_map(subrelations["ocel:eid"].values,
                                                  subrelations["ocel:oid"].values)
            subrelations["hash"] = subrelations["ocel:eid"].map(hash_map)

            grouped_hash_counts = subrelations.groupby("ocel:oid")["hash"].nunique()
            check1 = grouped_hash_counts.max() == 1
            grouped_ot1 = subrelations.loc[subrelations["ocel:type"] == ot1].groupby("ocel:oid")["hash"].nunique()
            check2 = grouped_ot1.max() == 1
            check = check1 or check2
            #check = subrelations.groupby("ocel:oid").nunique()["hash"].max() == 1 or \
            #    subrelations[subrelations["ocel:type"].isin([ot1])].groupby("ocel:oid").nunique()["hash"].max() == 1
            if check:
                result.append((ot1,ot2,a,b))
    return result



def check_relation(ot1, ot2, relations):

    #hash_map = relations.groupby("ocel:eid").apply(lambda frame:
    #    int(hashlib.md5(str(sorted(list(frame["ocel:oid"].unique()))).encode("utf_8")).hexdigest(), 16)).to_dict()
    hash_map = fast_hash.compute_hash_map(relations["ocel:eid"].values,
                                          relations["ocel:oid"].values)

    relations["hash"] = relations["ocel:eid"].apply(lambda eid: hash_map[eid])

    if relations.groupby("ocel:oid").nunique()["hash"].max() == 1:
        return "Sync " + str(ot1) + " With " + str(ot2) +" (Full)"


    if relations[relations["ocel:type"].isin(ot1)].groupby("ocel:oid").nunique()["hash"].max() > 1:
        return None

    ot1_hash_map = relations[relations["ocel:type"].isin(ot1)].groupby("ocel:eid").apply(lambda frame:
         int(hashlib.md5(str(sorted(list(frame["ocel:oid"].unique()))).encode("utf_8")).hexdigest(), 16)).to_dict()

    relations["ot1 hash"] = relations["ocel:eid"].apply(lambda eid: ot1_hash_map[eid] if eid in ot1_hash_map else
        int(hashlib.md5(str([]).encode("utf_8")).hexdigest(), 16))
    hash_groups = relations.groupby("ot1 hash").apply(lambda frame:frame["hash"].unique()).to_dict().values()
    hash_groups = [group for group in hash_groups if len(group) > 1]

    for group in hash_groups:
        sub_relations = relations[relations["hash"].isin(group)]
        time_frames = sub_relations.groupby("hash").apply(lambda frame:(frame["ocel:timestamp"].iloc[0],frame["ocel:timestamp"].iloc[-1])).to_dict().values()

        for frame_1 in time_frames:
            for frame_2 in time_frames:
                if frame_1[0] < frame_2[0] and frame_1[1] < frame_2[0]:
                    continue
                if frame_1[0] > frame_2[1] and frame_1[1] > frame_2[1]:
                    continue
                return "Imp " + str(ot1) + " With " + str(ot2) + " (Concurrent)"

    return "Imp " + str(ot1) + " With " + str(ot2) + " (Ordered)"


def get_extended_ocpt(ocpt, relations, done=[]):

    if isinstance(ocpt,LeafNode):
        return ocpt

    else:

        candidates = [{ot} for ot in relations["ocel:type"].unique()]

        activities = ocpt.get_activities()
        for ot1 in candidates:
            for ot2 in candidates:
                if ot1 == ot2:
                    continue
                if (ot1,ot2) in done:
                    continue
                sub_log = relations[relations["ocel:type"].isin(ot1|ot2) & relations["ocel:activity"].isin(activities)]
                if not ot1 in sub_log["ocel:type"].unique() and ot2 in sub_log["ocel:type"].unique():
                    continue
                if len(sub_log["ocel:activity"].unique()) <2:
                    continue
                operator = check_relation(ot1, ot2, sub_log)
                if operator:
                    done.append((ot1,ot2))
                    return OperatorNode(operator, [get_extended_ocpt(ocpt,relations,done)])

        return OperatorNode(ocpt.operator,[get_extended_ocpt(sub,relations,done) for sub in ocpt.subtrees])

