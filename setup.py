from setuptools import find_packages, setup

setup(
    name='microblog',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'boto3==1.10.17',
        'botocore==1.13.17',
        'Click==7.0',
        'docutils==0.15.2',
        'Flask==1.1.1',
        'itsdangerous==1.1.0',
        'Jinja2==2.10.3',
        'jmespath==0.9.4',
        'Markdown==3.1.1',
        'MarkupSafe==1.1.1',
        'mysqlclient==1.4.5',
        'peewee==3.11.2',
        'python-dateutil==2.8.0',
        's3transfer==0.2.1',
        'six==1.13.0',
        'urllib3==1.25.7',
        'Werkzeug==0.16.0'
    ],
)