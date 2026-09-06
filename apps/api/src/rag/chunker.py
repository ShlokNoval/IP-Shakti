"""
Document Chunker & Metadata Tagger

Reads raw text/markdown documents from the 'IP Shakti Sources' directory,
splits them into semantic chunks, and attaches the strict JSON metadata schema
required for accurate, authenticated retrieval.
"""
import os
import json
import fitz # PyMuPDF
from pathlib import Path
from typing import List, Dict, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentChunker:
    def __init__(self, sources_dir: str):
        self.sources_dir = Path(sources_dir)
        # We use a relatively small chunk size to ensure high precision in legal retrieval
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ".", " ", ""]
        )

    def _determine_metadata(self, filepath: Path) -> Dict[str, Any]:
        """
        Derives the strict JSON metadata schema based on the folder structure.
        Structure expected: IP Shakti Sources / [Jurisdiction] / [Category] / file.ext
        """
        parts = filepath.parts
        
        # Default metadata
        metadata = {
            "jurisdiction": "Unknown",
            "category": "Unknown",
            "source_name": filepath.stem,
            "is_official": True, # Assuming all provided docs are official
            "official_url": "Pending Verification" # To be updated manually or via mapping
        }

        try:
            # Find the index of the base sources directory
            base_idx = parts.index(self.sources_dir.name)
            if len(parts) > base_idx + 2:
                metadata["jurisdiction"] = parts[base_idx + 1] # e.g., 'India' or 'Global'
                metadata["category"] = parts[base_idx + 2]     # e.g., 'ABS [Biodiversity]'
        except ValueError:
            pass

        return metadata

    def _extract_text(self, filepath: Path) -> str:
        """Extracts text from a file based on its extension."""
        ext = filepath.suffix.lower()
        content = ""
        try:
            if ext == '.txt':
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
            elif ext == '.pdf':
                doc = fitz.open(filepath)
                for page in doc:
                    content += page.get_text() + "\n"
                doc.close()
            else:
                print(f"Skipping unsupported file type: {filepath}")
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
        return content

    def process_directory(self) -> List[Dict[str, Any]]:
        """Processes all text and pdf files in the sources directory."""
        all_chunks = []
        
        # Look for both txt and pdf files
        files = list(self.sources_dir.rglob("*.txt")) + list(self.sources_dir.rglob("*.pdf"))
        
        for filepath in files:
            content = self._extract_text(filepath)
            if not content.strip():
                continue

            metadata = self._determine_metadata(filepath)
            
            # Split the document
            chunks = self.text_splitter.split_text(content)
            
            for chunk in chunks:
                all_chunks.append({
                    "content": chunk,
                    "metadata": metadata
                })
                
        return all_chunks

    def save_to_jsonl(self, chunks: List[Dict[str, Any]], output_path: str):
        """Saves the chunks to a JSONL file for embedding/database upload."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for chunk in chunks:
                f.write(json.dumps(chunk) + '\n')
        print(f"Saved {len(chunks)} chunks to {output_path}")

if __name__ == "__main__":
    # Example usage when run directly
    project_root = Path(__file__).parent.parent.parent.parent.parent
    sources_dir = project_root / "IP Shakti Sources"
    output_path = project_root / "apps" / "api" / "data" / "processed" / "chunks.jsonl"
    
    chunker = DocumentChunker(str(sources_dir))
    chunks = chunker.process_directory()
    chunker.save_to_jsonl(chunks, str(output_path))
