import sys
reload(sys)
sys.setdefaultencoding('utf8')


from lxml import etree
tree = etree.parse('input.xml')


ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
root = tree.getroot()
base_uri = root.get('{http://www.w3.org/XML/1998/namespace}base')


o = open('output1.rdf', mode='w')


o.write('<?xml version="1.0" encoding="UTF-8"?>')
o.write('''<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/"
         xmlns:frbroo="http://iflastandards.info/ns/fr/frbr/frbroo/"
         xmlns:owl="http://www.w3.org/2002/07/owl#"
         xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
         xmlns:schema="https://schema.org/"
         xmlns:tei="http://www.tei-c.org/ns/1.0">''')


def subject(person):
    o.write('<rdf:Description rdf:about="' + base_uri + '/person/' + person_id + '">')


def sameas(person):
    sameAs = person.get('sameAs').split()
    i = 0
    while i < len(sameAs):
        o.write('<owl:sameAs rdf:resource="' + sameAs[i] + '"/>')
        i += 1


def persname(person):
    persName = person.find('./tei:persName', ns)
    label = persName.text
    label_lang = persName.get('{http://www.w3.org/XML/1998/namespace}lang')
    if label_lang is not None:
        o.write('<rdfs:label ' + 'xml:lang="' + label_lang + '">' + label + '</rdfs:label>')
    else:
        o.write('<rdfs:label>' + label + '</rdfs:label>')


def referenced_person(person_id):
    ref = './tei:text//tei:persName[@ref="#' + person_id + '"]'
    for referenced_person in root.findall(ref, ns):
        parent = referenced_person.getparent()
        parent_id = parent.get('{http://www.w3.org/XML/1998/namespace}id')
        o.write('<dcterms:isReferencedBy rdf:resource="' + base_uri + '/text/' + parent_id + '"/>')


def referencing_fragment(person_id):
    ref = './tei:text//tei:persName[@ref="#' + person_id + '"]'
    for referencing_fragment in root.findall(ref, ns):
        parent = referencing_fragment.getparent()
        parent_id = parent.get('{http://www.w3.org/XML/1998/namespace}id')
        o.write('<rdf:Description rdf:about="' + base_uri + '/text/' + parent_id + '">')
        o.write('<rdf:type rdf:resource="http://iflastandards.info/ns/fr/frbr/frbroo/F23_Expression_Fragment"/>')
        o.write('<frbroo:R15i_is_fragment_of rdf:resource="' + base_uri + '"/>')
        o.write('</rdf:Description>')


def perstype(person):
    listPerson = person.find('./...', ns)
    perstype = listPerson.get('type')
    perscorr = listPerson.get('corresp')
    if perstype is not None:
        o.write('<dcterms:description>' + perstype + '</dcterms:description>')
    if perscorr is not None and perscorr.startswith('http'):
        o.write('<dcterms:subject rdf:resource="' + perscorr + '"/>')


for person in root.findall('.//tei:person', ns):
    person_id = person.get('{http://www.w3.org/XML/1998/namespace}id')
    person_ref = '#' + person_id
    subject(person)
    o.write('<rdf:type rdf:resource="https://schema.org/Person"/>')
    sameas(person)
    persname(person)
    referenced_person(person_id)
    perstype(person)
    o.write('</rdf:Description>')


for person in root.findall('.//tei:person', ns):
    person_id = person.get('{http://www.w3.org/XML/1998/namespace}id')
    person_ref = '#' + person_id
    referencing_fragment(person_id)


o.write('</rdf:RDF>')


o.close()