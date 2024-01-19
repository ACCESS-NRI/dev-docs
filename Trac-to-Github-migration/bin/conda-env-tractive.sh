#!/bin/bash

export MY_CONDA_ENV="/scratch/tm70/pcl851/conda/envs/tractive"
conda_env_tractive() {
__conda_setup="$(${MY_CONDA_ENV}'/bin/conda' 'shell.bash' 'hook' | sed '/conda activate/d')"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "${MY_CONDA_ENV}/etc/profile.d/conda.sh" ]; then
        . "${MY_CONDA_ENV}/etc/profile.d/conda.sh"
    else
        export PATH="${MY_CONDA_ENV}/bin:$PATH"
    fi
fi
unset __conda_setup
}

conda_activate() {
conda_env_tractive
eval "$(conda shell.bash activate)"
}

