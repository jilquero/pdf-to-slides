import mistune
from ..renderer import SlideRenderer

def markdown_to_latex(md_file, output_file):
    with open(md_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    renderer = SlideRenderer()
    markdown = mistune.create_markdown(renderer=renderer)
    latex_content = markdown(markdown_content)

    # Dodanie preambuły LaTeX do pliku
    latex_document = r"""
\documentclass{beamer}
\usepackage{graphicx}
\begin{document}
""" + latex_content + r"""
\end{document}
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(latex_document)
