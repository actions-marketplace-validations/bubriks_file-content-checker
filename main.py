import os
import sys
import json
import re


def get_lines_from_file(path):
    file = open(path, 'r')
    lines = file.readlines()
    if os.environ["INPUT_STRIP"] == "true":
        lines = [s.strip() for s in lines]
    if os.environ["INPUT_EMPTY"] == "false":
        lines = list(filter(None, lines))
    if os.environ["INPUT_LOWER"] == "true":
        lines = [s.lower() for s in lines]
    return lines


def verify_lines(json_input, lines):
    if isinstance(json_input, list):
        for json_value in json_input:
            response = verify_lines(json_value, lines)
            if response is not None:
                return response
        return None
    elif isinstance(json_input, dict):
        test_lines = lines.copy()
        for json_value in json_input:
            response = verify_lines(json_input[json_value], test_lines)
            if response is None:
                return None
            json_input[json_value] = response
        lines.clear()
        lines.extend(test_lines)
        return json_input
    elif isinstance(json_input, str):
        if len(lines) > 0 and re.search(json_input, lines[0]):
            return lines.pop(0)
        else:
            return None
    else:
        print(f"::set-output name=warning::incorrect data type: {json_input}")
        return None


def main():
    structure = os.environ["INPUT_STRUCTURE"]
    structure = r"" + structure.replace("\\", "\\\\")
    json_structure = json.loads(structure)
    path = os.environ["INPUT_PATH"]

    lines = get_lines_from_file(path)
    json_output = verify_lines(json_structure, lines)
    if json_output is not None:
        result = json.dumps(json_output)
        print("::set-output name=inform::Valid file contents")
        print(f"::set-output name=result::{result}")
        print("Match!")
        sys.exit(0)
    else:
        sys.exit("Contents don't match the provided structure")


if __name__ == "__main__":
    main()
