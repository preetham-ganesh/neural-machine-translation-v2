import os
import tarfile


def check_directory_path_existence(directory_path: str) -> str:
    """Creates the directory path.

    Creates the absolute path for the directory path given in argument if it does not already exist.

    Args:
        directory_path: A string for the directory path that needs to be created if it does not already exist.

    Returns:
        A string for the absolute directory path.
    """
    # Asserts type of arguments.
    assert isinstance(
        directory_path, str
    ), "Variable directory_path should be of type 'str'."

    # Creates the following directory path if it does not exist.
    home_directory_path = os.getcwd()
    absolute_directory_path = "{}/{}".format(home_directory_path, directory_path)
    if not os.path.isdir(absolute_directory_path):
        os.makedirs(absolute_directory_path)
    return absolute_directory_path


def extract_tar_file(
    file_name: str,
    extension: str,
    tar_file_directory_path: str,
    extracted_data_directory_path: str,
) -> None:
    """Loads Tar file, and extract files from it, and saves it for future use.

    Loads Tar file, and extract files from it, and saves it for future use.

    Args:
        file_name: A string for the name of Tar file.
        extension: A string for the extension of the Tar file.
        tar_file_directory_path: A string for the location where the tar file exists.
        extracted_data_directory_path: A string for the location where the extracted files should be stored.

    Returns:
        None.

    Exceptions:
        FileNotFoundError: If file path does not exist, then this error occurs.
    """
    # Types checks arguments.
    assert isinstance(file_name, str), "Variable file_name should be of type 'str'."
    assert isinstance(extension, str), "Variable extension should be of type 'str'."
    assert isinstance(
        tar_file_directory_path, str
    ), "Variable tar_file_directory_path should be of type 'str'."
    assert isinstance(
        extracted_data_directory_path, str
    ), "Variable extracted_data_directory_path should be of type 'str'."

    # Checks if the following directory path exists.
    extracted_data_directory_path = check_directory_path_existence(
        extracted_data_directory_path
    )

    # Extracts tar file to the extracted data directory path.
    tar_file_path = "{}/{}.{}".format(tar_file_directory_path, file_name, extension)
    try:
        out_file = tarfile.open(tar_file_path)
        out_file.extractall(extracted_data_directory_path)
        out_file.close()
    except FileNotFoundError:
        raise FileNotFoundError("File path {} does not exist.".format(tar_file_path))

    print(
        "Finished extracting files from {} successfully to {}.".format(
            tar_file_path, extracted_data_directory_path
        )
    )
    print()


def load_text_file(file_name: str, extension: str, directory_path: str) -> str:
    """Loads the text file as a string.

    Loads the text file as a string.

    Args:
        file_name: A string for the name of text file.
        extension: A string for the extension of the text file.
        directory_path: A string for the location where the text file exists.

    Returns:
        A string for the text loaded from the file.

    Exceptions:
        FileNotFoundError: If file path does not exist, then this error occurs.
    """
    # Types checks input arguments.
    assert isinstance(file_name, str), "Variable file_name should be of type 'str'."
    assert isinstance(extension, str), "Variable extension should be of type 'str'."
    assert isinstance(
        directory_path, str
    ), "Variable directory_path should be of type 'str'."

    # Loads the text file as a string.
    file_path = "{}/{}.{}".format(directory_path, file_name, extension)
    try:
        with open(file_path, "r") as out_file:
            text = out_file.read()
        out_file.close()
        return text

    except FileNotFoundError:
        raise FileNotFoundError("File path {} does not exist.".format(file_path))
