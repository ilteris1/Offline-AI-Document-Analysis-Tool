import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QTableWidget, QSizePolicy, QPushButton, QFileDialog, QTableWidgetItem, QMenu, QAction
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QUrl
from pyvis.network import Network
import pandas as pd
import shutil

class NetworkMapTab(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the layout
        main_layout = QHBoxLayout()

        # Left part: Spreadsheet View
        spreadsheet_layout = QVBoxLayout()
        spreadsheet_label = QLabel("Spreadsheet View")
        self.spreadsheet_view = QTableWidget(self)
        spreadsheet_layout.addWidget(spreadsheet_label)
        spreadsheet_layout.addWidget(self.spreadsheet_view)

        # Add a submit button
        self.submit_button = QPushButton("Submit")
        spreadsheet_layout.addWidget(self.submit_button)

        # Add an upload CSV button
        self.upload_button = QPushButton("Upload CSV")
        spreadsheet_layout.addWidget(self.upload_button)

        main_layout.addLayout(spreadsheet_layout)

        # Right part: Data Visualization
        visualization_layout = QVBoxLayout()
        visualization_label = QLabel("Data Visualization")
        self.visualization_webview = QWebEngineView(self)  # Use QWebEngineView for displaying HTML content
        self.visualization_webview.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        visualization_layout.addWidget(visualization_label)
        visualization_layout.addWidget(self.visualization_webview)
        main_layout.addLayout(visualization_layout)

        self.setLayout(main_layout)

        # Initialize the spreadsheet view
        self.initSpreadsheetView(self.spreadsheet_view)

        # Connect the signals
        self.submit_button.clicked.connect(self.submitData)
        self.upload_button.clicked.connect(self.uploadCSV)

        # Additional initialization for Pyvis Network
        self.net = Network(height="1024px", width="100%", bgcolor="#ffffff", font_color="black", select_menu=True)

        # Create a custom context menu
        self.custom_context_menu = QMenu(self.visualization_webview)

        # Add "Save Page" action
        save_page_action = QAction("Save Page", self)
        save_page_action.triggered.connect(self.savePage)
        self.custom_context_menu.addAction(save_page_action)

        # Set the context menu policy for the web view
        self.visualization_webview.setContextMenuPolicy(Qt.CustomContextMenu)
        self.visualization_webview.customContextMenuRequested.connect(self.showContextMenu)

    def showContextMenu(self, pos):
        # Show the custom context menu at the specified position
        self.custom_context_menu.exec_(self.visualization_webview.mapToGlobal(pos))

    def savePage(self):
        # Ask the user to choose a directory to save the HTML file
        directory = QFileDialog.getExistingDirectory(self, "Select Directory to Save HTML", "")
        if directory:
            # Copy the existing visualization.html file to the chosen directory
            source_path = "visualization.html"
            destination_path = os.path.join(directory, "network_map.html")

            try:
                shutil.copy(source_path, destination_path)
                print(f"Page saved successfully: {destination_path}")
            except Exception as e:
                print(f"Error copying file: {e}")

    def getHtmlContent(self):
        # Get the current HTML content of the web view
        result = None
        self.visualization_webview.page().toHtml(lambda data: self.getHtmlContentCallback(data, result))
        return result

    def getHtmlContentCallback(self, data, result):
        # Callback function to set the HTML content
        result = data

    def initSpreadsheetView(self, spreadsheet_view):
        # Set the column count and headers
        column_count = 11  # Set the desired number of columns
        spreadsheet_view.setColumnCount(column_count)
        headers = ['Main Node'] + [f'Node {i + 1}' for i in range(column_count - 1)]
        spreadsheet_view.setHorizontalHeaderLabels(headers)

        # Set the row count (initial)
        row_count = 2000  # Set the desired number of rows
        spreadsheet_view.setRowCount(row_count)

        # Enable item changes
        spreadsheet_view.setEditTriggers(QTableWidget.AllEditTriggers)

    def updateVisualization(self):
        
        # Retrieve data from the spreadsheet view
        main_nodes = set()
        edges = set()
        colors = ["blue", "red", "green", "purple", "orange", "brown", "pink", "gray", "cyan", "magenta"]

        for row in range(self.spreadsheet_view.rowCount()):
            unique_value_item = self.spreadsheet_view.item(row, 0)
            if unique_value_item:
                unique_value = unique_value_item.text().strip()
                if unique_value:
                    main_nodes.add(unique_value)

                    # Add main node with a unique color
                    self.net.add_node(unique_value, label=unique_value, color="blue", size=25)

                    # Iterate over child nodes (columns 1 and onward)
                    for col in range(1, self.spreadsheet_view.columnCount()):
                        child_node_item = self.spreadsheet_view.item(row, col)
                        if child_node_item:
                            child_nodes_text = child_node_item.text().strip()
                            if child_nodes_text:
                                # Split child nodes based on comma and add each as a separate node
                                child_nodes = [node.strip() for node in child_nodes_text.split(",")]

                                # Add child nodes with the same color as the column
                                color = colors[col % len(colors)]
                                for child_node in child_nodes:
                                    self.net.add_node(child_node, label=child_node, color=color, size=15)
                                    edges.add((unique_value, child_node, color))

        # Add edges, checking if nodes exist
        for edge in edges:
            source, target, color = edge[0], edge[1], edge[2]
            if source not in self.net.get_nodes():
                self.net.add_node(source, label=source, color="blue", size=25)
            if target not in self.net.get_nodes():
                self.net.add_node(target, label=target, color=color, size=15)
            self.net.add_edge(source, target, color=color)

        # Render to HTML
        self.net.show_buttons(filter_=['physics'])
        html_path = "visualization.html"
        self.net.save_graph(html_path)

        # Display HTML in QWebEngineView
        with open(html_path, "r", encoding="utf-8") as html_file:
            html = html_file.read()

        self.visualization_webview.setHtml(html)

    def submitData(self):
        # Recreate the Pyvis Network object
        self.net = Network(height="1024px", width="100%", bgcolor="#ffffff", font_color="black")
        # Call the visualization update method when the submit button is clicked
        self.updateVisualization()

    def uploadCSV(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        filePath, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)

        if filePath:
            # Read CSV and update the table
            self.df = pd.read_csv(filePath)
            self.spreadsheet_view.clear()
            self.initSpreadsheetView(self.spreadsheet_view)
            self.spreadsheet_view.setRowCount(len(self.df))
            self.spreadsheet_view.setColumnCount(len(self.df.columns) + 1)
            for row in range(len(self.df)):
                # Set main node value in the first column
                main_node_item = QTableWidgetItem(str(self.df.iloc[row, 0]))
                self.spreadsheet_view.setItem(row, 0, main_node_item)

                # Set child node values in the next columns
                for col in range(1, len(self.df.columns)):
                    child_node_item = QTableWidgetItem(str(self.df.iloc[row, col]))
                    self.spreadsheet_view.setItem(row, col, child_node_item)

    def showContextMenu(self, pos):
        # Show the custom context menu at the specified position
        self.custom_context_menu.exec_(self.visualization_webview.mapToGlobal(pos))

    def savePage(self):
        # Ask the user to choose a directory to save the HTML file
        directory = QFileDialog.getExistingDirectory(self, "Select Directory to Save HTML", "")
        if directory:
            # Copy the existing visualization.html file to the chosen directory
            source_path = "visualization.html"
            destination_path = os.path.join(directory, "network_map.html")

            try:
                shutil.copy(source_path, destination_path)
                print(f"Page saved successfully: {destination_path}")
            except Exception as e:
                print(f"Error copying file: {e}")


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = NetworkMapTab()
    window.show()
    sys.exit(app.exec_())
