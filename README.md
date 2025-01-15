# Currently under active development

- Currently, mainly targets computer science research, especially machine learning research.
- More functionalities will be added soon.
- Example usage and API documentation are available.

# Introduction

Auto-Research is a framework designed to simplify and accelerate academic research tasks. It offers a **modular and extensible architecture** to help researchers, developers, and academics efficiently search, organize, summarize, and analyze academic papers.

See [home page](https://jlx0.github.io/auto_research/index.html#) for API documentation and detailed examples

See this [Google Colab notebook](https://colab.research.google.com/drive/1Xj0xTpHvpnPfmK9tYnI8Ep7oRKrQ9gn7?usp=sharing) for an installation-free quick demo

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
question of interests to a survey over relevant papers. An example run of the script is available [here](https://jlx0.github.io/auto_research/_examples_gallery/top_to_survey).

If you want to use DeepSeek models, change the argument `target_key` in `get_api_key` and the argument `model` in various instance initiations accordingly.


