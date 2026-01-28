import time
from pinecone import Pinecone, ServerlessSpec
from config import PINECONE_API_KEY, INDEX_NAME

def get_pinecone_client():
    """
    Initializes the Pinecone client and returns the Index object.
    """
    if not PINECONE_API_KEY:
        raise ValueError("Error: PINECONE_API_KEY is missing in config.py or .env")

    # 1. Initialize the Client
    pc = Pinecone(api_key=PINECONE_API_KEY)

    # 2. Check if the index exists
    existing_indexes = [index.name for index in pc.list_indexes()]
    
    if INDEX_NAME not in existing_indexes:
        print(f"Index '{INDEX_NAME}' not found. Please create it in the Pinecone Console.")
        # programatically creating if index not there
        # pc.create_index(
        #     name=INDEX_NAME,
        #     dimension=1536, # Standard for text-embedding-3-small
        #     metric='cosine',
        #     spec=ServerlessSpec(cloud='aws', region='us-east-1')
        # )
    
    # 3. Connecting to the Index
    index = pc.Index(INDEX_NAME)
    
    return index