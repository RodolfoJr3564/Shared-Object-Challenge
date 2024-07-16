from setuptools import setup, Extension
from Cython.Build import cythonize

python_include_dir = "/usr/local/include/python3.10"
python_lib_dir = "/usr/local/lib"

extensions = [
    Extension(
        name="filter",
        sources=["processor_pyx/filter.pyx"],
        include_dirs=[python_include_dir],
        library_dirs=[python_lib_dir],
        libraries=["python3.10"],
        define_macros=[("CYTHON_NO_PYINIT_EXPORT", "1")],
    ),
    Extension(
        name="lexer",
        sources=["processor_pyx/lexer.pyx"],
        include_dirs=[python_include_dir],
        library_dirs=[python_lib_dir],
        libraries=["python3.10"],
        define_macros=[("CYTHON_NO_PYINIT_EXPORT", "1")],
    ),
    Extension(
        name="processor",
        sources=["processor_pyx/processor.pyx"],
        include_dirs=[python_include_dir],
        library_dirs=[python_lib_dir],
        libraries=["python3.10"],
        define_macros=[("CYTHON_NO_PYINIT_EXPORT", "1")],
    ),
    Extension(
        name="serializer",
        sources=["processor_pyx/serializer.pyx"],
        include_dirs=[python_include_dir],
        library_dirs=[python_lib_dir],
        libraries=["python3.10"],
        define_macros=[("CYTHON_NO_PYINIT_EXPORT", "1")],
    ),
]

setup(
    name="libcsv",
    ext_modules=cythonize(
        extensions,
        compiler_directives={
            "language_level": "3",
        },
    ),
    zip_safe=False,
)
