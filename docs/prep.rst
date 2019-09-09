
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

If your TEI document does not already contain unique identifiers, you can run |this XSLT transformation| on your document. The script, originally provided by Charlotte Tupman for the |SAWS project|, creates a unique identifier for each element that does not have an :code:`@xml:id`.

.. Add instructions for XSLT other than xsltproc stylesheet file in OSX Terminal


.. All links

.. |TEI Guidelines, 13. Names, Dates, People, and Places| raw:: html

   <a href="https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ND.html" target="_blank">TEI Guidelines, 13. Names, Dates, People, and Places</a>

.. |SAWS project| raw:: html

	<a href="http://www.ancientwisdoms.ac.uk" target="_blank">SAWS project</a>

.. |this XSLT transformation| raw:: html

	<a href="https://github.com/fgiovannetti/lift/blob/master/TEI2RDF_scripts/add_ids_to_elements.xsl" target="_blank">this XSLT transformation</a>

