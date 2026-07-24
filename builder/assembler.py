import os
import json

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(PACKAGE_DIR, 'templates')
STYLES_DIR = os.path.join(PACKAGE_DIR, 'styles')

def build_app(pdf_data_path='pdf_structure.json', quiz_data_path='quiz_data.json', output_path='index.html', css_output_path='css/styles.css'):
    """
    Assembles the digital textbook application HTML page from modular layout templates,
    CSS stylesheets, PDF structure data, and interactive quiz datasets.
    """
    # 1. Load Data Files
    if not os.path.exists(pdf_data_path):
        raise FileNotFoundError(f"PDF structure data file not found: {pdf_data_path}")
    if not os.path.exists(quiz_data_path):
        raise FileNotFoundError(f"Quiz data file not found: {quiz_data_path}")

    with open(pdf_data_path, 'r', encoding='utf-8') as f:
        pdf_structure_data = json.load(f)

    with open(quiz_data_path, 'r', encoding='utf-8') as f:
        quiz_data = json.load(f)

    pdf_json_str = json.dumps(pdf_structure_data, ensure_ascii=True)
    quiz_json_str = json.dumps(quiz_data, ensure_ascii=False)

    # 2. Compile and Output CSS Stylesheet
    main_css_src = os.path.join(STYLES_DIR, 'main.css')
    if os.path.exists(main_css_src):
        os.makedirs(os.path.dirname(os.path.abspath(css_output_path)), exist_ok=True)
        with open(main_css_src, 'r', encoding='utf-8') as sf:
            css_content = sf.read()
        with open(css_output_path, 'w', encoding='utf-8') as df:
            df.write(css_content)

    # 3. Load HTML Templates
    base_template_path = os.path.join(TEMPLATES_DIR, 'base.html')
    content_template_path = os.path.join(TEMPLATES_DIR, 'content.html')

    with open(base_template_path, 'r', encoding='utf-8') as f:
        base_html = f.read()

    with open(content_template_path, 'r', encoding='utf-8') as f:
        main_content = f.read()

    # 4. Interpolate and Assemble Document
    html_output = base_html.replace('__MAIN_CONTENT__', main_content)
    html_output = html_output.replace('__PDF_DATA__', pdf_json_str)
    html_output = html_output.replace('__QUIZ_DATA__', quiz_json_str)

    # 5. Write Output Document
    output_dir = os.path.dirname(os.path.abspath(output_path))
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_output)

    print(f"Successfully assembled textbook digital app at: {output_path}")
    return output_path
