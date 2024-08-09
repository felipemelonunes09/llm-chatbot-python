import yaml

CONFIG_FILENAME = 'config.yml' 

with open(CONFIG_FILENAME, 'r') as file:    
    config = yaml.safe_load(file)

    CHUNK_SIZE          = config.get("chunk-size", 100)
    CHUNK_OVERLAP       = config.get("chunk-overlap", 20)
    
    EMBEDDING_MODEL     = config.get("embedding-model", "text-embedding-ada-002")
    CONTEXT_PATH        = config.get("context-path", "./context")
    TEMPLATE_PATH       = config.get("template-path", "./template.txt")
    
    DEFAULT_LIMITE_K        = config.get("default-vector-store-k", 5)
    DEFAULT_LLM_TEMPERATURE = config.get("default-llm-temperature", 0)

 