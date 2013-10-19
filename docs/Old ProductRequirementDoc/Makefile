OBJDIR=obj
SRCDIR=src
MAINTEX=paper
TARGET=Unknown-prd.pdf

all: $(TARGET)

$(TARGET): $(SRCDIR)/$(MAINTEX).tex $(OBJDIR)
	xelatex -output-directory=$(OBJDIR) $<
	xelatex -output-directory=$(OBJDIR) $<
	@mv $(OBJDIR)/$(MAINTEX).pdf $(TARGET)
	@echo DONE!

$(OBJDIR):
	@mkdir -p $@

clean:
	rm -rf $(OBJDIR) $(TARGET)

