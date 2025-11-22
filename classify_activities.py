import pm4py
import pandas as pd
import sys
import time
import json
from collections import defaultdict
import itertools

from enum import Enum

MAINTAIN = "MAINTAIN"
CREATE = "CREATE"
DELETE = "DELETE"
UPDATE_PARENT = "UPDATE_PARENT"

Parameters = pm4py.algo.filtering.ocel.activity_type_matching.Parameters

verbose = True

def load_ocel_log(filename):
    """Load the OCEL log from the provided file."""
    return pm4py.read_ocel2_xml(filename)

def get_events_for_types(ocel, many_type, one_type):
    relations = ocel.relations.drop('ocel:qualifier', axis=1)
    # print(relations)
    relations_t1 = relations[relations["ocel:type"] == many_type]
    relations_t2 = relations[relations["ocel:type"] == one_type]

    if len(relations_t1) == 0:
        print("no events with %s found" % many_type)
    if len(relations_t2) == 0:
        print("no events with %s found" % one_type)
    
    try:
        reljoin = relations_t1.merge(relations_t2, on="ocel:eid", suffixes=["_t1", "_t2"], validate="m:1") # do the join
    except:
        if verbose:
          print("Relation %s : %s is not many-to-one in log." % (many_type, one_type))
        return None

    # drop some columns, not sure if this is of any help
    reljoin.drop(columns=['ocel:type_t1', 'ocel:type_t2', 'ocel:activity_t2', 'ocel:timestamp_t2'], inplace=True)
    print("after join:", len(reljoin), len(relations_t1), len(relations_t2))

    is_sorted = reljoin["ocel:timestamp_t1"].is_monotonic_increasing
    assert(is_sorted)
    
    events = {}
    for row in reljoin.itertuples():
        (_, eid, activity, timestamp, many_object, one_object) = row
        if eid not in events:
            events[eid] = {"activity": activity, 
                           "timestamp": timestamp,
                           "one": one_object,
                           "many": [many_object]
                           }
        else:
            events[eid]["many"].append(many_object)
    return events

def label_activities(events, one_type, relationship_data):
    reference_types = relationship_data["reference types"]
    rel = set([])
    labels = {}

    for eid,data in events.items():
        act = data["activity"]
        one_object = data["one"]
        elabels = set([])
        if reference_types[act] == one_type:
            for many_object in data["many"]:
                if (one_object, many_object) in rel:
                    elabels.add(MAINTAIN)
                else:
                    elabels.add(CREATE)
                    rel.add((one_object, many_object))
            for o in [ o for (u, o) in rel if u == one_object and o not in data["many"]]:
                rel.remove(one_object, o)
                elabels.add(DELETE)
        else:
            if not (len(data["many"]) == 1):
                print(data)
            assert(len(data["many"]) == 1)
            many_object = data["many"][0]
            if (one_object, many_object) in rel:
                elabels.add(MAINTAIN)
            else:
                parents = [u for (u,o) in rel if o == many_object]
                if len(parents) > 0:
                    assert(len(parents) == 1)
                    p = parents[0]
                    rel.remove((p,many_object))
                    rel.add((one_object, many_object))
                    elabels.add(UPDATE_PARENT)
                else:
                    elabels.add(CREATE)
                    rel.add((one_object, many_object))
        
        ltuple = tuple(sorted(list(elabels)))

        # add label for activity
        if not act in labels:
            labels[act] = set([])
        labels[act].add(ltuple)
    return labels

def classify(ocel, relationship_data, many_type, one_type):
    print("-------------------------------------------------------------------")
    print("one-type %s, many-type %s" % (one_type, many_type))

    events = get_events_for_types(ocel, many_type, one_type)

    labels = label_activities(events, one_type, relationship_data)

    print(labels)

          


def main():
    start_time = time.time()
    
    # Load OCEL log
    filename = sys.argv[1]
    ocel = load_ocel_log(filename)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Time taken for import: {execution_time:.2f} seconds")

    # get reference types
    reftypefile = sys.argv[2]
    with open(reftypefile, "r") as f:
        relationship_data = json.load(f)
    
        if len(sys.argv) > 4:
            object_type1 = sys.argv[3] # the first type is MANY
            object_type2 = sys.argv[4] # the second type is ONE
            classify(ocel, relationship_data, object_type1, object_type2)
        else:
            object_types = pm4py.ocel_get_object_types(ocel)
            for (object_type1, object_type2) in itertools.combinations(object_types, 2):
                classify(ocel, relationship_data, object_type1, object_type2)
            

    
    # Calculate execution time
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Time taken for execution: {execution_time:.2f} seconds")

if __name__ == "__main__":
    main()