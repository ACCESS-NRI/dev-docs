## Conda
## Anaconda Python environment on gadi
* Follow the instructions on: http://climate-cms.wikis.unsw.edu.au/Conda

### Creating a personal environment for debugging
* http://climate-cms.wikis.unsw.edu.au/Conda#Creating_personal_environments

#### Steps for debugging Payu
* Populate the `~/.condarc` by following the instructions above.
* `$ conda deactivate`
* If that returns the following error, simply follow the instructions, then log out and log back in: 
```
CommandNotFoundError: Your shell has not been properly configured to use 'conda deactivate'.
To initialize your shell, run

    $ conda init <SHELL_NAME>

Currently supported shells are:
  - bash
  - fish
  - tcsh
  - xonsh
  - zsh
  - powershell

See 'conda init --help' for more information and options.

IMPORTANT: You may need to close and restart your shell after running 'conda init'.
```
* Create a new Conda environment and install pip: `$ conda create -n <environment-name> -c conda-forge pip`
* List the Conda environments: `$ conda env list`
* Activate the Conda environment: `$ conda activate <environment-name>`
* `$ cd <payu-source-repository>`
* `$ pip install -e .`
