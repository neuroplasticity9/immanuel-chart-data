"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    This module contains the main chart generator class for producing
    chart data for several kinds of chart(s).

"""

import swisseph as swe

from immanuel import const, convert, ephemeris
from immanuel.datetime import DateTime
from immanuel.chart import Chart


class Generator:
    def __init__(self, dt, lat, lon, hsys = None, **kwargs):
        """ Standardise input ready for Chart class. """
        self._lat, self._lon = (convert.string_to_dec(v) for v in (lat, lon))
        self._datetime = dt
        self._dt = DateTime(dt, self._lat, self._lon)
        self._hsys = hsys
        self._kwargs = kwargs

        """ Set up extra ephemeris file location if extra asteroids
        have been requested and a dir has been provided. """
        if kwargs.get('asteroids', None):
            ephemeris_dir = kwargs.get('ephemeris', None)
            if ephemeris_dir:
                ephemeris.set_path(ephemeris_dir)
            else:
                raise Exception('Missing named argument "ephemeris" for asteroid ephemeris location.')

    def chart(self) -> Chart:
        """ Returns a Chart object for the given details. """
        return Chart(self._dt, self._lat, self._lon, self._hsys, self._kwargs)

    def solar_return_chart(self, year: int, lat = None, lon = None) -> Chart:
        """ Returns a solar return chart for the given year. """
        lat, lon = (convert.string_to_dec(v) for v in (lat, lon)) if lat and lon else (self._lat, self._lon)
        year_jd = DateTime(self._datetime.replace(year=year), self._lat, self._lon).jd
        # Get the sun's position & speed for both birthdays
        natal_res, _ = swe.calc_ut(self._dt.jd, const.PLANETS[const.SUN])
        year_res, _ = swe.calc_ut(year_jd, const.PLANETS[const.SUN])
        natal_lon, _, _, natal_speed = natal_res[:4]
        year_lon, _, _, year_speed = year_res[:4]
        # Begin with an approximate calculation
        distance = swe.difdeg2n(year_lon, natal_lon)
        jd = year_jd - (distance / min(natal_speed, year_speed))
        # Narrow it down
        while abs(distance) > const.MAX_ERROR:
            jd += const.JULIAN_INTERVAL if distance < 0 else -const.JULIAN_INTERVAL
            sr_lon = swe.calc_ut(jd, const.PLANETS[const.SUN])[0][0]
            distance = swe.difdeg2n(sr_lon, natal_lon)
        # Generate a chart
        dt = DateTime(jd, lat, lon)
        return Chart(dt, lat, lon, self._hsys, self._kwargs)

    def progressed_chart(self, date_str, lat, lon):
        # TODO: date/time/coords - calculate progressions
        return Chart(self._dt, self._lat, self._lon, self._hsys)

    def composite_chart(self, generator):
        # TODO: mix & relocate
        return Chart(generator.dt, generator.lat, generator.lon, self._hsys)

    def synastry_charts(self, generator):
        # TODO: return 2 charts with aspects to each other
        return Chart(generator.dt, generator.lat, generator.lon, self._hsys)

    def prenatal_lunar_eclipse_chart(self):
        # TODO: find eclipse date
        return Chart(self._dt, self._lat, self._lon, self._hsys)

    def postnatal_lunar_eclipse_chart(self):
        # TODO: find eclipse date
        return Chart(self._dt, self._lat, self._lon, self._hsys)

    def prenatal_solar_eclipse_chart(self):
        # TODO: find eclipse date
        return Chart(self._dt, self._lat, self._lon, self._hsys)

    def postnatal_solar_eclipse_chart(self):
        # TODO: find eclipse date
        return Chart(self._dt, self._lat, self._lon, self._hsys)
