"""
test_clock.py - tests for the clock module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""
import re
import datetime
import unittest
from mock import MagicMock, patch
from modules.clock import f_time, beats, yi, tock, npl
from nose.tools import nottest
from tools import is_up


@patch('time.time')
class TestClock(unittest.TestCase):
    def setUp(self):
        self.phenny = MagicMock()
        self.input = MagicMock()

    @nottest
    def test_time(self, mock_time):
        mock_time.return_value = 1338674651
        self.input.group.return_value = 'EDT'
        f_time(self.phenny, self.input)
        self.phenny.msg.called_once_with('#phenny',
                "Sat, 02 Jun 2012 18:04:11 EDT")

    def test_beats_zero(self, mock_time):
        mock_time.return_value = 0
        beats(self.phenny, None)
        self.phenny.say.assert_called_with('@041')

    def test_beats_normal(self, mock_time):
        mock_time.return_value = 369182
        beats(self.phenny, None)
        self.phenny.say.assert_called_with('@314')

    def test_yi_normal(self, mock_time):
        mock_time.return_value = 369182
        yi(self.phenny, None)
        self.phenny.say.assert_called_with('Not yet...')

    def test_yi_soon(self, mock_time):
        mock_time.return_value = 1339419000
        yi(self.phenny, None)
        self.phenny.say.assert_called_with('Soon...')

    def test_yi_now(self, mock_time):
        mock_time.return_value = 1339419650
        yi(self.phenny, None)
        self.phenny.say.assert_called_with('Yes! PARTAI!')

    def test_tock(self, mock_time):
        if not is_up('http://tycho.usno.navy.mil'):
            self.skipTest('US Military atomic clock server is down, skipping test.')
        tock(self.phenny, None)
        out = self.phenny.say.call_args[0][0]
        m = re.match('^.* - tycho.usno.navy.mil$',
                out, flags=re.UNICODE)
        self.assertTrue(m)

    def test_npl(self, mock_time):
        if not is_up('http://npl.co.uk'):
            self.skipTest('NPL NTP server is down, skipping test.')
        npl(self.phenny, None)
        out = self.phenny.say.call_args[0][0]
        m = re.match('^.* - ntp1.npl.co.uk$',
                out, flags=re.UNICODE)
        self.assertTrue(m)
