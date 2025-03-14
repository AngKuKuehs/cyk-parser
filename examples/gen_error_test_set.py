from error_inserter import *

if __name__ == "__main__":
    # get dict of tokens
    token_dict = get_tokens("references/python-3.0-library")
    small_file_token_dict = get_tokens("references/example_small_files")

    # get errors
    file_count = 40
    single_deletion_errors = create_test_set_randomly(add_single_deletion_error, file_count, token_dict)
    single_insertion_errors = create_test_set_randomly(add_single_insertion_error, file_count, token_dict)

    small_file_single_deletion_errors = create_test_set_all_files(add_single_deletion_error, small_file_token_dict)
    small_file_single_insertion_errors = create_test_set_all_files(add_single_insertion_error, small_file_token_dict)

    ver = 1
    # save error files
    directory = "references/error_test_set"
    save_error_file(directory + f"/{ver}/std_lib_single_deletion-40", single_deletion_errors)
    save_error_file(directory + f"/{ver}/std_lib_single_insertion-40", single_insertion_errors)

    save_error_file(directory + f"/{ver}/small_file_single_deletion", small_file_single_deletion_errors)
    save_error_file(directory + f"/{ver}/small_file_single_insertion", small_file_single_insertion_errors)

    # check that files match
    # we are saving files as a list of Tokens (from Lark) so pickle is preferable to json
    single_deletion_errors_loaded = load_error_file(f"references/error_test_set/{ver}/std_lib_single_deletion-40.pkl")
    single_insertion_errors_loaded = load_error_file(f"references/error_test_set/{ver}/std_lib_single_insertion-40.pkl")

    small_file_single_deletion_errors_loaded = load_error_file(f"references/error_test_set/{ver}/small_file_single_deletion.pkl")
    small_file_single_insertion_errors_loaded = load_error_file(f"references/error_test_set/{ver}/small_file_single_insertion.pkl")

    assert(single_deletion_errors == single_deletion_errors_loaded)
    assert(single_insertion_errors == single_insertion_errors_loaded)
    assert(small_file_single_deletion_errors == small_file_single_deletion_errors_loaded)
    assert(small_file_single_insertion_errors == small_file_single_insertion_errors_loaded)
