from lxml import etree
import time
tree = etree.parse('static/temp/input.xml')

ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

root = tree.getroot()

from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import XSD, DCTERMS

base_uri = root.get('{http://www.w3.org/XML/1998/namespace}base')
document_id = root.get('{http://www.w3.org/XML/1998/namespace}id')

current_date = Literal(time.strftime("%Y-%m-%d"), datatype=XSD.date)

ex = Namespace(base_uri + '/')
cao = Namespace("https://w3id.org/cao/")
lawd = Namespace("http://lawd.info/ontology/")
frbroo = Namespace("http://iflastandards.info/ns/fr/frbr/frbroo/")
crm = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
prov = Namespace("http://www.w3.org/ns/prov#")
oa = Namespace("http://www.w3.org/ns/oa#")

# empty dictionary for any prefix declared in TEI document within prefixDef

prefix_dict = {}

for prefixDef in root.findall('.//tei:prefixDef', ns):
	prefix = prefixDef.get('ident')
	prefix_uri = prefixDef.get('replacementPattern')
	prefix_uri = prefix_uri.replace('$1', '')
	
# update prefix dictionary
	
	prefix_dict[prefix] = prefix_uri


g = Graph()

# agent responsible for extracting the CAO graph from the TEI edition using this script

extraction_resp = 'f-giov' # agent id

extraction_resp_uri = URIRef(ex + 'agent/' + extraction_resp) #agent uri










############################

# extraction script begins

############################


# tei:app

for app in root.findall('.//tei:app', ns):
	app_id = app.get('{http://www.w3.org/XML/1998/namespace}id')
	app_uri = URIRef(ex + 'app/' + app_id)
	g.add( (app_uri, RDF.type, cao.VariationUnit))

# new annotation
	
	annot_uri = URIRef(ex + 'annot/an-' + app_id)
	varloc_uri = URIRef(ex + 'varloc/vl-' + app_id)
	g.add( (annot_uri, RDF.type, oa.Annotation))
	g.add( (annot_uri, oa.hasBody, app_uri))
	g.add( (annot_uri, oa.hasTarget, varloc_uri))
	g.add( (annot_uri, DCTERMS.created, current_date))
	g.add( (annot_uri, DCTERMS.creator, extraction_resp_uri))

# empty list to store @varSeq

	varlist = []

# tei:rdg and tei:lem in tei:app

	for rdg in app.xpath('./tei:rdg | ./tei:lem', namespaces=ns):
		rdg_id = rdg.get('{http://www.w3.org/XML/1998/namespace}id') 
		rdg_uri = URIRef(ex + 'rdg/' + rdg_id)
		expr_frag_uri = URIRef(ex + 'rdg-fragment/' + rdg_id)
		rdg_value = Literal(rdg.xpath('./text()', namespaces=ns), datatype=XSD.string)
		if rdg.tag == '{http://www.tei-c.org/ns/1.0}rdg':
			g.add( (app_uri, cao.hasReading, rdg_uri))
			g.add( (rdg_uri, RDF.type, cao.Reading))
		if rdg.tag == '{http://www.tei-c.org/ns/1.0}lem':
			g.add( (app_uri, cao.hasBaseReading, rdg_uri))
			g.add( (rdg_uri, RDF.type, cao.BaseReading))
		g.add( (rdg_uri, cao.isWitnessedBy, expr_frag_uri))
		g.add( (rdg_uri, RDF.value, rdg_value))

# expression fragment bearing the reading

		g.add( (expr_frag_uri, RDF.type, frbroo.F23_Expression_Fragment))
		
# @wit, @type, @cause, @hand, @resp, @source attributes on tei:rdg and tei:lem

		if rdg.get('wit') is not None:
			wit_id = rdg.get('wit').split()
			i = 0
			while i < len(wit_id):
				wit_uri = URIRef(ex + 'wit/' + wit_id[i].replace('#', ''))
				g.add( (expr_frag_uri, frbroo.R4_carriers_provided_by, wit_uri))
				i += 1

		if rdg.get('type') is not None:			
			rdg_type = rdg.get('type').split(':')
			rdg_type_prefix = rdg_type[0]
			rdg_type_value = rdg_type[1]
			if prefix_dict.has_key(rdg_type_prefix):
				rdg_type_uri = URIRef(prefix_dict[rdg_type_prefix] + rdg_type[1])
				g.add( (rdg_uri, cao.hasReadingType, rdg_type_uri))

		# omission
		if rdg.get('type') is None and rdg.find("./[Value='']"):
			g.add( (rdg_uri, cao.hasReadingType, cao.omission))


		if rdg.get('cause') is not None:			
			rdg_cause = rdg.get('cause').split(':')
			rdg_cause_prefix = rdg_cause[0]
			rdg_cause_value = rdg_cause[1]
			if prefix_dict.has_key(rdg_cause_prefix):
				rdg_cause_uri = URIRef(prefix_dict[rdg_cause_prefix] + rdg_cause[1])
				g.add( (rdg_uri, cao.hasReadingCause, rdg_cause_uri))
		
		if rdg.get('varSeq') is not None:	
			rdg_seq = rdg.get('varSeq')
			varlist.insert(int(rdg_seq)-1, rdg_uri)

		if rdg.get('hand') is not None:	
			rdg_hand = rdg.get('hand')
			rdg_hand_uri = URIRef(ex + 'hand/' + rdg_hand.replace('#', ''))
			g.add( (expr_frag_uri, cao.hasAttributedHand, rdg_hand_uri))


		if rdg.get('resp') is not None:
			rdg_resp = rdg.get('resp')
			rdg_resp_uri =  URIRef(ex + 'agent/' + rdg_resp.replace('#', ''))
			g.add( (rdg_uri, prov.wasAttributedTo, rdg_resp_uri))	

		if rdg.get('source') is not None:
			source_id = rdg.get('source').replace('#', '').split()
			i = 0
			while i < len(source_id):
				source_bibl_path = './ancestor::tei:text/preceding-sibling::tei:teiHeader//tei:bibl[@xml:id="' + source_id[i] + '"]'
				for path in rdg.xpath(source_bibl_path, namespaces=ns):
					if path.get('sameAs') is not None:
						source_uri = URIRef(path.get('sameAs'))
					else:
						source_uri = URIRef(ex + 'source-edition/' + source_id[i])
					g.add( (rdg_uri, prov.hadPrimarySource, source_uri))
				i += 1
				
# variants sequence for each tei:app

	i = len(varlist)-1
	while i > 0: 
		g.add( (varlist[i], cao.follows, varlist[i-1]))
		i = i-1

# tei:note in tei:app

	for note in app.xpath('./tei:note', namespaces=ns):
		note_id = note.get('{http://www.w3.org/XML/1998/namespace}id')
		note_uri = URIRef(ex + 'note/' + note_id)
		note_value = Literal(note.xpath('./text()', namespaces=ns), datatype=XSD.string)
		if note.get('target') is not None:
			target_rdg = URIRef(ex + 'rdg/' + note.get('target').replace('#',''))
		else:
			target = note.xpath('./ancestor::app[1]')
			target_rdg = app_uri
		g.add( (note_uri, RDF.type, crm.E62_String))
		g.add( (note_uri, RDF.value, note_value))

# @source on tei:note
		
		if note.get('source') is not None:
			source_id = note.get('source').replace('#', '').split()
			i = 0
			while i < len(source_id):
				source_bibl_path = './ancestor::tei:text/preceding-sibling::tei:teiHeader//tei:bibl[@xml:id="' + source_id[i] + '"]'
				for path in note.xpath(source_bibl_path, namespaces=ns):
					if path.get('sameAs') is not None:
						source_uri = URIRef(path.get('sameAs'))
					else:
						source_uri = URIRef(ex + 'source-edition/' + source_id[i])
					g.add( (note_uri, prov.hadPrimarySource, source_uri)) 
				i += 1

		if note.get('target') is not None:
			target_ref = note.get('target').replace('#', '')
			for rdg in app.xpath('./tei:rdg | ./tei:lem', namespaces=ns):
				rdg_id = rdg.get('{http://www.w3.org/XML/1998/namespace}id') 
				rdg_uri = URIRef(ex + 'rdg/' + rdg_id)
			if target_ref == rdg_id:
				g.add( (rdg_uri, crm.P3_has_note, note_uri))
			elif target_ref == app_id:
				g.add( (app_uri, crm.P3_has_note, note_uri))
			else:
				g.add( (app_uri, crm.P3_has_note, note_uri)) 
				
	

# Bind prefix

g.bind("prov", prov)
g.bind("frbroo", frbroo)
g.bind("crm", crm)
g.bind("cao", cao)
g.bind("", ex)
g.bind("oa", oa)
g.bind("dcterms", DCTERMS)

# RDF/XML output
g.serialize(destination="static/temp/output.rdf", format='xml')

# Notation3 output
g.serialize(destination="static/temp/output.n3", format='n3')

# N-triples output
g.serialize(destination="static/temp/output.nt", format='nt')

# Json-ld output
g.serialize(destination='static/temp/output.jsonld', format='json-ld')