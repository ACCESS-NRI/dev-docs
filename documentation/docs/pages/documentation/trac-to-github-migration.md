This page and documents the process for migration of Trac to GitHub, focusing on the migration of CABLE Trac tickets to GitHub issues, using [IETF-Ribose Tractive](https://github.com/ietf-ribose/tractive).

The full process is only partially documented at https://github.com/ietf-ribose/tractive with some necessary details missing. In summary, the full process is:
1. [Obtain all necessary permissions](#1-permissions).
1. [Set up communications between the migration host, the Trac server host, and GitHub](#2-communications).
1. [Set up a Conda environment and install all the required software](#3-software). 
1. [Use Reposurgeon to migrate the Subversion repository to Git](#4-reposurgeon).
1. [Build the SVN Revision to Git Commit RevMap](#5-revmap).
1. [Create the GitHub repository and grant permissions to relevant users](#6-repository).
1. [Bootstrap the Tractive config file](#7-bootstrapping).
1. [Create a Trac to GitHub user map](#8-user-map).
1. [Configure the Tractive config file](#9-configuration).
1. [Run Tractive](#10-running-tractive).
1. [Filter the local Git repository](#11-git-repository-filtering).
1. [Upload the local Git repository to GitHub](#12-uploading-the-git-repository-to-github).

These steps are described in more detail below.

## 1. Permissions
For the migration of CABLE Trac from https://trac.nci.org.au/trac/cable to https://github.com/CABLE-LSM/CABLE-Trac the following permissions are needed, at the minimum:
1. Permission to migrate from CABLE Subversion and CABLE Trac.

   Ensure that you can use an NCI userid with 
   1. SSH login permission to trac.nci.org.au
   1. File system permissions on trac.nci.org.au to Apache, Subversion and Trac directories such as
      ```
      /data/backups/svn
      /data/httpd/default/html/svn
      /data/svn
      /usr/lib64/python2.7/site-packages/svn
      /usr/lib/python2.7/site-packages/tracopt/versioncontrol/svn
      /var/www.old/html/svn
      ```
      ```
      /data/backups/trac
      /data/httpd/trac
      /data/httpd/usage/trac
      /data/trac
      /etc/trac
      /usr/lib/python2.7/site-packages/trac
      /usr/share/trac
      ```
1. Permission to create and populate CABLE-LSM repositories such as https://github.com/CABLE-LSM/CABLE-Trac.
 
   Ensure that you can use a GitHub userid that is a member of both of the https://github.com/orgs/CABLE-LSM teams [Admins](https://github.com/orgs/CABLE-LSM/teams/Admins) and [devs](https://github.com/orgs/CABLE-LSM/teams/devs). 

## 2. Communications
Setting up communications between the migration host, the Trac server host, and GitHub involves setting up SSH keys and configurations. In the case of migrating CABLE Trac from trac.nci.org.au to GitHub, the migration host is Gadi login and the Trac server host is trac.nci.org.au.
The reasons why `trac.nci.org.au` itself could not be used as the migration host are 
1. The software on `trac.nci.org.au` is quite old, making it harder to set up current Conda and Ruby software.
2. The `trac.nci.org.au` host itself is due to be retired, probably by the end of 2023.
3. At the time that I set up the migration software at `/g/data/tm70`, the user `pcl851` did not have needed permissions to install software on `trac.nci.org.au`.

The complication involved in setting up communication between Gadi and `trac.nci.org.au` is that `trac.nci.org.au` is accessible only from `accessdev.nci.org.au`, making it necessary to configure an SSH `ProxyJump`.

The documentation for setting up SSH communication to GitHub is at https://docs.github.com/en/authentication/connecting-to-github-with-ssh

The user `pcl851` has the following files set up on each of Gadi, Accessdev, and trac.nci.org.au:

### Gadi
`~/.ssh/authorized_keys`: Authorized keys including:
```
ssh-rsa A... pcl851@accessdev.nci.org.au
ssh-rsa A... pcl851@tracv7.nci.org.au
```
`~/.ssh/config`: SSH config containing:
```
Host accessdev
    HostName accessdev
    IdentityFile ~/.ssh/id_rsa_trac
    IdentitiesOnly yes
#
Host trac
    HostName trac
    IdentityFile ~/.ssh/id_rsa_trac
    IdentitiesOnly yes
    ProxyJump accessdev
```
`~/.ssh/id_ed25519*`: Private and public SSH keys for GitHub.

`~/.ssh/id_rsa_trac*`: Private and public SSH keys for Trac.

`~/.ssh/known_hosts`: Known hosts including:
```
accessdev,130.56.244.72 ssh-rsa A...
trac ecdsa-sha2-nistp256 A...
github.com ssh-ed25519 A...
```
### Accessdev
`~/.ssh/authorized_keys`: Authorized keys including:

```
ssh-rsa A... pcl851@gadi-login-02.gadi.nci.org.au
ssh-rsa A... pcl851@gadi-login-04.gadi.nci.org.au
ssh-rsa A... pcl851@tracv7.nci.org.au
```
`~/.ssh/id_rsa_trac*`: Private and public SSH keys for Trac.

`~/.ssh/known_hosts`: Known hosts including:
```
trac,192.43.239.236 ssh-rsa A...
gadi,203.0.19.85 ssh-rsa A...
gadi.nci.org.au ssh-rsa A...
```

### trac.nci.org.au
`~/.ssh/authorized_keys`: Authorized keys including:
```
ssh-rsa A... pcl851@accessdev.nci.org.au
ssh-rsa A... pcl851@gadi-login-02.gadi.nci.org.au
ssh-rsa A... pcl851@accessdev.nci.org.au
ssh-rsa A... pcl851@gadi-login-04.gadi.nci.org.au
```
`~/.ssh/id_rsa_trac*`: Private and public SSH keys for Trac.

`~/.ssh/known_hosts`: Known hosts including:
```
accessdev,130.56.244.72 ssh-rsa A...
gadi,203.0.19.85 ecdsa-sha2-nistp256 A...
```
## 3. Software
The main software components used in the migration are [Reposurgeon](http://www.catb.org/~esr/reposurgeon/) and [IETF-Ribose Tractive](https://github.com/ietf-ribose/tractive). [PyGitHub](https://pygithub.readthedocs.io/en/stable/introduction.html) is also used, mainly to look up GitHub usernames. [git filter-repo](https://github.com/newren/git-filter-repo) is used to enable the upload of the migrated local Git repository to GitHub.

The easiest way to track and maintain the software needed for the migration of Trac to GitHub is to create a Conda environment.
This is despite the fact that Reposurgeon is written in Go, and IETF-Ribose Tractive is written in Ruby.

A script to create a Conda environment for the migration is included as [Trac-to-GitHub-migration/bin/install-tractive-conda.sh](https://github.com/ACCESS-NRI/dev-docs/blob/main/Trac-to-Github-migration/bin/install-tractive-conda.sh) in this repository.
The corresponding script to install the Ruby Gem for IETF-Ribose Tractive is [Trac-to-GitHub-migration/bin/install-tractive-gem.sh](https://github.com/ACCESS-NRI/dev-docs/blob/main/Trac-to-Github-migration/bin/install-tractive-gem.sh).

A typical Conda environment for Reposurgeon and IETF-Ribose Tractive would be similar to the following list, including `git-filter-repo`, `pygithub`, `reposurgeon` and `ruby`:
```
(base) conda list
# packages in environment at /scratch/tm70/pcl851/conda/envs/tractive:
#
# Name                    Version                   Build  Channel
_libgcc_mutex             0.1                 conda_forge    conda-forge
_openmp_mutex             4.5                       2_gnu    conda-forge
archspec                  0.2.1              pyhd3eb1b0_0  
binutils                  2.40                 hdd6e379_0    conda-forge
binutils_impl_linux-64    2.40                 hf600244_0    conda-forge
binutils_linux-64         2.40                 hbdbef99_2    conda-forge
boltons                   23.0.0          py311h06a4308_0  
brotli-python             1.0.9           py311h6a678d5_7  
bzip2                     1.0.8                h7b6447c_0  
c-ares                    1.19.1               h5eee18b_0  
c-compiler                1.7.0                hd590300_0    conda-forge
ca-certificates           2023.12.12           h06a4308_0  
certifi                   2023.11.17      py311h06a4308_0  
cffi                      1.16.0          py311h5eee18b_0  
charset-normalizer        2.0.4              pyhd3eb1b0_0  
conda                     23.11.0         py311h06a4308_0  
conda-libmamba-solver     23.12.0            pyhd3eb1b0_1  
conda-package-handling    2.2.0           py311h06a4308_0  
conda-package-streaming   0.9.0           py311h06a4308_0  
cryptography              41.0.7          py311hdda0065_0  
curl                      8.5.0                hdbd6064_0  
cxx-compiler              1.7.0                h00ab1b0_0    conda-forge
deprecated                1.2.14             pyh1a96a4e_0    conda-forge
distro                    1.8.0           py311h06a4308_0  
fmt                       9.1.0                hdb19cb5_0  
gcc                       12.3.0               h8d2909c_2    conda-forge
gcc_impl_linux-64         12.3.0               he2b93b0_3    conda-forge
gcc_linux-64              12.3.0               h76fc315_2    conda-forge
gdbm                      1.18                 h0a1914f_2    conda-forge
gettext                   0.21.1               h27087fc_0    conda-forge
git                       2.43.0          pl5321h7bc287a_0    conda-forge
git-filter-repo           2.38.0             pyhd8ed1ab_0    conda-forge
gmp                       6.3.0                h59595ed_0    conda-forge
gxx                       12.3.0               h8d2909c_2    conda-forge
gxx_impl_linux-64         12.3.0               he2b93b0_3    conda-forge
gxx_linux-64              12.3.0               h8a814eb_2    conda-forge
icu                       73.1                 h6a678d5_0  
idna                      3.4             py311h06a4308_0  
jsonpatch                 1.32               pyhd3eb1b0_0  
jsonpointer               2.1                pyhd3eb1b0_0  
kernel-headers_linux-64   2.6.32              he073ed8_16    conda-forge
krb5                      1.20.1               h143b758_1  
ld_impl_linux-64          2.40                 h41732ed_0    conda-forge
libarchive                3.6.2                h6ac8c49_2  
libcurl                   8.5.0                h251f7ec_0  
libedit                   3.1.20230828         h5eee18b_0  
libev                     4.33                 h7f8727e_1  
libexpat                  2.5.0                hcb278e6_1    conda-forge
libffi                    3.4.4                h6a678d5_0  
libgcc-devel_linux-64     12.3.0             h8bca6fd_103    conda-forge
libgcc-ng                 13.2.0               h807b86a_3    conda-forge
libgomp                   13.2.0               h807b86a_3    conda-forge
libiconv                  1.17                 hd590300_2    conda-forge
libmamba                  1.5.6                haf1ee3a_0  
libmambapy                1.5.6           py311h2dafd23_0  
libnghttp2                1.57.0               h2d74bed_0  
libsanitizer              12.3.0               h0f45ef3_3    conda-forge
libsodium                 1.0.18               h36c2ea0_1    conda-forge
libsolv                   0.7.24               he621ea3_0  
libssh2                   1.10.0               hdbd6064_2  
libstdcxx-devel_linux-64  12.3.0             h8bca6fd_103    conda-forge
libstdcxx-ng              13.2.0               h7e041cc_3    conda-forge
libuuid                   1.41.5               h5eee18b_0  
libxcrypt                 4.4.36               hd590300_1    conda-forge
libxml2                   2.10.4               hf1b16e4_1  
libzlib                   1.2.13               hd590300_5    conda-forge
lz4-c                     1.9.4                h6a678d5_0  
menuinst                  2.0.1           py311h06a4308_1  
ncurses                   6.4                  h6a678d5_0  
openssl                   3.2.0                hd590300_1    conda-forge
packaging                 23.1            py311h06a4308_0  
pcre2                     10.42                hebb0a14_0  
perl                      5.32.1          7_hd590300_perl5    conda-forge
pip                       23.3.1          py311h06a4308_0  
platformdirs              3.10.0          py311h06a4308_0  
pluggy                    1.0.0           py311h06a4308_1  
pybind11-abi              4                    hd3eb1b0_1  
pycosat                   0.6.6           py311h5eee18b_0  
pycparser                 2.21               pyhd3eb1b0_0  
pygithub                  2.1.1              pyhd8ed1ab_0    conda-forge
pyjwt                     2.8.0              pyhd8ed1ab_0    conda-forge
pynacl                    1.5.0           py311h459d7ec_3    conda-forge
pyopenssl                 23.2.0          py311h06a4308_0  
pysocks                   1.7.1           py311h06a4308_0  
python                    3.11.7               h955ad1f_0  
python-dateutil           2.8.2              pyhd8ed1ab_0    conda-forge
python_abi                3.11                    2_cp311    conda-forge
pyyaml                    6.0.1           py311h459d7ec_1    conda-forge
readline                  8.2                  h5eee18b_0  
reposurgeon               4.35                          0    dnachun
reproc                    14.2.4               h295c915_1  
reproc-cpp                14.2.4               h295c915_1  
requests                  2.31.0          py311h06a4308_0  
ruamel.yaml               0.17.21         py311h5eee18b_0  
ruby                      3.2.2                h983345b_1    conda-forge
setuptools                68.2.2          py311h06a4308_0  
six                       1.16.0             pyh6c4a22f_0    conda-forge
sqlite                    3.41.2               h5eee18b_0  
sysroot_linux-64          2.12                he073ed8_16    conda-forge
tk                        8.6.12               h1ccaba5_0  
tqdm                      4.65.0          py311h92b7b1e_0  
truststore                0.8.0           py311h06a4308_0  
typing-extensions         4.9.0                hd8ed1ab_0    conda-forge
typing_extensions         4.9.0              pyha770c72_0    conda-forge
tzdata                    2023d                h04d1e81_0  
urllib3                   1.26.18         py311h06a4308_0  
wheel                     0.41.2          py311h06a4308_0  
wrapt                     1.16.0          py311h459d7ec_0    conda-forge
xz                        5.4.5                h5eee18b_0  
yaml                      0.2.5                h7f98852_2    conda-forge
yaml-cpp                  0.8.0                h6a678d5_0  
zlib                      1.2.13               hd590300_5    conda-forge
zstandard                 0.19.0          py311h5eee18b_0  
zstd                      1.5.5                hc292b87_0  
```
Rather than using the `~/.bashrc` edits added by `conda init`, the following convenience function is added to [Trac-to-GitHub-migration/bin/conda-env-tractive.sh](https://github.com/ACCESS-NRI/dev-docs/blob/main/Trac-to-Github-migration/bin/conda-env-tractive.sh) and used instead:
```
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
```
The script also contains the following function to replace `conda activate`:
```
conda_activate() {
conda_env_tractive
eval "$(conda shell.bash activate)"
}
```
It is recommended that your `~/.bashrc` contains the line
```
source /g/data/tm70/pcl851/tractive/bin/conda-env-tractive.sh
```
so that the environment variable `MY_CONDA_ENV` and the functions `conda_env_tractive` and `conda_activate` are always available to the Bash shell.

Additionally, the following Ruby gems are installed, including `ruby` and `tractive`:
```
(base) gem list

*** LOCAL GEMS ***

abbrev (default: 0.1.1)
activesupport (7.1.3)
base64 (default: 0.1.1)
benchmark (default: 0.2.1)
bigdecimal (default: 3.1.3)
bundler (default: 2.4.10)
cgi (default: 0.3.6)
concurrent-ruby (1.2.3)
connection_pool (2.4.1)
csv (default: 3.2.6)
date (default: 3.3.3)
delegate (default: 0.3.0)
did_you_mean (default: 1.6.3)
digest (default: 3.1.1)
domain_name (0.6.20240107)
drb (default: 2.1.1)
english (default: 0.7.2)
erb (default: 4.0.2)
error_highlight (default: 0.5.1)
etc (default: 1.4.2)
fcntl (default: 1.0.2)
fiddle (default: 1.1.1)
fileutils (default: 1.7.0)
find (default: 0.1.1)
forwardable (default: 1.3.3)
getoptlong (default: 0.2.0)
graphql (1.13.3)
graphql-client (0.18.0)
http-accept (1.7.0)
http-cookie (1.0.5)
i18n (1.14.1)
io-console (default: 0.6.0)
io-nonblock (default: 0.2.0)
io-wait (default: 0.3.0)
ipaddr (default: 1.2.5)
irb (default: 1.6.2)
json (default: 2.6.3)
logger (default: 1.5.3)
mime-types (3.5.2)
mime-types-data (3.2023.1205)
minitest (5.21.2)
mutex_m (default: 0.1.2)
mysql2 (0.5.5)
net-http (default: 0.3.2)
net-protocol (default: 0.2.1)
netrc (0.11.0)
nkf (default: 0.1.2)
observer (default: 0.1.1)
open-uri (default: 0.3.0)
open3 (default: 0.1.2)
openssl (default: 3.1.0)
optparse (default: 0.3.1)
ostruct (default: 0.5.5)
ox (2.14.17)
pathname (default: 0.2.1)
pp (default: 0.4.0)
prettyprint (default: 0.1.1)
pstore (default: 0.1.2)
psych (default: 5.0.1)
racc (default: 1.6.2)
rdoc (default: 6.5.0)
readline (default: 0.0.3)
readline-ext (default: 0.1.5)
reline (default: 0.3.2)
resolv (default: 0.2.2)
resolv-replace (default: 0.1.1)
rest-client (2.1.0)
rinda (default: 0.1.1)
ruby2_keywords (default: 0.0.5)
securerandom (default: 0.2.2)
sequel (5.76.0)
set (default: 1.0.3)
shellwords (default: 0.1.0)
singleton (default: 0.1.1)
sqlite3 (1.7.0 x86_64-linux)
stringio (default: 3.0.4)
strscan (default: 3.0.5)
syntax_suggest (default: 1.0.2)
syslog (default: 0.1.1)
tempfile (default: 0.1.3)
thor (1.3.0)
time (default: 0.2.2)
timeout (default: 0.3.1)
tmpdir (default: 0.1.3)
tractive (1.0.26)
tsort (default: 0.1.1)
tzinfo (2.0.6)
un (default: 0.2.1)
uri (default: 0.12.1)
weakref (default: 0.1.2)
yaml (default: 0.2.1)
zlib (default: 3.0.0)
```

## 4. Reposurgeon
This section describes the use of [Reposurgeon](http://www.catb.org/~esr/reposurgeon/repository-editing.html) to migrate a Subversion repository to Git. In the case of migration of CABLE Trac to GitHub, the Subversion repository is https://trac.nci.org.au/svn/cable/

The brief summary of the migration steps given on the [IETF-Ribose Tractive page](https://github.com/ietf-ribose/tractive#migrate-svn) is incomplete and incorrect in parts. 
1. Step 1 should say `repotool initialize {name-of-repo} {source-vcs-type} {destination-vcs-type}`. 
   In the case of migration of CABLE Trac to GitHub, in the working directory `/g/data/tm70/pcl851/tractive/cable-trac-github`:
   ```
   $ conda_activate
   $ repotool initialize cable svn git
   ```
2. In Step 2, the `--branchify` option [was retired after Reposurgeon 4.30](http://www.catb.org/esr/reposurgeon/repository-editing.html), so in the case of migration of CABLE Trac to GitHub, `READ_OPTIONS` remains empty, and the following changes are made to `Makefile`:
   ```
   $ diff -ub Makefile ../cable-trac-github/Makefile 
   --- Makefile    2023-09-28 09:59:03.000000000 +1000
   +++ ../cable-trac-github/Makefile       2023-09-28 10:12:35.000000000 +1000
   @@ -34,9 +34,9 @@
    #
   
    EXTRAS = 
   -REMOTE_URL = svn://svn.debian.org/cable
   +REMOTE_URL = https://trac.nci.org.au/svn/cable
    #REMOTE_URL = https://cable.googlecode.com/svn/
   -CVS_HOST = cable.cvs.sourceforge.net
   +#CVS_HOST = cable.cvs.sourceforge.net
    #CVS_HOST = cvs.savannah.gnu.org
    CVS_MODULE = cable
    #REMOTE_URL = cvs://$(CVS_HOST)/cable\#$(CVS_MODULE)
   ``` 
3. Step 3 is OK.
4. Step 4 (downloading the Subversion repository in mirror mode) is quite complicated and needs a more detailed description.
   In the case of migration of CABLE Trac to GitHub, the URL `svn://trac.nci.org.au/svn/cable/` does not work from Gadi login. It fails with (e.g.):

   ```
   $ svn list svn://trac.nci.org.au/svn/cable
   svn: E170013: Unable to connect to a repository at URL 'svn://trac.nci.org.au/svn/cable'
   svn: E000113: Can't connect to host 'trac.nci.org.au': No route to host
   ```
   Also, to prevent Subversion from storing plaintext passwords, the file `~/.subversion/servers` must contain (e.g.)
   ```
   [groups]
   ncitrac = trac.nci.org.au

   [global]

   [ncitrac]
   username = pcl851
   store-plaintext-passwords = no
   ```
   Once this is done, the URL https://trac.nci.org.au/svn/cable works.
   ```
   $ svn list https://trac.nci.org.au/svn/cable
   Authentication realm: <https://trac.nci.org.au:443> NCI Projects
   Password for 'pcl851': ******************

   branches/
   tags/
   trunk/
   ```
   The steps to create the mirror of the Subversion CABLE repository are then:
   ```
   $ conda_activate
   $ svnrdump dump https://trac.nci.org.au/svn/cable >cable.dump
   $ svnadmin create cable-mirror
   $ cp -a cable-mirror/hooks/pre-revprop-change.tmpl cable-mirror/hooks/pre-revprop-change
   $ repocutter expunge '.git'  '.gitignore' < cable.dump > cable.filtered.dump
   $ mkdir -p logs
   $ svnadmin load cable-mirror < cable.filtered.dump 2>&1 | tee logs/cable-mirror.load.log
   ```
   Note that if the `repocutter` command is omitted, the load log indicates that some of the Subversion commits for CABLE include `.git` directories:
   ```
   $ grep '\/\.git\/' cable-mirror.load.log |sed 's/\/\.git\/.*/\/.git\//'|sort -u|more
     * editing path : branches/Users/jxs599/CABLE/dev/2014/ACCESS-offline/PostProcessBin2NCDF-mapped/ACCESS_forcing_pkg/.git/
     * editing path : branches/Users/jxs599/CABLE/dev/2014/model_analysis1_NetbeansGit/.git/
     * editing path : branches/Users/jxs599/CABLE/dev/2014/T-DependenceVcmax_svn/python/.git/
     * editing path : branches/Users/jxs599/CABLE/dev/branches/2014/Research/model_analysis1/.git/
     * editing path : branches/Users/jxs599/CABLE/Tickets/Ticket49/Ticket49diff_strip.py/.git/
     * editing path : branches/Users/jxs599/CABLE/tools/CABLE_benchmarking_template/.git/
     * editing path : branches/Users/mm3972/CABLE_documentation/.git/
   ```
   [GitHub and Gitlab do not allow pushes](https://stackoverflow.com/questions/63096268/git-push-failed-with-error-object-hasdotgit-contains-git) if the directory tree being pushed contains a `.git` directory.
   The error message is generated by `git fsck` and is similar to:
   ```
   remote: error: object ...: hasDotgit: contains '.git'
   remote: fatal: fsck error in packed object
   ```
   The [Reposurgeon documentation](http://www.catb.org/esr/reposurgeon/repository-editing.html#_avoid_git_svn_lossage_with_repocutter_filtering) says to use `repocutter` as follows:
   ```
   $ repocutter expunge "/.git$"  "/.gitignore$"
   ```
   but this actually produces an output dump file identical to the input. The [Repocutter documentation](http://www.catb.org/~esr/reposurgeon/repocutter.html) explains that

   > In the command descriptions, PATTERN arguments are regular expressions to match pathnames, constrained so that each match must be a path segment or a sequence of path segments; that is, the left end must be either at the start of path or immediately following a /, and the right end must precede a / or be at end of string.
 
5. Step 5 involves running `make stubmap`.
   In the case of migration of CABLE Trac to GitHub, the command used is
   ```
   $ mkdir -p logs
   $ make stubmap 2>&1 | tee logs/make-stubmap.log
   ```
   so that a log file is also created. The resulting `cable.map` file then undergoes postprocessing as follows.
   1. Start with the the RTF file, `current_cable_users.rtf` provided by Jhan Srbinovsky.
   2. On a Macbook, using MacOS TextEdit, [convert this file to plain text](https://support.lesley.edu/support/solutions/articles/4000111343-how-to-convert-a-document-into-plain-text-in-textedit-on-a-mac) as `current_cable_users.txt`.
   3. Upload this file to the working directory.
   4. In the working directory, on Gadi login, run
      ```
      $ sed '/./{H;$!d} ; x ; s/\ncn:[:]*/ =/' current_cable_users.txt|sort -u > current_cable_users.sorted.txt
      ```
      This produces a file that is almost clean enough for further processing.
   5. Use `gvim` to manually clean up `current_cable_users.sorted.txt`: remove the initial blank line, then capitalize and repair names, to produce `current_cable_users.clean.txt`.
   6. Sort `cable.map` as follows:
      ```
      $ cp -a cable.map cable.map.orig
      $ sort -u cable.map > cable.sorted.map
      ```
   7. Use the Python script [format_author_map.py](https://github.com/ACCESS-NRI/dev-docs/blob/main/Trac-to-GitHub-migration/bin/format_author_map.py) to produce the sorted, postprocessed `cable.map` as follows;
      ```
      $ conda_activate
      $ ../bin/format_author_map.py cable.sorted.map current_cable_users.clean.txt >cable.map
      ```

6. Step 6 involves running `make`.
   The `make` succeeds, but due to Step 4, it renumbers the commits. Note also that running `make` creates both the stream dump file `cable.svn` and the `cable-git` repository. At this point, the repository is local to Gadi and has not yet been uploaded to GitHub.

## 5. Revmap
The next step in the Trac to GitHub migration process, [as documented by the Tractive page](https://github.com/ietf-ribose/tractive#building-the-trac-revision-to-git-commit-revmap) is generating the RevMap.

In the case of migration of CABLE Trac to GiHub, the following commands are used.
```
$ conda_activate
$ tractive generate revmap --svn-url https://trac.nci.org.au/svn/cable --git-local-repo-path $(pwd)/cable-git --rev-timestamp-file cable.fo --revmap-output-file cable.revmap.txt
...
Progress: [==================================================] 100.00% |[2023-09-29 02:04:51] INFO  | 

Following revisions are skipped because they don't have a corresponding git commit. []
$
```
Note that the same `tractive` command, using `--svn-local-path` instead of `--svn-url` fails.
```
$ tractive generate revmap --svn-local-path $(pwd)/cable-mirror --git-local-repo-path $(pwd)/cable-git --rev-timestamp-file cable.fo --revmap-output-file cable.revmap.txt
Progress: [====                                              ] 9.49% |
svn: E155007: '/g/data/tm70/pcl851/tractive/cable-trac-github/cable-mirror' is not a working copy
/g/data/tm70/pcl851/envs/tractive/share/rubygems/gems/tractive-1.0.22/lib/tractive/revmap_generator.rb:94:in `load': invalid format, document not terminated at line 3, column 3 [parse.c:561] (Ox::ParseError)
...
```

## 6. Repository
In order to migrate Trac to GitHub, you need to create a GitHub repository to host the GitHub issues.

In the case of migrating CABLE Trac to GitHub, the repository is https://github.com/CABLE-LSM/CABLE-Trac, created from the https://github.com/orgs/CABLE-LSM/repositories page.

1. On the https://github.com/orgs/CABLE-LSM/repositories page, create the repository.
1. On the https://github.com/CABLE-LSM/CABLE-Trac/settings/access page, click on the Add Teams button and add `CABLE-LSM/devs` with `Role: Write`.
1. You will also need to create a Personal Access Token for organizational repositories. At https://github.com/settings/tokens create a Personal Access Token with scopes: `admin:org, admin:public_key, admin:repo_hook, repo, user`. Some of these scopes are not strictly necessary.

## 7. Bootstrapping
The process for [Boostrapping the Tractive configuration file](https://github.com/ietf-ribose/tractive#boostrapping-the-tractive-configuration-file) is documented on the IETF-Ribose Tractive documentation page.
Unfortunately that documentation is also incomplete and slightly incorrect.

In the case of the migration of the CABLE Trac to GitHub, the following steps are performed:

```
(base) CONFIG_YAML=$(find /scratch/tm70/pcl851/conda/envs/tractive -name config.example.yaml)
(base) echo $CONFIG_YAML
/scratch/tm70/pcl851/conda/envs/tractive/share/rubygems/gems/tractive-1.0.26/config.example.yaml
(base) cp $CONFIG_YAML tractive.config.yaml
```
In `tractive.config.yaml`, replace
```
trac:
  # Trac database location
  database: sqlite://db/trac.db
  # database: mysql2://user:password@host:port/database
  # database: mysql2://root:password@mysql:3306/foobar

  # URL of the Trac "tickets" interface
  ticketbaseurl: https://example.org/trac/foobar/ticket

# GitHub-specific information
github:
  # Target GitHub organization and repo name
  repo: 'example-org/target-repository'

  # GitHub user Personal Access Token
  token: [redacted]

# RevMap file to use for migration
revmap_path: ./example-revmap.txt
```
with
```
trac:
  # Trac database location
  database: sqlite://data/trac/cable/db/trac.db

  # URL of the Trac "tickets" interface
  ticketbaseurl: https://trac.nci.org.au/trac/cable

# GitHub-specific information
github:
  # Target GitHub organization and repo name
  repo: 'CABLE-LSM/CABLE-Trac'

  # GitHub user Personal Access Token
  token: [redacted]

  local_repo_path: ./cable-git
# RevMap file to use for migration
revmap_path: ./cable.revmap.txt
```
The bootstrapping then proceeds as follows:
```
$ conda_activate
$ mkdir -p data/trac/cable/db
$ rsync -a trac:/data/trac/cable/db/*.db data/trac/cable/db
$ tractive -i 2>&1 | tee tractive.config.bootstrap.yaml
```
Note that here we have copied the Sqlite `*.db` file from the `trac` server since Gadi login has SSH access to `trac`, but SQLite3
cannot see the database remotely. Without this copy, the `tractive -i` bootstrapping results in the following error.
```
$ tractive -i
[2023-10-04 19:15:11] ERROR | SQLite3::CantOpenException: unable to open database file
```

## 8. User Map
[The IETF-Ribose Tractive documentation](https://github.com/ietf-ribose/tractive) [describes the Trac to GitHub user mapping within the Tractive configuration file](https://github.com/ietf-ribose/tractive#user-mapping) `tractive.config.yaml` but does not provide any method to automate this mapping beyond the [creation of the bootstrap configuration information](https://github.com/ietf-ribose/tractive#bootstrapping-the-configuration-file-with-information).

In the case of migration of CABLE Trac to GitHub, in the working directory `/g/data/tm70/pcl851/tractive/cable-trac-github`, run the following commands:
```
$ conda_activate
$ sed -i '1d' tractive.config.bootstrap.yaml
$ export PYTHONPATH=$PWD/../bin:$PYTHONPATH
$ ../bin/bootstrap_tractive_users.py cable.map tractive.config.bootstrap.yaml >tractive.config.users.raw.yaml
```
where [bootstrap_tractive_users.py](https://github.com/ACCESS-NRI/dev-docs/blob/main/Trac-to-GitHub-migration/bin/bootstrap_tractive_users.py) uses the two files `cable.map` and `tractive.config.bootstrap.yaml` to create a YAML file with GitHub usernames corresponding to most of the NCI usernames found in these two files. 

The output file `tractive.config.users.raw.yaml` is then postprocessed:
```
$ sed "s/? ''/'':/;s/: email:/  email:/" tractive.config.users.raw.yaml >tractive.config.users.yaml
```

## 9. Configuration
The Tractive config file is configured in stages.

In Stage 1, the previously created files are split and combined as follows:
```
$ cp -a tractive.config.yaml tractive.config.orig.yaml
$ csplit -f tractive.config.orig. tractive.config.orig.yaml '/^users:/';chmod go-rwx tractive.config.orig.*
$ csplit -f tractive.config.bootstrap. tractive.config.bootstrap.yaml '/^milestones:/'
$ rm tractive.config.orig.01 tractive.config.bootstrap.00
$ cat tractive.config.orig.00 tractive.config.users.yaml tractive.config.bootstrap.01 > tractive.config.yaml;chmod go-rwx tractive.config.yaml 
```

Stage 2 exists because the user map in the config file is incomplete. It does not necessarily include all of the Trac ticket owners as users.
To find all of these owners, create a personal GitHub repository and run `tractive` to migrate the Trac tickets to GitHub issues.

In the case of migration of CABLE Trac to GitHub, Stage 2 includes the following steps.
1. Save a copy of `tractive.config.yaml` as `tractive.config.all.0.yaml`.
1. Add the following lines to `tractive.config.yaml`:
   ```
   ticket:
       delete_mocked: true
   ```
   This is to avoid [the following error](https://github.com/ietf-ribose/tractive/issues/107):
   ```
   /g/data/tm70/pcl851/envs/trac/share/rubygems/gems/tractive-1.0.22/lib/tractive/migrator/engine.rb:66:in `initialize': undefined method `[]' for nil:NilClass (NoMethodError)
         @delete_mocked_tickets = args[:cfg]["ticket"]["delete_mocked"]
   ```
   Note: [Newer versions of Tractive have better error messages](https://github.com/ietf-ribose/tractive/pull/109).
1. Create the personal https://github.com/penguian/cable-trac repository.
1. Create a [GitHub user Personal Access Token](https://github.com/settings/tokens) with  `repo` and `user` scopes to allow `tractive` to add issues to the personal repository. 
1. Edit `tractive.config.yaml` to change `github:` `repo:` to `penguian/cable-trac`, `token:` to the new personal access token,
and every instance of `username:` to `penguian` (the owner of the personal repository). Save a copy as `tractive.config.personal.1.yaml`.
1. Run Tractive as follows:
   ```
   $ conda_activate
   (base) tractive --verbose 2>&1 | tee logs/tractive.personal.1.log
   ``` 
   This may result in an error such as:
   ```
   [2024-01-30 15:18:06] ERROR | Unable to find Github username for srb001@csiro.au this can be set in the config file.
   ```
   Each time this error occurs, add the owner as a new user in `tractive.config.yaml` and run Tractive again as above, replacing `personal.1.` with `personal.n.` for each step `n`.
1. In this case, the users added after two runs are:
   ```
   ned@nedhaughton.com:
     email: ned@nedhaughton.com
     name: Ned Haughton
     username: penguian
   [...]
   srb001@csiro.au:
     email: srb001@csiro.au
     name: Jhan Srbinovsky
     username: penguian
   ```
1. In this case, the `tractive` command succeeds on the third run.
1. Run the following command to obtain a list of owners.
   ```
   $ grep owner logs/tractive.personal.*.log | cut -d':' -f5 | sort -u > cable.owners.txt
   ```
   The resulting file `cable.owners.txt` contains 34 lines.
   ```
   $ wc -l cable.owners.txt
   34 cable.owners.txt
   ```
Stage 3 involves reconciling the owners obtained in Stage 2 with the members of the GitHub organization to be used for the organizational repository. In the case of migration of CABLE Trac to GitHub, this organization is CABLE-LSM.
The problem in this case is that the names provided in `current_cable_users.txt` don't always correspond to the names of users known to GitHub. Luckily, only the 24 members of the `dev` team in CABLE-LSM organization need to be examined. This stage proceeds with the following steps.
1. Create `tractive.config.owners.yaml`, containing the users that needed to be added to `tractive.config.yaml` in Stage 2.
   ```
   $ cat tractive.config.owners.yaml
     ned@nedhaughton.com:
       email: ned@nedhaughton.com
       name: Ned Haughton
       username: penguian
     srb001@csiro.au:
       email: srb001@csiro.au
       name: Jhan Srbinovsky
       username: penguian
   ```
1. Run the following commands to obtain a sorted list of CABLE users from the previously created `tractive.config.users.yaml` and `tractive.config.owners.yaml` as the file `extra_cable_users.txt`.
   ```
   $ cat tractive.config.users.yaml tractive.config.owners.yaml >tractive.config.users.owners.yaml
   $ grep '^  [^ ]' tractive.config.users.owners.yaml|sort >extra_cable_users.txt
   ```
   The resulting file contains 127 lines.
   ```
   $ wc -l extra_cable_users.txt 
   127 extra_cable_users.txt
   ```
1. Edit the `current_cable_users.clean.txt` file produced in [4 Reposurgeon](#4-reposurgeon) Step 5 to produce the file `current_cable_users.github.txt`, by changing the names of members of the `CABLE-LSM` `dev` team to their GitHub names. The differences are as follows.
   ```
   $ diff -y --suppress-common-lines current_cable_users.clean.txt current_cable_users.github.txt
   ab7412 = Alison Bennett                                       | ab7412 = Alison C Bennett
   amu561 = Anna Ukkola                                          | amu561 = aukkola
   aph502 = Aidan P Heerdegen                                    | aph502 = Aidan Heerdegen
   jxs599 = Jhan Srbinovsky                                      | jxs599 = JhanSrbinovsky
   mm3972 = Mengyuan Mu                                          | mm3972 = Mu Mengyuan
   rk4417 = Ramzi Kutteh                                         | rk4417 = rkutteh
   rml599 = Rachel Law                                           | rml599 = rml599gh
   yxw599 = Yingping Wang                                        | yxw599 = yingping Wang
   zh1263 = Zhongmin Hu                                          | zh1263 = zhongmin2023
   ```
1. Edit `current_cable_users.github.txt` to produce `current_cable_users.github.extra.txt`, by adding owners from `extra_cable_users.txt`
that correspond to members of the `CABLE-LSM` `dev` team, and also checking against `cable.owners.txt`. The differences are as follows.
   ```
   $ diff -y --suppress-common-lines current_cable_users.github.txt current_cable_users.github.extra.txt
                                                                 > B Pak = Bernard Pak
                                                                 > EAK/JS/BP = JhanSrbinovsky
                                                                 > jhan = JhanSrbinovsky
                                                                 > Jhan = JhanSrbinovsky
                                                                 > lxs599 jxs599 = Lauren Stevens
                                                                 > ned@nedhaughton.com = Ned Haughton
                                                                 > srb001@csiro.au = JhanSrbinovsky 
                                                                 > ying-ping wang = yingping Wang
                                                                 > yp wang = yingping Wang
   ```
1. Sort `current_cable_users.github.extra.txt` as follows, to produce `current_cable_users.github.extra.sorted.txt`.
   ```
   $ sort -k 3 current_cable_users.github.extra.txt > current_cable_users.github.extra.sorted.txt
1. Edit `cable.map` to produce `cable.github.map`, by changing the names of the `CABLE-LSM` `dev` team to their GitHub names, and adding missing members. The differences are as follows. 
   ```
   $ diff -yw --suppress-common-lines cable.map cable.github.map 
   ab7412 = Alison Bennett <ab7412@nci.org.au>                   | ab7412 = Alison C Bennett <ab7412@nci.org.au>
   amu561 = Anna Ukkola <amu561@nci.org.au>                      | amu561 = aukkola <amu561@nci.org.au>
                                                                 > aph502 = Aidan Heerdegen <aph502@nci.org.au>
   jxs599 = Jhan Srbinovsky <jxs599@nci.org.au>                  | jxs599 = JhanSrbinovsky <jxs599@nci.org.au>
   mm3972 = Mengyuan Mu <mm3972@nci.org.au>                      | mm3972 = Mu Mengyuan <mm3972@nci.org.au>
   rk4417 = Ramzi Kutteh <rk4417@nci.org.au>                     | rk4417 = rkutteh <rk4417@nci.org.au>
   rml599 = Rachel Law <rml599@nci.org.au>                       | rml599 = rml599gh <rml599@nci.org.au>
   yxw599 = Yingping Wang <yxw599@nci.org.au>                    | yxw599 = yingping Wang <yxw599@nci.org.au>
                                                                 > zh1263 = zhongmin2023 <zh1263@nci.org.au>
   ```
1. Run the following commands to set up the Python environment for Tractive and various Python scripts.
   ```
   $ conda_activate
   $ export PYTHONPATH=$PWD/../bin:$PYTHONPATH
   ```
1. Run the following command to use the Python script [format_github_map.py](https://github.com/ACCESS-NRI/dev-docs/blob/main/Trac-to-GitHub-migration/bin/format_github_map.py) to produce `cable.map`, a Trac to GitHub user map with complete and correct details.
   ```
   $ ../bin/format_github_map.py cable.github.map current_cable_users.github.extra.sorted.txt | sort -u > cable.map
   ```
1. Run the following command to use the Python script [create_tractive_users_as_devs.py](https://github.com/ACCESS-NRI/dev-docs/blob/main/Trac-to-GitHub-migration/bin/create_tractive_users_as_devs.py) to create a complete list of CABLE users, including their mapping to `CABLE-LSM` `dev` team members, as the file `tractive.config.users.as-devs.yaml`.
   ```
   $ ../bin/create_tractive_users_as_devs.py cable.map >tractive.config.users.as-devs.yaml
   ```
1. Split the previously created `tractive.config.yaml` file and combine it with `tractive.config.users.as-devs.yaml` as follows.
   ```
   $ csplit -f tractive.config. tractive.config.yaml '/^users:/' '/^milestones:/';chmod go-rwx tractive.config.00
   $ cat tractive.config.00 tractive.config.users.as-devs.yaml tractive.config.02 >tractive.config.yaml;chmod go-rwx tractive.config.yaml
   ```

## 10. Running Tractive
The final step in Trac to GitHub migration is to run Tractive. The [IETF-Ribose Tractive README file](https://github.com/ietf-ribose/tractive#running-tractive) gives a detailed description of how to run Tractive.

In the case of the CABLE Trac to GitHub migration, assuming that all of the previous steps have succeeded, run the following commands in the
`/g/data/tm70/pcl851/tractive/cable-trac-github` directory on Gadi login.
```
$ conda_activate
$ tractive --verbose 2>&1 | tee logs/tractive.organization.0.log
```
If the `tractive` command fails, the log should help to diagnose the problem.
Examples:

1.
   ```
   ERROR | 404 Not Found
   ```
   This sometimes occurs when the Personal Access Token does not include some necessary scope.

## 11. Git repository filtering

If an attempt is made to upload to GitHub the `cable-git` repository that was created by running the Resposurgeon `make` as per [Section 4](#4-reposurgeon) above, this is likely to fail because some blobs are too large for GitHub. The repository, including its entire hsitory, needs to be filtered to remove these large blobs.

1. Run the following commands in the `/g/data/tm70/pcl851/tractive/cable-trac-github` directory on Gadi login.
   ```
   $ conda_activate
   $ cd cable-git
   $ git filter-repo --analyze
   $ cd ..
   $ sort -n -r cable-git/.git/filter-repo/analysis/path-all-sizes.txt > cable-git-large-files.txt
   ```
1. Copy `cable-git-large-files.txt` to `cable-git-large-files.largest.txt` and edit this file to remove all references to blobs of less than (e.g.) 75 MB in unpacked size.
1. Run the following command in the `/g/data/tm70/pcl851/tractive/cable-trac-github` directory on Gadi login to produce a sorted list of paths.
   ```
   $ cut -c36- cable-git-large-files.largest.txt | sort > cable-git-large-files.largest.sorted.txt
   ```
1. Change directory to `/g/data/tm70/pcl851/tractive` and run the following `qsub` command to filter the `cable-git` repository,
   ```
   $ qsub bin/cable-git-filter-repo.pbs
   ```
   where `cable-git-filter-repo.pbs` is included as [Trac-to-GitHub-migration/bin/cable-git-filter-repo.pbs](https://github.com/ACCESS-NRI/dev-docs/blob/main/Trac-to-GitHub-migration/bin/cable-git-filter-repo.pbs) in this repository.
1. The log file `/g/data/tm70/pcl851/tractive/cable-trac-github/logs/cable-git-filter-repo.log` should now contain (e.g.)
   ```
   ...
   aa3958/mrd561/CABLE_AUX-dev/offline/CABLE_GSWP3_HGSD_DRT_Surface_Color_Data.nc
   Parsed 8980 commitsHEAD is now at 9303209ff first commit

   New history written in 34.49 seconds; now repacking/cleaning...
   Repacking your repo and cleaning out old unneeded objects
   Completely finished after 46.58 seconds.
   aa3958/mrd561/CABLE_AUX-dev/offline/CABLE_GSWP3_HGSD_DRT_Surface_Data_fix.nc
   Parsed 8980 commitsHEAD is now at 9303209ff first commit

   New history written in 20.95 seconds; now repacking/cleaning...
   Repacking your repo and cleaning out old unneeded objects
   Completely finished after 30.85 seconds.
   ...
   ```


## 12. Uploading the Git repository to GitHub

The filtered `cable-git` repository contains the following branches and remotes:
```
$ cd /g/data/tm70/pcl851/tractive/cable-trac-github/cable-git
$ git branch -a
  Registration
  Share
  Users
* main
$ git remote -v
origin	git@github.com:CABLE-LSM/CABLE-Trac.git (fetch)
origin	git@github.com:CABLE-LSM/CABLE-Trac.git (push)
```
Note: Uploading the repository could take some considerable time, so it is probably better to do so from an ARE terminal rather than Gadi login.

Starting with the `main` branch, upload each `BRANCH` to GitHub as follows.
```
$ cd /g/data/tm70/pcl851/tractive/cable-trac-github/cable-git
$ git checkout BRANCH
$ git push -u origin BRANCH | tee ../logs/git-push-u-origin-BRANCH.0.log
```
The content of the log files is (e.g.) as follows:
```
$ for log in ../logs/git-push-u-origin-*.log;do echo $log; cat $log; echo ""; done
../logs/git-push-u-origin-main.2.log
remote: warning: See https://gh.io/lfs for more information.        
remote: warning: File jk8585/Spatial_Vcmax/params/gm_LUT_351x3601x7_1pt8245_Bernacchi2002.nc is 67.53 MB; this is larger than GitHub's recommended maximum file size of 50.00 MB        
remote: warning: File lxs599/umplot/obs/ERA_INT_pr_8908.nc is 53.18 MB; this is larger than GitHub's recommended maximum file size of 50.00 MB        
remote: warning: File lxs599/umplot/obs/ERAi_monavg_t2m.nc is 56.72 MB; this is larger than GitHub's recommended maximum file size of 50.00 MB        
remote: warning: File vxh599/trunk_checks_extract_sli_optimise_JVratio/offline/param_files/climate_rst_CRU_glob.nc is 56.21 MB; this is larger than GitHub's recommended maximum file size of 50.00 MB        
remote: warning: File jk8585/Spatial_Vcmax/params/gm_LUT_351x3601x7_1pt8245_Walker2013.nc is 67.53 MB; this is larger than GitHub's recommended maximum file size of 50.00 MB        
remote: warning: GH001: Large files detected. You may want to try Git Large File Storage - https://git-lfs.github.com.        
To github.com:CABLE-LSM/CABLE-Trac.git
 * [new branch]          main -> main
branch 'main' set up to track 'origin/main'.

../logs/git-push-u-origin-Registration.0.log
remote: 
remote: Create a pull request for 'Registration' on GitHub by visiting:        
remote:      https://github.com/CABLE-LSM/CABLE-Trac/pull/new/Registration        
remote: 
To github.com:CABLE-LSM/CABLE-Trac.git
 * [new branch]          Registration -> Registration
branch 'Registration' set up to track 'origin/Registration'.

../logs/git-push-u-origin-Share.0.log
remote: warning: See https://gh.io/lfs for more information.        
remote: warning: File CABLE-POP_TRENDY/params/gm_LUT_351x3601x7_1pt8245_Bernacchi2002.nc is 67.53 MB; this is larger than GitHub's recommended maximum file size of 50.00 MB        
remote: warning: File CABLE-POP_TRENDY/params/gm_LUT_351x3601x7_1pt8245_Walker2013.nc is 67.53 MB; this is larger than GitHub's recommended maximum file size of 50.00 MB        
remote: warning: GH001: Large files detected. You may want to try Git Large File Storage - https://git-lfs.github.com.        
remote: 
remote: Create a pull request for 'Share' on GitHub by visiting:        
remote:      https://github.com/CABLE-LSM/CABLE-Trac/pull/new/Share        
remote: 
To github.com:CABLE-LSM/CABLE-Trac.git
 * [new branch]          Share -> Share
branch 'Share' set up to track 'origin/Share'.

../logs/git-push-u-origin-Users.0.log
remote: warning: See https://gh.io/lfs for more information.        
remote: warning: File 6b59c3d5298efbb81ddb5d901cb19d1e6027d017 is 67.53 MB; this is larger than GitHub's recommended maximum file size of 50.00 MB        
remote: warning: File 77552438e2eaab6e889eb86f476078b24326efb5 is 67.53 MB; this is larger than GitHub's recommended maximum file size of 50.00 MB        
remote: warning: GH001: Large files detected. You may want to try Git Large File Storage - https://git-lfs.github.com.        
remote: 
remote: Create a pull request for 'Users' on GitHub by visiting:        
remote:      https://github.com/CABLE-LSM/CABLE-Trac/pull/new/Users        
remote: 
To github.com:CABLE-LSM/CABLE-Trac.git
 * [new branch]          Users -> Users
branch 'Users' set up to track 'origin/Users'.
```

