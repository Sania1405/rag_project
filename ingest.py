import os
import chromadb
# Hint: You might need a library to read your document if it's a PDF
from PyPDF2 import PdfReader 

# Define the paths
DATA_DIR = "data"
DB_DIR = "vector_db"

def extract_text_from_file(file_path):
    """
    Step 1: Read the text from your resume/document.
    TODO: Write the code to open the file and return its text as a string.
    """
    pd=PdfReader(file_path)
    text=""
    for page in pd.pages:
        text+=page.extract_text()
    return text

def chunk_text(text, chunk_size=500, overlap=50):
    """
    Step 2: Split the large text into smaller chunks.
    TODO: Write the logic to break the 'text' into a list of smaller strings.
    """
    start=0
    chunks=[]
    while(start<len(text)):
        end=start+chunk_size
        curchunk=text[start:end]
        chunks.append(curchunk)
        start=start+(chunk_size-overlap)
    return chunks

def store_in_chroma(chunks):
    """
    Step 3: Convert chunks to embeddings and save to ChromaDB.
    TODO: 
    1. Initialize a ChromaDB PersistentClient pointing to DB_DIR.
    2. Create or get a collection.
    3. Add the chunks to the collection (Hint: ChromaDB has a default embedding function if you don't pass one).
    """
    client=chromadb.PersistentClient(path=DB_DIR)
    collection=client.get_or_create_collection(name="resume_data")
    chunk_ids=[f"id_{i}" for i in range(len(chunks))]
    collection.add(
        documents=chunks,
        ids=chunk_ids
    )

if __name__ == "__main__":
    print("Starting ingestion process...")
    # TODO: Tie the functions together here
    # 1. Provide the path to your file in the 'data' folder
    # 2. Call extract_text_from_file
    # 3. Call chunk_text
    # 4. Call store_in_chroma
    file_path="data/resume.pdf"
    data=extract_text_from_file(file_path)
    chunks=chunk_text(data)
    store_in_chroma(chunks)
    print("Ingestion complete!")
