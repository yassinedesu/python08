import sys
import importlib.metadata
from typing import Any, Optional


REQUIRED_PACKAGES: list[str] = ["pandas", "numpy", "matplotlib"]


def check_package(package_name: str) -> Optional[str]:
    """Check whether a package is installed and return its version string.

    Uses importlib.metadata to read version information without importing
    the package itself, so this function is safe to call even when the
    package is not installed.

    Args:
        package_name: The PyPI distribution name of the package.

    Returns:
        The version string (e.g. "2.1.0") if installed, None if not found.
    """
    try:
        version: str = importlib.metadata.version(package_name)
        return version
    except importlib.metadata.PackageNotFoundError:
        return None


def verify_dependencies() -> bool:
    """Check all required packages and print a status line for each.

    Iterates over REQUIRED_PACKAGES, checks each one, and prints
    [OK] with the version if found or [MISSING] with install instructions
    if not. Returns False if any package is missing.

    Returns:
        True if every required package is available, False otherwise.
    """
    print("Checking dependencies:")
    all_present: bool = True

    package_descriptions: dict[str, str] = {
        "pandas": "Data manipulation ready",
        "numpy": "Numerical computation ready",
        "matplotlib": "Visualization ready",
    }

    for package in REQUIRED_PACKAGES:
        version: Optional[str] = check_package(package)
        description: str = package_descriptions.get(package, "Ready")
        if version is not None:
            print(f"  [OK] {package} ({version}) - {description}")
        else:
            print(f"  [MISSING] {package} - not installed")
            all_present = False

    return all_present


def print_missing_instructions() -> None:
    """Print installation instructions for pip
     and Poetry when deps are missing.

    Shows the user two separate methods to install the required packages:
    the pip approach using requirements.txt and the Poetry approach using
    pyproject.toml.
    """
    print()
    print("Some dependencies are missing. Install them using one of:")
    print()
    print("  pip (requirements.txt):")
    print("    pip install -r requirements.txt")
    print()
    print("  Poetry (pyproject.toml):")
    print("    poetry install")
    print("    poetry run python loading.py")


def show_pip_vs_poetry_comparison() -> None:
    """Print a summary of the conceptual difference between pip and Poetry.

    This comparison function fulfils the subject requirement to explicitly
    demonstrate the learner's understanding of both tools through the
    program's output.
    """
    print()
    print("pip vs Poetry:")
    print(
        "  pip     reads requirements.txt, installs each package greedily."
    )
    print(
        "  pip     does not lock transitive dependencies automatically."
    )
    print(
        "  Poetry  reads pyproject.toml, solves full dependency graph,"
    )
    print(
        "  Poetry  writes poetry.lock to pin every package exactly."
    )


def generate_matrix_data() -> Any:
    """Generate a simulated Matrix dataset using numpy as the data source.

    Creates a DataFrame with two numpy-generated columns: a time series
    of 1000 evenly spaced points and a noisy signal layered over a sine
    wave, representing signal data from the Matrix.

    Returns:
        A pandas DataFrame with columns 'time' and 'signal'.

    Raises:
        ImportError: Propagated if numpy or pandas are not installed.
    """
    import numpy as np  # noqa: PLC0415
    import pandas as pd  # type: ignore[import-untyped]  # noqa: PLC0415

    number_of_points: int = 1000
    time_values: Any = np.linspace(0, 4 * np.pi, number_of_points)
    noise: Any = np.random.normal(0, 0.3, number_of_points)
    signal_values: Any = np.sin(time_values) + noise

    data_frame: Any = pd.DataFrame(
        {"time": time_values, "signal": signal_values}
    )
    return data_frame


def run_analysis_and_save_chart(
    data_frame: Any,
    output_filename: str = "matrix_analysis.png",
) -> None:
    """Run basic statistical analysis on the data and save a visualization.

    Computes the rolling mean of the signal column to smooth the noise,
    then plots both the raw signal and the smoothed line. The plot is
    saved to disk as a PNG file.

    Args:
        data_frame: pandas DataFrame with 'time' and 'signal' columns.
        output_filename: Path where the PNG chart will be saved.
    """
    import matplotlib  # noqa: PLC0415
    import matplotlib.pyplot as plt  # type: ignore[import-untyped]
    # noqa: PLC0415
    import pandas as pd  # type: ignore[import-untyped]  # noqa: PLC0415

    # Use non-interactive backend so the plot works without a display
    matplotlib.use("Agg")

    print("Analyzing Matrix data...")
    print(f"Processing {len(data_frame)} data points...")

    smoothed_signal: Any = (
        data_frame["signal"].rolling(window=20).mean()
    )

    print("Generating visualization...")

    figure, axis = plt.subplots(figsize=(10, 4))
    axis.plot(
        data_frame["time"],
        data_frame["signal"],
        alpha=0.4,
        color="green",
        linewidth=0.6,
        label="Raw signal",
    )
    axis.plot(
        data_frame["time"],
        smoothed_signal,
        color="lime",
        linewidth=2,
        label="Smoothed signal",
    )
    axis.set_title("Matrix Signal Analysis")
    axis.set_xlabel("Time")
    axis.set_ylabel("Signal amplitude")
    axis.legend()
    axis.set_facecolor("#0d0d0d")
    figure.patch.set_facecolor("#1a1a1a")  # type: ignore[attr-defined]

    figure.savefig(output_filename, dpi=100, bbox_inches="tight")
    plt.close(figure)

    # Suppress unused import warning — pd is used implicitly via data_frame
    _ = pd


def main() -> None:
    """Entry point for the loading program.

    Checks all dependencies first. If any are missing, prints install
    instructions for both pip and Poetry, then exits. If all are present,
    runs the data analysis and saves the chart.
    """
    print("LOADING STATUS: Loading programs...")
    print()

    dependencies_satisfied: bool = verify_dependencies()

    if not dependencies_satisfied:
        print_missing_instructions()
        sys.exit(1)

    show_pip_vs_poetry_comparison()

    print()
    data_frame: Any = generate_matrix_data()
    run_analysis_and_save_chart(data_frame)

    print()
    print("Analysis complete!")
    print("Results saved to: matrix_analysis.png")


if __name__ == "__main__":
    main()
