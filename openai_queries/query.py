import pandas as pd
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAI
from tqdm import tqdm

from .helpers import get_questions_from_xlsx
from openai_queries.populate_db import get_embedding_function

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def query_rag(query_text: str, chroma_root) -> dict:
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

def query_excel(excel_path, chroma_root) -> None:
    out_path = excel_path.split('.')[0]
    query_series = tqdm(get_questions_from_xlsx(excel_path))
    response_gen = map(lambda x: query_rag(x, chroma_root), query_series)
    df = pd.DataFrame.from_records(response_gen)
    df.to_excel(out_path + '_answers.xlsx', index=False)

def query_from_cli(query_text, chroma_root) -> None:
    response_dict = query_rag(query_text=query_text, chroma_root=chroma_root,)
    print('Question:\n', response_dict.get('question'))
    print('-----------------------------')
    print('Response:\n', response_dict.get('response'))
    print('-----------------------------')
    print('Sources:\n', response_dict.get('sources'))