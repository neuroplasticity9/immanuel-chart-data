"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    This module contains the main Chart class for producing chart data.

    Given a localised date/time and lat/lon coordinates, this class
    will gather all relevant data to create a chart, and is
    fully serialisable for JSON output.

"""

from decimal import Decimal
from operator import itemgetter

import swisseph as swe

from immanuel import angles, aspects, const, convert, dignities, transits
from immanuel.aspects import Aspect
from immanuel.dates import DateTime
from immanuel.items import House, AxisAngle, Planet, Point, Asteroid, FixedStar
from immanuel.serializable import Serializable, SerializableBoolean, SerializableDict


class Chart(Serializable):
    """ The Chart class converts data from pyswisseph's functions into
    useful chart-based data. A Chart class object and all its members
    are serializable.

    """

    ORB_CALC_MEAN = 0
    ORB_CALC_MAX = 1

    def __init__(self, dt: DateTime, lat: float, lon: float, hsys: str, kwargs):
        """ Set private members. """
        self._jd = dt.jd
        self._lat = lat
        self._lon = lon
        self._hsys = hsys
        self._orb_calc = kwargs.get('orb_calc', self.ORB_CALC_MEAN)
        self._aspect_rules = kwargs.get('aspect_rules', const.DEFAULT_ASPECT_RULES)
        self._show_items = kwargs.get('items', const.DEFAULT_ITEMS)
        self._show_aspects = kwargs.get('aspects', const.DEFAULT_ASPECTS)
        self._show_orbs = kwargs.get('orbs', const.DEFAULT_ORBS)
        self._extra_asteroids = kwargs.get('asteroids', ())
        self._stars = kwargs.get('stars', ())
        self._swe_houses_angles = self._get_swe_houses_angles(kwargs.get('swe_houses_angles', None))

        """ Set public members. """
        self.date = dt.isoformat()
        self.latitude = convert.dec_to_string(lat, convert.FORMAT_LAT)
        self.longitude = convert.dec_to_string(lon, convert.FORMAT_LON)
        self.type = self._type()
        self.moon_phase = self._moon_phase()
        self.obliquity = self._obliquity()
        self.houses = self._houses()
        self.angles = self._angles()
        self.planets = self._planets()
        self.points = self._points()
        self.asteroids = self._asteroids()
        self.fixed_stars = self._fixed_stars()
        self.aspects = self._aspects()

        """ Set planet relationship data. """
        self._mutual_receptions()
        self._dignities()

    def _get_swe_houses_angles(self, swe_houses_angles: tuple = None) -> dict:
        """ This must be called first before the other chart methods. """
        houses_angles = swe_houses_angles if swe_houses_angles is not None else swe.houses_ex2(self._jd, self._lat, self._lon, self._hsys)
        return dict(zip(('cusps', 'ascmc', 'cuspsspeed', 'ascmcspeed'), houses_angles))

    def _type(self) -> SerializableBoolean:
        """ Determine whether this is a day or a night chart. """
        sun = swe.calc_ut(self._jd, const.PLANETS[const.SUN])[0][0]
        asc = self._swe_houses_angles['ascmc'][const.ANGLES[const.ASC]]
        distance = swe.difdeg2n(sun, asc)

        return SerializableBoolean({
            const.DIURNAL: distance < 0,
            const.NOCTURNAL: distance >= 0,
        })

    def _houses(self) -> SerializableDict:
        """ Get the house cusps from _swe_houses_angles. """
        houses = SerializableDict()
        cusps, cuspsspeed = itemgetter('cusps', 'cuspsspeed')(self._swe_houses_angles)

        for i, cusp in enumerate(cusps):
            house_number = i + 1
            size = swe.difdeg2n(cusps[i+1 if i < 11 else 0], cusp)
            houses[house_number] = House(house_number, cusp, size, cuspsspeed[i])

        return houses

    def _angles(self) -> SerializableDict:
        """ Get the main axis angles from _swe_houses_angles. """
        angles = SerializableDict()
        ascmc, ascmcspeed = itemgetter('ascmc', 'ascmcspeed')(self._swe_houses_angles)

        for name, swe_index in self._requested(const.ANGLES).items():
            lon = ascmc[swe_index]
            speed = ascmcspeed[swe_index]

            if name in [const.DESC, const.IC]:
                lon = swe.degnorm(Decimal(str(lon)) - 180)

            angles[name] = AxisAngle(name, lon, speed)

        return angles

    def _planets(self) -> SerializableDict:
        """ Get the ten main planets. """
        planets = SerializableDict()

        for name, planet in self._requested(const.PLANETS).items():
            ec_res, _ = swe.calc_ut(self._jd, planet)
            eq_res, _ = swe.calc_ut(self._jd, planet, swe.FLG_EQUATORIAL)
            lon, lat, dist, speed = ec_res[:4]
            dec = eq_res[1]
            out_of_bounds = abs(dec) > self.obliquity
            house = self._get_house(lon)
            planets[name] = Planet(name, house, lon, lat, dist, speed, dec, out_of_bounds)

        return planets

    def _points(self) -> SerializableDict:
        """ Get the main calculated points. """
        points = SerializableDict()
        requested_points = self._requested(const.POINTS)

        """ Get the mean nodes. """
        if const.NORTH_NODE in requested_points:
            res, _ = swe.calc_ut(self._jd, const.POINTS[const.NORTH_NODE])
            lon, _, _, speed = res[:4]
            house = self._get_house(lon)
            points[const.NORTH_NODE] = Point(const.NORTH_NODE, house, lon, speed)

        if const.SOUTH_NODE in requested_points:
            lon = swe.degnorm(Decimal(str(lon)) - 180)
            house = self._get_house(lon)
            points[const.SOUTH_NODE] = Point(const.SOUTH_NODE, house, lon, speed)

        """ Get the true nodes. """
        if const.TRUE_NORTH_NODE in requested_points:
            res, _ = swe.calc_ut(self._jd, const.POINTS[const.TRUE_NORTH_NODE])
            lon, _, _, speed = res[:4]
            house = self._get_house(lon)
            points[const.TRUE_NORTH_NODE] = Point(const.TRUE_NORTH_NODE, house, lon, speed)

        if const.TRUE_SOUTH_NODE in requested_points:
            lon = swe.degnorm(Decimal(str(lon)) - 180)
            house = self._get_house(lon)
            points[const.TRUE_SOUTH_NODE] = Point(const.TRUE_SOUTH_NODE, house, lon, speed)

        """ Get the vertex. """
        if const.VERTEX in requested_points:
            ascmc, ascmcspeed = itemgetter('ascmc', 'ascmcspeed')(self._swe_houses_angles)
            lon = ascmc[const.POINTS[const.VERTEX]]
            speed = ascmcspeed[const.POINTS[const.VERTEX]]
            house = self._get_house(lon)
            points[const.VERTEX] = Point(const.VERTEX, house, lon, speed)

        """ Get the part of fortune. """
        if const.PARS_FORTUNA in requested_points:
            if self.type[const.DIURNAL]:
                formula = self.angles[const.ASC].longitude + self.planets[const.MOON].longitude - self.planets[const.SUN].longitude
            elif self.type[const.NOCTURNAL]:
                formula = self.angles[const.ASC].longitude + self.planets[const.SUN].longitude - self.planets[const.MOON].longitude

            lon = swe.degnorm(formula)
            house = self._get_house(lon)
            points[const.PARS_FORTUNA] = Point(const.PARS_FORTUNA, house, lon, 0)

        """ Get the latest pre-natal full/new moon. """
        if const.SYZYGY in requested_points:
            distance = self.planets[const.SUN].distance_to(self.planets[const.MOON])
            jd = transits.previous_new_moon(self._jd) if distance > 0 else transits.previous_full_moon(self._jd)
            res, _ = swe.calc_ut(jd, const.PLANETS[const.MOON])
            lon, _, _, speed = res[:4]
            house = self._get_house(lon)
            points[const.SYZYGY] = Point(const.SYZYGY, house, lon, speed)

        """ Get the Liliths. """
        if const.LILITH in requested_points:
            res, _ = swe.calc_ut(self._jd, const.POINTS[const.LILITH])
            lon, _, _, speed = res[:4]
            house = self._get_house(lon)
            points[const.LILITH] = Point(const.LILITH, house, lon, speed)

        if const.TRUE_LILITH in requested_points:
            res, _ = swe.calc_ut(self._jd, const.POINTS[const.TRUE_LILITH])
            lon, _, _, speed = res[:4]
            house = self._get_house(lon)
            points[const.TRUE_LILITH] = Point(const.TRUE_LILITH, house, lon, speed)

        return points

    def _asteroids(self) -> SerializableDict:
        """ Get supported asteroids requested in _show_items as well as
        any extra ones passed by number. """
        asteroids = SerializableDict()
        asteroid_list = self._requested(const.ASTEROIDS)

        for name, asteroid in asteroid_list.items():
            res, _ = swe.calc_ut(self._jd, asteroid)
            lon, _, dist, speed = res[:4]
            house = self._get_house(lon)
            asteroids[name] = Asteroid(name, house, lon, dist, speed)

        for extra_asteroid in self._extra_asteroids:
            pl = extra_asteroid + swe.AST_OFFSET
            name = swe.get_planet_name(pl)
            asteroid_list[name] = pl
            self._show_items.append(name)

        return asteroids

    def _fixed_stars(self) -> SerializableDict:
        """ Get any requested fixed stars by name. """
        fixed_stars = SerializableDict()

        for name in self._stars:
            res, stnam, _ = swe.fixstar2_ut(name, self._jd)
            name = stnam.partition(',')[0]
            lon, _, dist, speed = res[:4]
            house = self._get_house(lon)
            fixed_stars[name] = FixedStar(name, house, lon, dist, speed)
            self._show_items.append(name)

        return fixed_stars

    def _aspects(self) -> SerializableDict:
        """ Calculate all requested aspects between chart items. """
        item_aspects = SerializableDict({v: SerializableDict({}) for v in self._show_items})
        aspect_items = {**self.angles, **self.planets, **self.points, **self.asteroids, **self.fixed_stars}

        for item1_name, item1 in aspect_items.items():
            for item2_name, item2 in aspect_items.items():
                # Avoid conjuncting the same item
                if item1_name == item2_name:
                    continue

                active, passive = aspects.active_passive(item1, item2)

                # Avoid duplicates
                if passive.name in item_aspects[active.name]:
                    continue

                for aspect_type in self._show_aspects:
                    aspect_angle = const.ASPECTS[aspect_type]
                    active_orb = self._show_orbs[active.name][aspect_type] if active.name in self._show_orbs else const.DEFAULT_ORB
                    passive_orb = self._show_orbs[passive.name][aspect_type] if passive.name in self._show_orbs else const.DEFAULT_ORB
                    orb = (active_orb + passive_orb) / 2 if self._orb_calc == self.ORB_CALC_MEAN else max(active_orb, passive_orb)
                    distance = active.distance_to(passive)

                    if aspect_angle-orb <= abs(distance) <= aspect_angle+orb:
                        # Check the aspect rules & add if this aspect is allowed
                        active_aspect_rule = self._aspect_rules[active.name] if active.name in self._aspect_rules else const.DEFAULT_ASPECT_RULE
                        passive_aspect_rule = self._aspect_rules[passive.name] if passive.name in self._aspect_rules else const.DEFAULT_ASPECT_RULE

                        if aspect_type in active_aspect_rule[const.INITIATE] and aspect_type in passive_aspect_rule[const.RECEIVE]:
                            aspect = Aspect(active, passive, aspect_type, distance)
                            item_aspects[active.name][passive.name] = aspect
                            item_aspects[passive.name][active.name] = aspect

        return item_aspects

    def _moon_phase(self) -> SerializableBoolean:
        """ Calculate moon phase. """
        sun = swe.calc_ut(self._jd, const.PLANETS[const.SUN])[0][0]
        moon = swe.calc_ut(self._jd, const.PLANETS[const.MOON])[0][0]
        distance = swe.difdegn(moon, sun)

        for phase, end in const.MOON_PHASES.items():
            if distance < end:
                break

        return SerializableBoolean({k: k == phase for k, v in const.MOON_PHASES.items()})

    def _obliquity(self) -> bool:
        """ Get Earth's equatorial obliquity. """
        return swe.calc_ut(self._jd, swe.ECL_NUT)[0][0]

    def _get_house(self, lon: float) -> int:
        """ Returns which house a given longitude appears in. """
        for house_number, house in self.houses.items():
            lon_diff = swe.difdeg2n(lon, house.longitude)
            next_cusp_diff = swe.difdeg2n(house.longitude + house.size, house.longitude)

            if 0 < lon_diff < next_cusp_diff:
                return house_number

    def _requested(self, items: dict) -> dict:
        """ Returns which of the passed available items have been
        requested for display in this chart. """
        return {k: v for k, v in items.items() if k in self._show_items}

    def _mutual_receptions(self) -> None:
        """ TODO: Massively tidy this shit up. """
        for name, planet in self.planets.items():
            planet_sign_rulers = const.ESSENTIAL_DIGNITIES[planet.sign][const.DOMICILE]
            sign_exaltations = const.ESSENTIAL_DIGNITIES[planet.sign][const.EXALTED]
            # By sign ruler
            for planet_sign_ruler_name in planet_sign_rulers:
                if planet_sign_ruler_name == name:
                    continue
                planet_sign_ruler = self.planets[planet_sign_ruler_name]
                if name in const.ESSENTIAL_DIGNITIES[planet_sign_ruler.sign][const.DOMICILE]:
                    planet.mutual_reception = planet_sign_ruler_name
                    planet_sign_ruler.mutual_reception = name
            # By sign exaltation
            for sign_exaltation_name in sign_exaltations:
                if sign_exaltation_name == name:
                    continue
                sign_exaltation = self.planets[sign_exaltation_name]
                if name in const.ESSENTIAL_DIGNITIES[sign_exaltation.sign][const.EXALTED]:
                    planet.mutual_reception_exaltion = sign_exaltation_name
                    sign_exaltation.mutual_reception_exaltion = name

        # By house ruler
        for house_number, house in self.houses.items():
            house_rulers = const.ESSENTIAL_DIGNITIES[house.sign][const.DOMICILE]

            for house_ruler_name in house_rulers:
                planet = self.planets[house_ruler_name]
                if planet.house == house_number:
                    continue

                planet_house_rulers = const.ESSENTIAL_DIGNITIES[self.houses[planet.house].sign][const.DOMICILE]

                for planet_house_ruler_name in planet_house_rulers:
                    planet2 = self.planets[planet_house_ruler_name]
                    if planet2.house == house_number:
                        planet.mutual_reception_house = planet2.house
                        planet2.mutual_reception_house = planet.house

    def _dignities(self) -> None:
        """ Adds essential dignities, debilities and scores to the planets
        once their positions have been calculated.
        TODO: Also tidy up this absolute mess. """
        for planet_name, planet in self.planets.items():
            dignities_data = {
                const.DOMICILE: dignities.is_domicile(planet_name, planet.longitude),
                const.MUTUAL_RECEPTION_HOUSE: False,
                const.EXALTED: dignities.is_exalted(planet_name, planet.longitude),
                const.MUTUAL_RECEPTION_EXALTATION: False,
                const.TRIPLICITY_RULER: dignities.is_triplicity_ruler(planet_name, planet.longitude),
                const.TERM_RULER: dignities.is_term_ruler(planet_name, planet.longitude),
                const.FACE_RULER: dignities.is_face_ruler(planet_name, planet.longitude),
                const.DETRIMENT: False,
                const.FALL: False,
                const.PEREGRINE: False,
            }

            dignities_data[const.PEREGRINE] = not any(dignities_data.values())
            dignities_data[const.DETRIMENT] = dignities.is_in_detriment(planet_name, planet.longitude)
            dignities_data[const.FALL] = dignities.is_in_fall(planet_name, planet.longitude)
            # Currently peregrine does not take mutual receptions into account
            dignities_data[const.MUTUAL_RECEPTION_HOUSE] = planet.mutual_reception_house is not None
            dignities_data[const.MUTUAL_RECEPTION_EXALTATION] = planet.mutual_reception_exaltion is not None

            planet.dignities = SerializableBoolean(dignities_data)
            planet.score = sum([v for k, v in const.DIGNITY_SCORES.items() if dignities_data[k]])

def sign(lon: float) -> str:
    """ Returns the zodiac sign the passed longitude belongs to. """
    return const.SIGNS[int(lon / 30)]