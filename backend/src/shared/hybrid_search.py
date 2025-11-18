"""
Hybrid Search Service for Sign Language Units
Combines Semantic Search (Gemini Embeddings) and Keyword Search (BM25)
"""

import os
import re
from typing import List, Dict, Any
from collections import defaultdict
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document


class HybridSearchService:
    """Service for performing hybrid search on unit descriptions"""
    
    def __init__(self, gemini_api_key: str = None):
        """
        Initialize Hybrid Search Service
        
        Args:
            gemini_api_key: Gemini API key for embeddings
        """
        self.gemini_api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is required for hybrid search")
        
        # Initialize embeddings with correct model name
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            google_api_key=self.gemini_api_key
        )
        
        self.vectorstore = None
        self.keyword_retriever = None
        self.is_initialized = False
    
    def _split_descriptions(self, description_text: str) -> List[str]:
        """
        Split multiple descriptions into individual ones
        Example input: "Mô tả 1: ...\n\nMô tả 2: ...\n\nMô tả 3: ..."
        Returns: ["...", "...", "..."] (without prefixes)
        """
        if not description_text:
            return []
        
        # Split by "Mô tả X:" pattern
        parts = re.split(r'Mô tả \d+:\s*', description_text)
        # Remove empty strings and strip whitespace
        descriptions = [desc.strip() for desc in parts if desc.strip()]
        
        return descriptions
    
    def initialize_from_units(self, units: List[Dict[str, Any]]):
        """
        Initialize search indices from unit data
        
        Args:
            units: List of unit dictionaries with 'description', 'text', 'id' fields
        """
        if not units:
            print("Warning: No units provided for indexing")
            return
        
        # Create documents from units
        # Split each unit's description into multiple documents for better search accuracy
        documents = []
        for unit in units:
            if unit.get('description'):
                # Split descriptions (e.g., "Mô tả 1: ..., Mô tả 2: ...")
                descriptions = self._split_descriptions(unit['description'])
                
                # If no split happened, use original description
                if not descriptions:
                    descriptions = [unit['description']]
                
                # Create a document for each description variant
                for desc in descriptions:
                    doc = Document(
                        page_content=desc,
                        metadata={
                            'unit_id': unit.get('id'),
                            'text': unit.get('text', ''),
                            'video_url': unit.get('video_url', ''),
                            'image_url': unit.get('image_url', ''),
                            'transcription': unit.get('transcription', ''),
                            'full_description': unit.get('description', '')
                        }
                    )
                    documents.append(doc)
        
        if not documents:
            print("Warning: No valid descriptions found in units")
            return
        
        print(f"Indexing {len(documents)} description variants from {len(units)} units...")
        
        # Create vector store for semantic search
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings
        )
        
        # Create BM25 retriever for keyword search
        self.keyword_retriever = BM25Retriever.from_documents(documents)
        self.keyword_retriever.k = 10  # Increased to account for multiple descriptions per unit
        
        self.is_initialized = True
        print("✅ Hybrid search initialized successfully")
    
    def search(self, query: str, top_k: int = 5, weights: List[float] = None) -> List[Dict[str, Any]]:
        """
        Perform hybrid search combining semantic and keyword search
        
        Args:
            query: Search query (description of the sign)
            top_k: Number of results to return
            weights: Weights for [semantic_search, keyword_search], default [0.5, 0.5]
        
        Returns:
            List of units with relevance scores
        """
        if not self.is_initialized:
            raise ValueError("Search service not initialized. Call initialize_from_units() first.")
        
        if weights is None:
            weights = [0.3, 0.7]  # Equal weights for balanced results
        
        # Search more results to account for multiple descriptions per unit
        search_k = top_k * 3
        
        # Perform semantic search
        semantic_results = self.vectorstore.similarity_search(query, k=search_k)
        
        # Perform keyword search
        keyword_results = self.keyword_retriever.invoke(query)[:search_k]
        
        # Combine results with ensemble scoring, grouped by unit_id
        # For each unit, keep only the BEST matching description
        unit_best_scores = {}
        unit_docs = {}
        
        # Score semantic results - keep only best match per unit
        for rank, doc in enumerate(semantic_results):
            unit_id = doc.metadata.get('unit_id')
            if unit_id:
                # Use reciprocal rank scoring
                semantic_score = weights[0] / (rank + 1)
                
                # Only keep this if it's better than previous matches for this unit
                if unit_id not in unit_best_scores:
                    unit_best_scores[unit_id] = {'semantic': semantic_score, 'keyword': 0}
                    unit_docs[unit_id] = doc
                elif semantic_score > unit_best_scores[unit_id]['semantic']:
                    # This description matches better than previous ones
                    unit_best_scores[unit_id]['semantic'] = semantic_score
                    unit_docs[unit_id] = doc
        
        # Score keyword results - keep only best match per unit
        for rank, doc in enumerate(keyword_results):
            unit_id = doc.metadata.get('unit_id')
            if unit_id:
                keyword_score = weights[1] / (rank + 1)
                
                if unit_id not in unit_best_scores:
                    unit_best_scores[unit_id] = {'semantic': 0, 'keyword': keyword_score}
                    unit_docs[unit_id] = doc
                elif keyword_score > unit_best_scores[unit_id]['keyword']:
                    # This description matches better for keywords
                    unit_best_scores[unit_id]['keyword'] = keyword_score
                    # Update doc only if total score is better
                    current_total = unit_best_scores[unit_id]['semantic'] + unit_best_scores[unit_id]['keyword']
                    new_total = unit_best_scores[unit_id]['semantic'] + keyword_score
                    if new_total > current_total:
                        unit_docs[unit_id] = doc
        
        # Calculate final scores (sum of best semantic + best keyword for each unit)
        unit_scores = {
            unit_id: scores['semantic'] + scores['keyword']
            for unit_id, scores in unit_best_scores.items()
        }
        
        # Sort units by score and get top_k unique units
        sorted_unit_ids = sorted(
            unit_scores.keys(),
            key=lambda uid: unit_scores[uid],
            reverse=True
        )[:top_k]
        
        # Format results with full descriptions
        results = []
        for unit_id in sorted_unit_ids:
            doc = unit_docs[unit_id]
            result = {
                'unit_id': unit_id,
                'text': doc.metadata.get('text'),
                'description': doc.metadata.get('full_description'),  # Return full description
                'video_url': doc.metadata.get('video_url'),
                'image_url': doc.metadata.get('image_url'),
                'transcription': doc.metadata.get('transcription'),
                'relevance_score': unit_scores[unit_id],
                'matched_description': doc.page_content  # The specific description that matched
            }
            results.append(result)
        
        return results


# Global instance
_search_service = None


def get_search_service() -> HybridSearchService:
    """Get or create global search service instance"""
    global _search_service
    if _search_service is None:
        _search_service = HybridSearchService()
    return _search_service


def initialize_search_service(units: List[Dict[str, Any]]):
    """Initialize the global search service with units data"""
    service = get_search_service()
    service.initialize_from_units(units)
    return service
