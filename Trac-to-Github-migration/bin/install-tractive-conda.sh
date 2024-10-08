#!/bin/bash

module use /g/data/hh5/public/modules
module load conda/analysis3-24.04
source "./conda-env-tractive.sh"
conda create --solver=classic -y --prefix "$MY_CONDA_ENV" conda
module unload conda
conda_env_tractive
conda config --add channels defaults
conda install --solver=classic -y -c conda-forge c-compiler
conda install --solver=classic -y -c conda-forge cxx-compiler
conda install --solver=classic -y -c conda-forge conda
conda install --solver=classic -y -c conda-forge ruby
conda install --solver=classic -y -c conda-forge pygithub
conda install --solver=classic -y -c conda-forge git-filter-repo
conda install --solver=classic -y -c conda-forge pyyaml
conda install --solver=classic -y -c conda-forge reposurgeon

