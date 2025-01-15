AutoResearch: A General Framework for Academic Research Automation
==================================================================

*AutoResearch* is a framework designed to simplify and accelerate academic research tasks. It offers a **modular and extensible architecture** to help researchers, developers, and academics efficiently search, organize, summarize, and analyze academic papers.

Key Features
------------

- :doc:`Automated Paper Search <_examples_gallery/explain_a_paper>`
  - Search for academic papers using keywords and retrieve metadata from Google Scholar, Semantic Scholar, and arXiv.

- :doc:`Paper Organization and Filtering <tutorial/02_configuration>`
  - Organize and filter papers based on combined scores (citation count and recency).

- :doc:`Paper Summarization <tutorial/03_optimization_algorithms>`
  - Extract key sections (abstract, introduction, discussion, conclusion) and generate summaries using GPT models.
,
- :doc:`Code Availability Check <tutorial/04_parallelization>`
  - Check for GitHub links in papers and validate their availability.

- :doc:`Cost Tracking <tutorial/05_visualization>`
  - Track API usage costs for summarization and code availability checks.

Basic Concepts
--------------

Here are some basic terms used in *AutoResearch*:

- **Combined Score**: A metric to rank papers based on citation count and recency.
- **Threshold Filtering**: Filter papers based on rank (top N papers) or score (minimum combined score).
- **Metadata Management**: Store and retrieve metadata (e.g., paper details, summaries) in JSON files.

Below is a sample code to demonstrate how *AutoResearch* can be used:

.. code-block:: python

    from auto_research.search.core import AutoSearch
    from auto_research.survey.core import AutoSurvey

    # Search for papers
    search = AutoSearch(keywords="machine learning", num_results=10)
    search.run()

    # Summarize a paper
    survey = AutoSurvey(api_key="your-api-key", model="gpt-4", paper_path="path/to/paper.pdf")
    survey.run()

Examples
--------

Here are some examples of how *AutoResearch* can be used in practice:

1. **Searching and Downloading Papers**:
   - Search for papers on "machine learning" and download the top 10 results.
   - Filter papers based on a combined score threshold.

2. **Summarizing Papers**:
   - Extract and summarize key sections (abstract, introduction, discussion, conclusion) from a paper.
   - Store summaries for future reference.

3. **Checking Code Availability**:
   - Check if a paper includes a GitHub link for code implementation.
   - Validate the GitHub link and ensure it is functional.

4. **Visualizing Paper Scores**:
   - Plot combined scores vs. rank to visualize the impact and recency of papers.
   - Highlight downloaded papers in the plot.

.. TIP::

   Please check out the `Getting Started <https://example.com/getting-started>`__ section of the documentation.

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