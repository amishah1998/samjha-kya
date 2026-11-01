"""Extract a PDF's text page by page, so every card can cite the page it came from.

    uv run --with pypdf python pdf_text.py book.pdf > book.txt
    (or: pip install pypdf; falls back to the `pdftotext` command if pypdf is missing)

Output: one "=== page N ===" header per page, then that page's text. A final line reports pages
with no text (scanned images), which need OCR before they can become cards.
"""
import shutil
import subprocess
import sys


def pages(path):
    import os
    if not os.path.isfile(path):
        raise SystemExit(f"No such file: {path}")
    with open(path, "rb") as f:
        head = f.read(1024)
    if b"%PDF" not in head:
        kind = "a web page (the site probably blocked the download)" if b"<html" in head.lower() or b"<!doc" in head.lower() else "not a PDF"
        raise SystemExit(f"{path} is {kind}. Download it again in a browser, or ask the user for the file.")
    try:
        from pypdf import PdfReader
        return [(p.extract_text() or "") for p in PdfReader(path).pages]
    except ImportError:
        if not shutil.which("pdftotext"):
            raise SystemExit("Install pypdf (pip install pypdf) or poppler's pdftotext first.")
        out = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True, check=True).stdout
        return out.split("\f")


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    ps = pages(sys.argv[1])
    empty = []
    for i, t in enumerate(ps, 1):
        t = t.strip()
        if not t:
            empty.append(i)
        print(f"=== page {i} ===\n{t}\n")
    words = sum(len(t.split()) for t in ps)
    print(f"--- {len(ps)} pages, {words} words" + (f"; no text on pages {empty} (scanned? needs OCR)" if empty else ""))


if __name__ == "__main__":
    main()
