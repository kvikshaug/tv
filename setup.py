from setuptools import setup

setup(
    name="tv",
    version="0.0.1",
    py_modules=["tv"],
    install_requires=["click", "requests", "tabulate"],
    entry_points="""
        [console_scripts]
        tv=tv.tv:cli
    """,
)
