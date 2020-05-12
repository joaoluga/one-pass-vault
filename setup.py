import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="one_pass_vault",
    version="1.0.0",
    author="Joao Lugarinho Menezes",
    author_email="joao.menezes@creditas.com.br",
    description="Tools to safely interact with 1Password",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/one-pass-vault",
    packages=setuptools.find_namespace_packages(),
    entry_points={
        "console_scripts": [
            "one-pass-vault=one_pass_vault:one_pass_vault"
        ]
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    python_requires='>=3.6'
)
