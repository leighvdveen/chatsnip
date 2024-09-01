from setuptools import setup, find_packages

setup(
    name="chatsnip",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'Flask',
        'streamlit',
        'ijson',
        'Werkzeug',
    ],
    entry_points={
        'console_scripts': [
            'chatsnip=chatsnip:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    description="A tool for extracting and managing chat data from HTML files.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    exclude_package_data={'': ['uploads/*']},  # Exclude the uploads directory
    url="https://github.com/leighvdveen/chatsnip",  # Add your repository URL
    author="Leigh-Anne Wells",  # Add your name
    author_email="leighanne.vdveen@gmail.com",  # Add your email address
)