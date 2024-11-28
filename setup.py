from setuptools import setup, find_packages

setup(
    name='fantia-crawler',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    
    # Dependencies
    install_requires=[
        'selenium',
        'requests',
        'pillow',
    ],
    
    # Console script entry point
    entry_points={
        'console_scripts': [
            'fantia-crawler=fantia_crawler.cli:main',
        ],
    },
    
    # Metadata
    author='ChowDPa02K',
    author_email='chowdpa02k@outlook.com',
    description='A metadata crawler for downloaded Fantia videos',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ChowDPa02k/fantia-crawler',
    
    # Classifiers
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)