from setuptools import find_packages, setup


setup(
    name='pysite',
    url='https://pythondiscord.com',
    description="Python Discord community website",
    project_urls={
        'Source code': 'https://gitlab.com/python-discord/projects/site'
    },
    version='0.2.0',
    packages=find_packages(
        exclude=('**/static',)
    ),
    python_requires='>= 3.6',
    install_requires=[
        'django>=2.1.1',
        'djangorestframework>=3.8.2',
        'djangorestframework-bulk>=0.2.1',
        'django-hosts>=3.0',
        'django-environ>=0.4.5',
        'psycopg2-binary>=2.7.5'
    ],
    extras_require={
        'deploy': [
            'gunicorn>=19.9.0',
        ],
        'lint': [
            'flake8>=3.5.0',
            'flake8-bandit>=1.0.2',
            'flake8-bugbear>=18.8.0',
            'flake8-import-order>=0.18',
            'flake8-string-format>=0.2.3',
            'flake8-tidy-imports>=1.1.0',
            'pep8-naming>=0.7.0',
            'mccabe>=0.6.1'
        ],
        'test': [
            'coverage>=4.5.1'
        ]
    },
    entry_points={
        'console_scripts': (
            'psmgr = manage:main',
        )
    }
)
