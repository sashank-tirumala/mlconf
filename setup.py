from setuptools import find_packages, setup

setup(
    name="mlconf",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[],
    extras_require={
        "dev": [
            "pytest",
            "sphinx",
        ],
    },
)
