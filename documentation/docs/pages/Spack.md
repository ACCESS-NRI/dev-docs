## Spack-related Repositories

ACCESS-NRI maintains three Spack-related repositories:
* https://github.com/ACCESS-NRI/spack - a fork of https://github.com/spack/spack containing the Spack core
* https://github.com/ACCESS-NRI/spack-config - ACCESS-NRI Spack configuration files
* https://github.com/ACCESS-NRI/access-spack-packages - Spack Package Receipes (SPRs) maintained by ACCESS-NRI that are not available by default in Spack

## Create and activate Spack instance on Gadi

Follow the [Set up Spack for building ACCESS models](https://access-hive.org.au/getting_started/spack/) instructions.

## Documentation

* https://forum.access-hive.org.au/t/spack-v1-cheat-sheet/5942
* https://forum.access-hive.org.au/t/debug-spack-error-failed-to-concretize/5878

## Spack v1 Caveats

The way to specify a compiler has changed in Spack v1. Now a specific compiler can be specified for different programming languages.
### Spack v0.22
#### 2021.10.0
```
    all:
      require:
        - '%intel@2021.10.0'
        - target=x86_64
```
#### 2025.2.0
```
    all:
      require:
        - '%oneapi@2025.2.0'
        - target=x86_64
```
### Spack v1
#### 2021.10.0
```
    c:
      require:
        - intel-oneapi-compilers-classic@2021.10.0
    cxx:
      require:
        - intel-oneapi-compilers-classic@2021.10.0
    fortran:
      require:
        - intel-oneapi-compilers-classic@2021.10.0
    all:
      require:
        - target=x86_64
```
#### 2025.2.0
```
    c:
      require:
        - intel-oneapi-compilers@2025.2.0
    cxx:
      require:
        - intel-oneapi-compilers@2025.2.0
    fortran:
      require:
        - intel-oneapi-compilers@2025.2.0
    all:
      require:
        - target=x86_64
```

## Build software using Spack

After enabling the Spack instance, find the available compilers:
```
spack compiler list
```

Then run `spack install`. e.g.
```
spack install mom5@access-esm1.6 type=ACCESS-ESM %intel@2021.2.0 target=x86_64
```

It is possible to do a reverse lookup of how an existing package was built. e.g.
```
spack find --json mom5@git.2025.03.001=access-om2 %intel@19.0.5.281 target=x86_64
```

Human readable format:
```
spack find --json mom5@git.2025.03.001=access-om2 %intel@19.0.5.281 target=x86_64 | python3 -m json.tool
```

Some useful switches:
```
  --keep-stage          don't remove the build stage if installation succeeds
  --source              install source files in prefix
```
e.g.
```
spack install --keep-stage oasis3-mct %intel@2021.10.0 target=x86_64
spack install --source oasis3-mct %intel@2021.10.0 target=x86_64
```

## Edit/Develop ACCESS Spack Package Recipes

Find the the git repository by running, `spack repo list`. Ensure that the git repository is not a shallow clone by running the command `git fetch --unshallow $ACCESS_SPACK_PACKAGES_PATH`, where `$ACCESS_SPACK_PACKAGES_PATH` is a placeholder for the path to the `access-spack-packages` git repository.

To edit the file, the command, `spack edit <package-name>` can be used.

## Architecture Specifiers

https://spack.readthedocs.io/en/latest/basic_usage.html#architecture-specifiers

## ACCESS-OM2 Docker Container (`x86`)

Download the Spack development [Dockerfile](https://github.com/ACCESS-NRI/build-ci/blob/main/containers/Dockerfile.base-spack) and then build the dev image by running:
```
docker build -f Dockerfile.base-spack -t spack-dev:20230915 --target=dev  .
```
It contains the relevant Intel Compilers used to build `ACCESS-OM2`.

## Compiler Flag Override

Spack allows the user to centrally [override compiler flags](https://spack.readthedocs.io/en/latest/basic_usage.html#specs-dependencies) on the CLI or in an environment's `spack.yaml` file. Spack will add these flags at the end of the compilation arguments.

For example, in an environment, the `spack.yaml` can be modified to include a `fflags` definition:
```
    mom5:
      require:
        - '@git.2025.03.001=access-om2'
        - fflags="-fp-model strict -check all -check noarg_temp_created -init=snan -init=array -init=huge"
```

If the source package uses a CMake or Autotools build system and the Spack Package Recipe (SPR) explicitly sets `flag_handler` to `build_system_flags`, then the compiler flag overrides should appear in the package's Spack build logs (i.e. What the source package's build system sees). When an SPR uses the default flag handler, `inject_flags`, the compiler flags injected via `spack.yaml` are *not* seen by the build system. They are only seen by Spack's compiler wrapper and recorded in the Spack debug build logs.

Some SPRs may contain a variant named `direct_ldflags` because using the `ldflags` variant does not achieve the desired outcome. Verify the existence of the variant by running `spack info <package-name>`. The `direct_ldflags` variant can take an arbitrary string as an argument. e.g. `cice4@git.access-esm1.6-2025.04.000=access-esm1.5 fflags="-flto" direct_ldflags="-fuse-ld=lld -flto"`.

### Pre-release test builds
The `spack-cc*.out` Spack debug build logs containing compiler flag overrides are available at `/g/data/vk83/prerelease/apps/spack/0.22/logs/`

### Spack develop
> [!WARNING]
> Only **advanced C/C++/Fortran programmers** should attempt to use this feature with [spack develop](https://spack-tutorial.readthedocs.io/en/latest/tutorial_developer_workflows.html). It is important to understand that `spack develop` is an iterative build mechanism:
>> When spack performs a rebuild on a development package, it reruns all the build stages for your package without cleaning the source and build directories to a pristine state. If your build system can take advantage of the previously compiled object files then you’ll end up with an iterative build.

To use this feature with `spack develop`, do:
```
  develop:
    mom5:
      spec: mom5@git.2025.03.001=access-om2 fflags="-fp-model strict -check all -check noarg_temp_created -init=snan -init=array -init=huge"
```
If there was a previous build *without* or *with different* `fflags`, then a `make clean` is required to delete all the intermediate object files in-order for the new `fflags` to be applied.

Before compiling, look at the concretization output to check if Spack is going to apply the `fflags`
```
spack concretize -f | grep init=huge
[+]  6q35mje      ^mom5@git.2025.03.001=access-om2%intel@2021.10.0 fflags='-init=huge -init=snan -check noarg_temp_created -check all -init=array -fp-model strict' ~access-gtracers~deterministic~optimisation_report+restart_repro build_system=makefile type=ACCESS-OM arch=linux-rocky8-x86_64
```

Alternatively, `fflags` can be set on the CLI. Using `==` will propagate the flags to the dependencies. e.g.
```
spack -d install access-om2 %intel@2021.2.0 fflags=="-fp-model strict -check all -check noarg_temp_created -init=snan -init=array -init=huge" target=x86_64
```

If debugging is enabled by running `spack -d install`, there will be `spack-cc*.out` Spack debug build logs, in the directory that the command was run, that will document the compilation flags that were used. e.g.
```
[cc] /opt/release/linux-rocky8-x86_64/gcc-8.5.0/intel-oneapi-compilers-2021.2.0-3qhetzew7usio4mf62bjbbpdkme76fd5/compiler/2021.2.0/linux/bin/intel64/ifort -march=pentium4 -mtune=generic -I/opt/release/linux-rocky8-x86_64/intel-2021.2.0/openmpi-4.0.2-yrzgzaf3aktomsybuzqycqtetgq6qg7c/include -I/opt/release/linux-rocky8-x86_64/intel-2021.2.0/openmpi-4.0.2-yrzgzaf3aktomsybuzqycqtetgq6qg7c/lib -I/opt/release/linux-rocky8-x86_64/intel-2021.2.0/oasis3-mct-access-om2-ihisq5h7eghddnrvvow7isyyvb6ibk4c/include -I/opt/release/linux-rocky8-x86_64/intel-2021.2.0/netcdf-fortran-4.6.1-rxizzakyuq2wc2afua2ncpjba7mvv2ax/include -I/opt/release/linux-rocky8-x86_64/intel-2021.2.0/netcdf-c-4.9.2-ztw3hzqgjb6rhk4gja4ry6fd4y5lhnpo/include -I/opt/release/linux-rocky8-x86_64/intel-2021.2.0/libaec-1.0.6-lwwrs7phnldnxesrgbpibslh5rspujfj/include -I/opt/release/linux-rocky8-x86_64/intel-2021.2.0/hdf5-1.14.3-fbru4gdpf6wgazr76h3hdx7k4fmnkrv2/include -I/opt/release/linux-rocky8-x86_64/intel-2021.2.0/openmpi-4.0.2-yrzgzaf3aktomsybuzqycqtetgq6qg7c/include -I/opt/release/linux-rocky8-x86_64/intel-2021.2.0/pmix-4.2.2-zj5tvyh7ypekfcncabe3btx6mknyq23c/include -I/opt/release/linux-rocky8-x86_64/intel-2021.2.0/numactl-2.0.14-wc5kt2at6q4zlrx7fsmxhvtghlgortqs/include -I/opt/release/linux-rocky8-x86_64/intel-2021.2.0/libevent-2.1.12-ax3arpdz7yqilbdnehy3ljyte2zvtdzk/include -I/opt/release/linux-rocky8-x86_64/intel-2021.2.0/hwloc-2.9.1-3rpq2unylgkyy7falmub3hacgqodheir/include -I/opt/release/linux-rocky8-x86_64/intel-2021.2.0/libxml2-2.10.3-xihdlwh2airvir3uzav5r6sctizrkg3e/include/libxml2 -I/opt/release/linux-rocky8-x86_64/intel-2021.2.0/libxml2-2.10.3-xihdlwh2airvir3uzav5r6sctizrkg3e/include -I/opt/release/linux-rocky8-x86_64/intel-2021.2.0/xz-5.4.6-bqcqoj33v74rq73qcuruzon3gqj35o7z/include -I/opt/release/linux-rocky8-x86_64/intel-2021.2.0/libpciaccess-0.17-rvk6ysq6ew7v76xlj3cu75cmny3mxc56/include -I/opt/release/linux-rocky8-x86_64/intel-2021.2.0/c-blosc-1.21.5-i3eficrtj6rrgwhiwkmq6qngl3zfel7f/include -I/opt/release/linux-rocky8-x86_64/intel-2021.2.0/zstd-1.5.6-haxkjxttvv4a6qpnwnh3bxe22lb4wxo3/include -I/opt/release/linux-rocky8-x86_64/intel-2021.2.0/snappy-1.1.10-7shycnpzwx5shhi5lmadhw5gcj55ph5b/include -I/opt/release/linux-rocky8-x86_64/intel-2021.2.0/lz4-1.9.4-ho4lmqc5f5y7mgao6aoqppbux6u3zpc7/include -I/opt/release/linux-rocky8-x86_64/intel-2021.2.0/bzip2-1.0.8-37k3deqfl2w6ozrbvcpep5gpvytit2zi/include -I/opt/release/linux-rocky8-x86_64/intel-2021.2.0/json-fortran-8.3.0-ldowr5ste5phzbjemb3fdxctdzhihge3/include -I/opt/release/linux-rocky8-x86_64/intel-2021.2.0/datetime-fortran-1.7.0-xe2epyauchzvnjbgvck535ur6tdmk2qv/include -I/opt/release/linux-rocky8-x86_64/intel-2021.2.0/ncurses-6.5-wt3dyrjn5lwngk7adf7ombkw5vz5ob6u/include -I/opt/release/linux-rocky8-x86_64/intel-2021.2.0/openssl-3.3.0-4vblppxiggmmybf4cl4xpda4efcjinra/include -I/opt/release/linux-rocky8-x86_64/intel-2021.2.0/zlib-ng-2.1.6-qm7p5m7fjf5jrfuflddqmrsavnngcanc/include -I/opt/release/linux-rocky8-x86_64/intel-2021.2.0/libiconv-1.17-wt2wcjfstiob6aug6kebggdcyyvcvwvo/include -c /tmp/root/spack-stage/spack-stage-libaccessom2-access-om2-jo3puvsdvk335jejmdeafvjigpv4xdxm/spack-build-jo3puvs/CMakeFiles/FindMPI/test_mpi.f90 -o CMakeFiles/cmTC_b1a91.dir/test_mpi.f90.o -fp-model strict -check all -check noarg_temp_created -init=snan -init=array -init=huge`
```

## Environment Variables

Run the following command in the Spack source directory to find the environment variables read by Spack:
```
grep -r getenv lib/*
grep -r 'in os.environ' lib/*
```

## Mirror

A Spack mirror contains the source code for Spack packages. On Gadi, a compute node does not allow Spack to download the source code from the Internet. A Spack mirror allows building Spack packages on a Gadi compute node. More details are available at https://spack.readthedocs.io/en/latest/mirrors.html . Below are instructions on how to create a Spack mirror containing all the source code required to build a particular package.

### How to create a Spack mirror:
```
spack spec PACKAGE_NAME > ./mirror.list
spack mirror create --file ./mirror.list
```

### How to add a Spack mirror to a Spack repository
```
spack mirror add local_filesystem file://FULLPATH_TO_MIRROR_DIRECTORY
```

## OpenMPI
The OpenMPI SPR contains the mapping of MPI standard to OpenMPI implementation:
```
    provides("mpi")
    provides("mpi@:2.2", when="@1.6.5")
    provides("mpi@:3.0", when="@1.7.5:")
    provides("mpi@:3.1", when="@2.0.0:")
```

## Versioning Working Practice

See [related design document](https://github.com/ACCESS-NRI/dev-docs/wiki/Decision-Documents#spack-versioning).

### Guidelines

1. Use only full commit hashes as `REF` when using `@git.REF` (**NOT** tags)
2. Use only spack package `version()`s for released model deployments  (**NO** `@git.REF` versions)
3. Use `git` tag names and commit hashes as the 2nd and 3rd argument in the `version()`call in spack package recipes
4. Always have an [infinity version](https://spack.readthedocs.io/en/v0.23.1/packaging_guide.html#version-comparison) (`stable`) defined in our packages with a specific `branch` and `preferred=True`


## Packaging

* Use https://spack.readthedocs.io/en/latest/packaging_guide.html#patch-functions to modify files in source package from the SPR. e.g.
```
    def patch(self):
        if "+deterministic" in self.spec:
            filter_file(r"-traceback", "", "CMakeLists.txt")
            filter_file(r"-g3 -O2", "-g0 -O0", "CMakeLists.txt")
```
* Spack Package Recipe API: https://spack.readthedocs.io/en/latest/package_api.html

## Reverse Dependencies
```
$ spack dependents -t oasis3-mct
access-om2  cice5  libaccessom2  mom5
```

## Schemas

The schemas for the configuration files are located at `lib/spack/spack/schema/` in the Spack source directory.

## Spack Environments

Spack environments are a way to package up relevant spack packages, their configurations and compilers into a file, allowing a quick install of all the relevant packages into an isolated environment, in any spack installation. This isolated environment can take packages and compilers that are already installed in the global spack environment, allowing some caching to take place. 

### The Environment Files

The files that generate or represent an environment are broken down further: into abstract `spack.yaml` files, and concretized `spack.lock` files. 

These can be found in `spack/var/spack/environments/ENV_NAME/`.

#### The `spack.yaml` file (spec/manifest file)

The `spack.yaml` file is an abstract list of packages, configurations of said packages, compilers that packages will use, among many other things. Specific versions of dependencies do not have to be specified, and in fact the dependencies do not need to be specified at all, unless further customization is required. 

It looks like this:

```yaml
# This is a Spack Environment file.
#
# It describes a set of packages to be installed, along with
# configuration settings.
spack:
  # add package specs to the `specs` list
  specs:
  - intel-oneapi-compilers@2021.2.0 arch=linux-rocky8-x86_64
  - mom5@git.master=access-esm1.5 %intel@2021.2.0 arch=linux-rocky8-x86_64
  view: true
  concretizer:
    unify: true
  compilers:
  - compiler:
      spec: intel@=2021.2.0
      paths:
        cc: /opt/spack/opt/spack/linux-rocky8-x86_64/gcc-8.5.0/intel-oneapi-compilers-2021.2.0-lkzqdmlrys3wqeb3yakfwi3slmyvccf6/compiler/2021.2.0/linux/bin/intel64/icc
        cxx: /opt/spack/opt/spack/linux-rocky8-x86_64/gcc-8.5.0/intel-oneapi-compilers-2021.2.0-lkzqdmlrys3wqeb3yakfwi3slmyvccf6/compiler/2021.2.0/linux/bin/intel64/icpc
        f77: /opt/spack/opt/spack/linux-rocky8-x86_64/gcc-8.5.0/intel-oneapi-compilers-2021.2.0-lkzqdmlrys3wqeb3yakfwi3slmyvccf6/compiler/2021.2.0/linux/bin/intel64/ifort
        fc: /opt/spack/opt/spack/linux-rocky8-x86_64/gcc-8.5.0/intel-oneapi-compilers-2021.2.0-lkzqdmlrys3wqeb3yakfwi3slmyvccf6/compiler/2021.2.0/linux/bin/intel64/ifort
      flags: {}
      operating_system: rocky8
      target: x86_64
      modules: []
      environment: {}
      extra_rpaths: []
...
``` 
It contains what packages need to be installed (`mom5`), the ref at which it is built (`master`) as well as further configuration options (`arch=linux-rocky8-x86_64`). Furthermore, it notes what compilers are in this environment (`intel@=2021.2.0`). Compared to a lock file, it is fairly human readable, and can be edited either manually or (as noted later) built up through `spack install` calls as you would in the global environment.

As a note on versions (the bit after the `@`), they can be versions specified in an `SPR` which are of the form `@version` - for example `mom5@master`. They can also reference any `git commit`-ish object if a `git` repository is linked in the `SPR`, which is of the form `@git.GIT_REF` - for example `mom5@git.2023.11.01`.

More information on `git` version specifiers can be [found in general here](https://spack.readthedocs.io/en/latest/basic_usage.html#git-versions), or for a more in-depth look, [here in the API reference](https://spack.readthedocs.io/en/latest/spack.version.html#spack.version.GitVersion).

> [!WARNING]
> When a `git commit`-ish object is used to specify the version, the spack version to use with the `SPR` should also be explicitly provided as `@git.GIT_REF=SPACK_VERSION` - for example `mom5@git.2023.11.01=access-om2`. Spack will use the latter for version comparisons.

Regarding the `spack.yaml` file, it might look familiar if you've seen or edited files in the `ACCESS-NRI/spack-config` repository - it is the same, in fact, but is not tied to the global environment, but it's own isolated one. 

If you activate an environment that was based on a `spack.yaml` file, it will need to be concretized with specific versions and dependencies at install time. If you want to see the specifics of the concretized `spack.yaml` file, you can see the newly-generated `spack.lock` file. Read on below... 

#### The `spack.lock` file (lock file)

The `spack.lock` file is a concretized version of the `spack.yaml` file, essentially a reusable, replicable, moment-in-time snapshot of the decisions made by spack in determining what versions of dependencies to use. If you create an environment based on this file, it will nessecarily be exactly the same as where ever you took it from - this is not the case for `spack.yaml` files!

This file is not very human readable, but we can glean some information from it - mostly exact commit hashes of packages, their dependencies, and so on, as well as any configuration details.   

### Generating your own environment file

Generating your own environment files isn't complicated. It's exactly as it is done outside of an environment, but with some extra command-line flags. 

```bash
spack env create my-env  # create an empty environment
spack env activate my-env  # activate this environment (can also use 'spacktivate my-env')
# if you do 'spack env status' you will note that you are in the environment. This info is also present when doing 'spack find'
```

Now you can install compilers, packages and other things as normal, with said flags...

```bash
spack install --add cool-compiler@v1.2.3  # this '--add's the install of the compiler to the spack.yaml file 
spack compiler find --scope env:my-env  # this adds any newly installed compilers to the environment (and the spack.yaml file)
spack install --add cool-package@master%cool-compiler@v1.2.3  # packages work similarly
```

If you `cat spack/var/spack/environments/my-env/spack.yaml` you can verify that these packages and compilers have been added as expected. Likewise for the `spack.lock` file.

### Generating an environment based on a environment file

If you have an environment file, it's even simpler:

```bash
spack env create my-cool-env ./some-cool.spack.yaml  # this could also be a path to a lock file if you didn't want to concretize at install time
spack env activate my-cool-env  # verify with 'spack env status', if you want
spack install  # what to install is taken from the environment file definition!
```

Read more on environments in spacks own documentation: https://spack-tutorial.readthedocs.io/en/latest/tutorial_environments.html and https://spack.readthedocs.io/en/latest/environments.html

## Create or modify Spack Package Recipes (SPR) or Spack Package Bundles (SBR)

### Introduction

Start by familiarising yourself with the section headings in the  [Spack Packaging Guide](https://spack.readthedocs.io/en/latest/packaging_guide.html). Remember to read the relevant sections as needed.

### Style and Design

There are thousands of builtin Spack Package Recipes in the `builtin` [spack-packages](https://github.com/spack/spack-packages) git repository. Refer to them for clarity.

We have many SPRs and SBRs in [access-spack-packages' api-v2 branch](https://github.com/ACCESS-NRI/access-spack-packages/tree/api-v2/spack_repo/access/nri/packages) . Refer to them for style and design recommendations.

### Procedures

1. The SPR/SBR contains a list of `maintainers`. Please communicate with the maintainer about why you want to change the SPR/SBR. Add the maintainer as a reviewer when you want to merge the changes.

2. Before setting a Pull Request as Ready for Review, make sure you do a test build of the package via Github CI and/or Spack and ensure the output is accessible in the Pull Request.

### Layers of abstraction

A Spack Package Recipe (SPR) uses the build system of the underlying source package to build the binary package. A Model Deployment Repository (MDR) contains a Spack environment file (`spack.yaml`) that uses the SPR to build one or more source packages, including dependencies.

We prefer to define the exact version of the source package(s) and dependencies *only* in the `spack.yaml` file. Therefore, we avoid defining an exact version of dependencies in the SPR. If a dependency needs to be limited to a range of versions starting at a minimum version and/or finishing at a maximum version, that is acceptable.

Decisions regarding changing the source package's build system are subjective and the Model Release team can provide advice. A useful rule is to first decide whether you want to modify the source package and whether ACCESS-NRI will need to take responsibility for maintaining it. If you do not want to modify a source package, then any compiler flag modifications and/or dependency version changes should be made from the SPR. Spack provides functions to allow SPRs to modify the source package's build system.

### Compiler flags

Compiler flags can be set in the Spack environment file, the SPR and/or the source package's build system.

Generally, compiler flags should *not* be set in the Spack environment file (`spack.yaml`), unless it is for debugging or experimental purposes. This functionality should only be used by advanced Spack users because it can be complicated to verify that the compiler flags have been applied. For more details, please read: https://github.com/ACCESS-NRI/dev-docs/wiki/Spack#compiler-flag-override . The `inject_flags` option is the default `flag_handler`: https://spack.readthedocs.io/en/latest/packaging_guide_build.html#compiler-flags . This means that CMake and Autotools based SPRs need to set the `flag_handler` to `build_system_flags` in-order for compiler flag overrides to appear in the build logs. Otherwise, they only appear in the Spack debug build logs when `spack -d install` is run.

SPRs can contain compiler flags that are applied to the source package. In particular, an SPR may have a variant that modifies the source package's compiler flags. e.g. A variant for `deterministic` builds. For more details on variants, please read: https://spack.readthedocs.io/en/latest/packaging_guide_creation.html#variants . The way to use variants with CMake are documented with: https://spack.readthedocs.io/en/latest/build_systems/cmakepackage.html . The Model Release team can provide advice on appropriate defaults for variants.

All compiler flags that are *required* to build the package should be in the source package. The source package can contain compiler flags that are optional and can be enabled/disabled by the user. These compiler flags can be manipulated from the SPR. Consider grouping the compiler flags as required, optional and optimisation flags. Allow the user to override the optional and optimisation compiler flags.

### spack-config

The spack-config repository contains ACCESS-NRI's preferred Spack configuration. These configuration files also allow the HPC system's unique customisations to be hidden from the SPRs and users. e.g.
```
    - spec: openmpi@5.0.8
      prefix: /apps/openmpi/5.0.8
      modules: [openmpi/5.0.8]
      extra_attributes:
        environment:
          prepend_path:
            CMAKE_PREFIX_PATH: /apps/openmpi/5.0.8/include/Intel

    - spec: openmpi@5.0.8 %gcc@13.2.0
      prefix: /apps/openmpi/5.0.8
      modules: [openmpi/5.0.8]
      extra_attributes:
        environment:
          prepend_path:
            CMAKE_PREFIX_PATH: /apps/openmpi/5.0.8/include/GNU
```
In Spack v1.1, defining an external spec has strict requirements.

## Troubleshooting

1. Need information from your Spack instance. Provide the output of these commands:
```
git -C spack log -1
git -C spack-config log -1
spack repo list
```