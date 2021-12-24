"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    This module contains the main chart generator class for producing
    chart data for several kinds of chart(s).

"""

from immanuel import convert, ephemeris
from immanuel.datetime import DateTime
from immanuel.chart import Chart


class Generator:
    def __init__(self, dt, lat, lon, hsys = None, **kwargs):
        """ Standardise input ready for Chart class. """
        self._lat, self._lon = (convert.string_to_dec(v) for v in (lat, lon))
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

    def chart(self):
        # Natal / transit
        return Chart(self._dt, self._lat, self._lon, self._hsys, self._kwargs)

    def solar_return_chart(self, year):
        # TODO: find solar return date
        return Chart(self._dt, self._lat, self._lon, self._hsys)

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
