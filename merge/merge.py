import fitz

result = fitz.open()

pdfs = [
    "./ass2.pdf",
    "./ass3.pdf",
    "./ass1.pdf",
]

for pdf in pdfs:
    with fitz.open(pdf) as mfile:
        result.insert_pdf(mfile)

result.save("result.pdf")
