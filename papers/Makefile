abstract.pdf: abstract.tex guampa.bib
	pdflatex abstract
	bibtex abstract
	pdflatex abstract
	pdflatex abstract

clean:
	rm -f *.qry *.idx *.bbl *.blg *.out *.aux *.log abstract.pdf
