import sys
import re
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QListWidget, QPushButton, QFileDialog,
    QMessageBox, QListWidgetItem
)

class CustomTexGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom LaTeX Report Generator")
        self.setGeometry(200, 100, 600, 400)

        self.layout = QVBoxLayout()
        self.listWidget = QListWidget()
        self.listWidget.setSelectionMode(QListWidget.MultiSelection)

        self.loadButton = QPushButton("Load .tex File")
        self.generateButton = QPushButton("Generate PDF")

        self.loadButton.clicked.connect(self.load_tex)
        self.generateButton.clicked.connect(self.generate_pdf)

        self.layout.addWidget(self.loadButton)
        self.layout.addWidget(self.listWidget)
        self.layout.addWidget(self.generateButton)
        self.setLayout(self.layout)

        self.components = []
        self.original_path = ""

    def load_tex(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open LaTeX File", "", "TeX Files (*.tex)")
        if file_path:
            self.original_path = file_path
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.extract_components(content)

    def extract_components(self, content):
        pattern = r"(\\section\{.*?\}|\\subsection\{.*?\})"
        parts = re.split(pattern, content)
        self.components = []
        self.listWidget.clear()

        i = 1
        while i < len(parts):
            heading = parts[i].strip()
            body = parts[i + 1].strip() if i + 1 < len(parts) else ""
            self.components.append((heading, body))
            self.listWidget.addItem(QListWidgetItem(heading))
            i += 2

    def generate_pdf(self):
        selected_items = self.listWidget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select at least one component.")
            return

        content = [
             r"\documentclass{article}",
             r"\usepackage[utf8]{inputenc}",
             r"\usepackage{tabularx}",
             r"\usepackage{array}",
             r"\usepackage{longtable}",
             r"\usepackage{needspace}",       
             r"\usepackage[table]{xcolor}",
             r"\usepackage{colortbl}",
             r"\definecolor{OsdagGreen}{RGB}{0,100,0}",
             r"\definecolor{OsdagRed}{RGB}{180,0,0}",
             r"\begin{document}"
        ]

        for item in selected_items:
            index = self.listWidget.row(item)
            heading, body = self.components[index]
            content.append(heading)
            content.append(body)

        content.append(r"\end{document}")

        with open("custom_report.tex", "w", encoding='utf-8') as f:
            f.write("\n\n".join(content))

        try:
            subprocess.run([
    r"C:\Users\aryan\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe",
    "custom_report.tex"
    ], check=True)

            QMessageBox.information(self, "Success", "custom_report.pdf generated.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"PDF generation failed:\n{str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomTexGUI()
    window.show()
    sys.exit(app.exec_())
