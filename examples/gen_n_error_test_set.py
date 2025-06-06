from error_inserter import *

if __name__ == "__main__":
    # get dict of tokens
    token_dict = get_tokens("references/python-3.0-library", max_lines=50)
    small_file_token_dict = get_tokens("references/example_small_files")

    # get errors
    num_errors = 3
    file_count = 60
    n_deletion_errors = create_test_set_randomly(add_n_deletion_error, file_count, token_dict, num_errors)
    n_insertion_errors = create_test_set_randomly(add_n_insertion_error, file_count, token_dict, num_errors)
    n_random_errors = create_test_set_randomly(add_n_errors, file_count, token_dict, num_errors)

    ver = 5
    # save error files
    directory = "references/error_test_set"
    save_error_file(directory + f"/{ver}/std_lib_{num_errors}_deletion-{file_count}", n_deletion_errors)
    save_error_file(directory + f"/{ver}/std_lib_{num_errors}_insertion-{file_count}", n_insertion_errors)
    save_error_file(directory + f"/{ver}/std_lib_{num_errors}-{file_count}", n_random_errors)

    # check that files match
    # we are saving files as a list of Tokens (from Lark) so pickle is preferable to json
    n_deletion_errors_loaded = load_error_file(directory + f"/{ver}/std_lib_{num_errors}_deletion-{file_count}.pkl")
    n_insertion_errors_loaded = load_error_file(directory + f"/{ver}/std_lib_{num_errors}_insertion-{file_count}.pkl")
    n_errors_loaded = load_error_file(directory + f"/{ver}/std_lib_{num_errors}-{file_count}.pkl")

    assert(n_deletion_errors == n_deletion_errors_loaded)
    assert(n_insertion_errors == n_insertion_errors_loaded)
    assert(n_random_errors == n_errors_loaded)
