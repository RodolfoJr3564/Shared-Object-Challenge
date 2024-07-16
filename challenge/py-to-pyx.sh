#!/bin/bash
#
# py-to-pyx.sh
# 
# Descrição: Este script lista arquivos .py e converte-os para .pyx, mantendo a estrutura de diretórios.
# 
# Uso:
#   ./py-to-pyx.sh -l <path>
#   ./py-to-pyx.sh -c -i <input> -o <output> [-f]
#
# Opções:
#   -l <path>              Lista a estrutura de pastas e arquivos .py no caminho especificado
#   -c                     Converte arquivos .py para .pyx, mantendo a estrutura de diretórios
#   -i <input>             Diretório de entrada para conversão
#   -o <output>            Diretório de saída para os arquivos convertidos
#   -f                     Força a substituição da pasta de saída sem confirmação
#
# Exemplo:
#   ./py-to-pyx.sh -l processor
#   ./py-to-pyx.sh -c -i processor -o pasta-pyx
#   ./py-to-pyx.sh -c -i processor -o pasta-pyx -f
#
# ------------------------------------------

list_py_files() {
    local directory=$1
    find "$directory" -type f -name '*.py' ! -name '__init__.py'
}

convert_and_copy() {
    local source_dir=$1
    local target_dir=$2
    while IFS= read -r file; do
        relative_path="${file#$source_dir/}"
        pyx_file="${relative_path%.py}.pyx"
        mkdir -p "$target_dir/$(dirname "$pyx_file")"
        cp "$file" "$target_dir/$pyx_file"
        echo "Converted $file to $target_dir/$pyx_file"
    done < <(list_py_files "$source_dir")
}

show_help() {
    echo "Uso: $0 [-l <path>] [-c -i <input> -o <output> [-f]]"
    echo "Opções:"
    echo "  -l <path>              Lista a estrutura de pastas e arquivos .py no caminho especificado"
    echo "  -c                     Converte arquivos .py para .pyx, mantendo a estrutura de diretórios"
    echo "  -i <input>             Diretório de entrada para conversão"
    echo "  -o <output>            Diretório de saída para os arquivos convertidos"
    echo "  -f                     Força a substituição da pasta de saída sem confirmação"
    exit 1
}

list_flag=0
convert_flag=0
force_flag=0
input_dir=""
output_dir=""

while getopts "l:ci:o:f" opt; do
    case "$opt" in
        l) list_flag=1; path=$OPTARG ;;
        c) convert_flag=1 ;;
        i) input_dir=$OPTARG ;;
        o) output_dir=$OPTARG ;;
        f) force_flag=1 ;;
        *) show_help ;;
    esac
done

if [ $list_flag -eq 0 ] && [ $convert_flag -eq 0 ]; then
    show_help
fi

if [ $list_flag -eq 1 ]; then
    if [ -z "$path" ]; then
        show_help
    fi
    echo "Estrutura de diretórios e arquivos .py encontrados em $path:"
    list_py_files "$path"
    exit 0
fi

if [ $convert_flag -eq 1 ]; then
    if [ -z "$input_dir" ] || [ -z "$output_dir" ]; then
        show_help
    fi

    if [ -d "$output_dir" ]; then
        if [ $force_flag -eq 1 ]; then
            rm -rf "$output_dir"
        else
            read -p "A pasta de saída já existe. Deseja substituí-la? (s/N): " confirm
            if [[ ! "$confirm" =~ ^[Ss]$ ]]; then
                echo "Operação cancelada."
                exit 1
            fi
            rm -rf "$output_dir"
        fi
    fi

    echo "Convertendo arquivos de $input_dir para $output_dir..."
    convert_and_copy "$input_dir" "$output_dir"
    echo "Conversão concluída."
    exit 0
fi
