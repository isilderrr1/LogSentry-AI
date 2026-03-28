from setuptools import setup, find_packages

setup(
    name='log-sentry-ai',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'logsentry=src.cli.tui:main',
        ],
    },
    install_requires=[
        'click>=8.1.0',
        'pandas>=2.0.0',
        'pytest>=7.0.0',
        'openai>=1.0.0',
        'tqdm>=4.65.0',
        'rich>=13.0.0',
        'questionary>=2.0.0',
        'python-dotenv>=1.0.0'
    ]
)
