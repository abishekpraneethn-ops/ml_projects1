from setuptools import setup, find_packages
from typing import List

CONST = "-e ."
def get_requirements(file_path:str)->List[str]:
    """Read requirements from requirements.txt"""
    requirements = []
    with open(file_path) as file:
        requirements = file.readlines()
        requirements = [req.replace("\n", "") for req in requirements]

        if CONST in requirements:
            requirements.remove(CONST)

    return requirements


setup(
    name="ml_project_01",
    version="0.0.1",
    author="abishek_praneeth",
    author_email="abishekpraneethn@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt"),
)
