.PHONY: doc

doc: slides.pdf

slides.pdf: slides.odp
	libreoffice --convert-to pdf slides.odp
