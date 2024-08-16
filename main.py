import argparse
import os

import pandas as pd
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAI
from openai_queries.populate_db import (clear_database, load_documents,
                                        split_documents, add_to_chroma, get_embedding_function)

# Folders
data_root = "data"
pdf_root = os.path.join(data_root, "pdfs")
excel_root = os.path.join(data_root, "excel")
chroma_root = os.path.join(data_root, "chroma")

# helper function

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def get_questions_from_xlsx(excel_path: str):
    series = pd.read_excel(excel_path, header=None).iloc[:, 0]
    return series


def query_rag(query_text: str) -> dict:
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=chroma_root, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    # print(prompt)

    model = OpenAI()
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]

    return {'question': query_text, 'response': response_text, 'sources': sources}


# populate the db
# load the pdf documents
documents = load_documents(data_root)
chunks = split_documents(documents)
add_to_chroma(chunks, chroma_root)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--populate_db", action="store_true", help="populate database")
    parser.add_argument("--reset", action="store_true", help="Reset database")
    parser.add_argument("-x", "--excel-path", help="uses the excel path")
    parser.add_argument("-q", "--query_text", help="stores a query text")
    args = parser.parse_args()

    if args.reset:
        print("✨ Resetting database")
        clear_database(chroma_root)
    elif args.excel_path:
        excel_path = args.excel_path.split('.')[0]
        query_series = get_questions_from_xlsx(args.excel_path)
        response_gen = map(query_rag, query_series)
        df = pd.DataFrame.from_records(response_gen)
        df.to_excel(excel_path + '_answers.xlsx', index=False)
    elif args.query_text:
        query_rag(query_text=args.query_text)


if __name__ == "__main__":
    main()
