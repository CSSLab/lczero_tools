"""Package setup script."""
import setuptools

setuptools.setup(
    name='lczero-tools',
    version='0.2',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'numpy',
        'python-chess',
    ],
    extras_require={
        'tf': ['tensorflow'],
        'tf-gpu': ['tensorflow-gpu'],
        'torch': ['torch'],
        'util': ['tqdm', 'requests', 'BeautifulSoup4', 'fire'],
    },
    setup_requires=[],
    tests_require=[],
)
