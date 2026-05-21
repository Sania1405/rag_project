import google.generativeai as genai
import chromadb
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

DB_DIR = "vector_db"

def search_chroma(query, n_results=3):
    """
    Step 1: Search the vector database.
    TODO: 
    1. Initialize ChromaDB client (just like in ingest.py).
    2. Get the 'resume_data' collection.
    3. Use collection.query(query_texts=[query], n_results=n_results) 
    4. Return the retrieved documents (they will be in a list).
    """
    client = chromadb.PersistentClient(path=DB_DIR)
    collection = client.get_collection(name="resume_data")
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    # results['documents'] returns a list of lists: [['doc1', 'doc2']]
    return results['documents'][0]

def generate_answer(query, context_chunks, chat_history=""):
    """
    Step 2: Send the query, context, and history to Gemini.
    """
    # 1. Combine the list of text chunks into one big string
    context = "\n\n".join(context_chunks)
    
    # 2. Create the prompt instruction for Gemini
    prompt = f"""
    You are an AI assistant answering questions based on my resume.
    Use ONLY the following context to answer the user's question. 
    If the answer is not in the context, say "I don't have enough information to answer that based on the resume."

    Chat History (Use this to understand context if needed):
    {chat_history}

    Context:
    {context}

    Question:
    {query}

    Answer:
    """
    
    # 3. Initialize the Gemini model
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # 4. Generate and return the response
    response = model.generate_content(prompt)
    return response.text

def ask_resume(query, chat_history=""):
    """
    Step 3: Tie it together!
    """
    # 1. Retrieve the most relevant chunks from the database
    context_chunks = search_chroma(query)
    
    # 2. Pass the query, history, and retrieved chunks to Gemini
    answer = generate_answer(query, context_chunks, chat_history)
    
    # 3. Return the final AI-generated answer
    return answer
    
if __name__ == "__main__":
    print("Welcome to Sania's Resume Chatbot! (Type 'quit' to exit)")
    history = ""
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
            
        answer = ask_resume(user_input, history)
        print(f"\nSania's Assistant: {answer}")
        
        # Save this interaction to our memory variable
        history += f"User: {user_input}\nAssistant: {answer}\n\n"
