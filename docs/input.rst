.. _input:

Prepare your TEI document
==================================================


The TEI standard allows for multiple ways to encode the same textual features. For example, you can use the tag :code:`<persName>`, the tag :code:`<name>`, or even the tag :code:`<rs>` to markup a personal name (cf. |TEI Guidelines, 13. Names, Dates, People, and Places|).

This TEI feature has the advantage of flexibility, but it makes creating a universal TEI-to-RDF transformation script a difficult task. This is why this documentation includes a set of encoding guidelines designed to ensure a smooth TEI-to-RDF transformation via LIFT. In particular, in order for LIFT to work on your TEI document, you must adhere to the following simple guidelines:

1. `Provide TEI elements with unique identifiers using the @xml:id attribute`_;
2. `Provide an at least minimal TEI header`_;
3. `Use <person> and <persName> to represent persons and in-text references to such persons, respectively`_;
4. `Use <place> and <placeName> to represent places and in-text references to such places, respectively`_;
5. `Assign a @sameAs attribute to each real-world entity`_;
6. `Encode relationships between persons within <listRelation>`_;
7. `Use <event> to represent events, either within <person> or <place>`_.


Provide TEI elements with unique identifiers using the @xml:id attribute 
--------------------------------------------------------------------------------

A unique URI must be assigned to each entity of a linked data graph (for example, a person, a place, a literary work, etc.). LIFT uses @xml:id attributes to create unique URIs. To accomplish this, LIFT concatenates the value of the attribute @xml:base attribute of the <TEI> element is concatenated with the value of the @xml:id attribute of the element. For example, the element below representing a person

.. code-block:: xml

	<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:base="https://example.org">
		...
		<person xml:id="socr">...</person>
		...
	</TEI>

will be assigned the following URI: 

.. code-block:: xml

	<https://example.org/person/socr>


Note that the value of your @xml:base attribute should be registered as a permanent URL (i.e. through services such as `w3id.org <https://w3id.org>`_). Check the |W3C Permanent Identifier Community Group| for more information on how to register your URL. 

If your TEI document lacks unique identifiers, you can use Charlotte Tupman's |XSLT transformation stylesheet| (written for |SAWS|), which generates a unique identifier for each element that has no :code:`@xml:id`. You can run the transformation using `xsltproc <http://xmlsoft.org/XSLT/xsltproc2.html>`_ after downloading the stylesheet to the same folder as your TEI document. You can look at this `tutorial <http://fhoerni.free.fr/comp/xslt.html>`_ for detailed instructions about the process (last accessed 2021-10-25).


Provide an at least minimal TEI header
-----------------------------------------------------------------------------------------

Your TEI header should comprise, at least, the minimal recommended elements as shown below:

.. code-block:: xml

	<teiHeader>
		<fileDesc>
			<titleStmt>
				<title><!-- Title of the resource --></title>
				<author><!-- Author of the resource --></author>
			</titleStmt>
			<publicationStmt>
				<p><!-- Information about the distribution of the resource --></p>
			</publicationStmt>
			<sourceDesc>
				<p><!-- Information about the source from which the resource derives --></p>
			</sourceDesc>
		</fileDesc>
	</teiHeader>


Use <person> and <persName> to represent persons and in-text references to such persons, respectively
-------------------------------------------------------------------------------------------------------------------

Each person mentioned in the TEI document must be described in the TEI header within a :code:`<person>` element to which an :code:`@xml:id` has been assigned. 

It is possible to provide a normalized form of each person's name by nesting a :code:`<persName>` element containing the normalized name within :code:`<person>`. You can provide multiple normalizations, e.g. in different languages (to specify the language use the :code:`@xml:lang` attribute and a value from the |ISO 639 list| of language codes).

All in-text occurrences of personal names must be encoded using :code:`<persName>`. The attribute :code:`@ref` should be used on the element to relate each name to the corresponding person (via the person's :code:`@xml:id`). For example:


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


Persons can be grouped using :code:`<listPerson>`. Each :code:`<listPerson>` (or, alternatively, each :code:`<person>` element if :code:`<listPerson>` is not present) can be assigned a :code:`@type` and/or :code:`@corresp` containing a short description of the group or individual. In particular, use :code:`@type` for free-text descriptions (if using multi-word descriptions, please separate each word with an hyphen) or :code:`@corresp` to provide a URI from a controlled vocabulary. For example:

.. code-block:: xml

	<listPerson type="ancient-athenian-philosophers" corresp="http://dbpedia.org/class/yago/WikicatAncientAthenianPhilosophers">
		<person xml:id="Socr">
		...


Use <place> and <placeName> to represent places and in-text references to such places, respectively
-------------------------------------------------------------------------------------------------------------------

The guidelines for encoding persons apply to places as well. For example:

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

Assign a @sameAs attribute to each real-world entity
-----------------------------------------------------------------------------------------

By assigning a @sameAs attribute to your entities, you can disambiguate them by connecting them to external authority files, such as |VIAF|, |Worldcat|, or the |Library of Congress|. 

Provide a URI in a :code:`@sameAs` attribute. You can supply multiple URIs, separated by a whitespace. For example:

.. code-block:: xml
	
	<person xml:id="Socr" sameAs="http://viaf.org/viaf/88039167 http://id.loc.gov/rwo/agents/n79055329">


Encode relationships between persons within <listRelation>
-----------------------------------------------------------------------------------------

Use a series of :code:`<relation>` elements nested within :code:`<listRelation>` to markup relationships between persons in the TEI header. Note that :code:`<listRelation>` must be a child element of :code:`<listPerson>`. 

In particular, for unidirectional relationships (e.g. 'Socrates has student Plato') use the attributes :code:`@active` and :code:`@passive` to express the subject and the object of the relationship respectively; for bidirectional relationships (e.g. 'Plato has colleague Xenophon') use the attribute :code:`@mutual`. It is possible to represent a mutual relationship involving multiple persons by declaring more than one value for the :code:`@mutual` attribute. Multiple values must be separated by whitespaces. Finally, use the :code:`@name` attribute to express the nature of the relationship. You can reuse terms from |AgRelOn|, the Agent Relationship Ontology. For example:

.. code-block:: xml

	<listRelation>
		<relation xml:id="rel01" name="hasStudent" active="#socr" passive="#plat #xen #criti"/>
		<relation xml:id="rel02" name="hasColleague" mutual="#plat #xen"/>
	</listRelation>

Use <event> to represent events, either within <person> or <place>
----------------------------------------------------------------------------------------

It is possible to describe events that occur in relation to a specific person or place. Such descriptions should be nested within the corresponding <person> or <place> elements. 

The element :code:`<event>` contains the description of the event. The attributes :code:`@type` and :code:`@corresp` can be assigned to :code:`<event>` to provide a free-text label or a URI, respectively.

The date of the event must be recorded in :code:`@when` or :code:`@from/@to` attributes. Dates should be represented according to the |ISO 8601| standard.

A :code:`<label>` can be used to provide a short textual description of the event, while a :code:`<desc>` can contain the extended account of the event, including personal names, place names, and dates (encoded using the :code:`<date>` element).

It is possible to specify the role held by the person in the event using the attribute :code:`@role` and/or using the attribute :code:`@corresp` on :code:`<persName>`. The attribute :code:`@corresp` should only contain a URI representing the role.  

Furthermore, if there exist a primary or secondary source about the event, the element :code:`<bibl>` can be used to express it (either as a child of :code:`<desc>` or as a direct child of :code:`<event>`). The :code:`<bibl>` element may contain information about the :code:`<author>`, the :code:`<title>` and the :code:`<date>` of publication of the source. A :code:`@sameAs` can be associated to :code:`<bibl>`.

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
--------------------------------------

You can download a TEI XML pseudo-edition featuring all of the examples presented above from |this link|. 

.. All links

.. |TEI Guidelines, 13. Names, Dates, People, and Places| raw:: html

   <a href="https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ND.html" target="_blank">TEI Guidelines, 13. Names, Dates, People, and Places</a>

.. |SAWS| raw:: html

	<a href="http://www.ancientwisdoms.ac.uk" target="_blank">SAWS project</a>

.. |XSLT transformation stylesheet| raw:: html

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
