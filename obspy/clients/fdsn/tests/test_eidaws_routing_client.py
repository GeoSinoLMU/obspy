#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:copyright:
    The ObsPy Development Team (devs@obspy.org)
:license:
    GNU Lesser General Public License, Version 3
    (https://www.gnu.org/copyleft/lesser.html)
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from future.builtins import *  # NOQA

import unittest

import obspy
from obspy.core.compatibility import mock
from obspy.clients.fdsn.routing.eidaws_routing_client import \
    EIDAWSRoutingClient



class EIDAWSRoutingClientTestCase(unittest.TestCase):
    def test_get_waveforms_mocked(self):
        """
        Mock test to be less dependent on changes at the services.
        """
        c = EIDAWSRoutingClient()
        with mock.patch():
            c.get_waveforms("B*", "", "", "LHZ",
                            obspy.UTCDateTime(2016, 1, 1),
                            obspy.UTCDateTime(2016, 1, 1, 0, 1))


    def test_response_splitting(self):
        data = """
http://geofon.gfz-potsdam.de/fdsnws/station/1/query
NU * * * 2017-01-01T00:00:00 2017-01-01T00:10:00

http://www.orfeus-eu.org/fdsnws/station/1/query
NS * * * 2017-01-01T00:00:00 2017-01-01T00:10:00
NR * * * 2017-01-01T00:00:00 2017-01-01T00:10:00
NO * * * 2017-01-01T00:00:00 2017-01-01T00:10:00
NL * * * 2017-01-01T00:00:00 2017-01-01T00:10:00
NA * * * 2017-01-01T00:00:00 2017-01-01T00:10:00

http://webservices.ingv.it/fdsnws/station/1/query
NI * * * 2017-01-01T00:00:00 2017-01-01T00:10:00

http://ws.resif.fr/fdsnws/station/1/query
ND * * * 2017-01-01T00:00:00 2017-01-01T00:10:00
        """.strip()
        # This should return a dictionary that contains the root URL of each
        # fdsn implementation and the POST payload ready to be submitted.
        self.assertEqual(
            EIDAWSRoutingClient.split_routing_response(data),
            {
                "http://geofon.gfz-potsdam.de": (
                    "NU * * * 2017-01-01T00:00:00 2017-01-01T00:10:00"),
                "http://www.orfeus-eu.org": (
                    "NS * * * 2017-01-01T00:00:00 2017-01-01T00:10:00\n"
                    "NR * * * 2017-01-01T00:00:00 2017-01-01T00:10:00\n"
                    "NO * * * 2017-01-01T00:00:00 2017-01-01T00:10:00\n"
                    "NL * * * 2017-01-01T00:00:00 2017-01-01T00:10:00\n"
                    "NA * * * 2017-01-01T00:00:00 2017-01-01T00:10:00"),
                "http://webservices.ingv.it": (
                    "NI * * * 2017-01-01T00:00:00 2017-01-01T00:10:00"),
                "http://ws.resif.fr": (
                    "ND * * * 2017-01-01T00:00:00 2017-01-01T00:10:00")})

        data = """
http://geofon.gfz-potsdam.de/fdsnws/station/1/query
NU * * * 2017-01-01T00:00:00 2017-01-01T00:10:00
        """.strip()
        # This should return a dictionary that contains the root URL of each
        # fdsn implementation and the POST payload ready to be submitted.
        self.assertEqual(
            EIDAWSRoutingClient.split_routing_response(data),
            {
                "http://geofon.gfz-potsdam.de": (
                    "NU * * * 2017-01-01T00:00:00 2017-01-01T00:10:00")})


def suite():
    return unittest.makeSuite(EIDAWSRoutingClientTestCase, 'test')


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
