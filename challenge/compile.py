import os
import shutil
import sysconfig
from subprocess import run, CalledProcessError


def list_and_copy_dependencies(lib_path, dest_dir):
    try:
        output = run(["ldd", lib_path], capture_output=True, text=True).stdout
        lines = output.split("\n")
        for line in lines:
            parts = line.split("=>")
            if len(parts) == 2:
                dep_path = parts[1].strip().split(" ")[0]
                if os.path.exists(dep_path):
                    shutil.copy(dep_path, dest_dir)
    except Exception as e:
        print(f"Erro ao listar e copiar dependências: {e}")


def compile_cython_modules():
    try:
        run(["cythonize", "-i", "-3", "processor_pyx/*.pyx"], check=True)
        for file in os.listdir("processor_pyx"):
            if file.endswith(".c"):
                run(
                    [
                        "gcc",
                        "-c",
                        os.path.join("processor_pyx", file),
                        "-o",
                        os.path.join("processor_pyx", file.replace(".c", ".o")),
                        "-fPIC",
                        f"-I{sysconfig.get_path('include')}",
                    ],
                    check=True,
                )
    except CalledProcessError as e:
        print(f"Erro na compilação dos módulos Cython: {e}")
        return False
    return True


def compile_main_binary():
    try:
        object_files = [
            os.path.join("processor_pyx", f)
            for f in os.listdir("processor_pyx")
            if f.endswith(".o")
        ]
        command = (
            ["gcc", "-shared", "-o", "libcsv.so", "main.o"]
            + object_files
            + [
                f"-L{sysconfig.get_config_var('LIBDIR')}",
                "-lpython3.10",
                "-Wl,-rpath,/usr/lib",
                "-static-libgcc",
                "-static-libstdc++",
                "-Wl,--copy-dt-needed-entries",
            ]
        )
        run(command, check=True)
    except CalledProcessError as e:
        print(f"Erro na compilação do binário principal: {e}")
        return False
    return True


def main():
    if not compile_cython_modules():
        return

    if not compile_main_binary():
        return

    if not os.path.exists("build"):
        os.makedirs("build")

    shutil.move("libcsv.so", "build/libcsv.so")
    list_and_copy_dependencies("build/libcsv.so", "build")

    print("Build successful and all .so files moved to build/ directory.")


if __name__ == "__main__":
    main()
