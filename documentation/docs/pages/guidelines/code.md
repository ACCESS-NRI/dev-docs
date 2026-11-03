## POSIX compliance

* Line: "A sequence of zero or more non-\<newline\> characters plus a terminating \<newline\> character." (https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap03.html#tag_03_206)
* [How can I make all line endings (EOLs) in all files in Visual Studio Code, Unix-like?](https://stackoverflow.com/questions/48692741/how-can-i-make-all-line-endings-eols-in-all-files-in-visual-studio-code-unix)

## Python
All Python code should <i>where possible</i> follow the [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/).

A quick reference is provided below for some of the most commonly used examples:

## Supported versions of Python

Packages should support stable Python versions (security and bugfix).
Refer to the [Python Developer Guide for the current status of Python versions](https://devguide.python.org/versions/).
Package updates should announce the deprecation of Python versions that have reached their end-of-life.


## Imports
### Jupyter notebooks
All package imports should be grouped together and contained within a single cell, which is ideally the cell immediately following any cells containing titles, descriptions and licenses. Ideally all lines beginning with `import` should come first, with lines beginning with `from` second.

### Python files (*.py)
All package imports should be grouped together and immediately follow any comments containing titles, descriptions and licenses. Ideally all lines beginning with `import` should come first, with lines beginning with `from` second.

## Naming conventions
### Overriding Principle
Names that are visible to the user as public parts of the API should follow conventions that reflect usage rather than implementation.

### Package names
Python packages should have short, all-lowercase names. The use of underscores is discouraged as per [PEP 8](https://peps.python.org/pep-0008/#package-and-module-names), however they can be included only if required to improve readability.

Examples: 
* `mypackage`
* `my_complex_package_name`

### Module names
Module names should be short, all-lowercase, and ideally semantic in nature. Underscores can be used in the module name if it improves readability as per [PEP 8](https://peps.python.org/pep-0008/#package-and-module-names).

Examples: 
* `mymodule`
* `my_module`
* `my_more_complex_module`

### Class names  
Class names should be short, ideally semantic in nature, and normally use the <b>CapWords</b> convention as per [PEP 8](https://peps.python.org/pep-0008/#class-names).

Example: 
* `MyNewClass`

### Function and method names  
Function names should be lowercase and ideally semantic in nature with words separated by underscores as necessary to improve readability as per [PEP 8](https://peps.python.org/pep-0008/#method-names-and-instance-variables). 

Examples: 
* `my_function`
* `my_more_complex_function`

### Variable names
Variable names should be lowercase and ideally semantic in nature, with words separated by underscores as necessary to improve readability as per [PEP 8](https://peps.python.org/pep-0008/#method-names-and-instance-variables).

Example:
* `my_variable`
* `my_more_complex_variable`

Note: Never use the characters ‘l’ (lowercase letter el), ‘O’ (uppercase letter oh), or ‘I’ (uppercase letter eye) as single character variable names. In some fonts, these characters are indistinguishable from the numerals one and zero. When tempted to use ‘l’ (lowercase letter el), use ‘L’ instead.

### ACCESS-NRI organisation references
All references to ACCESS-NRI within 'code situations' outside of already defined naming conventions (e.g. databases, arrays, dictionaries, lists etc) should use `access_nri`. For all 'non-code' examples (e.g. plot titles, script names, docstring descriptions etc), use `ACCESS-NRI`.

## Private functions/methods
To define a private attribute or function/method within a given class, prefix the name with a single underscore(`_`).

Example:
* `my_function` becomes `_my_function`
* `my_variable` becomes `_my_variable`

Note: Python does not have _true_ private functions/methods, so restrictions to attributes or functions/methods prepended with an underscore (`_`) are not strictly enforced. The single underscore(`_`) is just a convention to denote an attribute or function/method is intended to be private.

## Documentation
### Overriding Principle
Documenting software is very important! Documentation helps both users and developers to understand everything about a given piece of software or code. From more high-level aspects such as what is the purpose of the code, how it is put together and how it is deployed, to more low-level information including installation, troubleshooting and how the code can be implemented and/or extended.  

### Comments
If a line of code does something, describe it with a comment! Comments should be complete sentences and be placed on the line above the line of code they are describing. The first word should be capitalized, unless it is an identifier that begins with a lower case letter (never alter the case of identifiers!). Comments that contradict the code are worse than no comments. Always make a priority of keeping the comments up-to-date when the code changes!

#### Block comments 
Block comments generally apply to some (or all) code that follows them, and are indented to the same level as that code. Each line of a block comment starts with a # and a single space (unless it is indented text inside the comment). Paragraphs inside a block comment are separated by a line containing a single #.

#### Inline comments
Use inline comments sparingly.

An inline comment is a comment on the same line as a statement. Inline comments should be separated by at least two spaces from the statement. They should start with a # and a single space.

See [PEP 8 - Comments](https://peps.python.org/pep-0008/#comments) for a full description of good commenting practices. 

### Docstrings
A docstring (or documentation string) is a string literal that occurs as the first statement in a module, function, class, or method definition. This docstring becomes the `__doc__` special attribute of that object. All modules should normally have docstrings, and all functions and classes exported by a module should also have docstrings. A full description of general docstring best practices can be found in the [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/).

Beyond providing code-level information to the user via the `__doc__` special attribute, docstrings can (and should) also be used to auto-generate package/API reference documentation. For this task, it is recommended to use [Sphinx](https://www.sphinx-doc.org/en/master/index.html).

To auto-generate documentation using Sphinx, specific docstring formatting is required (i.e. you cannot use [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/) formatting). For this, please use the [numpydoc](https://numpydoc.readthedocs.io/en/latest/format.html) syntax. Documentation should use the `sphinx-rtd-theme` found [here](https://pypi.org/project/sphinx-rtd-theme/).

Example Sphinx-compatible [numpydoc](https://numpydoc.readthedocs.io/en/latest/format.html) formatting for a multiline docstring describing a function containing multiple explicit arguments:
 
    def my_function(arg1, arg2, arg3=True):

        """
        Clear and concise function description.

        Parameters
        ----------
        arg1 : string
               Argument 1 description
        arg2 : float
               Argument 2 description
        arg3 : bool, default True
               Argument 3 description

        Returns
        ----------
        string
            Description of returned object
        """

        if type(arg1) == str and type(arg2) == float and type(arg3) == bool:

            result = 'winning'
      
        else:

            result = 'not winning'

        return result

    
## Testing
### Overriding Principle
Robust and consistent software formatting and testing is a very important phase of the complete development cycle. Routinely evaluating and linting classes, functions and scripts not only ensures that code is working correctly, it also informs code optimisation.

### Linting and formatting
Linting is a 'quality-control' process to check code syntax and highlight issues or inconsistencies (e.g. spelling errors in function or variable names, incorrect indentation etc). This process is often automated in dedicated Python IDE's (e.g. Jupyter, PyCharm etc), so is typically most useful for evaluating *.py files. We recommend using the [Flake8](https://flake8.pycqa.org/en/latest/) package. In addition to linting, we recommend using the [black](https://pypi.org/project/black/) package as a code formatter.

### Unit testing
To evaluate code stability, functionality and performance, [unit testing](https://realpython.com/pytest-python-testing/) is considered an industry-standard approach.

For testing Python code at ACESS-NRI, it is recommended that unit testing be completed using the [pytest framework](https://docs.pytest.org/en/7.3.x/). A library of pytest examples can be found [here](https://docs.pytest.org/en/7.3.x/example/index.html). 

### Unit testing code coverage

See [coverage.py](https://github.com/nedbat/coveragepy).

### Versioning

TODO which tool(s) should be used for versioning ACCESS NRI repos?


## Fortran

## R

## C/C++


## Copyright license

See the [licensing policy](../policies/licensing.md).