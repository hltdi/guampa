lrec2014.pdf: lrec2014.tex guampa.bib
	pdflatex lrec2014
	bibtex lrec2014
	pdflatex lrec2014
	pdflatex lrec2014

abstract.pdf: abstract.tex guampa.bib
	pdflatex abstract
	bibtex abstract
	pdflatex abstract
	pdflatex abstract

clean:
	rm -f *.bbl *.blg *.out *.aux *.log abstract.pdf lrec2014.pdf
