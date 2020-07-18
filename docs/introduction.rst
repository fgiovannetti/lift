Introduction
============

LIFT (*Linked data from TEI*) is a Digital Humanities tool based on Python 2.7 that you can use for generating linked open data out of TEI documents and editions.
This documentation is devised to give you insight on how LIFT works both from the point of view of technology and methodology. After reading this documentation you should be able to leverage LIFT as is, or adapt its scripts to your own project-specific needs.

LIFT contains 4 different TEI-to-LOD scripts written in Python 2.7. Each script addresses the transformation to LOD of a set of specific TEI entities (persons, persons and events, persons and relations, places). The scripts can be used independently from one another. A fifth script comprehensive of all entities (i.e. persons, events, relations, and places) is also available. Two additional scripts, one for bibliographic entities and the other for critical apparatus entries, are currently under development (expected release: Spring 2021). 

This documentation has a pedagogical purpose: to show and discuss step-by-step a workflow for TEI-to-LOD transformation which does not entail the use of XSLT, but instead adopts Python with the library `lxml <lxmlhttps://lxml.de/>`_ for processing XML documents, and the library `RDFLib <https://rdflib.readthedocs.io/en/stable/>`_ for creating RDF triples. 

Although XSLT is a widely-adopted language for XML processing within the Digital Humanities community, we hope for LIFT to demonstrate how Python offers more flexible methods and tools for working with linked open data.

**Please note that this documentation is still under development and growing.**

This documentation is divided into four main parts:

1. :ref:`input`, which provides a set of encoding requirements for the input TEI document
2. :ref:`output`, illustrating the structure and semantics of the generated graph by juxtaposing the TEI input with the corresponding RDF output. This section explains why and how users may choose other ontologies for their projects or adapt the scripts to different input data
3. :ref:`scripts`, where users can access an interactive Jupyter Notebook containing the scripts with instructions and line-by-line explanations. The notebook should help users acquire the skills necessary to write their own transformation scripts
4. :ref:`resources`, which proposes relevant publications and provides examples of TEI digital scholarly editions enriched by means of linked open data

You can either run the scripts from the web application (`<https://projects.dharc.unibo.it/lift/quickstart.html>`_) or `download the scripts <https://github.com/fgiovannetti/lift/tree/master/TEI2RDF_scripts>`_ for local use (see :ref:`scripts` for detailed instructions on how to run the scripts locally from Terminal).