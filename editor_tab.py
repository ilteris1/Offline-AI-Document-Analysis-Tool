import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLabel, QFileDialog, QScrollArea, QMenu, QAction
from PyQt5.QtGui import QFont, QClipboard
from PyQt5.QtCore import Qt
import pandas as pd

class TagWidget(QWidget):
    def __init__(self, tag, editor_tab):
        super().__init__()
        self.tag = tag
        self.editor_tab = editor_tab
        self.initUI()

    def initUI(self):
        tag_label = QLabel(self.tag)
        tag_label.setStyleSheet("background-color: #5b92e5; color: white; padding: 8px; border-radius: 4px;")

        # Increase the font size
        font = QFont()
        font.setPointSize(11)  # Adjust the font size as needed
        tag_label.setFont(font)

        tag_layout = QHBoxLayout()
        tag_layout.addWidget(tag_label)
        self.setLayout(tag_layout)

        # Set a fixed height for the tag widget
        self.setFixedHeight(75)  # Adjust the height as needed

        # Create a context menu
        self.context_menu = QMenu(self)
        copy_action = QAction("Copy", self)
        copy_action.triggered.connect(self.copyToClipboard)
        delete_action = QAction("Delete", self)
        delete_action.triggered.connect(self.deleteTag)
        delete_all_action = QAction("Delete All", self)
        delete_all_action.triggered.connect(self.deleteAllTags)
        self.context_menu.addActions([copy_action, delete_action, delete_all_action])

    def contextMenuEvent(self, event):
        # Show the context menu at the cursor position
        self.context_menu.exec_(event.globalPos())

    def copyToClipboard(self):
        # Copy the tag text to the clipboard
        clipboard = QApplication.clipboard()
        clipboard.setText(self.tag, QClipboard.Clipboard)

    def deleteTag(self):
        # Delete the tag from the UI
        self.setParent(None)

        # Delete the tag from the CSV file and save it
        if self.editor_tab.csv_file:
            df = pd.read_csv(self.editor_tab.csv_file)

            # Find the corresponding row in the CSV
            selected_rows = df[df.iloc[:, 1].str.contains(self.tag, na=False, regex=False)].index

            # Check if the tag exists in the DataFrame
            if not selected_rows.empty:
                # Remove the tag from the DataFrame
                df[df.columns[1]] = df.apply(
                    lambda row: self.process_tags(row[df.columns[1]], self.tag),
                    axis=1
                )

                # Save the updated DataFrame to the CSV file
                df.to_csv(self.editor_tab.csv_file, index=False)

    def process_tags(self, tags_str, tag_to_remove):
        # Custom function to handle NaN values and remove the specified tag
        if pd.notna(tags_str):
            tags = [tag.strip() for tag in tags_str.split(', ')]
            tags = [tag for tag in tags if tag != tag_to_remove]
            return ', '.join(tags)
        return tags_str

    def deleteAllTags(self):
        # Delete all occurrences of the tag from the UI and CSV file
        self.setParent(None)

        if self.editor_tab.csv_file:
            df = pd.read_csv(self.editor_tab.csv_file)

            # Remove the tag from all rows
            df[df.columns[1]] = df.apply(
                lambda row: self.process_tags(row[df.columns[1]], self.tag),
                axis=1
            )

            # Save the updated DataFrame to the CSV file
            df.to_csv(self.editor_tab.csv_file, index=False)


class EditorTab(QWidget):
    def __init__(self):
        super().__init__()

        self.csv_file = None  # Initialize the csv_file attribute

        self.initUI()

    def initUI(self):
        # Create main layout
        main_layout = QHBoxLayout()

        # Create left sidebar (QListWidget)
        self.list_widget = QListWidget()
        self.list_widget.setMaximumWidth(150)  # Set maximum width for the left sidebar
        self.list_widget.itemClicked.connect(self.showContent)

        # Set up a vertical layout for the left sidebar
        left_sidebar_layout = QVBoxLayout()
        left_sidebar_layout.addWidget(QPushButton('Upload CSV', clicked=self.uploadCSV))
        left_sidebar_layout.addWidget(self.list_widget)

        # Create a scroll area for the right side content (Container for tag widgets)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(1)  # Always show horizontal scroll bar
        self.tags_container = QWidget()
        tags_layout = QVBoxLayout(self.tags_container)
        self.scroll_area.setWidget(self.tags_container)

        # Add the left sidebar layout to the main layout
        main_layout.addLayout(left_sidebar_layout)

        # Add the scroll area to the main layout
        main_layout.addWidget(self.scroll_area)

        # Set main layout for the EditorTab
        self.setLayout(main_layout)

        self.setWindowTitle('CSV Editor')

    def uploadCSV(self):
        # Open a file dialog to select a CSV file
        file_dialog = QFileDialog()
        csv_file, _ = file_dialog.getOpenFileName(self, 'Open CSV File', '', 'CSV Files (*.csv)')

        if csv_file:
            # Read the CSV file using pandas
            df = pd.read_csv(csv_file)

            # Populate the left sidebar with the first column values
            self.list_widget.clear()
            self.list_widget.addItems(df.iloc[:, 0].astype(str))

            # Set the csv_file attribute
            self.csv_file = csv_file

    def showContent(self, item):
        # Get the selected item's text
        selected_text = item.text()

        # Check if csv_file is defined
        if self.csv_file:
            # Read the CSV file using pandas
            df = pd.read_csv(self.csv_file)

            # Find the corresponding row in the CSV and display the second column in the right-side container
            selected_row = df[df.iloc[:, 0] == selected_text]

            if not selected_row.empty:
                # Check if the second column is not empty or NaN
                if pd.notna(selected_row.iloc[0, 1]) and selected_row.iloc[0, 1] != '':
                    second_column_value = selected_row.iloc[0, 1]

                    # Process comma-separated values and create a TagWidget for each tag
                    tags = [tag.strip() for tag in second_column_value.split(', ')]
                    tag_widgets = [TagWidget(tag, self) for tag in tags]

                    # Clear existing tag widgets in the container
                    for i in reversed(range(self.tags_container.layout().count())):
                        self.tags_container.layout().itemAt(i).widget().setParent(None)

                    # Add the new tag widgets to the container
                    for tag_widget in tag_widgets:
                        self.tags_container.layout().addWidget(tag_widget)
                else:
                    # You can choose to display a message or do nothing
                    pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor_tab = EditorTab()
    editor_tab.show()
    sys.exit(app.exec_())
