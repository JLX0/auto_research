#!/bin/bash
# This script checks and formats Python source code using tools such as `black`, `blackdoc`, `flake8`, `isort`, and `mypy`.
# If run with the `-n` option, the script performs checks without making any modifications.
# If run with the `-f <filepath>` option, it uses the specified file for testing and
# overrides the settings in this file.

# Initialize default variables.
update=1  # Default is to update files.
target="/home/j/experiments/formatter/target_file.py"  # Default target file path.
mypy_target="/home/j/experiments/formatter/target_file.py"  # Default mypy target file path.
# Initialize an empty array to track missing dependencies.
missing_dependencies=()

# Check if the `black` formatting tool is installed.
command -v black &> /dev/null
if [ $? -eq 1 ] ; then
  # Add `black` to the list of missing dependencies if it's not found.
  missing_dependencies+=(black)
fi

# Check if the `blackdoc` tool is installed.
command -v blackdoc &> /dev/null
if [ $? -eq 1 ] ; then
  # Add `blackdoc` to the list of missing dependencies if it's not found.
  missing_dependencies+=(blackdoc)
fi

# Check if the `flake8` linting tool is installed.
command -v flake8 &> /dev/null
if [ $? -eq 1 ] ; then
  # Add `flake8` to the list of missing dependencies if it's not found.
  missing_dependencies+=(flake8)
fi

# Check if the `isort` import-sorting tool is installed.
command -v isort &> /dev/null
if [ $? -eq 1 ] ; then
  # Add `isort` to the list of missing dependencies if it's not found.
  missing_dependencies+=(isort)
fi

# Check if the `mypy` static type checker is installed.
command -v mypy &> /dev/null
if [ $? -eq 1 ] ; then
  # Add `mypy` to the list of missing dependencies if it's not found.
  missing_dependencies+=(mypy)
fi

# If there are missing dependencies, prompt the user to install them.
if [ ! ${#missing_dependencies[@]} -eq 0 ]; then
  echo "The following dependencies are missing:" "${missing_dependencies[@]}"
  # Prompt the user with a yes/no question about installing missing dependencies.
  read -p "Would you like to install the missing dependencies? (y/N): " yn
  # If the user agrees, proceed with installation. Otherwise, exit the script.
  case "$yn" in [yY]*) ;; *) echo "abort." ; exit ;; esac
  # Install the missing dependencies using `pip`.
  pip install "${missing_dependencies[@]}"
fi



# Parse command-line options.
while getopts "nf:" OPT
do
  case $OPT in
    n) update=0  # Set update flag to 0 if `-n` is provided.
       ;;
    f) target="$OPTARG"  # Set target file path based on user input.
       mypy_target="$OPTARG"  # Set mypy target file path to match the specified file.
       ;;
    *) ;;        # Ignore other options.
  esac
done

# Initialize a variable to track if any checks fail.
res_all=0

# Run `black` to check formatting.
res_black=$(black $target --check --diff 2>&1)
if [ $? -eq 1 ] ; then
  # If `black` check fails:
  if [ $update -eq 1 ] ; then
    # Automatically format the code with `black` if the update flag is set.
    echo "black failed. The code will be formatted by black."
    black $target
  else
    # Output the diff and error message if in check-only mode.
    echo "$res_black"
    echo "black failed."
    res_all=1
  fi
else
  echo "black succeeded."  # Indicate success for `black`.
fi

# Run `blackdoc` to check and format docstrings.
res_blackdoc=$(blackdoc $target --check --diff 2>&1)
if [ $? -eq 1 ] ; then
  # If `blackdoc` check fails:
  if [ $update -eq 1 ] ; then
    # Automatically format docstrings with `blackdoc` if the update flag is set.
    echo "blackdoc failed. The docstrings will be formatted by blackdoc."
    blackdoc $target
  else
    # Output the diff and error message if in check-only mode.
    echo "$res_blackdoc"
    echo "blackdoc failed."
    res_all=1
  fi
else
  echo "blackdoc succeeded."  # Indicate success for `blackdoc`.
fi

# Run `flake8` to check for style issues.
res_flake8=$(flake8 $target)
if [ $? -eq 1 ] ; then
  # If `flake8` check fails, display the errors and mark the check as failed.
  echo "$res_flake8"
  echo "flake8 failed."
  res_all=1
else
  echo "flake8 succeeded."  # Indicate success for `flake8`.
fi

# Run `isort` to check import sorting.
res_isort=$(isort $target --check 2>&1)
if [ $? -eq 1 ] ; then
  # If `isort` check fails:
  if [ $update -eq 1 ] ; then
    # Automatically sort imports with `isort` if the update flag is set.
    echo "isort failed. The code will be formatted by isort."
    isort $target
  else
    # Output the errors if in check-only mode.
    echo "$res_isort"
    echo "isort failed."
    res_all=1
  fi
else
  echo "isort succeeded."  # Indicate success for `isort`.
fi

# Run `mypy` to perform static type checking.
res_mypy=$(mypy $mypy_target)
if [ $? -eq 1 ] ; then
  # If `mypy` check fails, display the errors and mark the check as failed.
  echo "$res_mypy"
  echo "mypy failed."
  res_all=1
else
  echo "mypy succeeded."  # Indicate success for `mypy`.
fi

# Exit with a non-zero status if any checks failed.
if [ $res_all -eq 1 ] ; then
  exit 1
fi
