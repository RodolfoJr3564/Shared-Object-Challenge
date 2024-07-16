#!/bin/sh

error_exit() {
    echo "$1" 1>&2
    exit 1
}

echo "Instalando dependências necessárias..."
apk add --no-cache python3 python3-dev gcc g++ make libffi-dev musl-dev curl || error_exit "Falha ao instalar dependências."

DEST_DIR="./build"

echo "Criando diretório de destino se não existir..."
mkdir -p $DEST_DIR || error_exit "Falha ao criar o diretório de destino."

echo "Instalando Poetry..."
curl -sSL https://install.python-poetry.org | python3 - || error_exit "Falha ao instalar Poetry."

export PATH="/root/.local/bin:$PATH"

PROJECT_DIR=$(dirname "$(find . -name 'pyproject.toml')")
echo "Acessando o diretório do projeto: $PROJECT_DIR"
cd "$PROJECT_DIR" || error_exit "Falha ao acessar o diretório $PROJECT_DIR."

echo "Instalando dependências do projeto com Poetry..."
poetry install || error_exit "Falha ao instalar dependências do projeto."

echo "Ativando o ambiente virtual do Poetry..."
source $(poetry env info --path)/bin/activate || error_exit "Falha ao ativar o ambiente virtual do Poetry."

echo "Executando o script Python para compilação..."
poetry run python compile.py || error_exit "Falha ao executar o script Python de compilação."

echo "Movendo libcsv.so para a raiz do projeto..."
mv build/libcsv.so .. || error_exit "Falha ao mover libcsv.so."

PYTHON_LIB_PATH=$(find /usr -name "libpython3.10.so.1.0" 2>/dev/null)
if [ -z "$PYTHON_LIB_PATH" ]; then
    PYTHON_LIB_PATH=$(find / -name "libpython3.10.so.1.0" 2>/dev/null)
    if [ -z "$PYTHON_LIB_PATH" ]; then
        error_exit "libpython3.10.so.1.0 não encontrada no sistema."
    fi
fi

echo "libpython3.10.so.1.0 encontrada em $PYTHON_LIB_PATH."

echo "Copiando libpython3.10.so.1.0 para a raiz do projeto..."
cp "$PYTHON_LIB_PATH" ../ || error_exit "Falha ao copiar libpython3.10.so.1.0."

echo "Definindo LD_LIBRARY_PATH..."
export LD_LIBRARY_PATH=../:$LD_LIBRARY_PATH

echo "Build e configuração de ambiente bem-sucedidos."
