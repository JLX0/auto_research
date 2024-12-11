# mypy: disable-error-code="assignment"
# flake8: noqa
import os
import pkgutil


# Dynamically import all subcomponents in the current directory
__all__ = []  # Define public API
for _, module_name, _ in pkgutil.iter_modules([os.path.dirname(__file__)]):
    __all__.append(module_name)  # Add to public API
    globals()[module_name] = __import__(f"{__name__}.{module_name}", fromlist=[module_name])


"""
Dynamic imports, like the code here, are generally safe if the following conditions are met:
1. Unique Submodule Names: All submodules have distinct names to avoid naming collisions in 
globals().
2. No Top-Level Side Effects: Submodules do not execute significant logic or alter state at the 
time of import.
3. Controlled Import Scope: Dynamically imported modules are only accessible within their parent 
namespace and not exposed at higher levels unless explicitly re-exported.
4. Modular and Lightweight Submodules: Submodules are small and modular, minimizing performance or 
memory overhead.

This code does no support cross-level imports.

This code disables the mypy error code "assignment" to suppress the checks for 
reassignment of variables.

This code disables the flake8 error code "noqa" to suppress the checks for
flake8 errors.
"""
