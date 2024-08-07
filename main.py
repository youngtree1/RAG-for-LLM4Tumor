import argparse

from openai_queries.populate_db import (clear_database, load_documents,
                                        split_documents, add_to_chroma)


# Folders


# populate the db
## load the pdf documents


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset database")
    args = parser.parse_args()

    if args.reset:
        print("✨ Resetting database")
        clear_database()

    documents = load_documents()
    chunks = split_documents(documents)
    add_to_chroma(chunks)


if __name__ == "__main__":
    main()
