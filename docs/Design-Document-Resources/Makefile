TARGET=report
TEX=xelatex -shell-escape
BIBTEX=biber
READER=evince
OUTPUT=../Design-Document.pdf

all: rebuild

rebuild output/$(TARGET).pdf: *.tex *.bib output
	cd output && rm -f *.tex *.bib && ln -s ../*.tex ../*.bib .
	cd output &&  $(TEX) $(TARGET).tex && $(BIBTEX) $(TARGET)
	cp output/$(TARGET).pdf $(OUTPUT) -f

output:
	mkdir output -p
	cd output && rm -f res img && ln -s ../res ../img .

view: output/$(TARGET).pdf
	$(READER) $(OUTPUT) &

clean:
	rm -rf output

# compile twice to get cross reference right
final : *.tex *.bib output
	cd output && rm -f *.tex *.bib && ln -s ../*.tex ../*.bib .
	cd output && $(TEX) $(TARGET).tex && $(BIBTEX) $(TARGET) && \
		$(TEX) $(TARGET).tex && $(TEX) $(TARGET).tex

count:
	@word_count *.tex

run: view

.PHONY: all view clean rebuild run
