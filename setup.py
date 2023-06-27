import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name="showcase",
    description="Development showcase for Lean TECHniques",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="0.0",
    author="Paul Svensson",
    author_email="paul@svensson.org",
    home_page="https://github.com/PaulSvensson/showcase.git",
    platforms=["any"],
    packages=[],
    entry_points={
        "console_scripts": [
            "photo_album = photo_album:main",
        ],
    },
    license="For candidate evaluation only",
)
