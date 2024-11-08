from importlib.metadata import version, PackageNotFoundError
import os


def get_package_version(package_name: str) -> str:
    """
    Get the version of the specified package.
    """
    try:
        return version(package_name)
    except PackageNotFoundError:
        return "Package not found"


def get_api_huggingface_key() -> str:
    api_key = os.environ.get("HUGGINGFACE_API_KEY")
    if api_key is None:
        raise ValueError(
            "HUGGINGFACE_API_KEY is not set, please set it in your environment variables")
    return api_key


def get_openai_api_key() -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key is None:
        raise ValueError(
            "OPENAI_API_KEY is not set, please set it in your environment variables")
    return api_key


def get_groq_api_key() -> str:
    api_key = os.environ.get("GROQ_API_KEY")
    if api_key is None:
        raise ValueError(
            "GROQ_API_KEY is not set, please set it in your environment variables")
    return api_key
