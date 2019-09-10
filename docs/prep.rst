
Prepare your TEI XML edition for transformation
===============================================


TEI allows different ways to encode the same textual features. A trivial example is the possibility to validly mark up a person name using the tags :code:`<persName>`, :code:`<name>`, or :code:`<rs>` (|TEI Guidelines, 13. Names, Dates, People, and Places|).

Despite its important advantages, such a heterogeneity makes it challenging to develop transformation scripts that adapt to any encoding model.

On this account, in order to ensure a correct functioning of the transformation script, it is necessary to follow specific encoding guidelines to prepare the input TEI XML document for transformation via LIFT. 

1. Provide all TEI elements with unique identifiers 
---------------------------------------------------

Each entity within a linked data graph is uniquely represented by a URI. LIFT transforms a TEI element unique identifier (defined through the attribute :code:`@xml:id`) into an entity URI by concatenating the TEI document base URI (defined on the :code:`<TEI>` element through the attribute :code:`@xml:base`) with the element unique identifier. 

For example, from this TEI input

.. code-block:: xml

	<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:base="https://example.org">
		...
		<person xml:id="socr">...</person>
		...
	</TEI>

we obtain the following person URI: <https://example.org/person/socr>.

Make sure you create a permanent URL for your edition (we have used the domain example.org for example purposes only). Check the |W3C Permanent Identifier Community Group| for more information.  

If your TEI document does not already contain unique identifiers, you can run |this XSLT transformation| on your document. The script, originally provided by Charlotte Tupman for the |SAWS project|, creates a unique identifier for each element that does not have an :code:`@xml:id`.

Once downloaded to your TEI project folder, you can run the transformation stylesheet via xsltproc (see |xsltproc tutorial|, last accessed 2019-09-09), a command line tool for applying XSLT stylesheets to XML documents.

.. Add instructions for XSLT other than xsltproc stylesheet file in OSX Terminal


.. People

2. Use <person> and <persName> for a person
-------------------------------------------

Every personal name cited in the TEI text should be marked up as a :code:`<persName>`. The attribute :code:`@ref` should be used to relate such a personal name to the unique identifier of the person. 

A description of each person (intended as a real-world entity) should be included in the TEI header within an element :code:`<person>`, to which a unique identifier is assigned for reference later. In order to define a standard label for the person, a :code:`<persName>` can be nested within the :code:`<person>` element. Multiple labels can be specified. Use :code:`@xml:lang` to specify the language (refer to the |ISO 639 list| of language codes). For example:

.. code-block:: xml

	<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:base="https://example.org">
		<teiHeader>
		...
			<person xml:id="socr">
				<persName xml:lang="en">Socrates</persName>
				<persName xml:lang="el">Σωκρᾰ́της</persName>
			</person>
		...
		</teiHeader>
		<text>
		...
			<persName ref="#socr">Socrates</persName>
		...
		</text>
	</TEI>

It is possible to nest a set of :code:`<person>` elements within a :code:`<listPerson>`. The attributes @type and/or @corresp can be assigned to a <listPerson> (or even to a single <person>) to provide a description: @type is used for a literal description, with each word separated by an hyphen; @corresp is used to provide an external URL. For example:

.. code-block:: xml

	<listPerson type="ancient-athenian-philosophers" corresp="http://dbpedia.org/class/yago/WikicatAncientAthenianPhilosophers">
		<person xml:id="Socr">
		...

3. Use <place> and <placeName> for a place
------------------------------------------

The same instructions as above are also valid for places. For example:

.. code-block:: xml

	<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:base="https://example.org">
		<teiHeader>
		...
			<place xml:id="athens">
				<placeName xml:lang="en">Athens</placeName>
			</place>
		...
		</teiHeader>
		<text>
		...
			<placeName ref="#athens">Athens</persName>
		...
		</text>
	</TEI>

4. Assign a @sameAs to disambiguate your entity
-----------------------------------------------

In order to disambiguate your named entities so to create meaningful connections between your linked data graph and related resources on the web, you should associate a permanent URI to your person or place. Such a URI should be provided by an authority record, such as |VIAF|, |Worldcat|, or the |Library of Congress|. 

The servise |sameas.org| can help you find equivalent URIs.

You can use a @sameAs attribute to store your URIs, separated by whitespaces. For example:

.. code-block:: xml
	
	<person xml:id="Socr" sameAs="http://viaf.org/viaf/88039167">

5. Express personal relationships through <listRelation>
--------------------------------------------------------

Use the element :code:`<relation>` nested within a :code:`<listRelation>` to mark up personal relationships. Note that :code:`<listRelation>` should be a child of :code:`<listPerson>`. 

For a unidirectional relation, you should use the attributes :code:`@active` and :code:`@passive` to define the subject and the object of the relationship (e.g. Socrates has student Plato); for bidirectional relationships you should use the attribute :code:`@mutual` (e.g. Plato has colleague Xenophon). It is possible to express multiple values separated by whitespaces. 

The @name attribute is used to express the nature of the relationship. Use terms from |AgRelOn| (Agent Relationship Ontology).  

For example:

.. code-block:: xml

	<listRelation>
		<relation xml:id="rel01" name="hasStudent" active="#socr" passive="#plat #xen #criti"/>
		<relation xml:id="rel02" name="hasColleague" mutual="#plat #xen"/>
	</listRelation>

6. Use <event> for an event, either within <person> or <place>
--------------------------------------------------------------

Accounts of events may be included within a related <person> elements or <place> element. The element <event> holds the entire event account. The attributes @type and @corresp can be used to describe the event using a textual label and a URI respectively (the example below uses the URI for the concept of "trial" provided by Wordnet).

An event's time can be marked up either using @when or @from/@to. Date should be represented using the |ISO 8601 standard|.

The element <label> can be used to provide a short textual description of the event, while the element <desc> can contain a extended account of the event including detailed information such as personal names (marked up with <persName>), locations (marked up with <placeName>), times (marked up with <date>).

It is possible to specify the role held by the person in the event through the attribute @role and/or through the attribute @corresp on <persName>. As before, @corresp should contain a URI representing the role.  

Finally, if there is a primary or secondary source narrating the event, the element <bibl> can be used (either as a child of <desc> or as a direct child of <event>). The element <bibl> may contain information about the <author>, the <title> and the <date> of publication. It is possible to attach a @sameAs holding an authority URI to the <bibl> element in order to disambiguate the source.

.. FRBR

For example:

.. code-block:: xml

	<person xml:id="socr" sameAs="http://viaf.org/viaf/88039167">
		...
		<event xml:id="ev01" type="trial" when="-0399" corresp="http://wordnet-rdf.princeton.edu/id/01198357-n">
			<label>Socrates trial</label>
			<desc xml:id="desc01">The trial of <persName ref="#socr" role="defendant" corresp="http://wordnet-rdf.princeton.edu/id/09781524-n">Socrates</persName> for impiety and corruption of the youth took place in <placeName ref="#athens">Athens</placeName> in <date when="-0399">399 B.C.</date></desc>
			<bibl xml:id="bibl01" sameAs="http://viaf.org/viaf/214045129"><author ref="#plat">Plato</author> gives a contemporary account of the trial in his work titled <title ref="Apology_of_Socr">Apology of Socrates</title>.</bibl>
		</event>
		...
	</person>

.. bibliographic references upcoming

.. critical apparatus upcoming

.. provenance upcoming

Full example
------------

You can dowload a TEI XML pseudo-edition featuring all the examples presented above from |this link|. 

.. All links

.. |TEI Guidelines, 13. Names, Dates, People, and Places| raw:: html

   <a href="https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ND.html" target="_blank">TEI Guidelines, 13. Names, Dates, People, and Places</a>

.. |SAWS project| raw:: html

	<a href="http://www.ancientwisdoms.ac.uk" target="_blank">SAWS project</a>

.. |this XSLT transformation| raw:: html

	<a href="https://github.com/fgiovannetti/lift/blob/master/TEI2RDF_scripts/add_ids_to_elements.xsl" target="_blank">this XSLT transformation</a>

.. |xsltproc tutorial| raw:: html

	<a href="http://fhoerni.free.fr/comp/xslt.html" target="_blank">xsltproc tutorial</a>

.. |W3C Permanent Identifier Community Group| raw:: html

	<a href="https://www.w3.org/community/perma-id/" target="_blank">W3C Permanent Identifier Community Group</a>

.. |ISO 639 list| raw:: html
	
	<a href="https://www.loc.gov/standards/iso639-2/php/English_list.php" target="_blank">ISO 639 list</a>

.. |VIAF| raw:: html
	
	<a href="https://viaf.org/" target="_blank">VIAF</a>

.. |Worldcat| raw:: html
	
	<a href="https://www.worldcat.org/" target="_blank">Worldcat</a>

.. |Library of Congress| raw:: html
	
	<a href="https://id.loc.gov/" target="_blank">Library of Congress</a>

.. |sameas.org| raw:: html
	
	<a href="http://sameas.org" target="_blank">sameas.org</a>

.. |this link| raw:: html
	
	<a href="https://github.com/fgiovannetti/lift/blob/master/input-test/input-test.xml" target="_blank">this link</a>

.. |AgRelOn| raw:: html
	
	<a href="https://d-nb.info/standards/elementset/agrelon" target="_blank">AgRelOn</a>

.. |ISO 8601 standard| raw:: html

	<a href="https://www.iso.org/iso-8601-date-and-time-format.html" target="_blank">ISO 8601 standard</a>
