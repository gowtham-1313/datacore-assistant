# backend/rag.py
import os
import chromadb
from sentence_transformers import SentenceTransformer
import PyPDF2
import hashlib
from typing import List, Dict

# Initialize embedding model
print("🔄 Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("✅ Embedding model loaded!")

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="backend/data/chroma_db")

# Get or create collection
collection = chroma_client.get_or_create_collection(
    name="pdf_documents"
)

def chunk_text(text: str, chunk_size: int = 400, overlap: int = 50) -> List[str]:
    """Split text into chunks with overlap"""
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
        if i + chunk_size >= len(words):
            break
    
    return chunks

def load_pdf(file_path: str) -> str:
    """Extract text from PDF"""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text += f"\n--- Page {page_num + 1} ---\n"
                    text += page_text
            return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

def index_pdf(file_path: str):
    """Index a PDF file into ChromaDB"""
    print(f"📄 Indexing: {file_path}")
    
    text = load_pdf(file_path)
    if not text:
        print("   No text extracted")
        return
    
    chunks = chunk_text(text, chunk_size=400, overlap=50)
    print(f"   Created {len(chunks)} chunks")
    
    file_name = os.path.basename(file_path)
    ids = [hashlib.md5(f"{file_name}_{i}".encode()).hexdigest()[:10] for i in range(len(chunks))]
    metadatas = [{"source": file_name, "chunk_index": i} for i in range(len(chunks))]
    
    collection.add(
        documents=chunks,
        ids=ids,
        metadatas=metadatas
    )
    print(f"   ✅ Indexed {len(chunks)} chunks")

def search_pdf(query: str, top_k: int = 3) -> List[Dict]:
    """Search for relevant PDF chunks"""
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    
    formatted_results = []
    if results['documents'] and len(results['documents'][0]) > 0:
        for i in range(len(results['documents'][0])):
            formatted_results.append({
                'text': results['documents'][0][i],
                'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                'score': results['distances'][0][i] if 'distances' in results else None
            })
    
    return formatted_results

def index_all_pdfs():
    """Index all PDFs in the pdf_files folder"""
    pdf_folder = 'backend/data/pdf_files/'
    if not os.path.exists(pdf_folder):
        print("❌ PDF folder not found")
        return
    
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
    
    if not pdf_files:
        print("❌ No PDF files found")
        return
    
    print(f"📂 Found {len(pdf_files)} PDF files")
    for pdf_file in pdf_files:
        index_pdf(os.path.join(pdf_folder, pdf_file))
    
    print(f"✅ Total chunks in database: {collection.count()}")

if __name__ == "__main__":
    print("="*50)
    print("📚 INDEXING PDF DOCUMENTS")
    print("="*50)
    index_all_pdfs()