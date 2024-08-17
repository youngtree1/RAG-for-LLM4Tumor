import argparse
import os
from dotenv import load_dotenv
from openai_queries.populate_db import (db_reset, populate_db)
from openai_queries.query import query_excel, query_from_cli

__version__ = "1.0.0"

def main():
    parser = argparse.ArgumentParser(prog="rag_query",
                                     description="creating and querying a document chat",
                                     epilog="OwO Happy Chatting UwU")
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s {version}'.format(version=__version__))
    parser.add_argument("-p", "--populate_db", action="store_true", help="populate database")
    parser.add_argument("--reset", action="store_true", help="Reset database")
    parser.add_argument("-x", "--excel-path", help="uses the excel path")
    parser.add_argument("-q", "--query_text", help="stores a query text")
    args = parser.parse_args()

    if args.reset:
        db_reset(chroma_root, pdf_root)
    elif args.excel_path:
        print(args.excel_path)
        query_excel(args.excel_path, chroma_root)
    elif args.query_text:
        query_from_cli(args.query_text, chroma_root)
    elif args.populate_db:
        populate_db(data_root, chroma_root)

if __name__ == "__main__":
    data_root = "data"
    pdf_root = os.path.join(data_root, "pdfs")
    excel_root = os.path.join(data_root, "excel")
    chroma_root = os.path.join(data_root, "chroma")
    template_root = os.path.join("templates")

    load_dotenv(dotenv_path=".env")
    main()
