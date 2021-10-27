.. _scripts:

How the scripts work
===============================

LIFT features a set of five transformation scripts written in Python 2.7. LIFT leverages two libraries:

* `lxml <https://lxml.de>`_ to find and select the relevant TEI constructs from the input XML document;
* `RDFLib <https://rdflib.readthedocs.io/en/stable>`_ to create the RDF triples forming the knowledge graph.

Any of the scripts can be applied to your TEI document. If you use the scripts as is, make sure to read LIFT's encoding guidelines at :ref:`input` and update your input TEI document accordingly.

A Jupyter notebook walking through LIFT's TEI to RDF transformation line-by-line
-----------------------------------------------------------------------------------------------

The section :ref:`output` displays the input TEI constructs next to the output RDF statements. A Jupyter notebook, available at `this link <https://nbviewer.jupyter.org/github/fgiovannetti/lift/blob/master/jupyter_nb/TEItoRDF.ipynb>`_, walks you through the scripts line-by-line. 

You can read a non-interactive preview of the notebook by following the link above, or you can install Jupyer to access the notebook interactively. The second option requires a minimum familiarity with the command line (the `Programming Historian <https://programminghistorian.org/>`_ provides excellent introductory tutorials for `Windows <https://programminghistorian.org/en/lessons/intro-to-powershell>`_ as well as `Mac/Linux <https://programminghistorian.org/en/lessons/intro-to-bash>`_ users).

In order to access the notebook interactively

1. open Terminal or Prompt. If Python is already installed on your machine, run :code:`pip install notebook` (visit `<https://jupyter.org/install>`_ for further help); 
2. `download the notebook <https://github.com/fgiovannetti/lift/blob/master/jupyter_nb/TEItoRDF.ipynb>`_;
3. in Terminal or Prompt navigate to the folder where the notebook was saved;
4. run :code:`juptyter notebook` to open Jupyter on your browser;
5. from the browser, click on TEItoRDF.ipynb to access the notebook.


Modify the scripts and/or run them locally
-----------------------------------------------------------------------------------------------

After reading the notebook, you should be able to modify LIFT's scripts to meet the needs of your project. You can, for example, change how LIFT extracts information from the input file to avoid modifying your original TEI encoding, or you can enrich the knowledge graph with new RDF triples.

To modify LIFT the scripts and/or run them locally

1. go to `LIFT's repository on Github <https://github.com/fgiovannetti/lift/tree/master/TEI2RDF_scripts>`_ and download the scripts; 
2. open and change the scripts with an editor of your choice (remeber to update the path to the input TEI document (modify the line :code:`tree = etree.parse('input.xml')` at the very beginning of the script);
3. to run the transformation locally
	1. open your Terminal or Prompt;
	2. navigate to the folder where the scripts are;
	3. run :code:`python [name-of-your-script].py`.
