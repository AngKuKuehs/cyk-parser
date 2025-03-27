from error_inserter import *

if __name__ == "__main__":
    # get dict of tokens
    small_file_token_dict = get_tokens("references/example_small_files")

    # get errors
    num_errors = 3
    file_count = 40
    n_errors = create_test_set_all_files(add_n_errors, small_file_token_dict, num_errors)

    ver = 4
    # save error files
    directory = "references/error_test_set"
    save_error_file(directory + f"/{ver}/small_files_{num_errors}_errors", n_errors)

    # check that files match
    # we are saving files as a list of Tokens (from Lark) so pickle is preferable to json
    n_errors_loaded = load_error_file(directory + f"/{ver}/small_files_{num_errors}_errors.pkl")

    assert(n_errors == n_errors_loaded)