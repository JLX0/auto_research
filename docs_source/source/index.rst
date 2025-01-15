AutoResearch: A General Framework for Academic Research Automation
==================================================================

*AutoResearch* is a framework designed to simplify and accelerate academic research tasks. It offers a **modular and extensible architecture** to help researchers, developers, and academics efficiently search, organize, summarize, and analyze academic papers.


Key Features
------------

- :doc:`Automated Paper Search <_examples_gallery/search_papers>`
  - Search for academic papers using keywords and retrieve metadata from Google Scholar, Semantic Scholar, and arXiv. Organize results by relevance or date, apply filters, and save articles to a specified folder.

- :doc:`Paper Summarization <_examples_gallery/summarize_a_paper>`
  - Summarize individual papers or all papers in a folder. Extract key sections (abstract, introduction, discussion, conclusion) and generate summaries using GPT models. Track and display the total cost of summarization.

- :doc:`Explain a Paper with LLMs <_examples_gallery/explain_a_paper>`
  - Interactively explain concepts, methodologies, or results from a selected paper using LLMs. Supports user queries and detailed explanations of specific sections.

- :doc:`Code Availability Check <_examples_gallery/get_github_link>`
  - Check for GitHub links in papers and validate their availability.

- :doc:`Topic-to-Survey Automation <_examples_gallery/top_to_survey>`
  - Convert a topic or research question into a comprehensive survey of relevant papers. Generate keywords, retrieve articles, summarize content, and optionally check code availability. Organize and zip results for easy access.

Basic Example
--------------

.. code-block:: python

    from auto_research.search.core import AutoSearch
    from auto_research.survey.core import AutoSurvey

    # Search for papers
    search = AutoSearch(keywords="machine learning", num_results=10)
    search.run()

    # Summarize a paper
    survey = AutoSurvey(api_key="your-api-key", model="gpt-4", paper_path="path/to/paper.pdf")
    survey.run()


See :doc:`Examples <_examples_gallery/index>` for more advanced usages

Communication
-------------

- `GitHub Discussions <https://github.com/JLX0/auto_research/discussions>`__: For general questions and community support.

- `GitHub Issues <https://github.com/JLX0/auto_github/issues>`__: For bug reports and feature requests.

Contribution
------------

We welcome contributions! Please see the `Contribution Guide <https://github.com/JLX0/auto_github/blob/main/CONTRIBUTING.md>`__ for details.

License
-------

MIT License. See `LICENSE <https://github.com/JLX0/auto_github/blob/main/LICENSE>`__ for details.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   tutorial/index
   api
   reference/index
   _examples_gallery/index
   _api_gallery/index
   faq

Indices
==================

* :ref:`genindex`
* :ref:`modindex`

.. |projectlogo| image:: https://via.placeholder.com/800x200.png
  :width: 800
  :alt: Project Logo