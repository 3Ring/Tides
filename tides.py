import asyncio
from typing import Any, Awaitable
from datetime import datetime

import pytz
from selenium.webdriver.common.by import By

from browser import Browser


class Tides(Browser):
    def __init__(self, driver):
        super().__init__(driver)
        self.dt = datetime.utcnow()

    def _convert_time(self, time: str) -> int:
        """
        It takes a string of time in the format "HH:MM AM/PM" and returns an integer of the time in the
        format "HHMM"

        :param time: The time to convert
        :return: The integer representation of time in 24 hour format.
        """
        time = "".join(time.split(":"))
        if time[-2] == "P":
            return int(str(int(time[0]) + 12) + time[1:-2])
        return int(time[:-2])

    def check_if_daylight(self, sunrise: str, time: str, sunset: str) -> bool:
        """If the time is between sunrise and sunset, return True"""
        return (
            self._convert_time(sunrise)
            < self._convert_time(time)
            < self._convert_time(sunset)
        )

    def set_alpha_day(self, time: datetime, tmzn: str) -> str:
        """
        It takes a datetime object and a timezone string as arguments, and returns the day of the week in
        alpha format
        """
        days = {
            1: "Mon",
            2: "Tue",
            3: "Wed",
            4: "Thu",
            5: "Fri",
            6: "Sat",
            7: "Sun",
        }
        pdt = pytz.timezone(tmzn)
        return days[time.astimezone(pdt).isoweekday()]

    def set_date(self, time: datetime, tmzn: str) -> str:
        """
        It takes a datetime object and a timezone string as arguments, and returns a string of the date in
        the specified timezone
        """

        pdt = pytz.timezone(tmzn)
        pytz.all_timezones
        fmt = "%Y-%m-%d"
        return time.astimezone(pdt).strftime(fmt)

    async def wait_for_change(self, day: str) -> None:
        """waits for the DOM to update after clicking on the column header"""
        check = (
            By.CSS_SELECTOR,
            f"table.tide-table__table > tbody > tr:nth-child(2) > td:first-child",
        )
        waiting = 0
        checking = await self.get_element(check)
        while day not in checking.text:
            await asyncio.sleep(0.25)
            checking = await self.get_element(check)
            waiting += 1
            if waiting == 3:
                raise Exception

    async def scrape(self, *functions: Awaitable[Any]) -> Any:
        return await self._run_parallel(*functions)
