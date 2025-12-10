from setuptools import setup, find_packages

setup(
    name="dataops-toolkit",
    version="0.1.0",
    description="A Modular Automation Framework for JSON, CSV, and Excel Workflows",
    author="QA Automation Engineer",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas",
        "openpyxl",
        "click",
    ],
    extras_require={
        "dev": [
            "pytest",
            "black",
            "flake8",
        ]
    },
    entry_points={
        "console_scripts": [
            "dataops=dataops.cli:main",
        ],
    },
    python_requires=">=3.8",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
