from lxml import etree
tree = etree.parse('static/temp/input.xml')


ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
root = tree.getroot()
base_uri = root.get('{http://www.w3.org/XML/1998/namespace}base')
edition_id = root.get('{http://www.w3.org/XML/1998/namespace}id')

from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef, RDFS
from rdflib.namespace import XSD, DCTERMS, OWL
frbroo = Namespace("http://iflastandards.info/ns/fr/frbr/frbroo/")
schema = Namespace("https://schema.org/")

g = Graph()

############################

# extraction script begins

############################

# person

for person in root.findall('.//tei:person', ns):
	person_id = person.get('{http://www.w3.org/XML/1998/namespace}id')
	person_ref = '#' + person_id
	person_uri = URIRef(base_uri + '/person/' + person_id)
	g.add( (person_uri, RDF.type, schema.Person))
	
	# sameas
	same_as = person.get('sameAs').split()
	i = 0
	while i < len(same_as):
		same_as_uri = URIRef(same_as[i])
		g.add( (person_uri, OWL.sameAs, same_as_uri))
		i += 1
	
	# persname
	persname = person.find('./tei:persName', ns)
	label = persname.text
	label_lang = persname.get('{http://www.w3.org/XML/1998/namespace}lang')
	if label_lang is not None:
		g.add( (person_uri, RDFS.label, Literal(label, lang=label_lang)))
	else:
		g.add( (person_uri, RDFS.label, Literal(label)))

	# perstype
	listperson = person.find('./...', ns)
	perstype = listperson.get('type')
	perscorr = listperson.get('corresp')
	if perstype is not None:
		g.add( (person_uri, DCTERMS.description, Literal(perstype)))
	if perscorr is not None and perscorr.startswith('http'):
		g.add( (person_uri, DCTERMS.subject, URIRef(perscorr)))

# referenced_person

ref = './tei:text//tei:persName[@ref="#' + person_id + '"]'
for referenced_person in root.findall(ref, ns):
		parent = referenced_person.getparent()
		parent_id = parent.get('{http://www.w3.org/XML/1998/namespace}id')
		parent_uri = URIRef(base_uri + '/text/' + parent_id)
		g.add( (person_uri, DCTERMS.isReferencedBy, parent_uri))
		g.add( (parent_uri, RDF.type, frbroo.F23_Expression_Fragment))
		g.add( (parent_uri, frbroo.R15i_is_fragment_of, URIRef(base_uri + '/' + edition_id)))

# bind prefix

g.bind("frbroo", frbroo)
g.bind("dcterms", DCTERMS)
g.bind("schema", schema)
g.bind("owl", OWL)

g.serialize(destination='static/temp/output.nt', format='nt')
g.serialize(destination='static/temp/output.n3', format='n3')
g.serialize(destination='static/temp/output.rdf', format='xml')