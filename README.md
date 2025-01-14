# Currently under active development

- Documentations and more examples will be added soon.
- Currently, mainly targets computer science research, especially machine learning research.
- Example usage is available.

# Auto-Research
Automatically assisting academic research with LLMs etc.

# Requirements

OS: Linux-based

Python: >= 3.10

# Installation

`git clone https://github.com/JLX0/auto_research`

`cd auto_research`

`pip install .`

# Usage

First, fill in your API keys for LLMs with your actual keys in `key.json`. You only need to fill in at least one type of key. 

Then, see `examples`.

For example, `python examples/topic_to_survey` converts your research topic or 
question of interests to a survey over relevant papers.

If you want to use DeepSeek models, change the argument `target_key` in `get_api_key` and the argument `model` in various instance initiations accordingly.



