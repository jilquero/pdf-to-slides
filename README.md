![image](https://github.com/RobertNeat/RobertNeat/assets/47086490/9125fa28-9979-4f79-81c0-ad74aa65d46d)

# LaTeX Presentation Generator

[![Python](https://img.shields.io/badge/python-3.12-3776AB?logo=python)](https://www.python.org/)
[![marker-pdf](https://img.shields.io/badge/marker--pdf-0.2.13-8A2BE2)](https://pypi.org/project/marker-pdf/)
[![typer](https://img.shields.io/badge/typer-0.12.3-007ACC?logo=typer)](https://pypi.org/project/typer/)
[![markdown-to-json](https://img.shields.io/badge/markdown--to--json-2.1.1-000000?logo=markdown)](https://pypi.org/project/markdown-to-json/)
[![spacy](https://img.shields.io/badge/spacy-3.7.5-09A3D5?logo=spacy)](https://pypi.org/project/spacy/)
[![pytextrank](https://img.shields.io/badge/pytextrank-3.3.0-FF4500)](https://pypi.org/project/pytextrank/)
[![jinja2](https://img.shields.io/badge/jinja2-3.1.4-B41789?logo=jinja)](https://pypi.org/project/Jinja2/)
[![babel](https://img.shields.io/badge/babel-2.15.0-F9DC3E?logo=babel)](https://pypi.org/project/Babel/)

## Project Overview

This project provides a tool for generating LaTeX presentations saved as PDF file from Markdown file or existing PDF document. It streamlines the process of creating professional presentations by leveraging the power of LaTeX and the simplicity of Markdown and power of OpenAI platform.

## Features

- Convert Markdown files to LaTeX presentations
- Merge existing PDF documents into a single presentation
- Customize templates for different presentation styles
- Easy-to-use command-line interface

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Basic Conversion](#basic-conversion)
  - [Custom Templates](#custom-templates)
- [Configuration](#configuration)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Installation

Project dependencies:

- [Python 12.4.0](https://www.python.org/downloads/release/python-3120/),
- [Poetry](https://python-poetry.org/docs/) (best to install using [PipX](https://pipx.pypa.io/stable/installation/)),

To after installing python and poetry unzip the source files and use following commands in project main directory:

```ps

PS C:\pdf-to-slides> poetry shell
Spawning shell within C:\virtualenvs\pdf-to-slides-wM9OptYn-py3.12
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

Install the latest PowerShell for new features and improvements! https://aka.ms/PSWindows

(pdf-to-slides-py3.12) PS C:\pdf-to-slides> poetry install
Installing dependencies from lock file

No dependencies to install or update

Installing the current project: pdf-to-slides (0.1.0)
(pdf-to-slides-py3.12) PS C:\pdf-to-slides> pts <command>

```

Make sure that you have added your LaTex interpreter to the system PATH and you have installed all the required packages such as Polish - to ensure that pdf file can generate from LaTex document inside the solution.

## Usage

### Basic Conversion

To convert a Markdown file (raletive path) to a LaTeX presentation, use the following command:

```python
pts convert markdown.md output.pdf
```

Presentation LaTex file will be saved as pdf in the project if you have LaTex interpreter added to PATH.
You can change the location of the input and the output file by providing paths instead of file names.

## Examples

Here are some example commands that are specified in the project:

Note that all commands should be executed in virtual environment (i.e. inside poetry shell)

- **Convert PDF to Markdown:**:

```python
pts md <path/article.pdf> <path/output.md>
```

- **Convert Markdown to JSON:**:

```python
pts json <path/markdown.md> <path/output.json>
```

- **Convert JSON to LaTeX:**:

```python
pts latex <path/markdown.md> <path/output.json>
```

- **Convert LaTeX to PDF:**:

```python
pts pdf <path/markdown.md> <path/output.json>
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
