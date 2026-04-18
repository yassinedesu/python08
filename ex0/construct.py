import os
import sys
import site


def is_virtual_environment() -> bool:
    """Detect whether this process is running inside a virtual environment.

    Compares sys.prefix (the current env root) with sys.base_prefix
    (the original Python installation root). They are equal in a global
    environment and differ when inside a venv.

    Returns:
        True if running inside a virtual environment, False otherwise.
    """
    return sys.prefix != sys.base_prefix


def get_virtual_environment_name() -> str:
    """Extract the name of the active virtual environment from its path.

    Reads the VIRTUAL_ENV environment variable (set by the activate script)
    and returns only the final directory component.

    Returns:
        The name of the virtual environment folder, e.g. "matrix_env".
        Returns "Unknown" if the variable is not set.
    """
    virtual_env_path: str = os.environ.get("VIRTUAL_ENV", "")
    if virtual_env_path:
        return os.path.basename(virtual_env_path)
    return "Unknown"


def get_package_installation_path() -> str:
    """Return the first site-packages directory for the current environment.

    Uses the site module to locate where installed packages live in this
    Python environment.

    Returns:
        Absolute path to the site-packages directory as a string.
        Falls back to a descriptive message if the path cannot be found.
    """
    try:
        packages: list[str] = site.getsitepackages()
        return packages[0]
    except AttributeError:
        # site.getsitepackages is not available in all environments
        return "Path unavailable in this environment"


def show_virtual_environment_details() -> None:
    """Print environment details when running inside a virtual environment.

    Displays the MATRIX STATUS header, current Python executable path,
    virtual environment name, environment root path, a success message,
    and the package installation path.
    """
    venv_name: str = get_virtual_environment_name()
    venv_path: str = os.environ.get("VIRTUAL_ENV", sys.prefix)
    package_path: str = get_package_installation_path()

    print("MATRIX STATUS: Welcome to the construct")
    print()
    print(f"Current Python: {sys.executable}")
    print(f"Virtual Environment: {venv_name}")
    print(f"Environment Path: {venv_path}")
    print()
    print("SUCCESS: You're in an isolated environment!")
    print("Safe to install packages without affecting")
    print("the global system.")
    print()
    print("Package installation path:")
    print(package_path)


def show_global_environment_warning() -> None:
    """Print a warning and setup instructions
     when not in a virtual environment.

    Tells the user they are in the global Python environment and provides
    step-by-step instructions for creating and activating a virtual
    environment before running the program again.
    """
    print("MATRIX STATUS: You're still plugged in")
    print()
    print(f"Current Python: {sys.executable}")
    print("Virtual Environment: None detected")
    print()
    print("WARNING: You're in the global environment!")
    print("The machines can see everything you install.")
    print()
    print("To enter the construct, run:")
    print("  python -m venv matrix_env")
    print("  source matrix_env/bin/activate  # On Unix")
    print("  matrix_env\\Scripts\\activate     # On Windows")
    print()
    print("Then run this program again.")


def main() -> None:
    """Entry point. Route to the correct output based on venv detection."""
    if is_virtual_environment():
        show_virtual_environment_details()
    else:
        show_global_environment_warning()


if __name__ == "__main__":
    main()
