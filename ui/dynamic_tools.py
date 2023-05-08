import os


def get_seasalt_modules():
    seasalt_modules = {}
    scrapers = []
    for scraper in os.listdir("seasalt/modules/scrapers"):
        if scraper.endswith(".py"):
            scraper = scraper.replace(".py", "")
            scrapers.append(scraper)
    seasalt_modules["scrapers"] = scrapers
    return seasalt_modules
