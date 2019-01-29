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
         xmlns:frbroo="http://iflastandards.info/ns/fr/frbr/frbroo/"
         xmlns:owl="http://www.w3.org/2002/07/owl#"
         xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
         xmlns:schema="https://schema.org/"
         xmlns:tei="http://www.tei-c.org/ns/1.0">''')


def subject(place):
    global o
    global base_uri
    global place_id
    o.write('<rdf:Description rdf:about="' + base_uri + '/place/' + place_id + '">')


def sameas(place):
    global o
    sameAs = place.get('sameAs').split()
    i = 0
    while i < len(sameAs):
        o.write('<owl:sameAs rdf:resource="' + sameAs[i] + '"/>')
        i += 1


def placename(place):
    global o
    global ns
    placeName = place.find('./tei:placeName', ns)
    label = placeName.text
    label_lang = placeName.get('{http://www.w3.org/XML/1998/namespace}lang')
    if label_lang is not None:
        o.write('<rdfs:label ' + 'xml:lang="' + label_lang + '">' + label + '</rdfs:label>')
    else:
        o.write('<rdfs:label>' + label + '</rdfs:label>')


def referenced_place(place_id):
    global o
    global root
    ref = './/tei:placeName[@ref="#' + place_id + '"]'
    for referenced_place in root.findall(ref, ns):
        parent = referenced_place.getparent()
        parent_id = parent.get('{http://www.w3.org/XML/1998/namespace}id')
        o.write('<dcterms:isReferencedBy rdf:resource="' + base_uri + '/text/' + parent_id + '"/>')


def referencing_fragment(place_id):
    global o
    global base_uri
    global edition_id
    ref = './/tei:placeName[@ref="#' + place_id + '"]'
    for referencing_fragment in root.findall(ref, ns):
        parent = referencing_fragment.getparent()
        parent_id = parent.get('{http://www.w3.org/XML/1998/namespace}id')
        o.write('<rdf:Description rdf:about="' + base_uri + '/text/' + parent_id + '">')
        o.write('<rdf:type rdf:resource="http://iflastandards.info/ns/fr/frbr/frbroo/F23_Expression_Fragment"/>')
        o.write('<frbroo:R15i_is_fragment_of rdf:resource="' + base_uri + edition_id + '"/>')
        o.write('</rdf:Description>')


for place in root.findall('.//tei:place', ns):
    place_id = place.get('{http://www.w3.org/XML/1998/namespace}id')
    place_ref = '#' + place_id
    subject(place)
    o.write('<rdf:type rdf:resource="https://schema.org/Place"/>')
    sameas(place)
    placename(place)
    referenced_place(place_id)
    o.write('</rdf:Description>')


for place in root.findall('.//tei:place', ns):
    place_id = place.get('{http://www.w3.org/XML/1998/namespace}id')
    place_ref = '#' + place_id
    referencing_fragment(place_id)


o.write('</rdf:RDF>')


o.close()