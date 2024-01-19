#!/bin/bash

module use /g/data/hh5/public/modules
module load conda/analysis3-23.04
source "./conda-env-tractive.sh"
conda create -y --prefix "$MY_CONDA_ENV" conda
module unload conda
conda_env_tractive

conda install -y -c conda-forge c-compiler
conda install -y -c conda-forge cxx-compiler
conda install -y -c conda-forge conda
conda install -y -c conda-forge ruby
conda install -y -c conda-forge pygithub
conda install -y -c conda-forge git-filter-repo
conda install -y -c conda-forge pyyaml
conda install -y -c dnachun reposurgeon

