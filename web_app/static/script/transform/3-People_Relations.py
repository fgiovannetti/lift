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
         xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
         xmlns:schema="https://schema.org/"
         xmlns:tei="http://www.tei-c.org/ns/1.0">''')


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


for person in root.findall('.//tei:person', ns):
    person_id = person.get('{http://www.w3.org/XML/1998/namespace}id')
    person_ref = '#' + person_id
    subject(person)
    o.write('<rdf:type rdf:resource="https://schema.org/Person"/>')
    sameas(person)
    persname(person)
    referenced_person(person_id)
    perstype(person)
    relation(person)
    o.write('</rdf:Description>')


for person in root.findall('.//tei:person', ns):
    person_id = person.get('{http://www.w3.org/XML/1998/namespace}id')
    person_ref = '#' + person_id
    referencing_fragment(person_id)


o.write('</rdf:RDF>')

o.close()