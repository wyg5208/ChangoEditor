"""
Chango Editor - 轻量级代码编辑器
一个类似Sublime Text的Python代码编辑器
"""
import os
from setuptools import setup, find_packages

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="chango-editor",
    version="0.1.0",
    author="Chango Team",
    author_email="team@chango.com",
    description="轻量级Python代码编辑器",
    long_description=open("README.md", "r", encoding="utf-8").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/aweng1977/chango/chango-editor",
    packages=find_packages(),
    package_dir={"": "src"},
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Text Editors",
        "Topic :: Software Development",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "chango-editor=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["resources/*", "resources/themes/*", "resources/icons/*"],
    },
)
