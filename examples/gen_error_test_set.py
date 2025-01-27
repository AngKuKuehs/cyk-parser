from error_inserter import *

if __name__ == "__main__":
    # get dict of tokens
    token_dict = get_tokens("references/python-3.0-library")
    small_file_token_dict = get_tokens("references/example_small_files")

    # get errors
    file_count = 20
    single_deletion_errors = create_test_set_randomly(add_single_deletion_error, file_count, token_dict)
    single_insertion_errors = create_test_set_randomly(add_single_insertion_error, file_count, token_dict)

    small_file_single_deletion_errors = create_test_set_all_files(add_single_deletion_error, small_file_token_dict)
    small_file_single_insertion_errors = create_test_set_all_files(add_single_insertion_error, small_file_token_dict)

    ver = 0
    # save error files
    save_error_file(single_deletion_errors, f"std_lib_single_deletion-{ver}-20")
    save_error_file(single_insertion_errors, f"std_lib_single_insertion-{ver}-20")

    save_error_file(small_file_single_deletion_errors, f"small_file_single_deletion-{ver}-20")
    save_error_file(small_file_single_insertion_errors, f"small_file_single_insertion-{ver}-20")

    # check that files match
    single_deletion_errors_loaded = load_error_file(f"references/error_test_set/std_lib_single_deletion-{ver}-20.pkl")
    single_insertion_errors_loaded = load_error_file(f"references/error_test_set/std_lib_single_insertion-{ver}-20.pkl")

    small_file_single_deletion_errors_loaded = load_error_file(f"references/error_test_set/small_file_single_deletion-{ver}-20.pkl")
    small_file_single_insertion_errors_loaded = load_error_file(f"references/error_test_set/small_file_single_insertion-{ver}-20.pkl")

    assert(single_deletion_errors == single_deletion_errors_loaded)
    assert(single_insertion_errors == single_insertion_errors_loaded)
    assert(small_file_single_deletion_errors == small_file_single_deletion_errors_loaded)
    assert(small_file_single_insertion_errors == small_file_single_insertion_errors_loaded)
