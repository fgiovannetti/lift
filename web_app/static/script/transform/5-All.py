from lxml import etree


tree = etree.parse('static/temp/input.xml')


root = tree.getroot()


base_uri = root.get('{http://www.w3.org/XML/1998/namespace}base')
edition_id = root.get('{http://www.w3.org/XML/1998/namespace}id')


tei = {'tei': 'http://www.tei-c.org/ns/1.0'}


from rdflib import Graph, Literal, BNode, Namespace, URIRef


from rdflib.namespace import RDF, RDFS, XSD, DCTERMS, OWL


agrelon = Namespace("https://d-nb.info/standards/elementset/agrelon#")
crm = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
frbroo = Namespace("http://iflastandards.info/ns/fr/frbr/frbroo/")
pro = Namespace("http://purl.org/spar/pro/")
proles = Namespace("http://www.essepuntato.it/2013/10/politicalroles/")
prov = Namespace("http://www.w3.org/ns/prov#")
schema = Namespace("https://schema.org/")
tvc = Namespace("http://www.essepuntato.it/2012/04/tvc/")


g = Graph()


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









#############################
#                           #
#        Persons            #
#                           #
#############################

for person in root.findall('.//tei:person', tei):
    person_id = person.get('{http://www.w3.org/XML/1998/namespace}id')
    person_uri = URIRef(base_uri + '/person/' + person_id)
    person_ref = '#' + person_id
    
    # person 
    g.add( (person_uri, RDF.type, schema.Person))
    
    # same as
    same_as = person.get('sameAs').split()
    i = 0
    while i < len(same_as):
        same_as_uri = URIRef(same_as[i])
        g.add( (person_uri, OWL.sameAs, same_as_uri))
        i += 1
    
    # person name
    persname = person.find('./tei:persName', tei)
    label = persname.text
    label_lang = persname.get('{http://www.w3.org/XML/1998/namespace}lang')
    if label_lang is not None:
        g.add( (person_uri, RDFS.label, Literal(label, lang=label_lang)))
    else:
        g.add( (person_uri, RDFS.label, Literal(label)))
    
    # person type
    listperson = person.find('./...', tei)
    perstype = listperson.get('type')
    perscorr = listperson.get('corresp')
    if perstype is not None:
        g.add( (person_uri, DCTERMS.description, Literal(perstype)))
    if perscorr is not None and perscorr.startswith('http'):
        g.add( (person_uri, DCTERMS.subject, URIRef(perscorr)))

    # value

    value = etree.tostring(person, pretty_print=True, method="xml")
    g.add( (person_uri, RDF.value, Literal(value, datatype=RDF.XMLLiteral)) )
    
    # person references
    ref = './tei:text//tei:persName[@ref="#' + person_id + '"]'
    for referenced_person in root.findall(ref, tei):
        parent = referenced_person.getparent()
        parent_id = parent.get('{http://www.w3.org/XML/1998/namespace}id')
        parent_uri = URIRef(base_uri + '/text/' + parent_id)
        g.add( (person_uri, DCTERMS.isReferencedBy, parent_uri))
        g.add( (parent_uri, RDF.type, frbroo.F23_Expression_Fragment))
        g.add( (parent_uri, frbroo.R15i_is_fragment_of, URIRef(base_uri + '/' + edition_id)))
        # value
        value = etree.tostring(parent, pretty_print=True, method="xml")
        g.add( (parent_uri, RDF.value, Literal(value, datatype=RDF.XMLLiteral)) )











#############################
#                           #
#        Events             #
#                           #
#############################


for person in root.findall('.//tei:person', tei):
    person_id = person.get('{http://www.w3.org/XML/1998/namespace}id')
    person_uri = URIRef(base_uri + '/person/' + person_id)
    person_ref = '#' + person_id
    for event in person.findall('./tei:event', tei):
        event_id = event.get('{http://www.w3.org/XML/1998/namespace}id')
        event_uri = URIRef(base_uri + '/event/' + event_id)  
        rit_uri = URIRef(base_uri + '/rit/' + person_id + '-at-' + event_id)
        
        #partic_event(person)
        partic_event_uri = URIRef(base_uri + '/' + person_id + '-in-' + event_id)
        g.add( (person_uri, pro.holdsRoleInTime, partic_event_uri))

        #role_in_event(person)
        g.add( (rit_uri, RDF.type, pro.RoleInTime))
        pers_in_event = event.find('./tei:desc/tei:persName', tei)
        if pers_in_event is not None and pers_in_event.get('ref') == person_ref and pers_in_event.get('role') is not None:
            role_uri = URIRef(base_uri + '/role/' + pers_in_event.get('role'))
            g.add( (rit_uri, pro.withRole, role_uri))
            g.add( (role_uri, RDF.type, pro.Role))
            g.add( (role_uri, RDFS.label, Literal(pers_in_event.get('role'))))
            if pers_in_event.get('corresp') is not None:
                corresp_role_uri = URIRef(pers_in_event.get('corresp'))
                g.add( (role_uri, OWL.sameAs, corresp_role_uri)) 
            else:
                g.add( (rit_uri, pro.withRole, URIRef(base_uri + '/role/participant')))
                role_uri = URIRef(base_uri + '/role/participant')
                g.add( (role_uri, RDF.type, pro.Role))
                g.add( (role_uri, OWL.sameAs, URIRef('http://wordnet-rdf.princeton.edu/id/10421528-n')))
                g.add( (role_uri, RDFS.label, Literal('participant')))    

        #event_time()
        event_time_uri = URIRef(base_uri + '/' + event_id + '-time')
        g.add( (rit_uri, tvc.atTime, event_time_uri))
        g.add( (event_time_uri, RDF.type, URIRef('http://www.ontologydesignpatterns.org/cp/owl/timeinterval.owl#TimeInterval')))
        if event.get('when') is not None:
            g.add( (event_time_uri, OWL.hasIntervalStartDate, Literal(event.get('when'), datatype=XSD.date)))
            g.add( (event_time_uri, OWL.hasIntervalEndDate, Literal(event.get('when'), datatype=XSD.date)))
        if event.get('from') is not None:
            g.add( (event_time_uri, OWL.hasIntervalStartDate, Literal(event.get('from'), datatype=XSD.date)))
        if event.get('to') is not None:
            g.add( (event_time_uri, OWL.hasIntervalEndDate, Literal(event.get('to'), datatype=XSD.date)))

        #event_desc()
        g.add( (rit_uri, pro.relatesToEntity, URIRef(base_uri + '/event/' + event_id)))
        g.add( (event_uri, RDF.type, crm.E5_Event))
        g.add( (event_uri, RDF.type, schema.Event))
        if event.find('./tei:label', tei) is not None:
            label = event.find('./tei:label', tei).text
            g.add( (event_uri, RDFS.label, Literal(label)))
        if event.get('type') is not None:
            g.add( (event_uri, DCTERMS.description, Literal(event.get('type'))))
        if event.get('corresp') is not None and event.get('corresp').startswith('http'):
            g.add( (event_uri, DCTERMS.subject, URIRef(event.get('corresp'))))

        #event_place()
        place = event.find('./tei:desc/tei:placeName', tei)
        if place > 1:
            place_of_event = place.get('type="place_of_event"')
            g.add( (rit_uri, proles.relatesToPlace, URIRef(base_uri + '/place/' + place.get('ref').replace("#", ""))))
        elif event.find('./tei:desc/tei:placeName', tei) == 1:
            g.add( (rit_uri, proles.relatesToPlace, URIRef(base_uri + '/place/' + place.get('ref').replace("#", ""))))  

        #event_source()
        source = event.find('./tei:bibl', tei)
        if source is not None:
            source_id = source.get('{http://www.w3.org/XML/1998/namespace}id')
            source_uri = URIRef(base_uri + '/source/' + source_id)
            g.add( (event_uri, prov.hadPrimarySource, source_uri))
            g.add( (source_uri, RDF.type, prov.PrimarySource))
            if source.find('./tei:author', tei) is not None and source.find('./tei:author', tei).get('ref') is not None:
                author_ref = source.find('./tei:author', tei).get('ref')
                author_id = author_ref.split('#')
                g.add( (source_uri, DCTERMS.creator, URIRef(base_uri + '/person/' + author_id[1])))
            if source.find('.tei:title', tei) is not None:
                g.add( (source_uri, DCTERMS.title, Literal(source.find('.tei:title', tei).text)))
            if source.find('.tei:date', tei) is not None:
                evdate = source.find('.tei:date', tei)
                g.add( (source_uri, DCTERMS.date, Literal(evdate.get('when'), datatype=XSD.date)))
            if source.get('sameAs') is not None:
                sameAs = source.get('sameAs')
                if sameAs.startswith('http'):
                    g.add( (source_uri, OWL.sameAs, URIRef(source.get('sameAs')))) 

        # value
        value = etree.tostring(event, pretty_print=True, method="xml")
        g.add( (event_uri, RDF.value, Literal(value, datatype=RDF.XMLLiteral)) )







#############################
#                           #
#        Relations          #
#                           #
#############################



for person in root.findall('.//tei:person', tei):
    person_id = person.get('{http://www.w3.org/XML/1998/namespace}id')
    person_uri = URIRef(base_uri + '/person/' + person_id)
    person_ref = '#' + person_id
    for relation in root.findall('.//tei:listRelation/tei:relation', tei):
        if relation.get('active') is not None and relation.get('active') == person_ref:
            passive = relation.get('passive').replace("#", "").split()
            i = 0
            while i < len(passive):
                g.add( (person_uri, agrelon[relation.get('name')], URIRef(base_uri + '/' + passive[i])))
                i += 1
        elif relation.get('mutual') is not None:
            if person_ref in relation.get('mutual').split():
                mutual = relation.get('mutual').replace("#", "").replace(person_id, "").split()
                i = 0
                while i < len(mutual):
                    g.add( (person_uri, agrelon[relation.get('name')], URIRef(base_uri + '/' + mutual[i])))
                    i += 1

        # value
        value = etree.tostring(relation, pretty_print=True, method="xml")
        g.add( (person_uri, RDF.value, Literal(value, datatype=RDF.XMLLiteral)) )







#############################
#                           #
#        Places             #
#                           #
#############################


for place in root.findall('.//tei:place', tei):
    place_id = place.get('{http://www.w3.org/XML/1998/namespace}id')
    place_uri = URIRef(base_uri + '/place/' + place_id)
    place_ref = '#' + place_id
    
    #place
    g.add( (place_uri, RDF.type, schema.Place))
    
    #place_sameas(place)
    same_as = place.get('sameAs').split()
    i = 0
    while i < len(same_as):
        same_as_uri = URIRef(same_as[i])
        g.add( (place_uri, OWL.sameAs, same_as_uri))
        i += 1

    #placename(place)
    placename = place.find('./tei:placeName', tei)
    label = placename.text
    label_lang = placename.get('{http://www.w3.org/XML/1998/namespace}lang')
    if label_lang is not None:
        g.add( (place_uri, RDFS.label, Literal(label, lang=label_lang)))
    else:
        g.add( (place_uri, RDFS.label, Literal(label)))
    # value
        value = etree.tostring(place, pretty_print=True, method="xml")
        g.add( (place_uri, RDF.value, Literal(value, datatype=RDF.XMLLiteral)) )


    #referenced_place(place_id)
    ref = './/tei:placeName[@ref="#' + place_id + '"]'
    for referenced_place in root.findall(ref, tei):
        parent = referenced_place.getparent()
        parent_id = parent.get('{http://www.w3.org/XML/1998/namespace}id')
        parent_uri = URIRef(base_uri + '/text/' + parent_id)
        g.add( (place_uri, DCTERMS.isReferencedBy, parent_uri))
        g.add( (parent_uri, RDF.type, frbroo.F23_Expression_Fragment))
        g.add( (parent_uri, frbroo.R15i_is_fragment_of, URIRef(base_uri + '/' + edition_id)))

        # value
        value = etree.tostring(parent, pretty_print=True, method="xml")
        g.add( (parent_uri, RDF.value, Literal(value, datatype=RDF.XMLLiteral)) )


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