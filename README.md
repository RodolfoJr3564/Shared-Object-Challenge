## Sumário

- [Requisitos de Instalação](#requisitos-de-instalação)
- [Iniciando o Ambiente de Desenvolvimento](#iniciando-o-ambiente-de-desenvolvimento)
- [Executando Testes](#executando-testes)
- [Cobertura de Testes](#cobertura-de-testes)
- [Formatando Código](#formatando-código)
- [Verificando Estilo do Código](#verificando-estilo-do-código)
- [Estrutura Final do Projeto](#estrutura-final-do-projeto)
- [Conversão Estruturada de Arquivos `.py` para `.pyx`](#conversão-estruturada-de-arquivos-py-para-pyx)
  - [Funcionalidades](#funcionalidades)
  - [Uso do Script](#uso-do-script)

## Requisitos de Para Execução do projeto

Para simplificar a instalação de dependências e gerenciamento de ambientes virtuais, este projeto utiliza o `poetry` como gerenciador de dependências.
Se você ainda não tem essa ferramenta instalada, siga as instruções no link abaixo:

- [Instruções para instalar o poetry](https://python-poetry.org/docs/#installation)

Depois de instalar o `poetry`, você pode verificar se a instalação foi bem-sucedida executando o seguinte comando:

## Iniciando o Ambiente de Desenvolvimento

Entre na pasta do desafio:

```bash
cd challenge
```

Para iniciar o ambiente utilizando o `poetry` precisamos instalar as dependências listadas no `pyproject.toml`:

```bash
poetry install
```

Depois de instalar as dependências, você pode ativar o ambiente virtual gerado pelo `poetry` com o seguinte comando:

```bash
poetry shell
```

Para garantir que está no ambiente correto execulte:

```bash
poetry env list
```

O resultado deve ser algo como:

```bash
.venv (Activated)
```

E agora você está pronto para testar, formatar e verificar o código do seu projeto.

## Executando Testes

Para executar os testes do seu projeto, você pode usar o `pytest`:

```bash
poetry run pytest
```

## Cobertura de Testes

Para verificar a cobertura de testes do seu projeto, você pode usar o `pytest-cov`:

```bash
poetry run pytest --cov=processor
```

## Formatando Código

Para formatar o código do seu projeto, você pode usar o `black`:

```bash
poetry run black .
```

## Verificando Estilo do Código

Para verificar o estilo do código e encontrar possíveis erros, você pode usar o `flake8`:

```bash
poetry run flake8
```

## Estrutura Final do Projeto

A estrutura do projeto deve parecer com isto:

```
challenge/
├── challenge/
│   ├── __init__.py
│   └── main.py
├── tests/
│   └── __init__.py
├── .gitignore
├── .python-version
├── pyproject.toml
└── README.md
```

## Conversão Estruturada de Arquivos `.py` para `.pyx`

Este projeto inclui um script chamado `py-to-pyx.sh` que facilita a conversão de arquivos `.py` para `.pyx`, preservando a estrutura original de diretórios. O script oferece funcionalidades para listar e converter arquivos, tornando o processo mais eficiente e automatizado para prepará-los para a compilação com Cython.

### Funcionalidades

1. **Listar Arquivos**:

   - O script pode listar a estrutura de pastas e arquivos `.py` encontrados em um diretório especificado.

2. **Converter Arquivos**:
   - Converte arquivos `.py` para `.pyx`, mantendo a estrutura original de diretórios.
   - Cria automaticamente a pasta de saída se ela não existir.
   - Substitui a pasta de saída se ela já existir, com uma opção para forçar a substituição sem confirmação do usuário.

### Uso do Script

1. **Tornar o Script Executável**:

   - Antes de executar o script, é necessário torná-lo executável com o comando:
     ```bash
     chmod +x py-to-pyx.sh
     ```

2. **Comandos Disponíveis**:

   - **Listar Arquivos**:

     - Para listar a estrutura de pastas e arquivos `.py` em um diretório:
       ```bash
       ./py-to-pyx.sh -l <path>
       ```
     - Exemplo:
       ```bash
       ./py-to-pyx.sh -l processor
       ```

   - **Converter Arquivos**:
     - Para converter arquivos `.py` para `.pyx`:
       ```bash
       ./py-to-pyx.sh -c -i <input> -o <output> [-f]
       ```
     - Exemplo para converter arquivos da pasta `processor` para a pasta `processor-pyx`:
       ```bash
       ./py-to-pyx.sh -c -i processor -o processor-pyx
       ```
     - Exemplo para converter e forçar a substituição da pasta de saída:
       ```bash
       ./py-to-pyx.sh -c -i processor -o processor-pyx -f
       ```
