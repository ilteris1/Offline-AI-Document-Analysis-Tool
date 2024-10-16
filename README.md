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

![resim](https://github.com/user-attachments/assets/387cd15d-69ab-4f2e-bcd3-0e48ff178cf2)
![resim](https://github.com/user-attachments/assets/dd1231bd-1eda-4658-b044-1ea685a86d02)
![resim](https://github.com/user-attachments/assets/449de39a-714a-487a-944c-b856d6eaaf5a)
![resim](https://github.com/user-attachments/assets/bcb33e49-1062-43f4-b253-8a2d29c4759d)
![resim](https://github.com/user-attachments/assets/4fa845ac-e79e-425e-9948-6869ee26f4f1)
![resim](https://github.com/user-attachments/assets/42cb8878-d3c9-4170-bc9d-0159720c1020)
![resim](https://github.com/user-attachments/assets/6a48202b-e8e0-45ed-8560-1706303da9b6)
![resim](https://github.com/user-attachments/assets/2f27c699-1be3-42e5-a8cf-b7d5914feb11)
![resim](https://github.com/user-attachments/assets/fc077442-7e80-4114-beac-10d7865a78d5)






