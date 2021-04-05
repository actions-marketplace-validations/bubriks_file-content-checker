# YAML linter Action

[![Actions Status](https://github.com/bubriks/file-content-checker/workflows/Lint/badge.svg)](https://github.com/bubriks/file-content-checker/actions)
[![Actions Status](https://github.com/bubriks/file-content-checker/workflows/Integration%20Test/badge.svg)](https://github.com/bubriks/file-content-checker/actions)

This action will validate the contents of your files using json file containing regex string values. It sets the status of PR to failure in case of no match.

## Usage

The verification of file contents is done using json schema, with possible usage of three value types: dictionary, list and string.

Dictionary- All contents within dictionary must be sattisfied.
List- Atleast one of the lists elements must match (takes the first match).
String- Regex value used for line content verification.

As a result of successfull execution, a moddified version of the provided json (containing retrieved data) is returned.

### Example workflow

```yaml
name: My Workflow
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@master
	
    - name: Check content
      uses: bubriks/file-content-checker@master
      with:
        path: path/to/my/file/README.md
		structure: json
```

### Inputs

| Input                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `path`  | Path to the file to be verified.    |
| `structure` | Expected file content structure (json string).    |
| `strip` _(optional)_  | Remove spaces at the beginning and at the end of the line read from the file path.    |
| `empty` _(optional)_  | Use empty lines for comparison.    |
| `lower` _(optional)_  | Text from file to lowercase.    |

### Outputs

| Output                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `warnings`  | Problem encountered during run.    |
| `result`  | Result of the execution (json file with regex expression replaced by the matched line).    |
| `inform`  | Informative message.    |

## Examples

### Running using json string

Here is an example of yaml containing json.

```yaml
name: My Workflow
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@master
	
    - name: Check content
      uses: bubriks/file-content-checker@master
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

Response in the case of lists first element matching.

```json
{
	'test': {
		'Name&Email': 'foo bar (bar@gmail.com)', 
		'GitHub': 'github: https://github.com/bar'
	}
}
```

### Running using json file

Here is an example of yaml using json file.

```yaml
name: My Workflow
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@master
	
	- id: readfile
      run: echo ::set-output name=json::$(cat path/to/my/json/test.json)

    - name: Check content
      uses: bubriks/file-content-checker@master
      with:
        path: path/to/my/file/README.md
        structure: ${{ steps.readfile.outputs.json }}
```