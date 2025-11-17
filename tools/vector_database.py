#!/usr/bin/env python3

"""
Vector Database Manager for document ingestion and semantic search.
Supports FOSS vector databases: ChromaDB, Qdrant, Weaviate
"""

import json
import os
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime

class VectorDatabaseManager:
    """
    Unified interface for FOSS vector databases.
    Prioritizes ChromaDB as the default FOSS option (Apache 2.0 license).
    """
    
    def __init__(self, db_type: str = "chromadb", config: Optional[Dict] = None):
        """
        Initialize vector database manager.
        
        Args:
            db_type: Type of vector DB ("chromadb", "qdrant", "weaviate")
            config: Database-specific configuration
        """
        self.db_type = db_type.lower()
        self.config = config or {}
        self.client = None
        self.collection = None
        
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize the selected vector database"""
        if self.db_type == "chromadb":
            self._init_chromadb()
        elif self.db_type == "qdrant":
            self._init_qdrant()
        elif self.db_type == "weaviate":
            self._init_weaviate()
        else:
            raise ValueError(f"Unsupported database type: {self.db_type}")
    
    def _init_chromadb(self):
        """Initialize ChromaDB (default FOSS option)"""
        try:
            import chromadb
            from chromadb.config import Settings
            
            persist_directory = self.config.get("persist_directory", "./chroma_data")
            
            self.client = chromadb.Client(Settings(
                persist_directory=persist_directory,
                anonymized_telemetry=False  # FOSS privacy principle
            ))
            
            collection_name = self.config.get("collection_name", "opencode_docs")
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"description": "OpenCode multi-agent document store"}
            )
            
            print(f"ChromaDB initialized: {collection_name}")
            
        except ImportError:
            print("ChromaDB not installed. Install with: pip install chromadb")
            raise
    
    def _init_qdrant(self):
        """Initialize Qdrant (FOSS vector database)"""
        try:
            from qdrant_client import QdrantClient
            from qdrant_client.models import Distance, VectorParams
            
            host = self.config.get("host", "localhost")
            port = self.config.get("port", 6333)
            
            self.client = QdrantClient(host=host, port=port)
            
            collection_name = self.config.get("collection_name", "opencode_docs")
            vector_size = self.config.get("vector_size", 384)  # Default for MiniLM
            
            # Create collection if not exists
            try:
                self.client.get_collection(collection_name)
            except Exception:
                self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
                )
            
            self.collection = collection_name
            print(f"Qdrant initialized: {collection_name}")
            
        except ImportError:
            print("Qdrant client not installed. Install with: pip install qdrant-client")
            raise
    
    def _init_weaviate(self):
        """Initialize Weaviate (FOSS vector database)"""
        try:
            import weaviate
            
            url = self.config.get("url", "http://localhost:8080")
            
            self.client = weaviate.Client(url)
            
            collection_name = self.config.get("collection_name", "OpencodeDoc")
            
            # Create schema if not exists
            schema = {
                "class": collection_name,
                "description": "OpenCode multi-agent document store",
                "properties": [
                    {
                        "name": "content",
                        "dataType": ["text"],
                        "description": "Document content"
                    },
                    {
                        "name": "metadata",
                        "dataType": ["text"],
                        "description": "Document metadata as JSON"
                    },
                    {
                        "name": "doc_id",
                        "dataType": ["text"],
                        "description": "Document ID"
                    }
                ]
            }
            
            try:
                self.client.schema.create_class(schema)
            except Exception as e:
                if "already exists" not in str(e).lower():
                    raise
            
            self.collection = collection_name
            print(f"Weaviate initialized: {collection_name}")
            
        except ImportError:
            print("Weaviate client not installed. Install with: pip install weaviate-client")
            raise
    
    def add_documents(self, documents: List[Dict[str, Any]], 
                     embeddings: Optional[List[List[float]]] = None) -> List[str]:
        """
        Add documents to vector database.
        
        Args:
            documents: List of documents with 'content' and optional 'metadata'
            embeddings: Pre-computed embeddings (optional, will compute if None)
        
        Returns:
            List of document IDs
        """
        doc_ids = []
        
        if self.db_type == "chromadb":
            doc_ids = self._add_chromadb(documents, embeddings)
        elif self.db_type == "qdrant":
            doc_ids = self._add_qdrant(documents, embeddings)
        elif self.db_type == "weaviate":
            doc_ids = self._add_weaviate(documents, embeddings)
        
        return doc_ids
    
    def _add_chromadb(self, documents: List[Dict[str, Any]], 
                      embeddings: Optional[List[List[float]]]) -> List[str]:
        """Add documents to ChromaDB"""
        doc_ids = [doc.get("id", str(uuid.uuid4())) for doc in documents]
        contents = [doc["content"] for doc in documents]
        metadatas = [doc.get("metadata", {}) for doc in documents]
        
        if embeddings:
            self.collection.add(
                ids=doc_ids,
                embeddings=embeddings,
                documents=contents,
                metadatas=metadatas
            )
        else:
            # ChromaDB will compute embeddings automatically
            self.collection.add(
                ids=doc_ids,
                documents=contents,
                metadatas=metadatas
            )
        
        return doc_ids
    
    def _add_qdrant(self, documents: List[Dict[str, Any]], 
                    embeddings: Optional[List[List[float]]]) -> List[str]:
        """Add documents to Qdrant"""
        from qdrant_client.models import PointStruct
        
        if not embeddings:
            embeddings = self._compute_embeddings([doc["content"] for doc in documents])
        
        doc_ids = [doc.get("id", str(uuid.uuid4())) for doc in documents]
        
        points = []
        for i, doc in enumerate(documents):
            points.append(PointStruct(
                id=doc_ids[i],
                vector=embeddings[i],
                payload={
                    "content": doc["content"],
                    "metadata": doc.get("metadata", {})
                }
            ))
        
        self.client.upsert(
            collection_name=self.collection,
            points=points
        )
        
        return doc_ids
    
    def _add_weaviate(self, documents: List[Dict[str, Any]], 
                      embeddings: Optional[List[List[float]]]) -> List[str]:
        """Add documents to Weaviate"""
        doc_ids = []
        
        for doc in documents:
            doc_id = doc.get("id", str(uuid.uuid4()))
            
            data_object = {
                "content": doc["content"],
                "metadata": json.dumps(doc.get("metadata", {})),
                "doc_id": doc_id
            }
            
            if embeddings:
                # Weaviate handles embeddings automatically in most cases
                self.client.data_object.create(
                    data_object=data_object,
                    class_name=self.collection
                )
            else:
                self.client.data_object.create(
                    data_object=data_object,
                    class_name=self.collection
                )
            
            doc_ids.append(doc_id)
        
        return doc_ids
    
    def search(self, query: str, top_k: int = 5, 
               filters: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """
        Search for similar documents.
        
        Args:
            query: Search query
            top_k: Number of results to return
            filters: Optional metadata filters
        
        Returns:
            List of matching documents with scores
        """
        if self.db_type == "chromadb":
            return self._search_chromadb(query, top_k, filters)
        elif self.db_type == "qdrant":
            return self._search_qdrant(query, top_k, filters)
        elif self.db_type == "weaviate":
            return self._search_weaviate(query, top_k, filters)
        
        return []
    
    def _search_chromadb(self, query: str, top_k: int, 
                         filters: Optional[Dict]) -> List[Dict[str, Any]]:
        """Search ChromaDB"""
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k,
            where=filters
        )
        
        matches = []
        if results and results["documents"]:
            for i, doc in enumerate(results["documents"][0]):
                matches.append({
                    "id": results["ids"][0][i],
                    "content": doc,
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "score": results["distances"][0][i] if results["distances"] else 0.0
                })
        
        return matches
    
    def _search_qdrant(self, query: str, top_k: int, 
                       filters: Optional[Dict]) -> List[Dict[str, Any]]:
        """Search Qdrant"""
        query_embedding = self._compute_embeddings([query])[0]
        
        results = self.client.search(
            collection_name=self.collection,
            query_vector=query_embedding,
            limit=top_k
        )
        
        matches = []
        for result in results:
            matches.append({
                "id": result.id,
                "content": result.payload.get("content", ""),
                "metadata": result.payload.get("metadata", {}),
                "score": result.score
            })
        
        return matches
    
    def _search_weaviate(self, query: str, top_k: int, 
                         filters: Optional[Dict]) -> List[Dict[str, Any]]:
        """Search Weaviate"""
        results = (
            self.client.query
            .get(self.collection, ["content", "metadata", "doc_id"])
            .with_near_text({"concepts": [query]})
            .with_limit(top_k)
            .do()
        )
        
        matches = []
        if results and "data" in results and "Get" in results["data"]:
            for item in results["data"]["Get"].get(self.collection, []):
                matches.append({
                    "id": item.get("doc_id", ""),
                    "content": item.get("content", ""),
                    "metadata": json.loads(item.get("metadata", "{}")),
                    "score": 1.0  # Weaviate doesn't always return scores
                })
        
        return matches
    
    def _compute_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Compute embeddings using local FOSS model.
        Uses sentence-transformers (FOSS) with MiniLM model.
        """
        try:
            from sentence_transformers import SentenceTransformer
            
            model_name = self.config.get("embedding_model", "all-MiniLM-L6-v2")
            model = SentenceTransformer(model_name)
            
            embeddings = model.encode(texts, convert_to_numpy=True)
            return embeddings.tolist()
            
        except ImportError:
            print("sentence-transformers not installed. Install with: pip install sentence-transformers")
            raise
    
    def ingest_file(self, file_path: str, chunk_size: int = 500, 
                   overlap: int = 50) -> List[str]:
        """
        Ingest a document file into the vector database.
        
        Args:
            file_path: Path to document file
            chunk_size: Size of text chunks
            overlap: Overlap between chunks
        
        Returns:
            List of document IDs
        """
        # Read file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Chunk the document
        chunks = self._chunk_text(content, chunk_size, overlap)
        
        # Create document objects
        documents = []
        for i, chunk in enumerate(chunks):
            documents.append({
                "content": chunk,
                "metadata": {
                    "source": file_path,
                    "chunk_id": i,
                    "total_chunks": len(chunks),
                    "ingested_at": datetime.now().isoformat()
                }
            })
        
        # Add to database
        return self.add_documents(documents)
    
    def _chunk_text(self, text: str, chunk_size: int, overlap: int) -> List[str]:
        """Split text into overlapping chunks"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            
            if chunk:
                chunks.append(chunk)
            
            start += chunk_size - overlap
        
        return chunks
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        if self.db_type == "chromadb":
            count = self.collection.count()
            return {
                "database": "ChromaDB",
                "collection": self.collection.name,
                "document_count": count,
                "status": "active"
            }
        elif self.db_type == "qdrant":
            info = self.client.get_collection(self.collection)
            return {
                "database": "Qdrant",
                "collection": self.collection,
                "document_count": info.points_count,
                "status": "active"
            }
        elif self.db_type == "weaviate":
            result = self.client.query.aggregate(self.collection).with_meta_count().do()
            count = result.get("data", {}).get("Aggregate", {}).get(self.collection, [{}])[0].get("meta", {}).get("count", 0)
            return {
                "database": "Weaviate",
                "collection": self.collection,
                "document_count": count,
                "status": "active"
            }
        
        return {"status": "unknown"}


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python vector_database.py <action> [args...]")
        print("Actions:")
        print("  init <db_type> - Initialize database (chromadb, qdrant, weaviate)")
        print("  ingest <file_path> - Ingest a document")
        print("  search <query> - Search for documents")
        print("  stats - Get database statistics")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == "init":
        db_type = sys.argv[2] if len(sys.argv) > 2 else "chromadb"
        manager = VectorDatabaseManager(db_type=db_type)
        print(f"Initialized {db_type}")
        print(json.dumps(manager.get_stats(), indent=2))
    
    elif action == "ingest":
        if len(sys.argv) < 3:
            print("Error: file_path required")
            sys.exit(1)
        
        file_path = sys.argv[2]
        db_type = sys.argv[3] if len(sys.argv) > 3 else "chromadb"
        
        manager = VectorDatabaseManager(db_type=db_type)
        doc_ids = manager.ingest_file(file_path)
        print(f"Ingested {len(doc_ids)} chunks from {file_path}")
        print(f"Document IDs: {doc_ids[:5]}...")
    
    elif action == "search":
        if len(sys.argv) < 3:
            print("Error: query required")
            sys.exit(1)
        
        query = sys.argv[2]
        db_type = sys.argv[3] if len(sys.argv) > 3 else "chromadb"
        top_k = int(sys.argv[4]) if len(sys.argv) > 4 else 5
        
        manager = VectorDatabaseManager(db_type=db_type)
        results = manager.search(query, top_k=top_k)
        
        print(f"Found {len(results)} results for: {query}")
        for i, result in enumerate(results):
            print(f"\n{i+1}. Score: {result['score']:.4f}")
            print(f"   Content: {result['content'][:200]}...")
            print(f"   Metadata: {result['metadata']}")
    
    elif action == "stats":
        db_type = sys.argv[2] if len(sys.argv) > 2 else "chromadb"
        manager = VectorDatabaseManager(db_type=db_type)
        print(json.dumps(manager.get_stats(), indent=2))
    
    else:
        print(f"Unknown action: {action}")
