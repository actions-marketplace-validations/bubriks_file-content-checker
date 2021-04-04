# YAML linter Action

[![Actions Status](https://github.com/bubriks/file-content-checker/workflows/Lint/badge.svg)](https://github.com/bubriks/file-content-checker/actions)
[![Actions Status](https://github.com/bubriks/file-content-checker/workflows/Integration%20Test/badge.svg)](https://github.com/bubriks/file-content-checker/actions)

This action will validate the contents of your files

## Usage

Describe how to use your action here.

### Example workflow

```yaml
name: My Workflow
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@master
    - name: Run action
      uses: jacobtomlinson/gha-lint-yaml@master
      with:
        path: path/to/my/yaml/file.yaml
```

### Inputs

| Input                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `path`  | Path to the YAML file to be linted.    |
| `strict` _(optional)_  | Run the linter in strict mode (error on warnings).    |

### Outputs

| Output                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `warnings`  | The number of warnings raised if successful.    |

## Examples

### Running in strict mode

Here is an example of a very strict linting job.

```yaml
name: My Workflow
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - name: Run action
      uses: jacobtomlinson/gha-lint-yaml@master
      with:
        path: path/to/my/yaml/file.yaml
        strict: true
```

### Using outputs

Here is an example of using the warnings outputs.

```yaml
name: My Workflow
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - name: Run action
      id: yamllint
      uses: jacobtomlinson/gha-lint-yaml@master
      with:
        path: path/to/my/yaml/file.yaml

    - name: Check outputs
      run: |
        echo "There were ${{ steps.yamllint.outputs.warnings }} YAML linting warnings."
```