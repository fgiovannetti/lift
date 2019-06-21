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

	# relation

	for relation in root.findall('.//tei:listRelation/tei:relation', ns):
		person_ref = '#' + person_id
		relation_name_uri = URIRef("https://d-nb.info/standards/elementset/agrelon#" + relation.get('name'))
		if relation.get('active') is not None and relation.get('active') == person_ref:
			passive = relation.get('passive').replace("#", "").split()
			i = 0
			while i < len(passive):
				g.add( (person_uri, relation_name_uri, URIRef(base_uri + '/' + passive[i])))
				i += 1
		elif relation.get('mutual') is not None:
			relentity = relation.get('mutual').split()
			if person_ref in relentity:
				mutual = relation.get('mutual').replace("#", "").replace(person_id, "").split()
				i = 0
				while i < len(mutual):
					g.add( (person_uri, relation_name_uri, URIRef(base_uri + '/' + mutual[i])))
					i += 1

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