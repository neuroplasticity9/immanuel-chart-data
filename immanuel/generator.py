"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    This module contains the main chart generator class for producing
    chart data for several kinds of chart(s).

"""

from datetime import datetime
from dateutil.relativedelta import relativedelta

import swisseph as swe

from immanuel import const, convert, dates, ephemeris
from immanuel.chart import Chart
from immanuel.dates import DateTime


class Generator:
    def __init__(self, dt: datetime, lat: float, lon: float, hsys = None, **kwargs):
        """ Standardise input ready for Chart class. """
        self._lat, self._lon = (convert.string_to_dec(v) for v in (lat, lon))
        self._dt = DateTime(dt, self._lat, self._lon)
        self._hsys = const.HOUSE_SYSTEMS[hsys if hsys is not None else const.PLACIDUS]
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

    def solar_return_chart(self, year: int, lat: float = None, lon: float = None) -> Chart:
        """ Returns a solar return chart for the given year. """
        year_diff = year - self._dt.datetime.year
        jd = self._dt.jd + year_diff * const.YEAR_DAYS
        natal_lon = swe.calc_ut(self._dt.jd, const.PLANETS[const.SUN])[0][0]

        while True:
            sr_res = swe.calc_ut(jd, const.PLANETS[const.SUN])[0]
            sr_lon, sr_speed = sr_res[0], sr_res[3]
            distance = swe.difdeg2n(natal_lon, sr_lon)
            if abs(distance) <= const.MAX_ERROR:
                break
            jd += distance / sr_speed

        lat, lon = (convert.string_to_dec(v) for v in (lat, lon)) if lat and lon else (self._lat, self._lon)
        dt = DateTime(jd, lat, lon)
        return Chart(dt, lat, lon, self._hsys, self._kwargs)

    def progressed_chart(self, dt: datetime, lat: float = None, lon: float = None) -> Chart:
        """ Calculates the number of years-as-days and returns a secondary
        progression chart. """
        lat, lon = (convert.string_to_dec(v) for v in (lat, lon)) if lat and lon else (self._lat, self._lon)
        progression_dt = DateTime(dt, lat, lon)
        days_diff = dates.datetime_to_jd(progression_dt) - dates.datetime_to_jd(self._dt)
        as_years = days_diff / const.YEAR_DAYS
        dt = DateTime(self._dt.datetime + relativedelta(days=as_years), lat, lon)

        armc = swe.houses_ex2(self._dt.jd, self._lat, self._lon, self._hsys)[1][swe.ARMC]
        armc += as_years * const.MEAN_MOTIONS[const.SUN]
        obliquity = swe.calc_ut(dt.jd, swe.ECL_NUT)[0][0]
        swe_angles_houses = swe.houses_armc_ex2(armc, lat, obliquity, self._hsys)

        kwargs = {
            **self._kwargs,
            'swe_houses_angles': swe_angles_houses,
        }

        return Chart(dt, lat, lon, self._hsys, kwargs)

    def composite_chart(self, generator):
        # TODO: mix & relocate
        return Chart(generator.dt, generator.lat, generator.lon, self._hsys)

    def synastry_charts(self, generator):
        # TODO: return 2 charts with aspects to each other
        return Chart(generator.dt, generator.lat, generator.lon, self._hsys)
