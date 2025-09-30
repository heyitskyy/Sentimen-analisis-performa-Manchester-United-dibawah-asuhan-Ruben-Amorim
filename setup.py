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
