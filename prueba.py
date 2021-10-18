from PaPDF import PaPDF

with PaPDF("test.pdf") as pdf:
    pdf.addText(40, 290, "Hello world")
    pdf.addPage()
    pdf.addText(40, 10, 'Hello world')