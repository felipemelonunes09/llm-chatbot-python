import sys
import getopt
import logging
import requests
import bs4
import config
import importlib
import openai
import pandas
import datetime
import utils


def help():
    print('\n### LLM Application ###\n')
    
    print('Usage: main.py --question [options] or main.py -q <question> [options]')
    print('    -q question       Define a question to the application (all undescore is replaced with " ")')
    print('Options:')
    print('    -h                       print the help message')
    print('    -s                       Save all the files generated')
    print('    -t <number>              set the temperature to the model when using -q or --question')
    print('    -k <number>              limite the search into the vector store when using -q or --question')
    print('    -f <filename>            define a name for the output file')
    print('    -c <filename>            use with -q or --question to provide a context for the question, if not specified will search using proximity beetween context and question and will use the 5 most common text to generate')
    print('    --lc                     List all the context files saved')
    print('    --question               Make the user type the question')
    print('    --scrap=<scrap_url>      scrap the url and chunk the text into an asset folder to to used in the vector database, use with -f to set output filename')
    print('    --embedding=<scrap_url>  generate an embedding dataframe after scrapping an url and chunking the text, use with -f to set the output filename, use -s to save the dataframe')
    print('    --config=<filename>      open the provided file and transfer the information to the config.yml')
    
    
def main(argv):
    
    def get_embedding(text, model=config.EMBEDDING_MODEL):
        text = text.replace("\n", " ")
        return openai.embeddings.create( input=text, model=model).data[0].embedding
    
    url              = None
    question         = None
    config_path      = None
    save_files       = False
    embedding        = False
    scrap            = False 
    context          = None
    k                = config.DEFAULT_LIMITE_K
    temperature      = config.DEFAULT_LLM_TEMPERATURE
    filename         = f"{datetime.datetime.now()}"
            
    try:
        opts, args = getopt.getopt(argv, "hsf:q:c:k:t:", ["config=", "embedding=", "scrap=", "question", "lc"])
        
        for option, argument in opts:
            if option == '-h':
                help()
                sys.exit(0)
            
            elif option == '-s':
                save_files = True
                
            elif option == '-f':
                filename = argument
                
            elif option == '-q':
                question = argument.replace("_", " ")
            
            elif option == '-c':
                context = argument
            
            elif option == '-k':
                k = int(argument)
                
            elif option == '-t':
                temperature = int(argument)
            
            if option == '--lc':
                contexts = utils.get_contexts()
                print('contexts files')
                print( ''.join([ f"\t{context}\n" for context in contexts ]) )
                
                sys.exit(0)
                
            elif option == "--question":
                question = input("Type the question to the model awnser: ")
                
            elif option == '--scrap':
                url = argument
                scrap = True
                logging.info(f"Target: {url}")
                
            elif option == '--embedding':
                url = argument
                embedding = True
                logging.info(f'Target: {url}')
                
            elif option == '--config':
                config_path = argument
                logging.info(f'Target path: {config_path}')
        
        # use case: user wants to define another configuration file
        if config_path:
            if not config_path.endswith(".yml"):
                raise RuntimeError("configuration file must be .yml")
            with open(config_path, 'r') as file:
                with open(config.CONFIG_FILENAME, 'w') as config_file:
                    config_file.write(file.read())
            
            importlib.reload(config)
            logging.info("copied information from file, reloading config module")
            logging.info(f"{config.CHUNK_SIZE}")
            
        # user case: user wants to extract info from a site and pre-processing
        if url and embedding:
            
            logging.info("Starting target scrap")
            
            response    = requests.get(url)
            soup        = bs4.BeautifulSoup(response.text, 'html.parser')
            text        = soup.get_text()
              
            texts = utils.text_splitter.create_documents([text])
            
            logging.info(f"Documents created --size {len(texts)}")
            
            text_chunks = []
            for text in texts:
                text_chunks.append(text.page_content)
                
            df = pandas.DataFrame({ 'text_chunks': text_chunks })  
            
            logging.info(f"Dataframe created")
            logging.info(f"Creating embeddings")
            
            df['embedding'] = df.text_chunks.apply(lambda x: get_embedding(x))
            if save_files:
                df.to_csv(f"df_{filename}.csv", index=True)
                
        # use case: user wants to scrap a page, and save to use into the vector store
        if url and scrap:
            
            logging.info("Starting url scrapping")
            response = requests.get(url)
            soup = bs4.BeautifulSoup(response.content, 'html.parser')
            
            text = soup.get_text()
            text = text.replace('\n', " ")
            
            logging.info(f"Saving scrap data in: {config.CONTEXT_PATH}/{filename}.txt")
            with open(f"{config.CONTEXT_PATH}/{filename}.txt", 'w', encoding='utf-8') as file:
                file.write(text)
                
        if question:
            
            from langchain_openai import OpenAI
            from langchain.prompts import PromptTemplate
            from langchain_openai import OpenAIEmbeddings
            from langchain_community.vectorstores import Chroma
            
            embedding = OpenAIEmbeddings()
            context = utils.load_context(context) if context else utils.load_context()
            
            logging.info("Loaded contexts")
            
            db = Chroma.from_documents(context, embedding)
            results = db.similarity_search(query=question, k=k)
            
            logging.info("Finded similarity in vector store")
            
            template = str()
            with open(config.TEMPLATE_PATH) as file:
                template = file.read()
                
            llm = OpenAI(temperature=temperature)
            
            logging.info("Formatting prompt")
                    
            prompt = PromptTemplate(template=template, input_variables=["context", "question"])
            prompt = prompt.format(context=results, question=question)
            
            result = llm(prompt)
            print(f"""
                  
                  Pergunta: {question}
                  
                  Resposta: {result}
                  
            """)
            
    except getopt.GetoptError as e:
        logging.warning(f'Invalid option {e.opt} : {e.msg}')
    except openai.OpenAIError as e:
        logging.error("Failed to call the api: make sure that envriment key OPENAI_API_KEY is setted\ntry: OPENAI_API_KEY=<key> python main.py [options]")
        logging.error(f'OpenAI error: {e}')
        
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        

if __name__ == "__main__":
    
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    main(sys.argv[1:])