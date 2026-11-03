## Versioning Working Practice

See [related design document](../documentation/decision-documents.md#spack-versioning).

### Guidelines

1. Use only full commit hashes as `REF` when using `@git.REF` (**NOT** tags)
2. Use only spack package `version()`s for released model deployments  (**NO** `@git.REF` versions)
3. Use `git` tag names and commit hashes as the 2nd and 3rd argument in the `version()`call in spack package recipes
4. Always have an [infinity version](https://spack.readthedocs.io/en/v0.23.1/packaging_guide.html#version-comparison) (`stable`) defined in our packages with a specific `branch` and `preferred=True`

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

Generally, compiler flags should *not* be set in the Spack environment file (`spack.yaml`), unless it is for debugging or experimental purposes. This functionality should only be used by advanced Spack users because it can be complicated to verify that the compiler flags have been applied. For more details, please read: [Compiler Flag Override](../documentation/spack.md#compiler-flag-override). The `inject_flags` option is the default `flag_handler`: https://spack.readthedocs.io/en/latest/packaging_guide_build.html#compiler-flags . This means that CMake and Autotools based SPRs need to set the `flag_handler` to `build_system_flags` in-order for compiler flag overrides to appear in the build logs. Otherwise, they only appear in the Spack debug build logs when `spack -d install` is run.

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
