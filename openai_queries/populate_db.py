import os
import shutil

from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

CHROMA_PATH = "data/chroma"
DATA_PATH = "data/pdf"


def load_documents():
    return PyPDFDirectoryLoader(DATA_PATH).load()


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
            current_chunk_id = 0

        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        chunk.metadata["id"] = chunk_id

    return chunks


def clear_database():
    if os.path.exists(DATA_PATH):
        shutil.rmtree(DATA_PATH)


def add_to_chroma(chunks: list[Document]):
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_function())

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
        db.persist()
    else:
        print("✅ No new documents to add")
