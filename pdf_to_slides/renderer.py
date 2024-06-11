import mistune

class SlideRenderer(mistune.HTMLRenderer):
    def __init__(self):
        super().__init__()
        self.in_frame = False

    def heading(self, text, level, **kwargs):
        frame_end = ''
        if self.in_frame:
            frame_end = '\\end{frame}\n'
        self.in_frame = True

        if level == 1:
            self.current_section = text
            self.slide_number = 1
            return f'{frame_end}\\section{{{text}}}\n\\begin{{frame}}[fragile]{{{text}}}\n'
        elif level == 2:
            self.current_section = text
            self.slide_number = 1
            return f'{frame_end}\\begin{{frame}}[fragile]{{{text}}}\n'
        else:
            return f'\\textbf{{{text}}}\\\\\n'

    def list_item(self, text, **kwargs):
        return f'\\item {text}\n'

    def list(self, body, ordered, **kwargs):
        return f'\\begin{{itemize}}\n{body}\\end{{itemize}}\n'

    def paragraph(self, text, **kwargs):
        return f'{text}\\\\\n'

    def image(self, src, alt="", title=None, **kwargs):
        return f'\\begin{{figure}}[h]\n\\includegraphics[width=\\linewidth]{{{src}}}\n\\caption{{{alt}}}\n\\end{{figure}}\n'

    def newline(self):
        return '\n'

    def finalize(self, content):
        if self.in_frame:
            content += '\\end{frame}\n'
            self.in_frame = False
        return content
