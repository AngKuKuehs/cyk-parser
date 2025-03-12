from error_combiners import *
from error_comparators import *

def no_correction_config():
    return {
        "error_correct": False,
        "init_error": 0,
        "del_error_combiner": simple_del_addition,
        "std_error_combiner": simple_std_addition,
        "front_end_del_error_combiner": simple_front_end_del_addition,
        "error_comparator": simple_error_compare,
        "limit_comparator": simple_limit_compare,
        "init_ins_error": 1, # TODO: when this is 0, error correction still happens for some reason
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

def track_ins_config(error_limit=(1, 1)):
    config = custom_cost_correction_config(error_limit=error_limit, deletion_cost=(1, 0), insertion_cost=(1, 1))
    config["init_error"] = (0, 0)
    config["del_error_combiner"] = track_ins_del_addition
    config["std_error_combiner"] = track_ins_std_addition
    config["front_end_del_error_combiner"] = track_ins_front_end_del_addition
    config["error_comparator"] = ord_error_compare
    config["limit_comparator"] = ord_limit_compare
    config["init_ins_error"] = (1, 1)
    return config