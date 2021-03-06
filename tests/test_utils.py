import os
import subprocess
from utils import (
    get_avail_netdevs, get_avail_wlans, get_current_wlan,
    NetworkManager)


def test_get_avail_netdevs():
    # yes, we can get any network device name
    devs = get_avail_netdevs()
    assert "lo" in devs
    assert type(devs) == list


def test_get_avail_netdevs_can_extract_names(fake_ifconfig):
    # we can get an expected set of device names
    devs = get_avail_netdevs()
    assert "foobar0" in devs
    assert "lo" in devs
    assert "wlp1s0" in devs


def test_fake_ifconfig(fake_ifconfig):
    # ensure, the `fake_ifconfig` fixture works.
    lines = subprocess.check_output("ifconfig").decode("utf-8")
    assert os.path.exists(str(fake_ifconfig))
    assert "foobar0:" in lines


def test_get_avail_wlans():
    # we can get a list of wlans
    # FIXME: the list contents is not tested
    nets = get_avail_wlans()
    assert type(nets) is list


def test_get_current_wlan(fake_iwgetid):
    # we can determine the current wlan
    assert get_current_wlan() is None
    fake_iwgetid("MY NETWORK")
    assert get_current_wlan() == "MY NETWORK"


class TestNetworkManager(object):
    # tests for utils.NetworkManager instances

    def test_get_avail_wlans(self):
        # we can get a list of available wifi networks
        nets = NetworkManager().get_avail_wlans()
        assert type(nets) is list

    def test_get_current_wlan(self, fake_iwgetid):
        # we can determine the current wlan
        assert NetworkManager.get_current_wlan() is None
        fake_iwgetid("SOME NETWORK")
        assert NetworkManager.get_current_wlan() == "SOME NETWORK"

    def test_get_connections(self):
        # we can get a list of all wifi connections
        # FIXME: the list contents are not tested
        uuids = NetworkManager.get_connections()
        assert type(uuids) is list
        assert not uuids[-1].endswith("\n")

    def test_get_conn_by_ssid(self):
        # we can get a connection by SSID
        # FIXME: takes load of time
        # FIXME: the outcome is unreliable
        uuids = NetworkManager.get_conn_by_ssid("notanexisingssid")
        assert uuids == []
        assert type(uuids) is list
