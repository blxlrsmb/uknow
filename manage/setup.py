from setuptools import setup

setup_args = dict(
    name='uknow',
    install_requires=[
        'Flask>=0.9',
        'Flask-WTF>=0.8',
        'Flask-Login>=0.2.7',
        'pyjade>=1.6',

        'pymongo>=2.6.3',
        'celery>=3.1.1',
        'redis>=2.8.0',
        'gevent>=0.13.8',
        'sphinx>=1.1.3',
        'pep8>=1.4.6',
        'feedparser==5.1.3',

        'jieba>=0.31',
        'nltk>=2.0.4',
        'html2text>=3.200.3'
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
