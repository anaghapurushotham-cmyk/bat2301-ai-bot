import os
from pypdf import PdfReader

# The folder that holds your source files (the one Step 1 filled in).
INPUT_FOLDER = "Course_Data"

# The single text file your app will read.
OUTPUT_FILE = "course_data.txt"


def read_pdf(path):
    """Return the text of a PDF, or "" if it can't be read."""
    try:
        reader = PdfReader(path)
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    except Exception as e:
        print(f"Could not read PDF {path}: {e}")
        return ""


def read_text(path):
    """Return the contents of a plain-text file (.qmd, .csv, .txt)."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Could not read {path}: {e}")
        return ""


def main():
    if not os.path.exists(INPUT_FOLDER):
        os.makedirs(INPUT_FOLDER)
        print(f"Created '{INPUT_FOLDER}'. Put your files there and run this again.")
        return

    pieces = []
    for filename in os.listdir(INPUT_FOLDER):
        path = os.path.join(INPUT_FOLDER, filename)

        if filename.lower().endswith(".pdf"):
            text = read_pdf(path)
        elif filename.lower().endswith((".qmd", ".csv", ".txt")):
            text = read_text(path)
        else:
            continue  # skip anything we can't read as text

        if text.strip():
            # Wrap each file with a label so the model can tell where one
            # source ends and the next begins.
            pieces.append(f"\n\n--- SOURCE: {filename} ---\n{text}\n--- END ---\n")
            print(f"Added: {filename}")

    if pieces:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(pieces))
        print(f"\nDone. Combined {len(pieces)} file(s) into '{OUTPUT_FILE}'.")
    else:
        print("\nNo readable files found. Add .pdf, .qmd, .csv, or .txt files.")


if __name__ == "__main__":
    main()