import os
import platform
import subprocess


def latex_to_pdf(latex_code):

    with open("sample.tex", "w", encoding="utf-8", errors="replace") as tex_file:
        tex_file.write(latex_code)

    filename, ext = os.path.splitext("sample.tex")

    pdf_filename = filename + ".pdf"

    subprocess.run(["pdflatex", "-interaction=nonstopmode", "sample.tex"])

    if not os.path.exists(pdf_filename):
        raise RuntimeError("PDF output not found")

    if platform.system().lower() == "darwin":
        subprocess.run(["open", pdf_filename])
    elif platform.system().lower() == "windows":
        os.startfile(pdf_filename)
    elif platform.system().lower() == "linux":
        subprocess.run(["xdg-open", pdf_filename])
    else:
        raise RuntimeError('Unknown operating system "{}"'.format(platform.system()))
