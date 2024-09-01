from setuptools import setup, find_packages

setup(
    name="ChatExtractor",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4',
    ],
    entry_points={
        'console_scripts': [
            'extract_chat=extract_chat:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)