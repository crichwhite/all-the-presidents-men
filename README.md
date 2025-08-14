## Building Documents


### LaTeX

```sh
pdflatex main.tex
biber main
pdflatex main.tex
```

### Word `.docx`

```sh
pandoc -f latex -t docx --bibliography=main.bib --filter pandoc-crossref --citeproc  --csl cite-style.csl -o article.docx main.tex
```

pandoc -f latex -t docx --bibliography=main.bib --filter pandoc-crossref --citeproc -o article.docx main.tex


### HTML