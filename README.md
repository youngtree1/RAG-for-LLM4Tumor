# RAG for LLM4Tumor

RAG-based query system for evidence-based decision support in soft tissue sarcoma diagnostics.
Built as the technical foundation for a clinical research study at Mannheim University Hospital.

## Publication

Li C-P, Jia W-W, Chu Y, Menge F, Speer T, Reißfelder C, Hohenberger P, Jakob J, Yang C.
**Improving Accuracy and Source Transparency in Responses to Soft Tissue Sarcoma Queries Using GPT-4o Enhanced with German Evidence-Based Guidelines.**
*Oncology Research and Treatment.* 2025;48(6):351–359.
https://doi.org/10.1159/000544978

<details>
<summary>BibTeX</summary>

```bibtex
@article{Li2025,
  author    = {Li, Cheng-Peng and Jia, Wei-Wei and Chu, Yuan and Menge, Franka and Speer, Tobias and Rei{\ss}felder, Christoph and Hohenberger, Peter and Jakob, Jens and Yang, Cui},
  title     = {Improving Accuracy and Source Transparency in Responses to Soft Tissue Sarcoma Queries Using {GPT-4o} Enhanced with {German} Evidence-Based Guidelines},
  journal   = {Oncology Research and Treatment},
  year      = {2025},
  volume    = {48},
  number    = {6},
  pages     = {351--359},
  doi       = {10.1159/000544978},
  publisher = {S. Karger AG}
}
```

</details>

This system was developed to evaluate whether RAG-augmented GPT-4o responses to clinical queries about soft tissue sarcomas are more accurate and source-transparent than baseline LLM responses. The RAG pipeline ingests German evidence-based clinical guidelines (PDFs) into a Chroma vector store and uses them to ground GPT-4o answers with retrievable source references.

## Functionality

- Ingests clinical guidelines (PDF) into a Chroma vector database
- Accepts single-line queries or batch processing via Excel
- Outputs answers with source references to stdout and Excel
- Provider: OpenAI GPT-4o

## Usage

```bash
python rag_query.py --help
```

```
usage: rag_query [-h] [-v] [-p] [--reset] [-x EXCEL_PATH] [-q QUERY_TEXT]

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -p, --populate_db     populate the vector database from PDFs in data/pdfs/
  --reset               reset the vector database
  -x EXCEL_PATH         batch mode: Excel file with one query per row
  -q QUERY_TEXT         single query from stdin
```

## Setup

Place clinical guideline PDFs in `data/pdfs/`. Provide your OpenAI API key in a `.env` file:

```
OPENAI_API_KEY=sk-...
```

Populate the database before querying:

```bash
python rag_query.py --populate_db
```
