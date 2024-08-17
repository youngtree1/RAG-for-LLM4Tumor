import os
import shutil

from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_documents(data_path: str) -> list[Document]:
    return PyPDFDirectoryLoader(data_path).load()


def split_documents(documents: list[Document]):
    return RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    ).split_documents(documents)


def get_embedding_function():
    return OpenAIEmbeddings()


def calculate_chunk_ids(chunks):
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        chunk.metadata["id"] = chunk_id

    return chunks


def clear_database(db_path: str):
    if os.path.exists(db_path):
        shutil.rmtree(db_path)


def add_to_chroma(chunks: list[Document], chroma_path: str):
    db = Chroma(persist_directory=chroma_path, embedding_function=get_embedding_function())

    # Calculate Page IDs
    chunks_with_ids = calculate_chunk_ids(chunks)

    # Add or Update the documents
    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # Only add documents that don't exist in the DB.
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"👉 Adding new documents to DB: {len(new_chunks)}")
        new_chunks_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunks_ids)
    else:
        print("✅ No new documents to add")

def db_reset(db_path: str, data_path):
    print("✨ Resetting database")
    clear_database(db_path)
    print("🔍Checking for new documents...")
    populate_db(data_path, db_path)

def populate_db(data_root, chroma_root):
    print("🔍Checking for new documents...")
    documents = load_documents(data_root)
    chunks = split_documents(documents)
    add_to_chroma(chunks, chroma_root)