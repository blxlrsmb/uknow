from setuptools import setup


setup_args = dict(
    name='unknown',
    install_requires=[
        'Flask>=0.9',
        'Flask-WTF>=0.8',
        'pyjade>=1.6'
    ],
    entry_points=dict(
        console_scripts=[
            'unknown-website = unknown.website.app:main',
            ],
    ),
)

if __name__ == '__main__':
    setup(**setup_args)
