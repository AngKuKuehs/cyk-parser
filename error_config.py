from error_combiners import *
from error_comparators import *

def no_correction_config():
    return {
        "error_correct": False,
        "init_error": 0,
        "del_error_combiner": simple_del_addition,
        "ins_error_combiner": simple_ins_addition,
        "std_error_combiner": simple_std_addition,
        "front_end_del_error_combiner": simple_front_end_del_addition,
        "error_comparator": simple_error_compare,
        "limit_comparator": simple_limit_compare,
        "init_ins_error": 0,
        "init_del_error": 0, # not actually used in error metric calcs since deletions aren't part of the tree
        "error_limit": 0
        }

def basic_correction_config(error_limit=1):
    config = no_correction_config()
    config["error_correct"] = True
    config["init_ins_error"] = 1
    config["init_del_error"] = 1
    config["error_limit"] = error_limit
    return config

def custom_cost_correction_config(error_limit=1, deletion_cost=1, insertion_cost=1):
    config = no_correction_config()
    config["error_correct"] = True
    config["init_ins_error"] = insertion_cost
    config["init_del_error"] = deletion_cost
    config["error_limit"] = error_limit
    return config
