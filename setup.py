from setuptools import setup, find_packages

setup(
    name='scion',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['argparse', 'BytecodeAssembler',
                      'pyparsing', 'nose'],
    
    entry_points={
        'console_scripts' : [
            'scion=scion.run:main',
            ]
        }
    )
