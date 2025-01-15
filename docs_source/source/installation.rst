Installation Guide
==================

This guide provides step-by-step instructions for installing the *AutoResearch* package. Whether you're a beginner or a professional, you'll find the information you need here.

Quick Guide
-----------

For users who are highly familiar with Git, pip, and the command line, here's a quick installation guide:

**Requirements**:

- Linux-based OS
- Python >= 3.10

**Installation**:

.. code-block:: console

   $ git clone https://github.com/JLX0/auto_research
   $ cd auto_research
   $ pip install .

Detailed Installation Guide
---------------------------

If you're new to Python, Git, or the command line, follow the detailed steps below.

Requirements
------------

Before installing, ensure your system meets the following requirements:

- **Operating System**: Linux-based (e.g., Ubuntu, Debian, CentOS).
- **Python Version**: Python 3.10 or higher.

If you're unsure whether Python is installed or which version you have, follow the steps below to check.

Step 1: Check Python Installation
---------------------------------

1. **Open a Terminal**:
   - On Linux, you can open a terminal by pressing `Ctrl + Alt + T` or searching for "Terminal" in your applications menu.

2. **Check Python Version**:
   - Type the following command in the terminal and press `Enter`:

     .. code-block:: console

        $ python3 --version

   - If Python is installed, you'll see something like `Python 3.10.12`. If the version is **3.10 or higher**, you're good to go.
   - If Python is not installed or the version is too old, follow the official Python installation guide: https://www.python.org/downloads/.

Step 2: Install Git (if needed)
-------------------------------

Git is a tool used to download the *AutoResearch* code from GitHub. If you don't have Git installed, follow these steps:

1. **Install Git**:
   - On Ubuntu or Debian, run the following command in the terminal:

     .. code-block:: console

        $ sudo apt install git

   - On CentOS, run:

     .. code-block:: console

        $ sudo yum install git

2. **Verify Git Installation**:
   - After installation, check if Git is installed correctly:

     .. code-block:: console

        $ git --version

   - You should see something like `git version 2.25.1`. If not, revisit the installation steps.

Step 3: Download the *AutoResearch* Code
----------------------------------------

1. **Clone the Repository**:
   - Use Git to download the *AutoResearch* code from GitHub. Run the following command in the terminal:

     .. code-block:: console

        $ git clone https://github.com/JLX0/auto_research

   - This will create a folder named `auto_research` in your current directory.

2. **Navigate to the Project Folder**:
   - Move into the `auto_research` folder by running:

     .. code-block:: console

        $ cd auto_research

Step 4: Install the Package Using pip
-------------------------------------

`pip` is a tool used to install Python packages. If you don't have `pip` installed, follow these steps:

1. **Install pip**:
   - Run the following command to install `pip`:

     .. code-block:: console

        $ sudo apt install python3-pip

2. **Install *AutoResearch***:
   - Once `pip` is installed, run the following command to install *AutoResearch*:

     .. code-block:: console

        $ pip install .

   - This will install the package and all its dependencies.

Step 5: Verify the Installation
-------------------------------

To confirm that *AutoResearch* was installed successfully, run the following command:

.. code-block:: console

   $ python3 -c "import auto_research; print(auto_research.__version__)"

If the installation was successful, this will print the version of *AutoResearch* (e.g., `1.0.0`).


.. _setting_up_api_keys:

Setting up API keys for LLMs
---------------

The package uses the `get_api_key <https://github.com/JLX0/LLM_utilities/blob/main/LLM_utils/inquiry.py#L60>`_ function from `LLM_utilities <https://github.com/JLX0/LLM_utilities/>`_ to process the keys for LLMs.

To set the keys for your Python application, you have two options: using a JSON file or directly
typing the key into the code. If you choose the JSON file method, create a file named `key.json` in
the specified directory (e.g., the same folder as your script or a custom path). Inside the file,
format the content as a JSON object with key-value pairs, like this:

.. code-block:: json

    {
        "OpenAI": "aa-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "DeepSeek": "aa-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    }

Replace the dummy keys (aa-aaaaaaaa...) with your actual API keys. Ensure the file is valid JSON
and contains the target key you want to retrieve.

Alternatively, you can directly type the key into the code by setting the `default_key` parameter
in the `get_api_key` function, such as `default_key="your_key_here"`. This method skips the file
check and uses the provided key directly. Choose the option that best fits your workflow that
best fits your workflow.

Troubleshooting
---------------

If you encounter any issues during installation, here are some common solutions:

1. **Permission Errors**:
   - If you see a permission error when running `pip install .`, try adding `--user` to the command:

     .. code-block:: console

        $ pip install --user .

2. **Python or pip Not Found**:
   - Ensure Python and pip are installed correctly. You can check their versions with:

     .. code-block:: console

        $ python3 --version
        $ pip3 --version

3. **Git Not Found**:
   - If the `git` command is not recognized, ensure Git is installed by following **Step 2** above.

4. **Still Stuck?**:
   - Visit `Discussions <https://github.com/JLX0/auto_research/discussions>`_ for more help or open an issue on the `GitHub repository <https://github.com/JLX0/auto_research/issues>`_.

Next Steps
----------

Now that *AutoResearch* is installed, you can start using it! Check out the :doc:`_examples_gallery/index` to learn how to use the package.