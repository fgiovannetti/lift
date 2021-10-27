
from lxml import etree


tree = etree.parse('input.xml')


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
tvc = Namespace("http://www.essepuntato.it/2012/04/tvc/")


g = Graph()


g.bind("agrelon", agrelon)
g.bind("crm", crm)
g.bind("frbroo", frbroo)
g.bind("dcterms", DCTERMS)
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
    g.add( (person_uri, RDF.type, crm.E21_Person))
    
    # same as
    same_as = person.get('sameAs')
    if same_as is not None:
        same_as = same_as.split()
        i = 0
        while i < len(same_as):
            same_as_uri = URIRef(same_as[i])
            g.add( (person_uri, OWL.sameAs, same_as_uri))
            i += 1
    
    # person name
    persname = person.find('./tei:persName', tei)
    if persname is not None:
        label = persname.text
        label_lang = persname.get('{http://www.w3.org/XML/1998/namespace}lang')
        if label_lang is not None:
            g.add( (person_uri, RDFS.label, Literal(label, lang=label_lang)))
        else:
            g.add( (person_uri, RDFS.label, Literal(label)))
    
    # person type
    listperson = person.find('./...', tei)
    perstype = listperson.get('type').replace('-',' ')
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

    

# RDF/XML output
g.serialize(destination="output.rdf", format='xml')

# Notation3 output
g.serialize(destination="output.n3", format='n3')

# N-triples output
g.serialize(destination="output.nt", format='nt')

# Json-ld output
g.serialize(destination='output.jsonld', format='json-ld')