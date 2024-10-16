from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton
from PyQt5.QtGui import QTextCharFormat, QColor, QTextCursor, QFont
import spacy

class ReaderTab(QWidget):
    def __init__(self):
        super().__init__()

        # Load the English NLP model from spaCy
        self.nlp = spacy.load('en_core_web_lg')

        # Create the layout for the Reader tab
        layout = QVBoxLayout()

        # Top part: Text Viewer and NER Analysis Buttons
        text_viewer_layout = QVBoxLayout()

        self.text_viewer = QTextEdit()
        text_viewer_layout.addWidget(self.text_viewer)

        ner_button_layout = QHBoxLayout()
        self.ner_labels = ['SUBJECT', 'PLACE', 'NORP', 'FAC', 'LOC', 'PRODUCT', 'DATE', 'LAW', 'QUANTITY']

        self.ner_buttons = []
        for label in self.ner_labels:
            button = QPushButton(label)
            button.clicked.connect(lambda _, l=label: self.extract_entities(l))
            ner_button_layout.addWidget(button)
            self.ner_buttons.append(button)

        text_viewer_layout.addLayout(ner_button_layout)
        layout.addLayout(text_viewer_layout)

        # Set the font size and family for the text viewer
        font_viewer = self.text_viewer.document().defaultFont()
        font_viewer.setPointSize(12)  # Adjust the value as needed
        font_viewer.setFamily("Times New Roman")
        self.text_viewer.document().setDefaultFont(font_viewer)

        # Bottom part: Extracted Entities Display
        self.extracted_entities_editor = QTextEdit()
        self.extracted_entities_editor.setFixedHeight(40)  # Set a fixed height for one line

        # Set the font size for the extracted entities editor
        font = self.extracted_entities_editor.document().defaultFont()
        font.setPointSize(11)  # Adjust the value as needed
        self.extracted_entities_editor.document().setDefaultFont(font)

        layout.addWidget(self.extracted_entities_editor)

        # Set the layout for the Reader tab
        self.setLayout(layout)

    def extract_entities(self, label):
        # Get the text from the text viewer
        text = self.text_viewer.toPlainText()

        # Replace line breaks with spaces
        text = text.replace('\n', ' ')

        # Process the text with spaCy NLP model
        doc = self.nlp(text)

        # Extract entities based on the specified label
        if label == 'SUBJECT':
            entities = set(ent.text for ent in doc.ents if ent.label_ in ['PERSON', 'ORG'])
        elif label == 'PLACE':
            entities = set(ent.text for ent in doc.ents if ent.label_ in ['GPE', 'LOC'])
        else:
            entities = set(ent.text for ent in doc.ents if ent.label_ == label)

        # Display the extracted entities in the bottom editor
        self.extracted_entities_editor.setPlainText(', '.join(entities))

        # Highlight the extracted entities in the text viewer
        self.highlight_entities(entities)

    def highlight_entities(self, entities):
        cursor = self.text_viewer.textCursor()

        # Clear any previous formatting
        cursor.select(QTextCursor.Document)
        cursor.setCharFormat(QTextCharFormat())

        # Highlight the extracted entities
        for entity in entities:
            pos = 0
            while pos != -1:
                # Find the start and end positions of the entity
                start_pos = self.text_viewer.toPlainText().find(entity, pos)
                end_pos = start_pos + len(entity)

                if start_pos != -1:
                    cursor.setPosition(start_pos)
                    cursor.setPosition(end_pos, QTextCursor.KeepAnchor)
                    char_format = QTextCharFormat()
                    char_format.setBackground(QColor("yellow"))  # Highlight background color
                    cursor.setCharFormat(char_format)
                    pos = end_pos
                else:
                    pos = -1
