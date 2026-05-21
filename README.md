# RAG Resume Chatbot
## Overview
This project implements a Retrieval-Augmented Generation (RAG) system that creates an AI-powered chat interface for querying resume documents. The system combines ChromaDB for vector storage, Google Gemini for AI responses, and Streamlit for the web interface. The process involves ingesting PDF resumes, chunking the text into manageable segments, storing them in a vector database, and using semantic search to retrieve relevant context for answering user questions about the resume.

## Requirements
To run this project, you'll need a machine with internet connectivity for API access and sufficient memory for vector database operations.

### Software
- Python 3.9 or higher
- Streamlit web framework
- ChromaDB vector database
- Google Generative AI (Gemini)
- Sentence Transformers
- PyPDF2 for PDF processing
- python-dotenv for environment management

You can install the required Python packages by running the following command:

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install chromadb sentence-transformers google-generativeai streamlit python-dotenv PyPDF2
```

### Hardware Requirements
- Minimum 4GB RAM (8GB recommended)
- Internet connection for Google Gemini API
- Sufficient storage for vector database (~50-100MB depending on resume size)

## Installation

### 1. Download the Code
Download or clone the project files to your local machine, including:
- `app.py` - Main Streamlit application
- `ingest.py` - Resume ingestion and vector database setup
- `rag_logic.py` - RAG logic and AI integration
- `requirements.txt` - Python dependencies
- `.env` - Environment configuration file

### 2. Install Dependencies
Open a terminal or command prompt, navigate to the project directory, and run:

```bash
pip install -r requirements.txt
```

### 3. API Key Setup
Create a `.env` file in the project directory and add your Google Gemini API key:

```
GEMINI_API_KEY=your_api_key_here
```

Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey).

### 4. Resume Setup
Place your resume PDF file in the `data/` directory. The default expected filename is `resume.pdf`. You can modify this in `ingest.py` if needed.

### 5. Ingest the Resume
Run the ingestion script to process your resume and create the vector database:

```bash
python ingest.py
```

This will extract text from the PDF, chunk it, and store it in ChromaDB.

## Usage

### Web Application
Run the Streamlit application from your terminal:

```bash
streamlit run app.py
```

The application will start on `http://localhost:8501` by default. Open this URL in your web browser to access the resume chat interface.

### Using the Interface
1. **Ask Questions**: Type questions about the resume in the chat input
2. **View Responses**: The AI will search the resume and provide relevant answers
3. **Chat History**: Maintain context across multiple questions in the session

### Command Line Interface
For testing and development, you can run the RAG logic directly:

```bash
python rag_logic.py
```

This provides a simple command-line chat interface for querying the resume.

## Features

### Intelligent Retrieval
- **Semantic Search**: Uses ChromaDB with sentence transformers for context-aware retrieval
- **Chunk-based Storage**: Splits resume into overlapping chunks for better context preservation
- **Vector Embeddings**: Converts text to embeddings for efficient similarity search

### AI-Powered Responses
- **Context-Aware Answers**: Uses Google Gemini to generate responses based on retrieved context
- **Chat History**: Maintains conversation context across multiple questions
- **Fallback Handling**: Gracefully handles questions when information is not in the resume

### Flexible Ingestion
- **PDF Support**: Extracts text from PDF documents using PyPDF2
- **Configurable Chunking**: Adjustable chunk size and overlap parameters
- **Persistent Storage**: Vector database persists across sessions

### User-Friendly Interface
- **Streamlit UI**: Clean, modern web interface
- **Real-time Responses**: Fast query processing and response generation
- **Session Management**: Maintains chat history within a session

## Troubleshooting

### Import Errors
If you see ImportError, make sure all dependencies are installed correctly:
```bash
pip install -r requirements.txt
```

### API Key Issues
- Ensure `GEMINI_API_KEY` is set in your `.env` file
- Verify your API key is valid and active
- Check your internet connection for API access

### Vector Database Issues
- Ensure you've run `python ingest.py` before querying
- Check that the `vector_db/` directory exists and contains data
- If issues persist, delete the `vector_db/` directory and re-run ingestion

### PDF Processing Errors
- Ensure your resume PDF is in the `data/` directory
- Verify the PDF is not password-protected
- Check that the PDF contains extractable text (not scanned images)

### Memory Issues
- Large resumes may cause memory errors during ingestion
- Reduce chunk size in `ingest.py` if needed
- Close other applications to free up RAM

### Streamlit Issues
- If the interface doesn't load, try clearing the Streamlit cache:
  ```bash
  streamlit cache clear
  ```
- Ensure you're running the command from the correct directory
- Check that port 8501 is not already in use

## API Reference

### Core Functions

#### `ingest.py`
- `extract_text_from_file(file_path)`: Extracts text from PDF files
- `chunk_text(text, chunk_size=500, overlap=50)`: Splits text into overlapping chunks
- `store_in_chroma(chunks)`: Stores chunks in ChromaDB vector database

#### `rag_logic.py`
- `search_chroma(query, n_results=3)`: Searches vector database for relevant chunks
- `generate_answer(query, context_chunks, chat_history="")`: Generates AI response using Gemini
- `ask_resume(query, chat_history="")`: Main function that ties retrieval and generation together

## Configuration

### Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key (required)

### Customization
- Modify `chunk_size` and `overlap` in `ingest.py` for different chunking strategies
- Adjust `n_results` in `rag_logic.py` to retrieve more or fewer context chunks
- Change the model in `rag_logic.py` (currently `gemini-2.5-flash`) to use different Gemini models
- Customize the prompt template in `generate_answer()` for different response styles

### File Paths
- `DATA_DIR`: Directory containing resume PDF (default: "data")
- `DB_DIR`: Directory for vector database (default: "vector_db")

## License
This project is licensed under the MIT License.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## Privacy and Security
- This tool processes resume data locally; the vector database is stored on your machine
- API calls to Google Gemini are sent over HTTPS; ensure you trust Google's privacy policy
- Resume data is not stored permanently on external servers
- Ensure you have permission to process and query the resume data
- Keep your API key secure and never commit it to version control
