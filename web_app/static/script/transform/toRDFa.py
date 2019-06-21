import sys
reload(sys)
sys.setdefaultencoding('utf8')


from lxml import etree


tree = etree.parse('static/temp/output.rdf')



ns = {'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#', 
      'rdfs': 'http://www.w3.org/2000/01/rdf-schema#', 
      'xmlns' : 'http://www.w3.org/1999/xhtml'}


v = open('static/temp/viz.html', mode='w')


root = tree.getroot()


v.write('''<div xmlns="http://www.w3.org/1999/xhtml" 
    xmlns:dcterms="http://purl.org/dc/terms/" 
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


nodes = root.findall('./rdf:Description', ns)
for node in nodes:
    newroot = etree.Element('div')
    about = node.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about')
    target = '_blank'
    newroot.set('style', 'margin-bottom:15px' ) 
    newroot.set('resource', about)
    
    lis = []
    for rdftype in node.findall('./rdf:type', ns):
        typeof = rdftype.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource')
        lis.append(typeof)
    typeof = " ".join(lis)
    newroot.set('typeof', typeof)
    
    opangle = etree.SubElement(newroot, 'span')
    opangle.text = '<' 
    subject = etree.SubElement(newroot, 'a')
    subject.set('href', about)
    subject.set('target', target)
    subject.text = about
    clangle = etree.SubElement(newroot, 'span')
    clangle.text = '>' 
    
    label = node.find('{http://www.w3.org/2000/01/rdf-schema#}label')
    if label is not None:
        slabel = etree.SubElement(newroot, 'span')
        slabel.set('style', 'color: orange')
        slabel.text = ' # ' + label.text
    
    etree.SubElement(newroot, 'br')
    a = etree.SubElement(newroot, 'span')
    a.set('style', 'margin-left:2rem;')
    a.text = 'a '
    
    classdecl = etree.SubElement(newroot, 'a')
    
    list2=[]
    for i in lis:
            i = '<' + str(i) + '>'
            list2.append(i)

    classdecl.set('href', typeof)
    classdecl.set('target', target)
    
    lis2=[]
    for i in lis:
            i = '<' + str(i) + '>'
            lis2.append(i)
    typeof = " , ".join(lis2)
    classdecl.text = typeof
    
    semic = etree.SubElement(newroot, 'span')
    semic.text = ' ;'
    etree.SubElement(newroot, 'br')
    
    # all properties except rdf:type and rdfs:label
    children = node.getchildren()
    for child in children:
        c = child.prefix + ':' + etree.QName(child.tag).localname  
        if c != 'rdf:type' and c != 'rdfs:label':
            prop = etree.SubElement(newroot, 'a')
            prop.set('style', 'text-decoration:none;padding-right:0.3rem;margin-left:2rem;' )
            url = str(child.tag).replace('{', '').replace('}', '')
            prop.set('href', url )
            prop.set('target', target)
            prop.text = c
            if child.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource') is not None:
                opangle = etree.SubElement(newroot, 'span')
                opangle.text = '<' 
                val = etree.SubElement(newroot, 'a')
                value = child.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource')
                val.set('href',  value )
                val.set('target', target)
                val.set('property', c)
                val.set('resource', value)
                clangle = etree.SubElement(newroot, 'span')
                clangle.text = '>' 
            else:
                quot = etree.SubElement(newroot, 'span')
                quot.text = '"'
                val = etree.SubElement(newroot, 'span')
                val.set('style',  'color:red' )
                val.set('property',  c )
                value = child.text
                quot = etree.SubElement(newroot, 'span')
                quot.text = '"'
            val.text = value
            semic = etree.SubElement(newroot, 'span')
            semic.text = ' ;' 
            etree.SubElement(newroot, 'br')

    v.write(etree.tostring(newroot))


v.write('</div>')

v.close()




