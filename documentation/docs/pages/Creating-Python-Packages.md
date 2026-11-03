## Scaffolding a Python Package

ACCESS-NRI maintain a [cookiecutter template](https://github.com/ACCESS-NRI/cookiecutter-pypackage-access) which can be used to scaffold a python package. This enables you to quickly scaffold much of the boilerplate required to create a python package, for example creating the package and tests directory structure, and setting up linters, type checkers, etc. 

If you don't already have cookiecutter installer (`which cookiecutter` to check):
```bash
$ python -m pip install cookiecutter
```
You can then scaffold the package with 
```bash
$ cookiecutter https://github.com/ACCESS-NRI/cookiecutter-pypackage-access
```

This will generate a series of prompts which enable you to customise your package - for example, setting contact details, configuring type checking strictness, whether to create placeholder entrypoints.

When you want to publish your package, you will need to configure publishing - see the Continuous integration and Deployment page. 

If the cookiecutter template does not include (or allow configuration for) something you think it should, please [raise an issue](https://github.com/ACCESS-NRI/cookiecutter-pypackage-access/issues).

## Publishing a Python package
To publish a pure python package the [publish-python-package](https://github.com/ACCESS-NRI/actions/blob/main/.github/workflows/publish-python-package.yml) workflow can be used. 

Examples of how to use the workflow can be found in its README's [Usage paragraph](https://github.com/ACCESS-NRI/actions/blob/main/.github/workflows/README.md#usage).