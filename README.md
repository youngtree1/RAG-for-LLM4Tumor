# OpenAI Queries

## Functionality
- reads single line queries
- reads excel files with single column of questions
- outputs to std and excel

## Usage
- the data 
- further insights to usage use:
```bash
❯ python rag_query.py -h
----------------------
usage: rag_query [-h] [-p] [--reset] [-x EXCEL_PATH] [-q QUERY_TEXT]

creating and querying a document chat

options:
  -h, --help            show this help message and exit
  -p, --populate_db     populate database
  --reset               Reset database
  -x EXCEL_PATH, --excel-path EXCEL_PATH
                        uses the excel path
  -q QUERY_TEXT, --query_text QUERY_TEXT
                        stores a query text

OwO Happy Chatting UwU

```
### For Open AI API users
- the program expects the OPENAI_API_KEY in an .env file
