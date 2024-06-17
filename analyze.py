from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama

parser = argparse.ArgumentParser(description='Analyze the reddit data using ollama and llama index')
parser.add_argument('--data_dir', default='data', help='directory to read from. It will analyze all txt files in this directory')
parser.add_argument('--embed_model', default='BAAI/bge-base-en-v1.5', help='embed model to use')
parser.add_argument('--llm_model_name', default='llama3:70b', help='will use ollama with this model')
parser.add_argument('--prompt', required=True, help='query or prompt to use to query the index')
parser.add_argument('--timeout', default=360.0, help='request timeout against ollama')

# Parse arguments
args = parser.parse_args()

documents = SimpleDirectoryReader(args.data_dir).load_data()

# bge-base embedding model
Settings.embed_model = HuggingFaceEmbedding(model_name=args.embed_model)

# ollama
Settings.llm = Ollama(model=args.llm_model_name, request_timeout=args.timeout)

index = VectorStoreIndex.from_documents(
    documents,
)

query_engine = index.as_query_engine()
response = query_engine.query(args.prompt)
print(response)
