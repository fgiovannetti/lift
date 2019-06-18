from lxml import etree
tree = etree.parse('static/temp/input.xml')


ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
root = tree.getroot()
base_uri = root.get('{http://www.w3.org/XML/1998/namespace}base')
edition_id = root.get('{http://www.w3.org/XML/1998/namespace}id')

from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef, RDFS
from rdflib.namespace import XSD, DCTERMS, OWL
agrelon = Namespace("https://d-nb.info/standards/elementset/agrelon#")
crm = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
frbroo = Namespace("http://iflastandards.info/ns/fr/frbr/frbroo/")
pro = Namespace("http://purl.org/spar/pro/")
proles = Namespace("http://www.essepuntato.it/2013/10/politicalroles/")
prov = Namespace("http://www.w3.org/ns/prov#")
schema = Namespace("https://schema.org/")
tvc = Namespace("http://www.essepuntato.it/2012/04/tvc/")
 

g = Graph()

############################

# extraction script begins

############################

for place in root.findall('.//tei:place', ns):
	place_id = place.get('{http://www.w3.org/XML/1998/namespace}id')
	place_ref = '#' + place_id
	place_uri = URIRef(base_uri + '/place/' + place_id)
	g.add( (place_uri, RDF.type, schema.Place))

	# sameas
	same_as = place.get('sameAs').split()
	i = 0
	while i < len(same_as):
		same_as_uri = URIRef(same_as[i])
		g.add( (place_uri, OWL.sameAs, same_as_uri))
		i += 1
	
	# placename

	placename = place.find('./tei:placeName', ns)
	label = placename.text
	label_lang = placename.get('{http://www.w3.org/XML/1998/namespace}lang')
	if label_lang is not None:
		g.add( (place_uri, RDFS.label, Literal(label, lang=label_lang)))
	else:
		g.add( (place_uri, RDFS.label, Literal(label)))
	
	# referenced places

	ref = './/tei:placeName[@ref="#' + place_id + '"]'
	for referenced_place in root.findall(ref, ns):
		parent = referenced_place.getparent()
		parent_id = parent.get('{http://www.w3.org/XML/1998/namespace}id')
		parent_uri = URIRef(base_uri + '/text/' + parent_id)
		g.add( (place_uri, DCTERMS.isReferencedBy, parent_uri))
		g.add( (parent_uri, RDF.type, frbroo.F23_Expression_Fragment))
		g.add( (parent_uri, frbroo.R15i_is_fragment_of, URIRef(base_uri + edition_id)))

# bind prefix
g.bind("agrelon", agrelon)
g.bind("crm", crm)
g.bind("frbroo", frbroo)
g.bind("dcterms", DCTERMS)
g.bind("schema", schema)
g.bind("owl", OWL)
g.bind("pro", pro)
g.bind("proles", proles)
g.bind("prov", prov)
g.bind("tvc", tvc)

g.serialize(destination='static/temp/output.nt', format='nt')
g.serialize(destination='static/temp/output.n3', format='n3')
g.serialize(destination='static/temp/output.rdf', format='xml')