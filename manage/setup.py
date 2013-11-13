from setuptools import setup

setup_args = dict(
    name='uknow',
    install_requires=[
        'Flask>=0.9',
        'Flask-WTF>=0.8',
        'pyjade>=1.6',

        'pymongo>=2.6.3',
        'celery>=3.1.1',
        'redis>=2.8.0',
        'gevent>=0.13.8'
    ],
    entry_points=dict(
        console_scripts=[
            'api-website = standalone_server:main',
            'fetcher-server = general_fetcher_server',
            'frontend-website = ukfrontend.app:main',
            ],
    ),
)

if __name__ == '__main__':
    setup(**setup_args)
