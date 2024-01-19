#!/bin/bash

source "./conda-env-tractive.sh"
conda_activate

gem install tractive
sed -i 's/\$bindir\/ruby/ruby/' $MY_CONDA_ENV/share/rubygems/bin/tractive

