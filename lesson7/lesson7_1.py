import nest_asyncio
import asyncio
from crawl4ai import AsyncWebCrawler
nest_asyncio.apply()

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://example.com")

if __name__ == "__main__":
    asyncio.run(main())
