.. _scripts:

How the scripts work
===============================

LIFT contains a set of Python 2.7 scripts. The scripts use the Python library `lxml <https://lxml.de>`_ to find and extract relevant data from the input TEI document, and the Python library `RDFLib <https://rdflib.readthedocs.io/en/stable>`_ to create RDF triples and merge them into a single knowledge graph.

You can apply any of the scripts to your TEI document. If you opt for using the scripts as are, make sure you read LIFT encoding guidelines at :ref:`input` and update your input TEI document accordingly (unless you modify them, the scripts will look for specific constructs in your input TEI document which will serve as a basis for creating RDF triples).

The previous section, :ref:`output`, shows the input TEI constructs next to the corresponding output RDF statements. A Jupyter notebook, available from `<https://nbviewer.jupyter.org/github/fgiovannetti/lift/blob/master/jupyter_nb/TEItoRDF.ipynb>`_, explains the code of the scripts line-by-line. 

You can either read a non-interactive preview of the notebook from the link above or install Jupyer to access the notebook interactively. The second option assumes some familiarity with the command line or check the tutorials by the `Programming Historian <https://programminghistorian.org/>`_ (for `Windows here <https://programminghistorian.org/en/lessons/intro-to-powershell>`_, or `Mac/Linux here <https://programminghistorian.org/en/lessons/intro-to-bash>`_): 

1. If you already have Python installed, you can run :code:`pip install notebook` on your Terminal or Prompt (visit `<https://jupyter.org/install>`_ for further help); 

2. `Download the LIFT notebook <https://github.com/fgiovannetti/lift/blob/master/jupyter_nb/TEItoRDF.ipynb>`_, then from Terminal or Prompt, navigate to the folder where the notebook has been saved;

3. You can now run :code:`juptyter notebook` to launch a web browser with the Jupyter Notebook applications. 






.. directions on how to use the jupyter notebook

.. download to modify

.. ADD INSTRUCTIONS FOR LOCAL USE