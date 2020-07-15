from setuptools import setup

setup(
    name='webpage_text',
    version='0.1.0.dev0',
    author='Joseph Borbely',
    author_email='joseph.borbely@measurement.govt.nz',
    url='https://github.com/MSLNZ/pr-webpage-text',
    description='Update and view text on a web page',
    long_description=open('README.rst').read().strip(),
    license='MIT',
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=['flask', 'gevent', 'requests'],
    packages=['webpage_text'],
    entry_points={
        'console_scripts': [
            'webpage-text = webpage_text:run',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
