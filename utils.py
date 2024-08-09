import config
import os

from langchain_text_splitters import RecursiveCharacterTextSplitter


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size      = config.CHUNK_SIZE,
    chunk_overlap   = config.CHUNK_OVERLAP,
    length_function = len
)

        
def get_contexts():
    return [f for f in os.listdir(config.CONTEXT_PATH) if os.path.isfile(os.path.join(config.CONTEXT_PATH, f))]



def load_context(context = None):
    
    if context:
        with open(f"{config.CONTEXT_PATH}/{context}", 'r') as file:
            file_content = file.read()
            return text_splitter.create_documents([file_content])
    else:
        
        contexts = get_contexts()
        texts = []
        for context in contexts:
            with open(f"{config.CONTEXT_PATH}/{context}", 'r') as file:
                file_content = file.read()
                texts.append(file_content)
        texts = text_splitter.create_documents(texts)
        return texts
        
        
                
