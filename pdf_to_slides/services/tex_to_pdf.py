import subprocess
import os
import shutil
import tempfile

def tex_to_pdf(tex_file_path, pdf_output_path):
    if not os.path.isfile(tex_file_path):
        raise FileNotFoundError(f"No such file: '{tex_file_path}'")
    
    pdflatex_path = shutil.which("pdflatex")
    if pdflatex_path is None:
        raise FileNotFoundError("pdflatex executable not found in system PATH")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            src_dir = os.path.dirname(tex_file_path)
            dest_dir = os.path.join(temp_dir, os.path.basename(src_dir))
            shutil.copytree(src_dir, dest_dir)
            
            temp_tex_file_path = os.path.join(dest_dir, os.path.basename(tex_file_path))
            
            subprocess.run([pdflatex_path, "-output-directory=" + dest_dir, temp_tex_file_path], check=True)
            print("PDF successfully generated")
            
            generated_pdf_path = os.path.join(dest_dir, os.path.splitext(os.path.basename(tex_file_path))[0] + ".pdf")
            
            if os.path.isfile(pdf_output_path):
                os.remove(pdf_output_path)
            
            shutil.move(generated_pdf_path, pdf_output_path)
            print(f"PDF moved to {pdf_output_path}")

        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
