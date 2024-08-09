# llm-chatbot-python

## Visão Geral

Este projeto é uma aplicação que utiliza modelos de linguagem (LLMs) para responder perguntas baseadas em contextos ou informações obtidas de URLs. Ele é projetado para ser executado a partir da linha de comando e oferece várias opções para personalizar a operação, como definir a temperatura do modelo, limitar a busca em um banco de dados vetorial e salvar arquivos gerados.

## Execução

```python
OPENAI_API_KEY=<api_key> python3 main.py --question [options]
```

```python
OPENAI_API_KEY=<api_key> python3 main.py -q "<question>" [options] 
```


## Configuração 
Instale as dependências 
```python
pip install pip install -r ./requirements.txt
```

## Opções
### Ajuda
Mostra na tela todas as opções possíveis dentro da aplicação.
```
python3 main.py -h
```
### Alterando arquivo de configuração
Você pode alterar as configurações básicas deste projeto passando um arquivo <file>.yml. O script irá copiar esse arquivo para o diretório de configuração da aplicação. O arquivo de configuração contém informações importantes, como o tamanho dos chunks a serem gerados e o modelo de IA utilizado. Abaixo, segue um exemplo de arquivo de configuração:
```yaml
chunk-size: 500
chunk-overlap: 20

embedding-model: ""
context-path: "./context"
template-path: "./template.txt"

default-vector-store-k: 5
default-llm-temperature: 0
```
```python
  python3 main.py --config=<filepath>
```



