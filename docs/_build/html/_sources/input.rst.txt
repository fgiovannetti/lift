.. _input:

Prepare your TEI file
=====================


TEI allows different ways to encode the same textual features. For example, it is possible to validly markup a person's name using either the tag :code:`<persName>`, or the tag :code:`<name>`, or even the tag :code:`<rs>` (cf. |TEI Guidelines, 13. Names, Dates, People, and Places|).

Such a characteristic of the TEI has the advantage of flexibility, but makes the creation of a universal TEI-to-RDF transformation script a complex  task. This is the reasong that this documentation provides a set of encoding guidelines aimed at ensuring a smooth TEI-to-RDF transformation via LIFT. In particular, in order for LIFT to work on your TEI document, you must follow these simple rules:

1. `Provide TEI elements with unique identifiers (@xml:id)`_
2. `Include (at least) a minimal TEI header`_
3. `Use <person> and <persName> to represent persons and in-text references to such persons`_
4. `Use <place> and <placeName> to represent place and in-text references to such places`_
5. `Assign a @sameAs attribute to each of your real-world entities`_
6. `Encode relationships between persons within a <listRelation> element`_
7. `Use <event> to represent events, either within a <person> or a <place> element`_


Provide TEI elements with unique identifiers (@xml:id) 
---------------------------------------------------------------------

Each entity of a linked data graph (e.g. a person, a place, a literary work, etc.) is represented by a unique URI. LIFT leverages @xml:id attributes to build a unique URI for the element. To do this, LIFT concatenates the value of the attribute @xml:base assigned to the <TEI> element on top of the TEI document with the value of the @xml:id attribute assigned to the element. For example, this TEI encoding

.. code-block:: xml

	<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:base="https://example.org">
		...
		<person xml:id="socr">...</person>
		...
	</TEI>

will result in the following unique URI: 

.. code-block:: xml

<https://example.org/person/socr>

A couple of points to consider:

- The value of the attribute @xml:base should be registered as a permanent URL (e.g. through services such as `w3id.org <https://w3id.org>`_). Check the |W3C Permanent Identifier Community Group| for more information on how to register your edition URL.  

- If your TEI document does not already feature unique identifiers, you can run |this XSLT transformation| on your document. The script, originally provided by Charlotte Tupman for the |SAWS project|, creates a unique identifier for each element where an :code:`@xml:id` is not already present. After downloading the stylesheet to the same folder where your TEI document is, you can run the transformation via xsltproc. You can check this `tutorial <http://fhoerni.free.fr/comp/xslt.html>`_ for detailed instructions about the process (last accessed 2020-07-24).


Include (at least) a minimal TEI header
-----------------------------------------------------------------------------------------

Your TEI header should at least comprise the minimal recommended elements, as shown below:

.. code-block:: xml

	<teiHeader>
		<fileDesc>
			<titleStmt>
				<title><!-- title of the resource --></title>
				<author><!-- author of the resource --></author>
			</titleStmt>
			<publicationStmt>
				<p><!-- Information about distribution of the resource --></p>
			</publicationStmt>
			<sourceDesc>
				<p><!-- Information about source from which the resource derives --></p>
			</sourceDesc>
		</fileDesc>
	</teiHeader>


Use <person> and <persName> to represent persons and in-text references to such persons
-----------------------------------------------------------------------------------------

All persons of the document must be described in the TEI header within :code:`<person>` elements, to which an @xml:id must be assigned. It is possible to provide a normalized form of each person's name by nesting a <persName> element containing the normalized name within <person>. You can also provide multiple normalizations, one for each language (to specify the language use the @xml:lang attribute and a value from the |ISO 639 list| of language codes).

All in-text occurrences of personal names must be encoded using :code:`<persName>` elements. The attribute :code:`@ref` should be used on the element to relate each name to the corresponding person (via the person's @xml:id). For example:


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

Sets of persons can be nested within a :code:`<listPerson>` element. The attributes @type and/or @corresp can be assigned to each <listPerson> (or, alternatively, to the single <person> if a <listPerson> is not present) to provide a short description of the group or individual: in particular, use the attribute @type for free-text descriptions (separate each word using an hyphen); or use the attribute @corresp to provide a URI from a controlled vocabulary. For example:

.. code-block:: xml

	<listPerson type="ancient-athenian-philosophers" corresp="http://dbpedia.org/class/yago/WikicatAncientAthenianPhilosophers">
		<person xml:id="Socr">
		...


Use <place> and <placeName> to represent place and in-text references to such places
-----------------------------------------------------------------------------------------

Places follow similar rules to persons. For example:

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

Assign a @sameAs attribute to each of your real-world entities
-----------------------------------------------------------------------------------------

By attributing a @sameAs attribute to your entities, you can disambiguate them by creating connections with external authority files or datasets, such as |VIAF|, |Worldcat|, and the |Library of Congress|. 

Provide a URI in a @sameAs attribute. You can provide multiple URIs, each separated by a whitespace. For example:

.. code-block:: xml
	
	<person xml:id="Socr" sameAs="http://viaf.org/viaf/88039167 http://id.loc.gov/rwo/agents/n79055329">


Encode relationships between persons within a <listRelation> element
-----------------------------------------------------------------------------------------

Use the element :code:`<relation>` nested within a :code:`<listRelation>` to markup relationships between persons. Note that :code:`<listRelation>` must be a child element of :code:`<listPerson>`. 

For unidirectional relationships (e.g. Socrates has student Plato), use the attributes :code:`@active` and :code:`@passive` to express the subject and the object of the relationship respectively; for bidirectional relationships (e.g. Plato has colleague Xenophon), use the attribute :code:`@mutual` . It is possible to represent a mutual relationship involving multiple persons by declaring more than one value for the @mutual attribute. Values must be separated by whitespaces. Finally, use the @name attribute to express the nature of the relationship. You can take terms from |AgRelOn|, the Agent Relationship Ontology. For example:

.. code-block:: xml

	<listRelation>
		<relation xml:id="rel01" name="hasStudent" active="#socr" passive="#plat #xen #criti"/>
		<relation xml:id="rel02" name="hasColleague" mutual="#plat #xen"/>
	</listRelation>

Use <event> to represent events, either within a <person> or a <place> element
----------------------------------------------------------------------------------------

It is possible to describe events related to a particular person or place. Such a description should be nested within the relevant <person> or <place> element. 

The element :code:`<event>` contains the entire account of the event. The attributes :code:`@type` and :code:`@corresp` can be used to provide a free-text label or a URI respectively.

The date of the event can be provided in a :code:`@when` or :code:`@from/@to` attribute. Date should be represented according to |ISO 8601|.

A :code:`<label>` can be used to provide a short textual description of the event, while a :code:`<desc>` can contain the extended account of the event, including personal names, place names, dates (encoded using the :code:`<date>` element).

It is possible to specify the role that the person held in the event using the attribute :code:`@role` and/or using the attribute :code:`@corresp` on :code:`<persName>`. The attribute :code:`@corresp` should only contain a URI for the role.  

Furthermore, if there exist a primary or secondary source for the event, the element :code:`<bibl>` can be used to express it (either as a child of :code:`<desc>` or as a direct child of :code:`<event>`). :code:`<bibl>` may contain information about the :code:`<author>`, the :code:`<title>` and the :code:`<date>` of publication. A :code:`@sameAs` can be attributed to the :code:`<bibl>`.

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

.. bibliographic references (upcoming)

.. critical apparatus (upcoming)

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

.. |ISO 8601| raw:: html

	<a href="https://www.iso.org/iso-8601-date-and-time-format.html" target="_blank">ISO 8601</a>
