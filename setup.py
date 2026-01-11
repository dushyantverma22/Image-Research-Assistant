from setuptools import setup, find_packages

setup(
    name="image-assistant",
    version="0.0.1",
    author="Dushyant Verma",
    author_email="dushyantdchss@gmail.com",
    description="Image Research Assistant using MCP, LangGraph and Gradio",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.9",
)
