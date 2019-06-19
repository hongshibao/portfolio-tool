from setuptools import setup, find_packages


about = {}
# read __version__ from version.py
with open('portfolio/version.py') as f:
    exec(f.read(), about)
# read README.md as long_description
with open('README.md') as f:
    long_description = '\n' + f.read()

setup(
    name='portfolio-tool',
    version=about['__version__'],
    description='A simple tool to compute portfolio daily price with currency impact',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.7.0',
    url='https://github.com/hongshibao/portfolio-tool',
    packages=find_packages(),
)
