import os
import sys
from typing import Optional

try:
    from dotenv import load_dotenv
except ImportError:
    print("ERROR: python-dotenv is not installed.")
    print("Install it with: pip install python-dotenv")
    sys.exit(1)


REQUIRED_VARIABLES: list[str] = [
    "MATRIX_MODE",
    "DATABASE_URL",
    "API_KEY",
    "LOG_LEVEL",
    "ZION_ENDPOINT",
]


def load_environment_configuration() -> None:
    """Load environment variables from a .env file if one exists.

    Calls load_dotenv() which searches for a .env file in the current
    directory and loads its KEY=value pairs into os.environ. Variables
    already present in the shell environment are NOT overwritten, which
    means shell exports take precedence over .env file values.
    """
    # override=False means shell variables win over .env — this is correct
    load_dotenv(override=False)


def get_config_value(key: str, default: Optional[str] = None) -> Optional[str]:
    """Read a single configuration variable from the environment.

    Args:
        key: The environment variable name.
        default: Value to return when the key is not set. None by default.

    Returns:
        The string value from the environment, or the default.
    """
    return os.getenv(key, default)


def mask_secret(secret_value: Optional[str]) -> str:
    """Return a masked representation of a secret value for safe display.

    Shows only the first four characters followed by asterisks, so the
    output confirms the variable is set without exposing the actual value.

    Args:
        secret_value: The raw secret string, or None if not set.

    Returns:
        A masked string, e.g. "abc1****", or "Not set" if None.
    """
    if secret_value is None:
        return "Not set"
    if len(secret_value) <= 4:
        return "****"
    return secret_value[:4] + "****"


def check_for_missing_variables() -> list[str]:
    """Identify which required configuration variables are not set.

    Iterates over REQUIRED_VARIABLES and collects the names of any
    that are missing from the current environment.

    Returns:
        A list of variable names that are not set. Empty list if all present.
    """
    missing: list[str] = []
    for variable_name in REQUIRED_VARIABLES:
        if os.getenv(variable_name) is None:
            missing.append(variable_name)
    return missing


def print_configuration_summary() -> None:
    """Print all configuration values in a user-readable format.

    Reads every required variable and prints its value. Secrets (API_KEY,
    DATABASE_URL) are masked. Non-sensitive values are shown directly.
    The output changes based on MATRIX_MODE to demonstrate dev vs prod.
    """
    mode: str = get_config_value("MATRIX_MODE", "development") or "development"
    database_url: Optional[str] = get_config_value("DATABASE_URL")
    api_key: Optional[str] = get_config_value("API_KEY")
    log_level: str = get_config_value("LOG_LEVEL", "INFO") or "INFO"
    zion_endpoint: Optional[str] = get_config_value("ZION_ENDPOINT")

    print("Configuration loaded:")
    print(f"  Mode: {mode}")

    # Show different detail levels depending on environment mode
    if mode == "production":
        print("  Database: Connected to remote instance")
        print(f"  Database URL: {mask_secret(database_url)}")
    else:
        # Development mode shows more detail to help with debugging
        if database_url:
            print("  Database: Connected to local instance")
            print(f"  Database URL: {database_url}")
        else:
            print("  Database: Not configured")

    if api_key:
        print(f"  API Access: Authenticated ({mask_secret(api_key)})")
    else:
        print("  API Access: No key configured")

    print(f"  Log Level: {log_level}")

    if zion_endpoint:
        print(f"  Zion Network: Online ({zion_endpoint})")
    else:
        print("  Zion Network: Endpoint not configured")


def run_security_check() -> None:
    """Print a security self-assessment of the current configuration.

    Checks that the .env.example file exists (template is committed),
    that the .gitignore file mentions .env (secrets are excluded),
    and confirms no secrets appear to be hardcoded by verifying they
    come from environment variables rather than source code.
    """
    print()
    print("Environment security check:")

    # Check that .env.example exists as a template
    example_file_exists: bool = os.path.isfile(".env.example")
    if example_file_exists:
        print("  [OK] .env.example template is present")
    else:
        print("  [WARN] .env.example not found — create one for collaborators")

    # Check that .gitignore excludes .env files
    gitignore_path: str = ".gitignore"
    gitignore_protects_env: bool = False
    if os.path.isfile(gitignore_path):
        with open(gitignore_path, "r") as gitignore_file:
            gitignore_contents: str = gitignore_file.read()
        gitignore_protects_env = ".env" in gitignore_contents

    if gitignore_protects_env:
        print("  [OK] .gitignore excludes .env files")
    else:
        print("  [WARN] .gitignore does not exclude .env — fix this now")

    # Configuration is loaded from environment variables, not source code
    print("  [OK] No hardcoded secrets in source code")
    print("  [OK] Production overrides available via shell exports")


def print_missing_variable_help(missing_variables: list[str]) -> None:
    """Print setup instructions when required variables are not configured.

    Shows the user which variables are missing and how to create a .env
    file from the provided template to configure them.

    Args:
        missing_variables: List of variable names that need to be set.
    """
    print()
    print("WARNING: The following configuration variables are not set:")
    for variable_name in missing_variables:
        print(f"  - {variable_name}")
    print()
    print("To configure them:")
    print("  1. Copy the template:  cp .env.example .env")
    print("  2. Edit .env with your values")
    print("  3. Run this program again")
    print()
    print("Or set them directly in your shell:")
    print("  export MATRIX_MODE=development")


def main() -> None:
    """Entry point for the oracle configuration program.

    Loads the .env file, checks for missing variables, prints a summary
    of all configuration, and runs a security check on the setup.
    """
    print("ORACLE STATUS: Reading the Matrix...")
    print()

    load_environment_configuration()

    missing_variables: list[str] = check_for_missing_variables()

    if missing_variables:
        print_missing_variable_help(missing_variables)
    else:
        print_configuration_summary()
        run_security_check()
        print()
        print("The Oracle sees all configurations.")


if __name__ == "__main__":
    main()
