# Offline AI Document Analysis Tool
This is an Offline AI Document Analysis Tool with Natural Language Processing, search, and data visualization functionalities. The tool comprises six tabs to address specific needs within document management, analysis, and visualization. Supported file formats for document analysis include:

- PDF
- DOCX
- TXT

The main purpose of developing this tool was to analyze documents via AI in an offline setting, allowing it to function without an internet connection. You are welcome to edit and improve this tool.

### Installation & Running Instructions

1. Install the required packages:
```python
`pip install -r requirements.txt`
```

2. Download the English language model for SpaCy:
```python
python -m spacy download en_core_web_lg
```

3. Run the Application:
```python
python main.py
```

### Deployment Instructions

To deploy the application as a standalone executable, you can use PyInstaller with the following command:
```python
pyinstaller -D -w --collect-all pyvis --additional-hooks-dir=. main.py
```

## Preview

Note: The open source documents analyzed in the preview were retrieved from [https://main.un.org/securitycouncil/en/sanctions/1267/aq_sanctions_list/summaries](https://main.un.org/securitycouncil/en/sanctions/1267/aq_sanctions_list/summaries "https://main.un.org/securitycouncil/en/sanctions/1267/aq_sanctions_list/summaries") in December 2023. 

