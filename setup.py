<<<<<<< HEAD
from setuptools import setup, find_packages

setup(
    name="twitter_sentiment_crawling",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "snscrape",
        "pandas",
        "matplotlib",
        "wordcloud",
        "textblob",
        "langdetect",
        "transformers",
        "torch"
    ],
    entry_points={
        "console_scripts": [
            "twitter-crawl=main:main"
        ]
    }
)
=======
from setuptools import setup, find_packages

setup(
    name="twitter_sentiment_crawling",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "snscrape",
        "pandas",
        "matplotlib",
        "wordcloud",
        "textblob",
        "langdetect",
        "transformers",
        "torch"
    ],
    entry_points={
        "console_scripts": [
            "twitter-crawl=main:main"
        ]
    }
)
>>>>>>> 5c68ab5b4314e747a6ae1232de0c8db13f6bf681
