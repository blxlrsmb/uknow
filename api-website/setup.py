from setuptools import setup


setup_args = dict(
    name='api-website',
    install_requires=[
        'Flask>=0.9',
    ],
    entry_points=dict(
        console_scripts=[
            'api-website = standalone_server:main',
            ],
    ),
)

if __name__ == '__main__':
    setup(**setup_args)
