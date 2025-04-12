from setuptools import setup, find_packages


REPO_NAME = "ML Based Book Recommender System"
AUTHOR_USER_NAME = "Amman Sajid"
AUTHOR_EMAIL = "ammansajid1@gmail.com"
SRC_REPO = "book_recommender"
LIST_OF_REQUIREMENTS = []

setup(
    name=SRC_REPO,
    version="0.0.1",
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    packages=find_packages(),
    install_requires=LIST_OF_REQUIREMENTS,
    python_requires=">=3.6",
)
