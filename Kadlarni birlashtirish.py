import os
from tkinter import Tk, filedialog, Text, Button, Scrollbar, messagebox
from bs4 import BeautifulSoup
from docx import Document
from pdfminer.high_level import extract_text


# HTML, CSS va JavaScript kodlarini ajratish uchun yordamchi funktsiyalar
def extract_html_code(content):
    """HTML kodini ajratib olish."""
    soup = BeautifulSoup(content, 'html.parser')
    html_code = str(soup.prettify())
    return html_code


def extract_css_code(content):
    """CSS kodini ajratib olish."""
    css_code = ''
    if '<style>' in content:
        start = content.find('<style>') + len('<style>')
        end = content.find('</style>')
        if start != -1 and end != -1:
            css_code = content[start:end].strip()
    return css_code


def extract_js_code(content):
    """JavaScript kodini ajratib olish."""
    js_code = ''
    if '<script>' in content:
        start = content.find('<script>') + len('<script>')
        end = content.find('</script>')
        if start != -1 and end != -1:
            js_code = content[start:end].strip()
    return js_code


def extract_from_pdf(pdf_path):
    """PDF faylidan matnni olish."""
    return extract_text(pdf_path)


def extract_from_docx(docx_path):
    """DOCX faylidan matnni olish."""
    doc = Document(docx_path)
    return '\n'.join([para.text for para in doc.paragraphs])


def extract_from_txt(txt_path):
    """TXT faylidan matnni olish."""
    with open(txt_path, 'r', encoding='utf-8') as file:
        return file.read()


def extract_code_from_file(file_path):
    """Faylni tahlil qilish va HTML, CSS, JS kodlarini ajratish."""
    extension = os.path.splitext(file_path)[-1].lower()
    content = ''

    if extension == '.html':
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    elif extension == '.pdf':
        content = extract_from_pdf(file_path)
    elif extension == '.docx':
        content = extract_from_docx(file_path)
    elif extension == '.txt':
        content = extract_from_txt(file_path)
    else:
        raise ValueError("Fayl formati qo'llab-quvvatlanmaydi.")

    html_code = extract_html_code(content)
    css_code = extract_css_code(content)
    js_code = extract_js_code(content)

    return html_code, css_code, js_code


# GUI yordamida interfeys yaratish
class CodeExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Extractor")
        self.root.geometry("600x400")

        self.file_content_text = Text(self.root, wrap="word", width=70, height=15)
        self.file_content_text.pack(pady=20)

        self.scrollbar = Scrollbar(self.root, command=self.file_content_text.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.file_content_text.config(yscrollcommand=self.scrollbar.set)

        self.upload_button = Button(self.root, text="Fayllarni yuklash", command=self.upload_files)
        self.upload_button.pack(pady=10)

        self.save_button = Button(self.root, text="Natijalarni saqlash", command=self.save_results, state="disabled")
        self.save_button.pack(pady=10)

        self.html_code = ''
        self.css_code = ''
        self.js_code = ''

    def upload_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("All files", "*.*")])
        if file_paths:
            try:
                self.html_code = ''
                self.css_code = ''
                self.js_code = ''

                for file_path in file_paths:
                    html, css, js = extract_code_from_file(file_path)
                    self.html_code += html
                    self.css_code += css
                    self.js_code += js

                self.show_results(self.html_code, self.css_code, self.js_code)
                self.save_button.config(state="normal")
            except Exception as e:
                messagebox.showerror("Xato", f"Fayllarni tahlil qilishda xatolik yuz berdi: {str(e)}")

    def show_results(self, html_code, css_code, js_code):
        """Kodlarni interfeysta ko'rsatish."""
        result_text = ''
        if html_code:
            result_text += "HTML KOD:\n" + html_code + "\n\n"
        if css_code:
            result_text += "CSS KOD:\n" + css_code + "\n\n"
        if js_code:
            result_text += "JavaScript KOD:\n" + js_code + "\n\n"

        if not result_text:
            result_text = "Fayllarda HTML, CSS yoki JavaScript topilmadi."

        self.file_content_text.delete(1.0, "end")
        self.file_content_text.insert("insert", result_text)

    def save_results(self):
        """Natijalarni faylga saqlash."""
        save_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"), ("HTML files", "*.html"),
                                                            ("CSS files", "*.css"), ("JavaScript files", "*.js")])
        if save_path:
            try:
                content = self.file_content_text.get(1.0, "end-1c")
                with open(save_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                messagebox.showinfo("Saqlash", "Natijalar muvaffaqiyatli saqlandi!")
            except Exception as e:
                messagebox.showerror("Xato", f"Natijalarni saqlashda xatolik yuz berdi: {str(e)}")


# Asosiy dastur
if __name__ == "__main__":
    root = Tk()
    app = CodeExtractorApp(root)
    root.mainloop()


