NAME=poster

$(NAME).pdf: $(NAME).tex 
	pdflatex $(NAME)
	pdflatex $(NAME)

clean:
	rm -f *.bbl *.blg *.out *.aux *.log $(NAME).pdf
	rm -f *.nav *.snm *.toc
