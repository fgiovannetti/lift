import sys
reload(sys)
sys.setdefaultencoding('utf8')


from lxml import etree
tree = etree.parse('static/temp/input.xml')


ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
root = tree.getroot()
base_uri = root.get('{http://www.w3.org/XML/1998/namespace}base')
edition_id = root.get('{http://www.w3.org/XML/1998/namespace}id')


o = open('static/temp/output.rdf', mode='w')


o.write('<?xml version="1.0" encoding="UTF-8"?>')


o.write('''<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/"
		 xmlns:agrelon="https://d-nb.info/standards/elementset/agrelon#"
		 xmlns:frbroo="http://iflastandards.info/ns/fr/frbr/frbroo/"
		 xmlns:owl="http://www.w3.org/2002/07/owl#"
		 xmlns:pro="http://purl.org/spar/pro"
		 xmlns:proles="http://www.essepuntato.it/2013/10/politicalroles"
		 xmlns:prov="http://www.w3.org/ns/prov#"
		 xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
		 xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
		 xmlns:schema="https://schema.org/"
		 xmlns:tei="http://www.tei-c.org/ns/1.0"
		 xmlns:tvc="http://www.essepuntato.it/2012/04/tvc/">''')


# Person


def subject(person):
	global o
	global base_uri
	global person_id
	o.write('<rdf:Description rdf:about="' + base_uri + '/person/' + person_id + '">')


def sameas(person):
	global o
	sameAs = person.get('sameAs').split()
	i = 0
	while i < len(sameAs):
		o.write('<owl:sameAs rdf:resource="' + sameAs[i] + '"/>')
		i += 1


def persname(person):
	global o
	global ns
	persName = person.find('./tei:persName', ns)
	label = persName.text
	label_lang = persName.get('{http://www.w3.org/XML/1998/namespace}lang')
	if label_lang is not None:
		o.write('<rdfs:label ' + 'xml:lang="' + label_lang + '">' + label + '</rdfs:label>')
	else:
		o.write('<rdfs:label>' + label + '</rdfs:label>')


def referenced_person(person_id):
	global o
	global root
	ref = './tei:text//tei:persName[@ref="#' + person_id + '"]'
	for referenced_person in root.findall(ref, ns):
		parent = referenced_person.getparent()
		parent_id = parent.get('{http://www.w3.org/XML/1998/namespace}id')
		o.write('<dcterms:isReferencedBy rdf:resource="' + base_uri + '/text/' + parent_id + '"/>')


def referencing_fragment(person_id):
	global o
	global base_uri
	global edition_id
	ref = './tei:text//tei:persName[@ref="#' + person_id + '"]'
	for referencing_fragment in root.findall(ref, ns):
		parent = referencing_fragment.getparent()
		parent_id = parent.get('{http://www.w3.org/XML/1998/namespace}id')
		o.write('<rdf:Description rdf:about="' + base_uri + '/text/' + parent_id + '">')
		o.write('<rdf:type rdf:resource="http://iflastandards.info/ns/fr/frbr/frbroo/F23_Expression_Fragment"/>')
		o.write('<frbroo:R15i_is_fragment_of rdf:resource="' + base_uri + edition_id + '"/>')
		o.write('</rdf:Description>')


def perstype(person):
	global o
	listPerson = person.find('./...', ns)
	perstype = listPerson.get('type')
	perscorr = listPerson.get('corresp')
	if perstype is not None:
		o.write('<dcterms:description>' + perstype + '</dcterms:description>')
	if perscorr is not None and perscorr.startswith('http'):
		o.write('<dcterms:subject rdf:resource="' + perscorr + '"/>')


# Event


def partic_event(person):
	for event in person.findall('./tei:event', ns):
		event_id = event.get('{http://www.w3.org/XML/1998/namespace}id')
		if event is not None:
			o.write('<pro:holdsRoleInTime rdf:resource="' + base_uri + '/' + person_id + '-in-' + event_id + '"/>')


def role_in_event(person):
	global person_ref
	for event in person.findall('./tei:event', ns):
		event_id = event.get('{http://www.w3.org/XML/1998/namespace}id')
		persName = person.find('./tei:persName', ns)
		label = persName.text
		o.write('<rdf:Description rdf:about="' + base_uri + '/rit/' + person_id + '-at-' + event_id + '">')
		o.write('<rdf:type rdf:resource="http://purl.org/spar/pro/RoleInTime"/>')
		pers_in_event = event.find('./tei:desc/tei:persName', ns)
		if pers_in_event is not None and pers_in_event.get('ref') == person_ref and pers_in_event.get('role') is not None:
			o.write('<pro:withRole rdf:resource="' + base_uri + '/role/' + pers_in_event.get('role') + '"/>')
		else:
			o.write('<pro:withRole rdf:resource="' + base_uri + '/role/participant' + '"/>')
		o.write('<tvc:atTime rdf:resource="' + base_uri + '/tvc/' + event_id + '-time' + '"/>')
		o.write('<pro:relatesToEntity rdf:resource="' + base_uri + '/event/' + event_id + '"/>')
		place = event.find('./tei:desc/tei:placeName', ns)
		if place > 1:
			place_of_event = place.get('type="place_of_event"')
			o.write('<proles:relatesToPlace rdf:resource="' + base_uri + '/place/' + place.get('ref').replace("#", "") + '"/>')
		elif event.find('./tei:desc/tei:placeName', ns) == 1:
			o.write('<proles:relatesToPlace rdf:resource="' + base_uri + '/place/' + place.get('ref').replace("#", "") + '"/>')
		o.write('</rdf:Description>')	   


def role_desc(person):
	for event in person.findall('./tei:event', ns):
		event_id = event.get('{http://www.w3.org/XML/1998/namespace}id')
		pers_in_event = event.find('./tei:desc/tei:persName', ns)  
		if pers_in_event is not None and pers_in_event.get('ref') == person_ref and pers_in_event.get('role') is not None:
			o.write('<rdf:Description rdf:about="' + base_uri + '/role/' + pers_in_event.get('role') + '">')
			o.write('<rdf:type rdf:resource="http://purl.org/spar/pro/Role"/>')
		if pers_in_event is not None and pers_in_event.get('corresp') is not None:
			o.write('<owl:sameAs rdf:resource="' + pers_in_event.get('corresp') + '"/>')
			o.write('<rdfs:label>' + pers_in_event.get('role') + '</rdfs:label>')
		else:
			o.write('<rdf:Description rdf:about="' + base_uri + '/role/participant' + '">')
			o.write('<rdf:type rdf:resource="http://purl.org/spar/pro/Role"/>')
			o.write('<owl:sameAs rdf:resource="http://wordnet-rdf.princeton.edu/id/10421528-n"/>')
			o.write('<rdfs:label>participant</rdfs:label>')
		o.write('</rdf:Description>')


def event_time():
	for event in root.findall('.//tei:event', ns):
		event_id = event.get('{http://www.w3.org/XML/1998/namespace}id')
		o.write('<rdf:Description rdf:about="' + base_uri + '/' + event_id + '-time' '">')
		o.write('<rdf:type rdf:resource="http://www.ontologydesignpatterns.org/cp/owl/timeinterval.owl#TimeInterval"/>')
		if event.get('when') is not None:
			o.write('<owl:hasIntervalStartDate rdf:datatype="https://www.w3.org/TR/xmlschema11-2/#date">' + event.get('when') + '</owl:hasIntervalStartDate>')
			o.write('<owl:hasIntervalEndDate rdf:datatype="https://www.w3.org/TR/xmlschema11-2/#date">' + event.get('when') + '</owl:hasIntervalEndDate>')
		if event.get('from') is not None:
			o.write('<owl:hasIntervalStartDate rdf:datatype="https://www.w3.org/TR/xmlschema11-2/#date">' + event.get('from') + '</owl:hasIntervalStartDate>')
		if event.get('to') is not None:
			o.write('<owl:hasIntervalEndDate rdf:datatype="https://www.w3.org/TR/xmlschema11-2/#date">' + event.get('to') + '</owl:hasIntervalEndDate>')
		o.write('</rdf:Description>')


def event_desc():
	for event in root.findall('.//tei:event', ns):
		event_id = event.get('{http://www.w3.org/XML/1998/namespace}id')
		evtype = event.get('type')
		evcorr = event.get('corresp')
		o.write('<rdf:Description rdf:about="' + base_uri + '/event/' + event_id + '">')
		o.write('<rdf:type rdf:resource="http://www.cidoc-crm.org/cidoc-crm/E5_Event"/>')
		o.write('<rdf:type rdf:resource="https://schema.org/Event"/>')
		label = event.find('./tei:label', ns)
		if label is not None:
			o.write('<rdfs:label>' + label.text + '</rdfs:label>')
		source = event.find('./tei:bibl', ns)
		if source is not None:
			source_id = source.get('{http://www.w3.org/XML/1998/namespace}id')
			o.write('<prov:hasPrimarySource rdf:resource="' + base_uri + '/source/' + source_id + '"/>')
		if evtype is not None:
			o.write('<dcterms:description>' + evtype + '</dcterms:description>')
		if evcorr is not None and evcorr.startswith('http'):
			o.write('<dcterms:subject rdf:resource="' + evcorr + '"/>')
		o.write('</rdf:Description>')


def event_source():
	for eventSource in root.findall('.//tei:event//tei:bibl', ns):
		source_id = eventSource.get('{http://www.w3.org/XML/1998/namespace}id')
		o.write('<rdf:Description rdf:about="' + base_uri + '/source/' + source_id + '">')
		o.write('<rdf:type rdf:resource="http://www.w3.org/ns/prov#PrimarySource"/>')
		if eventSource.find('./tei:author', ns) is not None and eventSource.find('./tei:author', ns).get('ref') is not None:
			author_ref = eventSource.find('./tei:author', ns).get('ref')
			author_id = author_ref.split('#')
			o.write('<dcterms:creator rdf:resource="' + base_uri + '/person/' + author_id[1] + '"/>')
		if eventSource.find('.tei:title', ns) is not None:
			o.write('<dcterms:title>' + eventSource.find('.tei:title', ns).text + '</dcterms:title>')
		if eventSource.get('sameAs') is not None:
			sameAs = eventSource.get('sameAs')
			if sameAs.startswith('http'):
				o.write('<owl:sameAs rdf:resource="' + eventSource.get('sameAs') + '"/>') 
		if eventSource.find('.tei:date', ns) is not None:
			evdate = eventSource.find('.tei:date', ns)
			o.write('<dcterms:date rdf:datatype="https://www.w3.org/TR/xmlschema11-2/#date">' + evdate.get('when') + '</dcterms:date>')
		o.write('</rdf:Description>')


# Relation


def relation(person):
	for relation in root.findall('.//tei:listRelation/tei:relation', ns):
		person_ref = '#' + person_id
		if relation.get('active') is not None and relation.get('active') == person_ref:
			passive = relation.get('passive').replace("#", "").split()
			i = 0
			while i < len(passive):
				o.write('<agrelon:' + relation.get('name') + ' rdf:resource="' + base_uri + '/' + passive[i] + '"/>')
				i += 1
		elif relation.get('mutual') is not None:
			relentity = relation.get('mutual').split()
			if person_ref in relentity:
				mutual = relation.get('mutual').replace("#", "").replace(person_id, "").split()
				i = 0
				while i < len(mutual):
					o.write('<agrelon:' + relation.get('name') + ' rdf:resource="' + base_uri + '/' + mutual[i] + '"/>')
					i += 1


# Place


def place_subject(place):
	global place_id
	o.write('<rdf:Description rdf:about="' + base_uri + '/place/' + place_id + '">')


def place_sameas(place):
	sameAs = place.get('sameAs').split()
	i = 0
	while i < len(sameAs):
		o.write('<owl:sameAs rdf:resource="' + sameAs[i] + '"/>')
		i += 1


def placename(place):
	placeName = place.find('./tei:placeName', ns)
	label = placeName.text
	label_lang = placeName.get('{http://www.w3.org/XML/1998/namespace}lang')
	if label_lang is not None:
		o.write('<rdfs:label ' + 'xml:lang="' + label_lang + '">' + label + '</rdfs:label>')
	else:
		o.write('<rdfs:label>' + label + '</rdfs:label>')


def referenced_place(place_id):
	ref = './/tei:placeName[@ref="#' + place_id + '"]'
	for referenced_place in root.findall(ref, ns):
		parent = referenced_place.getparent()
		parent_id = parent.get('{http://www.w3.org/XML/1998/namespace}id')
		o.write('<dcterms:isReferencedBy rdf:resource="' + base_uri + '/text/' + parent_id + '"/>')


def referencing_fragment(place_id):
	ref = './/tei:placeName[@ref="#' + place_id + '"]'
	for referencing_fragment in root.findall(ref, ns):
		parent = referencing_fragment.getparent()
		parent_id = parent.get('{http://www.w3.org/XML/1998/namespace}id')
		o.write('<rdf:Description rdf:about="' + base_uri + '/text/' + parent_id + '">')
		o.write('<rdf:type rdf:resource="http://iflastandards.info/ns/fr/frbr/frbroo/F23_Expression_Fragment"/>')
		o.write('<frbroo:R15i_is_fragment_of rdf:resource="' + base_uri + edition_id + '"/>')
		o.write('</rdf:Description>')


for person in root.findall('.//tei:person', ns):
	person_id = person.get('{http://www.w3.org/XML/1998/namespace}id')
	person_ref = '#' + person_id
	subject(person)
	o.write('<rdf:type rdf:resource="https://schema.org/Person"/>')
	sameas(person)
	persname(person)
	referenced_person(person_id)
	perstype(person)
	partic_event(person)
	relation(person)
	o.write('</rdf:Description>')


for person in root.findall('.//tei:person', ns):
	person_id = person.get('{http://www.w3.org/XML/1998/namespace}id')
	person_ref = '#' + person_id
	referencing_fragment(person_id)


for person in root.findall('.//tei:person', ns):
	person_id = person.get('{http://www.w3.org/XML/1998/namespace}id')
	person_ref = '#' + person_id
	role_in_event(person)


for person in root.findall('.//tei:person', ns):
	person_id = person.get('{http://www.w3.org/XML/1998/namespace}id')
	person_ref = '#' + person_id
	role_desc(person)


event_time()


event_desc()


event_source()


for place in root.findall('.//tei:place', ns):
	place_id = place.get('{http://www.w3.org/XML/1998/namespace}id')
	place_ref = '#' + place_id
	place_subject(place)
	o.write('<rdf:type rdf:resource="https://schema.org/Place"/>')
	place_sameas(place)
	placename(place)
	referenced_place(place_id)
	o.write('</rdf:Description>')


for place in root.findall('.//tei:place', ns):
	place_id = place.get('{http://www.w3.org/XML/1998/namespace}id')
	place_ref = '#' + place_id
	referencing_fragment(place_id)


o.write('</rdf:RDF>')


o.close()