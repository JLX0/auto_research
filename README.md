# Currently under active development

- Currently, mainly targets computer science research, especially machine learning research.
- More functionalities will be added soon.
- Example usage and API documentation are available.

# Introduction

Auto-Research is a framework designed to simplify and accelerate academic research tasks. It offers a **modular and extensible architecture** to help researchers, developers, and academics efficiently search, organize, summarize, and analyze academic papers.

See [home page](https://jlx0.github.io/auto_research/index.html#) for API documentation and detailed examples

See this [Google Colab notebook](https://colab.research.google.com/drive/1Xj0xTpHvpnPfmK9tYnI8Ep7oRKrQ9gn7?usp=sharing) for an installation-free quick demo

While there are many existing tools for research automation. But here are the key distinctions and advantages of the AutoResearch:

- No additional API keys besides LLM API keys are required (No API keys, such as Semantic Scholar keys, are needed for literature search and downloading papers)

- Support multiple search keywords for one inquiry.

- Rank the papers based on their impacts, and consider the most important papers first.

- Fast literature search process. It only takes about 3 seconds to automatically download a paper.

- Python code-base, which enables convenient deployment, such as Google Colab notebook, as well as efficient integration with other ML-based tools, such as other LLM agents

- API documentation are available

# Requirements

OS: Linux-based

Python: >= 3.10

# Installation

`git clone https://github.com/JLX0/auto_research`

`cd auto_research`

`pip install .`

# Quick Start

First, fill in your API keys for LLMs with your actual keys in `key.json`. See [Setting up API keys for LLMs](https://jlx0.github.io/auto_research/installation.html#setting-up-api-keys-for-llms) for more information. You only need to fill in at least one type of key. 

Then, check `examples`.

For example, `python examples/topic_to_survey` converts your research topic or 
question of interests to a survey over relevant papers. An explanation about the motivation behind
this functionality and an example run of the script is available [here](https://jlx0.github.io/auto_research/_examples_gallery/top_to_survey).

If you want to use DeepSeek models, change the argument `target_key` in `get_api_key` and the argument `model` in various instance initiations accordingly.