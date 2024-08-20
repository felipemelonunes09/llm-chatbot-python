# llm-chatbot-python

**Status Atual: ✅ Concluído**

Google Colab Article: 
https://github.com/felipemelonunes09/llm-chatbot-python/blob/main/ai_chatbot_python.ipynb


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

### Gerando embeddings
Nesta aplicação, você pode fornecer uma URL para realizar web scraping e exportar um arquivo .csv contendo os valores dos embeddings.

-s é um comando para salvar a estrutura.

-f é um parâmetro opcional para atribuir um nome ao arquivo final.

O comando para gerar os embeddings é:
```python
python3 main.py --embedding=<url> -s -f <filename>
```

### Scrap
Esta aplicação utiliza o conceito de injeção de contexto. Para isso, é necessário extrair informações de outras fontes (nesta versão, apenas da web). O comando a seguir é utilizado para obter uma URL, extrair as informações e armazenar o resultado no diretório ./context.

-f é um parâmetro opcional para atribuir um nome ao arquivo final.
```python
python3 main.py --scrap=<url> -f example_01.txt
```

### Listando contextos
Para listar os contextos que ja foram salvos 
```python
python3 main.py --lc
```
### Fazendo Perguntas ao Modelo 
Para fazer uma pergunta, basta utilizar este comando e, em seguida, informar a sua dúvida.
```python
python3 main.py -q "<question>"
```
Você também tem a opção de não fornecer a pergunta com este comando. No entanto, a aplicação solicitará um input em seguida.
```python
python3 main.py --question
```
É possível especificar um contexto único para ser utilizado. Caso essa opção não seja fornecida, a aplicação considerará todos os arquivos dentro do diretório ./context.
```python
python3 main.py --question -c example01.txt
```
A opção K define o nível de busca no vector store. Quanto menor esse número, menos texto será inserido no contexto; quanto maior, mais texto será incluído.
```python
python3 main.py --question -k 10
```
É possível também definir a temperatura da resposta na aplicação. Quanto mais próxima de 0, mais concisa e menos criativa será a resposta. Quanto mais próxima de 1, mais criativa e menos precisa será a resposta.
```python
python3 main.py --question -t 0.2
```

É possível encadear comandos, permitindo extrair dados de uma URL e utilizá-los imediatamente para responder à pergunta do usuário."
```python
python3 main.py --question --scrap=<url>
```
Outro exemplo de encadeamento das opções
```python
python3 main.py --question --scrap=<url> -f <filepath> -c <filename> -k 10 -t 0.9 --config=<filepath>
```

Embora não tenha sido explicitado nos exemplos, é necessário passar a chave da API como uma variável de ambiente sempre que executar os comandos. A aplicação não salvará essa chave em nenhum diretório em momento algum.
```python
OPENAI_API_KEY=<key> python3 main.py [comandos]
```

**Nota:** Este projeto está agora em modo de manutenção. Atualizações futuras serão baseadas em feedback e correções críticas.


