"""File I/O for specific file types."""

import json
from json import JSONDecodeError

from specparam.io.utils import fpath, fname
from specparam.core.utils import dict_lst_to_array

###################################################################################################
###################################################################################################

def load_json(file_name, file_path):
    """Load json file.

    Parameters
    ----------
    file_name : str or FileObject
        File to load data from.
    file_path : Path or str
        Path to directory to load from.

    Returns
    -------
    data : dict
        Dictionary of data loaded from file.
    """

    # Load data from file
    if isinstance(file_name, str):
        with open(fpath(file_path, fname(file_name, 'json')), 'r') as infile:
            data = json.load(infile)
    elif isinstance(file_name, io.IOBase):
        data = json.loads(file_name.readline())

    # Get dictionary of available attributes, and convert specified lists back into arrays
    data = dict_lst_to_array(data, OBJ_DESC['arrays'])

    return data


def load_jsonlines(file_name, file_path):
    """Load a json-lines file, yielding data line by line.

    Parameters
    ----------
    file_name : str
        File to load data from.
    file_path : Path or str
        Path to directory from load from.

    Yields
    ------
    dict
        Dictionary of data loaded from file.
    """

    with open(fpath(file_path, fname(file_name, 'json')), 'r') as f_obj:

        while True:

            # Load each line, as JSON file
            try:
                yield load_json(f_obj, '')

            # Break off when get a JSON error - end of the file
            except JSONDecodeError:
                break