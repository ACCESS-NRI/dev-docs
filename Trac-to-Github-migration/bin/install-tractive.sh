#!/bin/bash

conda_env_tractive() {
    my_conda_env='/g/data/tm70/pcl851/envs/tractive'
    my_conda_setup="$("${my_conda_env}/bin/conda" 'shell.bash' 'hook' 2> /dev/null)"
    if [ $? -eq 0 ]; then
        eval "$my_conda_setup"
    else
        if [ -f "${my_conda_env}/etc/profile.d/conda.sh" ]; then
            . "${my_conda_env}/etc/profile.d/conda.sh"
        else
            export PATH="${my_conda_env}/bin:$PATH"
        fi
    fi
}

module use /g/data/hh5/public/modules
module load conda/analysis3-23.07
conda create -y --prefix /g/data/tm70/pcl851/envs/tractive conda
conda_env_tractive
conda install -y conda -c conda-forge
conda install -y ruby
conda install -y reposurgeon -c dnachun
conda install -y pygithub -c conda-forge
conda install -y gcc_linux-64
conda install -y gxx_linux-64
gem install -q ruby
gem install -q tractive

