#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <dlfcn.h>

#define MODINIT(name)  PyInit_##name

PyMODINIT_FUNC MODINIT(filter)(void);
PyMODINIT_FUNC MODINIT(lexer)(void);
PyMODINIT_FUNC MODINIT(processor)(void);
PyMODINIT_FUNC MODINIT(serializer)(void);

int main(int argc, char *argv[]) {
    const char *libpython_path = "./build/libpython3.10.so";

    void *handle = dlopen(libpython_path, RTLD_NOW | RTLD_GLOBAL);
    if (!handle) {
        fprintf(stderr, "Erro ao carregar %s: %s\n", libpython_path, dlerror());
        return 1;
    }

    wchar_t *program = Py_DecodeLocale(argv[0], NULL);
    if (program == NULL) {
        fprintf(stderr, "Fatal error: cannot decode argv[0]\n");
        exit(1);
    }
    Py_SetProgramName(program);
    Py_Initialize();

    PyImport_AppendInittab("filter", MODINIT(filter));
    PyImport_AppendInittab("lexer", MODINIT(lexer));
    PyImport_AppendInittab("processor", MODINIT(processor));
    PyImport_AppendInittab("serializer", MODINIT(serializer));

    Py_Initialize();

    Py_Finalize();
    PyMem_RawFree(program);
    dlclose(handle);

    return 0;
}
