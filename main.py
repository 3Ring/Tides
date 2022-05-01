import sys
import asyncio
from typing import Awaitable, Tuple

from selenium.webdriver.common.by import By

from tides import Tides
from helpers import run_parallel


async def scrape_template(browser: Tides, day: str, date: str) -> Tuple:
    "scraper function designed for the 'Tide Times' table template"
    row = await browser.get_element((By.CSS_SELECTOR, f"[data-date='{date}']"))
    row.click()
    await browser.wait_for_change(day)
    sun, body = await run_parallel(
        browser.get_all_elements(
            (
                By.CSS_SELECTOR,
                f"table.tide-table__table > tbody > tr:nth-child(6) > td:first-child > div",
            ),
        ),
        browser.get_all_elements(
            (
                By.CSS_SELECTOR,
                f"table.tide-table__table > tbody > tr:nth-child(5) > td:first-child > div",
            ),
        ),
    )
    sunrise, sunset = sun[0].text, sun[1].text
    tides = []
    for el in body:
        time, height = el.text.split()
        if browser.check_if_daylight(sunrise, time, sunset) == True:
            tides.append((time, height))
    return tides


async def half_moon_bay(browser: Tides) -> dict:
    day = browser.set_alpha_day(browser.dt, "US/Pacific")
    date = browser.set_date(browser.dt, "US/Pacific")
    await browser.nav(
        "https://www.tide-forecast.com/locations/Half-Moon-Bay-California/tides/latest"
    )
    tides = await scrape_template(browser, day, date)
    return {"Half Moon Bay": tides}


async def huntington_beach(browser: Tides) -> dict:
    day = browser.set_alpha_day(browser.dt, "US/Pacific")
    date = browser.set_date(browser.dt, "US/Pacific")
    await browser.nav(
        "https://www.tide-forecast.com/locations/Huntington-Beach/tides/latest"
    )
    tides = await scrape_template(browser, day, date)
    return {"Huntington Beach": tides}


async def providence(browser: Tides) -> dict:
    day = browser.set_alpha_day(browser.dt, "US/Eastern")
    date = browser.set_date(browser.dt, "US/Eastern")
    await browser.nav(
        "https://www.tide-forecast.com/locations/Providence-Rhode-Island/tides/latest"
    )
    tides = await scrape_template(browser, day, date)
    return {"Providence": tides}


async def wrightsville(browser: Tides) -> dict:
    day = browser.set_alpha_day(browser.dt, "US/Eastern")
    date = browser.set_date(browser.dt, "US/Eastern")
    await browser.nav(
        "https://www.tide-forecast.com/locations/Wrightsville-Beach-North-Carolina/tides/latest"
    )
    tides = await scrape_template(browser, day, date)
    return {"Wrightsville Beach": tides}


async def worker(
    tasks: asyncio.Queue[Awaitable], browsers: asyncio.Queue[Tides]
) -> list[dict]:
    """
    Takes a scrape function and a browser from their respective queues and runs them together.

    :param tasks: asyncio.Queue filled with scrape functions
    :param browsers: asyncio.Queue filled with browsers
    """
    ret = []
    while not tasks.empty():
        if browsers.empty():
            await asyncio.sleep(0.1)
            continue
        task = await tasks.get()
        browser = await browsers.get()
        ret.append(await task(browser))
        browser.clear_cookies()
        await browsers.put(browser)
    return ret


async def main() -> list[dict]:
    """
    Main function that creates the headless browsers and delegates them to the per-page functions to scrape

    The amount of browsers created is determined from the command line.
    example "python main.py 1" will spawn 1 browser "python main.py 3" will spawn 3, etc...

    :return: A list of dictionaries.
    """
    workers = int(sys.argv[1]) if len(sys.argv) == 2 else 3
    try:
        browsers = await run_parallel(
            *(asyncio.to_thread(Tides.make_chrome) for _ in range(workers))
        )
        scrape_queue = asyncio.Queue()
        browser_queue = asyncio.Queue()
        for b in browsers:
            await browser_queue.put(Tides(b))
        for task in [half_moon_bay, huntington_beach, providence, wrightsville]:
            await scrape_queue.put(task)
        dicts = await run_parallel(
            *(
                asyncio.create_task(worker(scrape_queue, browser_queue))
                for _ in range(len(browsers))
            )
        )
        ret = []
        for thread in dicts:
            for location in thread:
                ret.append(location)
        return ret
    except:  # this is intentionally a naked exception
        print(f"Something went wrong")
    finally:
        await run_parallel(*(asyncio.to_thread(b.quit) for b in browsers))
        for b in browsers:
            try:
                assert b.service.process is None
            except AssertionError:
                b.quit()


print(asyncio.run(main()))
