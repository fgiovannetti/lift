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

	# partic_event

	for event in person.findall('./tei:event', ns):
		event_id = event.get('{http://www.w3.org/XML/1998/namespace}id')
		partic_event_uri = URIRef(base_uri + '/' + person_id + '-in-' + event_id)
		if event is not None:
			g.add( (person_uri, pro.holdsRoleInTime, partic_event_uri))

	# role_in_event

	for event in person.findall('./tei:event', ns):
		event_id = event.get('{http://www.w3.org/XML/1998/namespace}id')
		persName = person.find('./tei:persName', ns)
		label = persName.text
		rit_uri = URIRef(base_uri + '/rit/' + person_id + '-at-' + event_id)
		g.add( (rit_uri, RDF.type, pro.RoleInTime))
		pers_in_event = event.find('./tei:desc/tei:persName', ns)
		if pers_in_event is not None and pers_in_event.get('ref') == person_ref and pers_in_event.get('role') is not None:
			role_uri = URIRef(base_uri + '/role/' + pers_in_event.get('role'))
			g.add( (rit_uri, pro.withRole, role_uri))
			g.add( (role_uri, RDF.type, pro.Role))
		if pers_in_event.get('corresp') is not None:
			g.add( (role_uri, OWL.sameAs, pro.Role))
			g.add( (role_uri, RDFS.label, pro.Role))
			corresp_role_uri = URIRef(pers_in_event.get('corresp'))
			g.add( (role_uri, OWL.sameAs, corresp_role_uri))
			role_label = pers_in_event.get('role')
			g.add( (role_uri, RDFS.label, Literal(role_label)))
		else:
			g.add( (rit_uri, pro.withRole, URIRef(base_uri + '/role/participant')))
			role_uri = URIRef(base_uri + '/role/participant')
			g.add( (role_uri, RDF.type, pro.Role))
			g.add( (role_uri, OWL.sameAs, URIRef('http://wordnet-rdf.princeton.edu/id/10421528-n')))
			g.add( (role_uri, RDFS.label, Literal('participant'))) 
			
		g.add( (rit_uri, tvc.atTime, URIRef(base_uri + '/tvc/' + event_id + '-time')))
		g.add( (rit_uri, pro.relatesToEntity, URIRef(base_uri + '/event/' + event_id)))

		place = event.find('./tei:desc/tei:placeName', ns)
		if place > 1:
			place_of_event = place.get('type="place_of_event"')
			g.add( (rit_uri, proles.relatesToPlace, URIRef(base_uri + '/place/' + place.get('ref').replace("#", ""))))
		elif event.find('./tei:desc/tei:placeName', ns) == 1:
			g.add( (rit_uri, proles.relatesToPlace, URIRef(base_uri + '/place/' + place.get('ref').replace("#", ""))))

# referenced_person

ref = './tei:text//tei:persName[@ref="#' + person_id + '"]'
for referenced_person in root.findall(ref, ns):
		parent = referenced_person.getparent()
		parent_id = parent.get('{http://www.w3.org/XML/1998/namespace}id')
		parent_uri = URIRef(base_uri + '/text/' + parent_id)
		g.add( (person_uri, DCTERMS.isReferencedBy, parent_uri))
		g.add( (parent_uri, RDF.type, frbroo.F23_Expression_Fragment))
		g.add( (parent_uri, frbroo.R15i_is_fragment_of, URIRef(base_uri + edition_id)))

# event_time 

for event in root.findall('.//tei:event', ns):
	event_id = event.get('{http://www.w3.org/XML/1998/namespace}id')
	event_time = URIRef(base_uri + '/' + event_id + '-time')
	event_uri = URIRef(base_uri + '/event/' + event_id)
	evcorr = event.get('corresp')
	evtype = event.get('type')
	g.add( (event_time, RDF.type, URIRef('http://www.ontologydesignpatterns.org/cp/owl/timeinterval.owl#TimeInterval')))
	if event.get('when') is not None:
		g.add( (event_time, OWL.hasIntervalStartDate, Literal(event.get('when'), datatype=XSD.date)))
		g.add( (event_time, OWL.hasIntervalEndDate, Literal(event.get('when'), datatype=XSD.date)))
	if event.get('from') is not None:
		g.add( (event_time, OWL.hasIntervalStartDate, Literal(event.get('from'), datatype=XSD.date)))
	if event.get('to') is not None:
		g.add( (event_time, OWL.hasIntervalEndDate, Literal(event.get('to'), datatype=XSD.date)))
	
	# event_desc

	g.add( (event_uri, RDF.type, crm.E5_Event))
	g.add( (event_uri, RDF.type, schema.Event))
	if event.find('./tei:label', ns) is not None:
		label = event.find('./tei:label', ns).text
		g.add( (event_uri, RDFS.label, Literal(label)))
	if evtype is not None:
		g.add( (event_uri, DCTERMS.description, Literal(evtype)))
	if evcorr is not None and evcorr.startswith('http'):
		g.add( (event_uri, DCTERMS.subject, URIRef(evcorr)))
	source = event.find('./tei:bibl', ns)
	if source is not None:
		source_id = source.get('{http://www.w3.org/XML/1998/namespace}id')
		source_uri = URIRef(base_uri + '/source/' + source_id)
		g.add( (event_uri, prov.hasPrimarySource, source_uri))
		for event_source in root.findall('.//tei:event//tei:bibl', ns):
			g.add( (source_uri, RDF.type, prov.PrimarySource))
	        if event_source.find('./tei:author', ns) is not None and event_source.find('./tei:author', ns).get('ref') is not None:
	            author_ref = event_source.find('./tei:author', ns).get('ref')
	            author_id = author_ref.split('#')
	            g.add( (source_uri, DCTERMS.creator, URIRef(base_uri + '/person/' + author_id[1])))
	        if event_source.find('.tei:title', ns) is not None:
	            g.add( (source_uri, DCTERMS.title, Literal(event_source.find('.tei:title', ns).text)))
	        if event_source.get('sameAs') is not None:
	            sameAs = event_source.get('sameAs')
	            if sameAs.startswith('http'):
	            	g.add( (source_uri, OWL.sameAs, URIRef(event_source.get('sameAs')))) 
	        if event_source.find('.tei:date', ns) is not None:
	            evdate = event_source.find('.tei:date', ns)
	            g.add( (source_uri, DCTERMS.date, Literal(evdate.get('when'), datatype=XSD.date)))


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


# place

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