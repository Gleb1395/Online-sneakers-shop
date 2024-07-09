import asyncio

import aiohttp
import requests


# First publication
# count languges
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()


async def count_book_author(first_name: str, last_name: str):
    url = f"https://openlibrary.org/search.json?author={first_name}+{last_name}"
    async with aiohttp.ClientSession() as session:
        result = await fetch(session, url)
        if "docs" in result:
            dict_library = result.get("docs")
            list_of_books = []
            for name_book in dict_library:
                if not name_book.get("title") in list_of_books:
                    list_of_books.append(name_book.get("title"))
            return f"Count books: {len(list_of_books)}"
        else:
            return f"No books found"  # NOQA  F541


async def count_languages_author(first_name: str, last_name: str):
    url = f"https://openlibrary.org/search.json?author={first_name}+{last_name}"
    async with aiohttp.ClientSession() as session:
        result = await fetch(session, url)
        if "docs" in result:
            dict_library = result.get("docs")
            languages = set()
            for book in dict_library:
                if "language" in book:
                    languages.update(book["language"])
            return f"Count of languages: {len(languages)}"
        else:
            return f"No books found"  # NOQA  F541


async def get_first_publication_year(first_name: str, last_name: str):
    url = f"https://openlibrary.org/search.json?author={first_name}+{last_name}"
    async with aiohttp.ClientSession() as session:
        result = await fetch(session, url)
        if "docs" in result:
            dict_library = result.get("docs")
            publication_years = [
                book.get("first_publish_year") for book in dict_library if book.get("first_publish_year")
            ]
            if publication_years:
                first_publication_year = min(publication_years)
                return f"First publication year: {first_publication_year}"
            else:
                return f"No publication year found"  # NOQA  F541
        else:
            return f"No books found"  # NOQA  F541


async def main():
    authors = [
        ("Ernest", "Hemingway"),
        ("George", "Orwell"),
        ("Mark", "Twain"),
    ]

    # task_1 = asyncio.create_task(count_book_author('Ernest', 'Hemingway'))
    # task_2 = asyncio.create_task(count_book_author('George', 'Orwell'))
    # task_3 = asyncio.create_task(count_book_author('Mark', 'Twain'))
    # task_4 = asyncio.create_task(count_languages_author('Ernest', 'Hemingway'))
    # task_5 = asyncio.create_task(count_languages_author('George', 'Orwell'))
    # task_6 = asyncio.create_task(count_languages_author('Mark', 'Twain'))
    # task_7 = asyncio.create_task(get_first_publication_year('Ernest', 'Hemingway'))
    # task_8 = asyncio.create_task(get_first_publication_year('George', 'Orwell'))
    # task_9 = asyncio.create_task(get_first_publication_year('Mark', 'Twain'))
    task_1 = [count_book_author(first_name, last_name) for first_name, last_name in authors]
    task_2 = [get_first_publication_year(first_name, last_name) for first_name, last_name in authors]
    task_3 = [count_languages_author(first_name, last_name) for first_name, last_name in authors]
    results = await asyncio.gather(*task_1, *task_2, *task_3)

    for result in results:
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
