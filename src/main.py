from src.quotes_processing import QuotesAdapter
from src.speech_detector import SpeechDetector
from src.pipeline import Pipeline
from pandas import DataFrame
import argparse
import os

CR_V_DATA_PATH = "cross_validation_data"
TOKENS = "tokens.txt"
CONCEPTS = "concepts.txt"
WITH_TITLES_CONCEPTS = "concepts_with_titles.txt"
TEST_WITH_TITLES_CONCEPTS = "concepts_with_titles_test.txt"


# --------------------------------------------------------------------
# sys
# --------------------------------------------------------------------

def _get_data_from_cmd():
    parser = argparse.ArgumentParser(description='Train sequence translation for wikification')
    parser.add_argument('-d', type=str, dest='directory', metavar='<directory>',
                        required=False, help='directory for results')
    parser.add_argument('-i', type=str, dest='input_file', metavar='<single input file>',
                        required=False, help='single input file')
    parser.add_argument('-q', type=str, dest='quotes_csvfile', metavar='<quotes csv file>',
                        required=True, help='quotes csv file')
    parser.add_argument('-s', type=str, dest='speech_csvfile', metavar='<speech csv file>',
                        required=True, help='speech csv file')
    parser.add_argument('-o', type=str, dest='output_path', metavar='<output path>',
                        required=True, help='output path')

    args = parser.parse_args()
    directory = args.directory
    input_file = args.input_file
    quotes_file = args.quotes_csvfile
    speech_file = args.speech_csvfile
    output_path = args.output_path
    return directory, input_file, quotes_file, speech_file, output_path


def _create_folder_if_absent(path):
    if not os.path.exists(path):
        os.mkdir(path)


def _get_list_of_text_files(dirpath):
    file_paths = []
    for dirname, folders, filenames in os.walk(dirpath):
        for name in filenames:
            file_paths.append(os.path.join(dirname, name))
    return file_paths


# --------------------------------------------------------------------
# read and write
# --------------------------------------------------------------------

def _read_csv(path, sep):
    return DataFrame.from_csv(path, index_col=None, sep=sep)


def _read_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()


def _write_to_file(path, dirpath, name, data):
    if dirpath == None:
        output_path = name.replace("..\\", path+"\\")
    else:
        output_path = name.replace(dirpath, path)
    print(output_path)
    _create_folder_if_absent(os.path.dirname(output_path))
    with open(output_path, 'w', encoding='utf-8') as file:
        return file.write(data)


def main():
    directory_path, text_path, quotes_path, speech_path, output_path = _get_data_from_cmd()

    if directory_path == None:
        list_of_textfiles = [text_path]
    else:
        list_of_textfiles = _get_list_of_text_files(directory_path)

    for textpath in list_of_textfiles:
        text = _read_file(textpath)
        quotes_rules = _read_csv(quotes_path, ';')
        speech_rules = _read_csv(speech_path, ';')

        quotes_adapter = QuotesAdapter(quotes_rules)
        speech_detector = SpeechDetector(speech_rules)
        pipeline = Pipeline(quotes_adapter, speech_detector)

        text = pipeline.apply_to(text)
        _write_to_file(output_path, directory_path, textpath, text)


if __name__ == '__main__':
    main()
