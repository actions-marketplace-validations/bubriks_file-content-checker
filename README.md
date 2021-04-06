# File content checker

[![Actions Status](https://github.com/bubriks/file-content-checker/workflows/Lint/badge.svg)](https://github.com/bubriks/file-content-checker/actions)
[![Actions Status](https://github.com/bubriks/file-content-checker/workflows/Integration%20Test/badge.svg)](https://github.com/bubriks/file-content-checker/actions)

This action will validate the contents of your files using a JSON containing regex string values. It sets the status of PR to failure in case of no match.

## Usage

The verification of file contents is done using JSON schema, with possible usage of three value types: dictionary, list, and string.

- Dictionary- All contents within the dictionary must be satisfied.
- List- At least one of the list elements must match (takes the first match).
- String- Regex value used for line content verification.

As a result of successful execution, a modified version of the provided JSON (containing matched data) is returned.

### Example workflow

```yaml
name: My Workflow
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2

    - name: Check content
      uses: bubriks/file-content-checker@0.1.1
      with:
        path: path/to/my/file/README.md
        structure: json
```

### Inputs

| Input                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `path`  | Path to the file to be verified.    |
| `structure` | Expected file content structure (JSON string).    |
| `strip` _(optional)_  | Remove spaces at the beginning and the end of the line read from the file path.    |
| `empty` _(optional)_  | Use empty lines for comparison.    |
| `lower` _(optional)_  | Text from file to lowercase.    |

### Outputs

| Output                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `warnings`  | Problem encountered during the run.    |
| `result`  | Result of the execution (JSON file with regex expression replaced by the matched line).    |
| `inform`  | Informative message.    |

## Examples

### Running using JSON string

Here is an example of YAML containing JSON.

```yaml
name: My Workflow
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2

    - name: Check content
      uses: bubriks/file-content-checker@0.1.1
      with:
        path: path/to/my/file/README.md
        structure: >
            {
                "test": [
                    {
                        "nameAndEmail": "^[a-z]+( [a-z]+)* [a-z]+ \([a-z]+@gmail.com\)$",
                        "gitHub": "^github: https://github.com/[a-z]+$"
                    },
                    {
                        "nameAndEmail": "^[a-z]+( [a-z]+)* [a-z]+ \([a-z]+@gmail.com\)$"
                    },
                    {}
                ]
            }
```

Example response in the case of lists first element matching.


```json
{
    "test": {
        "nameAndEmail": "foo bar (bar@gmail.com)", 
        "gitHub": "github: https://github.com/bar"
    }
}
```

### Running using JSON file

Here is an example of YAML using JSON file.

```yaml
name: My Workflow
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2

    - id: readfile
      run: echo ::set-output name=json::$(cat path/to/my/json/test.json)

    - name: Check content
      uses: bubriks/file-content-checker@0.1.1
      with:
        path: path/to/my/file/README.md
        structure: ${{ steps.readfile.outputs.json }}
```