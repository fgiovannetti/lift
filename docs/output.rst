.. _output:

.. Persons

Persons
-----------

Test

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

	<https://example.org/person/Socr> a schema:Person ;
    	pro:holdsRoleInTime <https://example.org/Socr-in-ev01> .

    <https://example.org/rit/Socr-at-ev01> a pro:RoleInTime ;
    	pro:relatesToEntity <https://example.org/event/ev01> ;
    	pro:withRole <https://example.org/role/defendant> ;
    	tvc:atTime <https://example.org/ev01-time> ;
    	proles:relatesToPlace <https://example.org/place/Athens> .

    <https://example.org/ev01-time> a <http://www.ontologydesignpatterns.org/cp/owl/timeinterval.owl#TimeInterval> ;
    	owl:hasIntervalEndDate "-0399"^^xsd:date ;
    	owl:hasIntervalStartDate "-0399"^^xsd:date .

    <https://example.org/role/defendant> a pro:Role ;
    	rdfs:label "defendant" ;
    	owl:sameAs <http://wordnet-rdf.princeton.edu/id/09781524-n> .

