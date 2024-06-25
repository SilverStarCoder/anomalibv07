"""Setup file for anomalib_custom."""

from setuptools import find_packages, setup
from pathlib import Path
from importlib.util import module_from_spec, spec_from_file_location
from types import ModuleType

def load_module(name: str = "src/anomalib/__init__.py") -> ModuleType:
    """Load Python Module.

    Args:
        name (str, optional): Name of the module to load.
            Defaults to "src/anomalib/__init__.py".

    Returns:
        ModuleType: The loaded module.
    """
    location = str(Path(__file__).parent / name)
    spec = spec_from_file_location(name=name, location=location)
    module = module_from_spec(spec)  # type: ignore
    spec.loader.exec_module(module)  # type: ignore
    return module

def get_version() -> str:
    """Get version from `anomalib.__init__`.

    Version is stored in the main __init__ module in `anomalib`.
    The variable storing the version is `__version__`. This function
    reads the `__init__` file, checks the `__version__` variable, and returns
    the value assigned to it.

    Example:
        >>> # Assume that __version__ = "0.2.6"
        >>> get_version()
        "0.2.6"

    Returns:
        str: `anomalib` version.
    """
    anomalib = load_module(name="src/anomalib/__init__.py")
    version = anomalib.__version__
    return version

def get_required_packages(requirement_files: list[str]) -> list[str]:
    """Get packages from requirements.txt file.

    This function returns a list of required packages from requirement files.

    Args:
        requirement_files (list[str]): txt files that contain a list of required
            packages.

    Example:
        >>> get_required_packages(requirement_files=["openvino"])
        ['onnx>=1.8.1', 'networkx~=2.5', 'openvino-dev==2021.4.1', ...]

    Returns:
        list[str]: List of required packages.
    """

    required_packages: list[str] = []

    for requirement_file in requirement_files:
        with open(f"requirements/{requirement_file}.txt", encoding="utf8") as file:
            for line in file:
                package = line.strip()
                if package and not package.startswith(("#", "-f")):
                    required_packages.append(package)

    return required_packages

VERSION = get_version()
LONG_DESCRIPTION = (Path(__file__).parent / "README.md").read_text(encoding="utf8")
INSTALL_REQUIRES = get_required_packages(requirement_files=["base"])
EXTRAS_REQUIRE = {
    "loggers": get_required_packages(requirement_files=["loggers"]),
    "notebooks": get_required_packages(requirement_files=["notebooks"]),
    "openvino": get_required_packages(requirement_files=["openvino"]),
    "full": get_required_packages(requirement_files=["loggers", "notebooks", "openvino"]),
}

setup(
    name="anomalib_custom",
    version=VERSION,
    author="Intel OpenVINO",
    author_email="help@openvino.intel.com",
    description="anomalib - Anomaly Detection Library",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="",
    license="Apache License, Version 2.0",
    python_requires=">=3.7",
    package_dir={"": "src"},
    packages=find_packages(where="src", include=["anomalib", "anomalib.*", "anomalib_custom", "anomalib_custom.*"]),
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    include_package_data=True,
    package_data={"": ["config.yaml"]},
    entry_points={"console_scripts": ["anomalib_custom=anomalib.utils.cli.cli:main"]},
)
