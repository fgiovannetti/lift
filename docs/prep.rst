
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
   :linenos:

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
   :linenos:

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

3. Use <place> and <placeName> for a place
------------------------------------------

The same instructions as above are also valid for places. For example:

.. code-block:: xml
   :linenos:

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

3. Assign a @sameAs to disambiguate your entity
-----------------------------------------------



4. Describe a person through @type on <listPerson>
--------------------------------------------------


.. People and relationships


.. People and events



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
