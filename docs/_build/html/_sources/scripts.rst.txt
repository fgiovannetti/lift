.. _scripts:

How the scripts work
===============================

LIFT contains a set of Python 2.7 scripts. The scripts use the Python library `lxml <https://lxml.de>`_ to find and extract relevant data from the input TEI document, and the Python library `RDFLib <https://rdflib.readthedocs.io/en/stable>`_ to create RDF triples and merge them into a single knowledge graph.

You can apply any of the scripts to your TEI document. If you opt for using the scripts as are, make sure you read LIFT encoding guidelines at :ref:`input` and update your input TEI document accordingly (unless you modify them, the scripts will look for specific constructs in your input TEI document which will serve as a basis for creating RDF triples).

TEI to RDF: a Jupyter notebook with line-by-line explanations of LIFT's scripts
-----------------------------------------------------------------------------------------------

The previous section, :ref:`output`, shows the input TEI constructs next to the corresponding output RDF statements. A Jupyter notebook, available from `<https://nbviewer.jupyter.org/github/fgiovannetti/lift/blob/master/jupyter_nb/TEItoRDF.ipynb>`_, explains the code of the scripts line-by-line. 

You can either read a non-interactive preview of the notebook from the link above or install Jupyer to access the notebook interactively. The second option assumes some familiarity with the command line or check the tutorials by the `Programming Historian <https://programminghistorian.org/>`_ (for `Windows here <https://programminghistorian.org/en/lessons/intro-to-powershell>`_, or `Mac/Linux here <https://programminghistorian.org/en/lessons/intro-to-bash>`_): 

1. Open your Terminal or Prompt. If you already have Python installed, you can run :code:`pip install notebook` (visit `<https://jupyter.org/install>`_ for further help); 

2. `Download the LIFT notebook <https://github.com/fgiovannetti/lift/blob/master/jupyter_nb/TEItoRDF.ipynb>`_. 

3. Go back to Terminal or Prompt and navigate to the folder where the notebook has been saved;

3. Run :code:`juptyter notebook` to launch a web browser with the Jupyter Notebook applications;

4. On the web browser, click on TEItoRDF.ipynb to open the notebook interactively.


Modify LIFT's scripts and/or run them locally
-----------------------------------------------------------------------------------------------

After reading the Jupyter notebook, you should be able to modify LIFT's scripts to meet your project needs. For example, you may adapt the way LIFT extract information from the input TEI file so to avoid modifying your original TEI document, or you may enrich the transformation with new RDF triples.

To modify LIFT's transformations and/or run them locally on your machine:

1. Go to `LIFT's repository on Github <https://github.com/fgiovannetti/lift/tree/master/TEI2RDF_scripts>`_ and download the scripts; 

2. You can then open and change the scripts with any code editor. Remeber to update the path to the XML document to be parsed (modify the line :code:`tree = etree.parse('input.xml')` on top of the script).

3. In order to run the transformation locally
	1. Open your Terminal or Prompt;
	2. Navigate to the folder where the scripts have been saved;
	3. Run :code:`python the_name_of_your_script.py`.
