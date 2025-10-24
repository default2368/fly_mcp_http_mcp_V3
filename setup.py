from setuptools import setup, find_packages

setup(
    name="claude_mcp_remote",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'uvicorn',
    ],
    python_requires='>=3.7',
)
