import logging
import os


def save_string_to_file(file_path, string):
    with open(file_path, "w", encoding="utf-8") as text_file:
        text_file.write(string)
    logging.info(f'Saved string to file >> {file_path}')


def get_project_root_directory():
    """
    For instance C:/Users/directory/kickface_analytics
    :return: The projects root directory
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Navigate to the root directory of the project
    # Assuming this script is within a subdirectory of the root
    root_dir = os.path.dirname(current_dir)

    return root_dir


def concat_path(*path_elements: str) -> str:
    """
    Concatenates strings to a path os independent
    :param path_elements: the path elements as strings
    :return: a concatenated os independent path
    """
    result = ''
    for element in path_elements:
        result = os.path.join(result, element)
    return result
