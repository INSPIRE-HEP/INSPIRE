include ../config.mk
-include ../config-local.mk

WEBDESC='Mapping of SPIRES abbreviations for URLs to Displayable names'
OADESC='Journals that are fully OA'
CODDESC='Coden to short title mappings'
JOURNALDESC='Mapping of journal abbreviations to full names'
TALKTYPEDESC='List of types of talks'
COLLECTIONDESC='690C aliases'
SUBJECTDESC='65017 aliases'
PDGDESC='PDG codes'
NOTEDESC='A list of 088 report-number prefixes for which the 980-collection 'NOTE' should be appended.'
DEGREEDESC='List of type of Degrees'
HEPCOLLECTIONSDESC='List of possible HEP Collections'
PWD=`pwd`

all:
	@echo "Done."

test:
	@echo "Nothing to test."

install: install-journals-knowledge

install-journals-knowledge:
	$(INSTALL) -D journal-titles-inspire.kb $(ETCDIR)/docextract/journal-titles-inspire.kb

install-dbchanges: announce-kb-load truncate-kbs weblinks journals collection hep-collections subject pdg coden degree create-institutions-dynamic-kb create-experiments-dynamic-kb
	@echo "Done."

weblinks: load-weblinks-knowledge-base
journals: load-journals-knowledge-base
collection: load-collection-knowledge-base
hep-collections: load-hep-collections-knowledge-base
subject: load-subject-knowledge-base
pdg: load-pdg-knowledge-base
notes: load-note-collections-knowledge-base
coden: load-coden-knowledge-base
degree: load-degree-knowledge-base

announce-kb-load:
	@echo "Loading knowledge bases into DB..."

truncate-kbs:
	echo "TRUNCATE knwKBRVAL" | $(BINDIR)/dbexec
	echo "TRUNCATE knwKBDDEF" | $(BINDIR)/dbexec
	echo "TRUNCATE knwKB" | $(BINDIR)/dbexec

load-weblinks-knowledge-base:
	$(PYTHON) kb_load.py $(PWD)/weblinks.kb WEBLINKS --description="$(WEBDESC)"

load-coden-knowledge-base:
	$(PYTHON) kb_load.py $(PWD)/coden.kb CODENS --description="$(CODDESC)"

load-journals-knowledge-base:
	$(PYTHON) kb_load.py $(PWD)/journal.kb JOURNALS --description="$(JOURNALDESC)"

load-collection-knowledge-base:
	$(PYTHON) kb_load.py $(PWD)/collection.kb COLLECTION --description="$(COLLECTIONDESC)"

load-hep-collections-knowledge-base:
	$(PYTHON) kb_load.py $(PWD)/hep-collections.kb HEPCOLLECTIONS --description="$(HEPCOLLECTIONSDESC)"

load-subject-knowledge-base:
	$(PYTHON) kb_load.py $(PWD)/subject.kb SUBJECT --description="$(SUBJECTDESC)"

load-degree-knowledge-base:
	$(PYTHON) kb_load.py $(PWD)/degree.kb DEGREE --description="$(DEGREEDESC)"

load-pdg-knowledge-base:
	$(PYTHON) kb_load.py $(PWD)/pdg.kb PDG --description="$(PDGDESC)"

load-note-collections-knowledge-base:
	$(PYTHON) kb_load.py $(PWD)/note_collections.kb NOTE_COLLECTIONS --description="$(NOTEDESC)"

create-institutions-dynamic-kb:
	$(PYTHON) InstitutionsCollection_dynamic_KB.py

create-experiments-dynamic-kb:
	$(PYTHON) ExperimentsCollection_dynamic_KB.py

clean:
	@rm -f *.orig *~
