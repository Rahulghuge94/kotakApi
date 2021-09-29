import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'kotakApi',
    packages=setuptools.find_packages(),
    version = '0.0.1',
    include_package_data=True,
    description = 'kotak Trading api',
    long_description=long_description,
    long_description_content_type="text/markdown",  author = 'Rahul',
    author_email = '1994ghuge.gmail.com',
    url = 'https://github.com/Rahulghuge94/trade',
    install_requires=['requests', 'pandas',"retry"],
    keywords = ['kotak', 'api', 'python', 'sdk', 'trading', 'stock markets'],
    classifiers=[
      'Intended Audience :: Developers',
      'Natural Language :: English',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
      'Programming Language :: Python :: 3.6'])
