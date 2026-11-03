## CMake
## Exporting CMake Targets

**Acknowledgement: big thanks to Micael Oliveira for his work on exporting CMake targets in ACCESS-OM3 and providing a starting point for the organisation on this topic**

### Motivation

CMake projects which provide targets should install a [CMake package configuration file](https://cmake.org/cmake/help/latest/manual/cmake-packages.7.html). This is currently the best practice for library authors and has the benefit that projects can find and import targets out of the box via [`find_package()`](https://cmake.org/cmake/help/latest/command/find_package.html) without needing a find module.

This talk given by Daniel Pfeifer gives a great introduction to the topic:

- [YouTube: C++Now 2017: Daniel Pfeifer “Effective CMake" (30:00 - 44:40)][daniel-pfeifer-effective-cmake]

### Resources

Here are examples where we have done this at ACCESS-NRI:

- [ACCESS-OM3][access-om3] (deprecated):
  - See [CMakeLists.txt][access-om3-cmakeliststxt], [AccessOM3Config.cmake.in][access-om3-config-cmake]
- [access3-share][access3-share]:
  - See  [Access3LibInstall.cmake][access3-lib-install], [Access3ShareConfig.cmake.in][access3-share-config-cmake]

Other useful material:

- [CMake: Importing and Exporting Guide][cmake-importing-exporting-guide]
  - Examples from the tutorial can be found in the [CMake GitLab repository][cmake-importing-exporting-guide-examples].
- [It's Time To Do CMake Right](https://pabloariasal.github.io/2018/02/19/its-time-to-do-cmake-right/)

### What is `find_dependency` and why do we need it?

When a CMake package config file is installed, the targets which are exported often require dependencies on other packages - these dependencies must be available for consumers of your exported targets. For example, this may be necessary if any targets declare a `PUBLIC`  dependency, or if the dependency may be provided as a static library. This is because for these cases, the `INTERFACE_*` target properties of your exported targets will contain a reference to these dependencies and CMake will error if these dependencies cannot be found (see [target usage requirements][cmake-target-usage-requirements] for more details on these properties).

[`find_dependency()`][cmake-find-dependency] facilitates this by ensuring that the necessary dependencies are found when the package itself is found by the consuming project via [`find_package()`][cmake-find-package]. It also forwards the correct parameters for `QUIET` and `REQUIRED` which were passed to the original [`find_package()`][cmake-find-package] call.

### How do I export my targets when my projects relies on find modules?

If your project requires using find modules (`Find<project>.cmake` files) to find its dependencies, then these find modules should be installed along with your package config file so that these dependencies can be found using `find_dependency()`. Once the find modules are installed (typically in `CMAKE_CURRENT_LIST_DIR`), we can make these find modules discoverable in the package config file:

```cmake
list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_LIST_DIR})

find_dependency(foo)
find_dependency(bar)

list(REMOVE_ITEM CMAKE_MODULE_PATH ${CMAKE_CURRENT_LIST_DIR})
```

See the following for more details:
- [Exporting packages with a custom Find module][discourse-cmake-exporting-packages-with-custom-find-module]
- [Installing a CMake library: also ship find modules for the dependencies?][so-installing-a-cmake-library-also-ship-find-modules-for-the-dependencies]

### Relocatable targets

See [Creating Relocatable Packages][cmake-creating-relocatable-packages].

Relocatability has the benefit that the installed package will not break if the location of any installed dependencies and/or the package itself changes.

Common pitfalls which break relocatability:

1. **Hardcoded paths to third-party dependencies**
   - Be careful to not populate any properties which may contain paths, such as [`INTERFACE_INCLUDE_DIRECTORIES`][cmake-interface-include-directories] and [`INTERFACE_LINK_LIBRARIES`][cmake-interface-link-libraries] (see [target usage requirements][cmake-target-usage-requirements] for more details), with paths relevant to dependencies. This will result in hard coded paths to dependencies for your exported targets.
   - This can happen when using variables such as `Foo_LIBRARIES` or `Foo_INCLUDE_DIRS` to link against third party dependencies. Instead, link against a `Foo` imported target with [`target_link_libraries`][cmake-target-link-libraries] to avoid populating paths to dependencies in the exported targets. However, this may not always be possible and the CMake manual suggests two workarounds [here](https://cmake.org/cmake/help/latest/manual/cmake-packages.7.html#creating-relocatable-packages:~:text=Unfortunately%20many%20modules,package%20is%20installed.).

[daniel-pfeifer-effective-cmake]: https://youtu.be/bsXLMQ6WgIk?t=1779
[cmake-importing-exporting-guide]: https://cmake.org/cmake/help/latest/guide/importing-exporting/index.html
[cmake-importing-exporting-guide-examples]: https://gitlab.kitware.com/cmake/cmake/-/tree/master/Help/guide/importing-exporting
[cmake-target-usage-requirements]: https://cmake.org/cmake/help/latest/manual/cmake-buildsystem.7.html#target-usage-requirements
[cmake-find-dependency]: https://cmake.org/cmake/help/latest/module/CMakeFindDependencyMacro.html
[cmake-find-package]: https://cmake.org/cmake/help/latest/command/find_package.html
[cmake-target-link-libraries]: https://cmake.org/cmake/help/latest/command/target_link_libraries.html
[discourse-cmake-exporting-packages-with-custom-find-module]: https://discourse.cmake.org/t/exporting-packages-with-a-custom-find-module/3820/1
[so-installing-a-cmake-library-also-ship-find-modules-for-the-dependencies]: https://stackoverflow.com/questions/44920389/installing-a-cmake-library-also-ship-find-modules-for-the-dependencies
[cmake-creating-relocatable-packages]: https://cmake.org/cmake/help/latest/manual/cmake-packages.7.html#creating-relocatable-packages
[cmake-interface-include-directories]: https://cmake.org/cmake/help/latest/prop_tgt/INTERFACE_INCLUDE_DIRECTORIES.html#prop_tgt:INTERFACE_INCLUDE_DIRECTORIES
[cmake-interface-link-libraries]: https://cmake.org/cmake/help/latest/prop_tgt/INTERFACE_LINK_LIBRARIES.html#prop_tgt:INTERFACE_LINK_LIBRARIES
[access-om3]: https://github.com/ACCESS-NRI/ACCESS-OM3
[access3-share]: https://github.com/ACCESS-NRI/access3-share
[access-om3-config-cmake]: https://github.com/COSIMA/access-om3/blob/main/cmake/AccessOM3Config.cmake.in
[access-om3-cmakeliststxt]: https://github.com/COSIMA/access-om3/blob/main/CMakeLists.txt
[access3-share-config-cmake]: https://github.com/ACCESS-NRI/access3-share/blob/main/cmake/Access3ShareConfig.cmake.in
[access3-lib-install]: https://github.com/ACCESS-NRI/access3-share/blob/main/cmake/Access3LibInstall.cmake

