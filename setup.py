from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ChatBox",
    version="1.0.0",
    author="SantanaRichie",
    description="A peer-to-peer chat application using network connections",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SantanaRichie/ChatBox",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Communications :: Chat",
    ],
    python_requires=">=3.9",
    install_requires=[
        "customtkinter>=5.0",
        "pyyaml>=6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.900",
            "pyinstaller>=6.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "chatbox=scripts.login:main",
        ],
    },
)
