.. _output:

The RDF graph
============================

LIFT takes a TEI document and returns an RDF graph. The semantics of the RDF graph is predefined, but you can modify it to suit your needs. For example, you could choose to reuse different ontologies or create new transformation rules.

The semantics of LIFT's RDF graphs is defined by the following ontologies:

	- |CIDOC Conceptual Reference Model (CRM)| for representing persons and events
	- |Agent Relationship Ontology (AgRelOn)| for describing relationships between persons
	- |Dublin Core (DCTERMS)| for basic information about some entities
	- |Functional Requirements for Bibliographic Records object-oriented (FRBRoo)|, an extension of CIDOC CRM, for representing texts
	- |Web Ontology Language (OWL)| for establishing links to external resources such as authority files
	- |Publishing Roles Ontology (PRO)| for representing a person's role in the context of a specific event 
	- |Political Roles Ontology (PRoles)| for linking a specific place to a role 
	- |Time-indexed Value in Context (TVC)| for specyfing the duration of a role in the context of an event
	- |PROV Ontology (PROV-O)| for linking events to sources
	.. - |Critical Apparatus Ontology (CAO)| for representing critical apparatuses

This section compares the input TEI constructs with the corresponding RDF output to give you a better understanding of how LIFT creates your RDF triples. Please visit the above links to know more about each of the ontologies and properties reused in LIFT.

.. Persons

Persons
-----------

.. code-block:: xml
	:linenos:

	<?xml version="1.0" encoding="UTF-8"?>
	<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:base="https://example.org" xml:id="example_v1">
		<teiHeader>
			...
			<listPerson type="ancient-athenian-philosophers" corresp="http://dbpedia.org/class/yago/WikicatAncientAthenianPhilosophers">
				<person xml:id="Socr" sameAs="http://viaf.org/viaf/88039167">
					<persName xml:lang="en">Socrates</persName>
				</person>
			</listPerson>
			... 
		</teiHeader>
		<text> 
			... 
			<p xml:id="para02">Some text mentioning <persName ref="#Aristot">Aristotle</persName> and <placeName ref="#Sparta">Sparta</placeName> here.</p>    
			...
		</text>
	</TEI>



.. code-block:: ttl
	:linenos:

	<https://example.org/person/Aristot> a crm:E21_Person ;
		rdfs:label "Aristotle"@en ;
		owl:sameAs <http://dbpedia.org/resource/Aristotle>, <http://viaf.org/viaf/7524651> ;
		dcterms:description "ancient athenian philosophers" ;
		dcterms:subject <http://dbpedia.org/class/yago/WikicatAncientAthenianPhilosophers> ;
		dcterms:isReferencedBy <https://example.org/text/para02> .


.. Places

Places
--------

.. code-block:: xml
	:linenos:

	<?xml version="1.0" encoding="UTF-8"?>
	<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:base="https://example.org" xml:id="example_v1">
		<teiHeader>
			...
			<listPlace>
          		<place xml:id="Athens" sameAs="https://pleiades.stoa.org/places/579885">
            		<placeName xml:lang="en">Athens</placeName>
          		</place>
          		...
        	</listPlace>
			... 
		</teiHeader>
		<text> 
			... 
			<p xml:id="para01">Some text mentioning <persName ref="#Plat">Plato</persName> and <placeName ref="#Athens">Athens</placeName>.</p>    
			...
		</text>
	</TEI>

.. code-block:: ttl
	:linenos:

	<https://example.org/place/Athens> a crm:E53_Place ;
		rdfs:label "Athens"@en ;
		owl:sameAs <https://pleiades.stoa.org/places/579885> ;
		dcterms:isReferencedBy <https://example.org/text/para01> .

.. Relations (dep. Persons)

Relations
-----------

.. code-block:: xml
	:linenos:

	<?xml version="1.0" encoding="UTF-8"?>
	<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:base="https://example.org" xml:id="example_v1">
		<teiHeader>
			...
			<listPerson>
	          	<listRelation>
	            	<relation xml:id="rel01" name="hasStudent" active="#Socr" passive="#Plat #Xen #Criti"/>
	            	<relation xml:id="rel02" name="hasColleague" mutual="#Plat #Xen"/>
	         	</listRelation>
          		...
        	</listPerson>
			... 
		</teiHeader>
		...
	</TEI>


.. Unidir

.. code-block:: ttl
	:linenos:

	<https://example.org/person/Socr> a crm:E21_Person ;
		agrelon:hasStudent <https://example.org/person/Plat>, <https://example.org/person/Xen>, <https://example.org/person/Criti> .

.. Symm

.. code-block:: ttl
	:linenos:

	<https://example.org/person/Plat> a crm:E21_Person ;
		agrelon:hasColleague <https://example.org/person/Xen> .

.. Events (dep. Persons and Places)

Events
--------

.. code-block:: xml
	:linenos:

	<?xml version="1.0" encoding="UTF-8"?>
	<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:base="https://example.org" xml:id="example_v1">
		<teiHeader>
			...
			<listPerson type="ancient-athenian-philosophers" corresp="http://dbpedia.org/class/yago/WikicatAncientAthenianPhilosophers">
				<person xml:id="Socr" sameAs="http://viaf.org/viaf/88039167">
					...
					<event xml:id="ev01" type="trial" when="-0399" corresp="http://wordnet-rdf.princeton.edu/id/01198357-n">
              			<label>Socrates trial</label>
              			<desc xml:id="desc01">The trial of <persName ref="#Socr" role="defendant" corresp="http://wordnet-rdf.princeton.edu/id/09781524-n">Socrates</persName> for impiety and corruption of the youth took place in <placeName ref="#Athens">Athens</placeName> in <date when="-0399">399 B.C.</date></desc> <bibl xml:id="bibl01" sameAs="http://viaf.org/viaf/214045129"><author ref="#Plat">Plato</author> gives a contemporary account of the trial in his work titled <title ref="Apology_of_Socr">Apology of Socrates</title>.</bibl>
            		</event>
				</person>
			</listPerson>
			... 
		</teiHeader>  
		...
	</TEI>

.. code-block:: ttl
	:linenos:

	<https://example.org/event/ev01> a crm:E5_Event ;
		rdfs:label "Socrates trial" ;
		dcterms:description "trial" ;
    	dcterms:subject <http://wordnet-rdf.princeton.edu/id/01198357-n> ;
    	prov:hadPrimarySource <https://example.org/source/bibl01> .

   	<https://example.org/source/bibl01> a prov:PrimarySource ;
		dcterms:creator <https://example.org/person/Plat> ;
		dcterms:title "Apology of Socrates" ;
		owl:sameAs <http://viaf.org/viaf/214045129> .

.. Roles (dep. Persons, Events and Places)

.. Same TEI input as above

.. code-block:: ttl
	:linenos:

	<https://example.org/person/Socr> a crm:E21_Person ;
		pro:holdsRoleInTime <https://example.org/Socr-in-ev01> .

	<https://example.org/rit/Socr-at-ev01> a pro:RoleInTime ;
    	pro:relatesToEntity <https://example.org/event/ev01> ;
		pro:withRole <https://example.org/role/defendant> ;
		tvc:atTime <https://example.org/ev01-time> ;
		proles:relatesToPlace <https://example.org/place/Athens> .

	<https://example.org/ev01-time> a <http://www.ontologydesignpatterns.org/cp/owl/timeinterval.owl#TimeInterval> ;
		ti:hasIntervalEndDate "-0399"^^xsd:date ;
		ti:hasIntervalStartDate "-0399"^^xsd:date .

	<https://example.org/role/defendant> a pro:Role ;
		rdfs:label "defendant" ;
		owl:sameAs <http://wordnet-rdf.princeton.edu/id/09781524-n> .







.. All links

.. |AgRelOn| raw:: html
	
	<a href="https://d-nb.info/standards/elementset/agrelon" target="_blank">AgRelOn</a>

.. |CIDOC Conceptual Reference Model (CRM)| raw:: html
	
	<a href="http://www.cidoc-crm.org/cidoc-crm/" target="_blank">CIDOC Conceptual Reference Model (CRM)</a>

.. |DCMI Metadata Terms (DCTERMS)| raw:: html
	
	<a href="http://purl.org/dc/terms/" target="_blank">DCMI Metadata Terms (DCTERMS)</a>

.. |Functional Requirements for Bibliographic Records object-oriented (FRBRoo)| raw:: html
	
	<a href="http://iflastandards.info/ns/fr/frbr/frbroo/" target="_blank">Functional Requirements for Bibliographic Records object-oriented (FRBRoo)</a>

.. |Web Ontology Language (OWL)| raw:: html
	
	<a href="http://www.w3.org/2002/07/owl#" target="_blank">Web Ontology Language (OWL)</a>

.. |Publishing Roles Ontology (PRO)| raw:: html
	
	<a href="http://purl.org/spar/pro/" target="_blank">Publishing Roles Ontology (PRO)</a>

.. |Political Roles Ontology (PRoles)| raw:: html
	
	<a href="http://www.essepuntato.it/2013/10/politicalroles/" target="_blank">Political Roles Ontology (PRoles)</a>

.. |PROV Ontology (PROV-O)| raw:: html
	
	<a href="http://www.w3.org/ns/prov#" target="_blank">PROV Ontology (PROV-O)</a>

.. |Schema.org| raw:: html
	
	<a href="https://schema.org/" target="_blank">Schema.org</a>

.. |Time-indexed Value in Context (TVC)| raw:: html
	
	<a href="http://www.essepuntato.it/2012/04/tvc/" target="_blank">Time-indexed Value in Context (TVC)</a>

.. |"Prepare your TEI XML edition for transformation"| raw:: html

	<a href="https://linked-data-from-tei.readthedocs.io/en/latest/input.html" target="_blank">"Prepare your TEI XML edition for transformation"</a>

.. |"1. Provide all TEI elements with unique identifiers"| raw:: html

	<a href="https://linked-data-from-tei.readthedocs.io/en/latest/input.html#provide-all-tei-elements-with-unique-identifiers" target="_blank">"1. Provide all TEI elements with unique identifiers"</a>

..	|Critical Apparatus Ontology (CAO)| raw:: html

	<a href="https://w3id.org/cao" target="_blank">Critical Apparatus Ontology (CAO)</a>



