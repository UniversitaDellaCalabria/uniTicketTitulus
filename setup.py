from setuptools import setup, find_packages

setup(
    name="uni_ticket_titulus",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    description="Cineca Titulus interface for uniTicket based on dj-titulus-utility",
    author="Francesco Filicetti",
    author_email="francesco.filicetti@unical.it",

    install_requires=[
        "Django>=5.2",
        "django-titulus-utility @ git+https://github.com/UniversitaDellaCalabria/dj-titulus-utility.git",
    ],
)
