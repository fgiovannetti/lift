Introduction
============

LIFT (*Linked data from TEI*) is a Digital Humanities tool based on Python 2.7 for generating linked open data (LOD) out of TEI-encoded texts.
This documentation is intended to provide you with an understanding of how LIFT works from the standpoint of both the technologies and the methodology employed. After reading this documentation, you should be able to use LIFT as is or modify its scripts to meet your specific project requirements.

LIFT offers four different TEI-to-LOD scripts written in Python 2.7. Each script addresses the transformation of a set of specific TEI entities (persons, persons and events, persons and relations, places) to LOD. The scripts can be used independently from one another. A fifth script comprehensive of all entities (i.e. persons, events, relations, and places) is also available. 
.. Two additional scripts, one for bibliographic entities and the other for critical apparatus entries, are currently under development (expected release: Spring 2021).

This documentation, divided into four sections, serves a pedagogical purpose by demonstrating and discussing in detail a workflow for TEI-to-LOD transformation that does not require the use of XSLT and instead relies on Python (the `lxml <https://lxml.de/>`_ library is used for the processing of XML, while the `RDFLib <https://rdflib.readthedocs.io/en/stable/>`_ library is used for the creation of the RDF triples):

..1. :ref:`input`, which explains the encoding requirements for the input TEI document;
..2. :ref:`output`, illustrating the structure and semantics of the generated knowledge graph by comparing the TEI input with the corresponding RDF output (this section also discusses why and how users might choose different ontologies for their projects or modify the scripts to work with different input data);
..3. :ref:`scripts`, where users can access an interactive Jupyter notebook containing LIFT's scripts with instructions and line-by-line explanations that are meant to help users develop the skills required to write their own transformation scripts;
..4. :ref:`resources`, which lists relevant publications and provides examples of TEI digital scholarly editions which have been enriched by means of linked open data.

You can directly run the scripts from the web application (`<https://projects.dharc.unibo.it/lift/quickstart.html>`_) or `download them <https://github.com/fgiovannetti/lift/tree/master/TEI2RDF_scripts>`_ for local use 

..(see :ref:`scripts` for more detailed instructions ).