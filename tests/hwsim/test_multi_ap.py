# Test cases for Multi-AP
# Copyright (c) 2018, The Linux Foundation
#
# This software may be distributed under the terms of the BSD license.
# See README for more details.

import hostapd

def test_multi_ap_association(dev, apdev):
    """Multi-AP association in backhaul BSS"""
    run_multi_ap_association(dev, apdev, 1)
    dev[1].connect("multi-ap", psk="12345678", scan_freq="2412",
                   wait_connect=False)
    ev = dev[1].wait_event([ "CTRL-EVENT-DISCONNECTED",
                             "CTRL-EVENT-CONNECTED",
                             "CTRL-EVENT-ASSOC-REJECT" ],
                           timeout=5)
    dev[1].request("DISCONNECT")
    if ev is None:
        raise Exception("Connection result not reported")
    if "CTRL-EVENT-ASSOC-REJECT" not in ev:
        raise Exception("Association rejection not reported")
    if "status_code=12" not in ev:
        raise Exception("Unexpected association status code: " + ev)

def test_multi_ap_association_shared_bss(dev, apdev):
    """Multi-AP association in backhaul BSS (with fronthaul BSS enabled)"""
    run_multi_ap_association(dev, apdev, 3)
    dev[1].connect("multi-ap", psk="12345678", scan_freq="2412")

def run_multi_ap_association(dev, apdev, multi_ap):
    params = hostapd.wpa2_params(ssid="multi-ap", passphrase="12345678")
    params["multi_ap"] = str(multi_ap)
    hapd = hostapd.add_ap(apdev[0], params)

    dev[0].connect("multi-ap", psk="12345678", multi_ap_backhaul_sta="1",
                   scan_freq="2412")

def test_multi_ap_disabled_on_ap(dev, apdev):
    """Multi-AP association attempt when disabled on AP"""
    params = hostapd.wpa2_params(ssid="multi-ap", passphrase="12345678")
    hapd = hostapd.add_ap(apdev[0], params)

    dev[0].connect("multi-ap", psk="12345678", multi_ap_backhaul_sta="1",
                   scan_freq="2412", wait_connect=False)
    ev = dev[0].wait_event([ "CTRL-EVENT-DISCONNECTED",
                             "CTRL-EVENT-CONNECTED" ],
                           timeout=5)
    dev[0].request("DISCONNECT")
    if ev is None:
        raise Exception("Connection result not reported")
    if "CTRL-EVENT-DISCONNECTED" not in ev:
        raise Exception("Unexpected connection result")

def test_multi_ap_fronthaul_on_ap(dev, apdev):
    """Multi-AP association attempt when only fronthaul BSS on AP"""
    params = hostapd.wpa2_params(ssid="multi-ap", passphrase="12345678")
    params["multi_ap"] = "2"
    hapd = hostapd.add_ap(apdev[0], params)

    dev[0].connect("multi-ap", psk="12345678", multi_ap_backhaul_sta="1",
                   scan_freq="2412", wait_connect=False)
    ev = dev[0].wait_event([ "CTRL-EVENT-DISCONNECTED",
                             "CTRL-EVENT-CONNECTED",
                             "CTRL-EVENT-ASSOC-REJECT" ],
                           timeout=5)
    dev[0].request("DISCONNECT")
    if ev is None:
        raise Exception("Connection result not reported")
    if "CTRL-EVENT-ASSOC-REJECT" not in ev:
        raise Exception("Association rejection not reported")
    if "status_code=12" not in ev:
        raise Exception("Unexpected association status code: " + ev)
