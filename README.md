# OpenAI Queries

## Functionality
- reads single line queries
- reads Excel files with single column of questions
- outputs to stdout and excel

## Usage
for further insights to usage use:
```bash
❯ python rag_query.py --help
usage: rag_query [-h] [-v] [-p] [--reset] [-x EXCEL_PATH] [-q QUERY_TEXT]

creating and querying a document chat

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -p, --populate_db     populates database
  --reset               Resets database
  -x EXCEL_PATH, --excel-path EXCEL_PATH
                        uses the excel file to create a series of queries
  -q QUERY_TEXT, --query_text QUERY_TEXT
                        uses a line of text from stdin as query
```
### For Open AI API users
- the program expects the OPENAI_API_KEY in an .env file
