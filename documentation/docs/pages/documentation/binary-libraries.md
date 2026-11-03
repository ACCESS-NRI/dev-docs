[WIP] Summary from Kerrisk, Michael. The Linux Programming Interface: A Linux and UNIX System Programming Handbook. No Starch Press, 2010

### Object files

Binary representation of source files. The compiler asks `ld` to link all the object files together to form an executable or a library.

### Static libraries (archives)

Contains object files and attributes
* Attributes include timestamps unless determinstic flags are given to `ar`.

Create: `ar [<flags>] <archive-name> <object-files>+`

Link: `gcc -o <executable> <object-files> -L<dir> -l<archive-name>`
  * Executable contain all the symbols from the archive that are required. i.e. 'undefined symbols are resolved'.

### Shared libraries (.so)

* Single instance of the library is loaded into memory and can be used by multiple executables. The global and static variables are not shared.

* Must be compiled with position-independent code. There is a performance overhead on most architectures because an extra register is required.

* Symbol relocation can negatively impact performance.

* Create:
```
$ gcc -fPIC <source-files>
$ gcc -shared -o <library-name>.so <object-files>+
```

* -fPIC objects contain `_GLOBAL_OFFSET_TABLE_`
* non-fPIC objects contain `TEXTREL`

* Dependencies are in the `DT_NEEDED` tag in the executable.

* At runtime, dynamic linking required by /lib/ld-linux.so.2

#### soname (DT_SONAME)
* real name Vs soname Vs linker name . e.g. <library-name>.so.<major>.<minor> Vs <library-name>.so.<major> Vs <library-name>.so
* symlinking used in this way:
```
<library-name>.so.<major>.<minor>
<library-name>.so.<major> -> <library-name>.so.<major>.<minor>
<library-name>.so -> <library-name>.so.<major>.<minor>
```
* `gcc -shared -Wl,-soname,<library-name>.so.<major> -o <library-name>.so.<major>.<minor> <object-files>+`

* Major version change indicates that there's a break in ABI compatibility.

* Precedence: DT_RPATH, LD_LIBRARY_PATH, DT_RUNPATH, /etc/ld.so.cache , /lib , /usr/lib. Please don't explicitly use `-rpath` to set the library search directories.

* `-Wl,-Bsymbolic` will force the library functions to use functions with the same name in the library rather than functions in the executable that uses the library.

* Linker defaults to using the shared library instead of the static, if the names are the same. e.g. If  `<libraryname>.a` and `<libraryname>.so` reside in `<directory>` and `-L<directory> -l<libraryname>` is used.

* To force the static library to be used, provide flag `-static` option to gcc. Also see `-Wl,-Bstatic` and `-Wl,-Bdynamic` to toggle between shared and static libraries in the same command line.
```
$ gcc -g -o hello hello.c
$ gcc -g -static -o hello2 hello.c
$ ls -sh hello hello2
 20K hello  740K hello2
$ ldd hello
	linux-vdso.so.1 (0x00007fc26378a000)
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007fc26356a000)
	/lib64/ld-linux-x86-64.so.2 (0x00007fc26378c000)
$ ldd hello2
	not a dynamic executable
```
### Dynamically loaded libraries

Dynamically loaded libaries allow delayed loading of libraries when they are required. These are created the same way as shared libraries. However, they are loaded using explicit function calls, e.g. `dlopen`. Other related functions are `dlsym`, `dlclose` and `dlerror`.

To use a dynamically loaded library, the executable needs to be linked against `libdl` by specifying `-ldl`.

### Visibility

A well designed API needs to have a well implemented ABI. Only expose symbols (functions) that are part of the API. This will make it easier to maintain the library in the long-term, avoid symbol name conflicts with other libraries and keep the dynamic symbol table as small as possible.

In C, the keyword `static` restricts a function visibility to that file. Furthermore, functions that call that function name in the same file will not accidentally call a function of the same name in another library. The gcc compiler also has a "hidden" attribute (`__attribute__((visibility("hidden")))`) that exposes the function to the entire shared library, instead of just the source code file.

### Commands

* readelf [-d,-s]
* objdump --all-headers
* nm -A
* ldd
* ldconfig (update cache containing system library metadata)