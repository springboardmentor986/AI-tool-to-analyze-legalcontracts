"""
Enhanced Vector Store with Local Embeddings
MANDATORY Pinecone integration for Milestone 3
Uses sentence-transformers for embeddings (no API quota limits)
"""

import os
import sys
from dotenv import load_dotenv
from typing import List, Dict, Optional
import hashlib
import time

# Fix Windows console UTF-8 encoding for emoji support
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

try:
    from pinecone import Pinecone, ServerlessSpec
    PINECONE_AVAILABLE = True
except ImportError:
    PINECONE_AVAILABLE = False
    print("[WARNING] Pinecone not available")

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    LOCAL_EMBEDDINGS_AVAILABLE = True
except ImportError:
    LOCAL_EMBEDDINGS_AVAILABLE = False
    print("[WARNING] sentence-transformers not available")

# Google GenAI removed - using local sentence-transformers only (no API quota limits)

load_dotenv()


class VectorStore:
    """
    Vector database for storing contract embeddings
    Uses Pinecone for efficient similarity search
    Uses local sentence-transformers for embeddings (NO API QUOTA LIMITS)
    """
    
    def __init__(self, api_key: str = None):
        """Initialize Pinecone connection and local embedding model"""
        self.api_key = os.getenv("PINECONE_API_KEY")
        self.google_api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.environment = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
        self.index_name = "legal-contracts"
        self.pc = None
        self.index = None
        self.embedding_model = None
        
        # Initialize LOCAL embedding model (NO API QUOTA)
        if LOCAL_EMBEDDINGS_AVAILABLE:
            print("🚀 Loading local embedding model (no API limits)...")
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            print("[OK] Local embedding model loaded: all-MiniLM-L6-v2 (384 dim)")
        else:
            print("[ERROR] sentence-transformers not installed - Pinecone storage will fail!")
        
        if self.api_key and self.api_key != "your_pinecone_api_key_here":
            self._initialize_pinecone()
        else:
            print("[WARNING] Pinecone API key not configured in .env")
    
    def _initialize_pinecone(self):
        """Initialize Pinecone client and index"""
        if not PINECONE_AVAILABLE:
            print("[WARNING] Pinecone library not installed")
            return
        
        try:
            # Initialize Pinecone
            self.pc = Pinecone(api_key=self.api_key)
            
            # Create index if it doesn't exist (384 dimensions for local model)
            existing_indexes = [index.name for index in self.pc.list_indexes()]
            
            if self.index_name not in existing_indexes:
                print(f"[DATA] Creating Pinecone index: {self.index_name}")
                self.pc.create_index(
                    name=self.index_name,
                    dimension=384,  # all-MiniLM-L6-v2 dimension
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws",
                        region=self.environment
                    )
                )
                print("[WAIT] Waiting for index to be ready...")
                time.sleep(10)  # Wait for index creation
            
            # Connect to index
            self.index = self.pc.Index(self.index_name)
            print(f"[OK] Connected to Pinecone index: {self.index_name}")
            
        except Exception as e:
            print(f"[WARNING] Pinecone initialization error: {str(e)}")
            self.pc = None
            self.index = None
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings using LOCAL model (NO API QUOTA LIMITS)
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            List of embedding vectors
        """
        if not self.embedding_model:
            print("[ERROR] Local embedding model not available")
            return []
        
        try:
            # Generate embeddings using local model
            embeddings = self.embedding_model.encode(texts, show_progress_bar=False)
            return embeddings.tolist()
            
        except Exception as e:
            print(f"[ERROR] Error generating embeddings: {str(e)}")
            return []
    
    def generate_query_embedding(self, query_text: str) -> Optional[List[float]]:
        """
        Generate embedding for a query using LOCAL model
        
        Args:
            query_text: Query string to embed
            
        Returns:
            Embedding vector or None
        """
        if not self.embedding_model:
            return None
        
        try:
            embedding = self.embedding_model.encode([query_text], show_progress_bar=False)
            return embedding[0].tolist()
        except Exception as e:
            print(f"[ERROR] Error generating query embedding: {str(e)}")
            return None
    
    def store_contract(self, contract_id: str, contract_text: str, metadata: Dict = None):
        """
        Store contract in vector database
        
        Args:
            contract_id: Unique identifier for the contract
            contract_text: Full contract text
            metadata: Additional metadata to store
        """
        if not self.index:
            print("[WARNING] Pinecone index not available")
            return False
        
        try:
            # Generate embedding
            embeddings = self.generate_embeddings([contract_text])
            if not embeddings:
                return False
            
            # Prepare metadata
            meta = metadata or {}
            meta['text'] = contract_text[:500]  # Store first 500 chars
            meta['contract_id'] = contract_id
            
            # Upsert to Pinecone
            self.index.upsert(vectors=[
                {
                    'id': contract_id,
                    'values': embeddings[0],
                    'metadata': meta
                }
            ])
            
            print(f"[OK] Stored contract {contract_id} in Pinecone")
            return True
            
        except Exception as e:
            print(f"[ERROR] Error storing contract: {str(e)}")
            return False
    
    def search_similar_contracts(self, query_text: str, top_k: int = 5) -> List[Dict]:
        """
        Search for similar contracts
        
        Args:
            query_text: Text to search for
            top_k: Number of results to return
            
        Returns:
            List of similar contracts with scores
        """
        if not self.index:
            return []
        
        try:
            # Generate query embedding
            query_embedding = self.generate_query_embedding(query_text)
            if not query_embedding:
                return []
            
            # Query Pinecone
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )
            
            similar_contracts = []
            for match in results.matches:
                similar_contracts.append({
                    'contract_id': match.id,
                    'score': match.score,
                    'metadata': match.metadata
                })
            
            return similar_contracts
            
        except Exception as e:
            print(f"[ERROR] Error searching contracts: {str(e)}")
            return []
    
    def store_intermediate_results(self, contract_id: str, extracted_clauses: Dict,
                                  identified_risks: Dict) -> bool:
        """
        Store intermediate results (clauses and risks) in Pinecone (Milestone 3 MANDATORY)
        Uses LOCAL embeddings - NO API QUOTA LIMITS
        
        Args:
            contract_id: Unique contract identifier
            extracted_clauses: Dict of domain -> List[ExtractedClause]
            identified_risks: Dict of domain -> List[IdentifiedRisk]
            
        Returns:
            True if successful, False otherwise
        """
        if not self.index:
            print("[ERROR] Pinecone index not available - MANDATORY storage failed")
            return False
        
        if not self.embedding_model:
            print("[ERROR] Embedding model not available - MANDATORY storage failed")
            return False
        
        print(f"\n💾 Storing intermediate results for contract {contract_id}...")
        
        try:
            vectors_to_upsert = []
            
            # Store clauses (up to 10 per domain)
            for domain, clauses in extracted_clauses.items():
                for idx, clause in enumerate(clauses[:10]):  # Limit to 10 per domain
                    # Generate embedding for clause text
                    embedding = self.generate_query_embedding(clause.text)
                    if not embedding:
                        continue
                    
                    vector_id = f"{contract_id}_clause_{domain}_{idx}"
                    vectors_to_upsert.append({
                        'id': vector_id,
                        'values': embedding,
                        'metadata': {
                            'type': 'clause',
                            'domain': domain,
                            'clause_type': clause.clause_type,
                            'text': clause.text[:500],
                            'location': clause.location,
                            'confidence': clause.confidence,
                            'contract_id': contract_id
                        }
                    })
            
            # Store risks (up to 10 per domain)
            for domain, risks in identified_risks.items():
                for idx, risk in enumerate(risks[:10]):  # Limit to 10 per domain
                    # Generate embedding for risk description
                    risk_text = f"{risk.category}: {risk.description}"
                    embedding = self.generate_query_embedding(risk_text)
                    if not embedding:
                        continue
                    
                    vector_id = f"{contract_id}_risk_{domain}_{idx}"
                    vectors_to_upsert.append({
                        'id': vector_id,
                        'values': embedding,
                        'metadata': {
                            'type': 'risk',
                            'domain': domain,
                            'category': risk.category,
                            'severity': risk.severity.value,
                            'description': risk.description[:500],
                            'recommendation': risk.recommendation[:500],
                            'contract_id': contract_id
                        }
                    })
            
            # Batch upsert to Pinecone
            if vectors_to_upsert:
                # Upsert in batches of 100
                batch_size = 100
                for i in range(0, len(vectors_to_upsert), batch_size):
                    batch = vectors_to_upsert[i:i+batch_size]
                    self.index.upsert(vectors=batch)
                    time.sleep(0.1)  # Small delay between batches
                
                print(f"[OK] Stored {len(vectors_to_upsert)} intermediate result vectors")
                return True
            else:
                print("[WARNING] No vectors generated from results")
                return False
            
        except Exception as e:
            print(f"[ERROR] Error storing intermediate results: {str(e)}")
            return False
    
    def retrieve_similar_clauses(self, query_text: str, domain: str = None, 
                                top_k: int = 5) -> List[Dict]:
        """
        Retrieve similar clauses from stored contracts (Milestone 3)
        
        Args:
            query_text: Text to search for
            domain: Optional domain filter (compliance, finance, legal, operations)
            top_k: Number of results to return
            
        Returns:
            List of similar clauses with metadata
        """
        if not self.index:
            return []
        
        try:
            # Generate query embedding
            query_embedding = self.generate_query_embedding(query_text)
            if not query_embedding:
                return []
            
            # Build filter
            filter_dict = {"type": "clause"}
            if domain:
                filter_dict["domain"] = domain
            
            # Query Pinecone
            results = self.index.query(
                vector=query_embedding,
                filter=filter_dict,
                top_k=top_k,
                include_metadata=True
            )
            
            similar_clauses = []
            for match in results.matches:
                similar_clauses.append({
                    "id": match.id,
                    "score": match.score,
                    "metadata": match.metadata
                })
            
            return similar_clauses
            
        except Exception as e:
            print(f"[ERROR] Error retrieving similar clauses: {str(e)}")
            return []
    
    def retrieve_similar_risks(self, query_text: str, severity: str = None,
                              top_k: int = 5) -> List[Dict]:
        """
        Retrieve similar risks from stored contracts (Milestone 3)
        
        Args:
            query_text: Text to search for
            severity: Optional severity filter (Critical, High, Medium, Low)
            top_k: Number of results to return
            
        Returns:
            List of similar risks with metadata
        """
        if not self.index:
            return []
        
        try:
            # Generate query embedding
            query_embedding = self.generate_query_embedding(query_text)
            if not query_embedding:
                return []
            
            # Build filter
            filter_dict = {"type": "risk"}
            if severity:
                filter_dict["severity"] = severity
            
            # Query Pinecone
            results = self.index.query(
                vector=query_embedding,
                filter=filter_dict,
                top_k=top_k,
                include_metadata=True
            )
            
            similar_risks = []
            for match in results.matches:
                similar_risks.append({
                    "id": match.id,
                    "score": match.score,
                    "metadata": match.metadata
                })
            
            return similar_risks
            
        except Exception as e:
            print(f"[ERROR] Error retrieving similar risks: {str(e)}")
            return []
