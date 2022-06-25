"""
wifi channels
"""

channels_2ghz = list(range(0, 14))
channels_5ghz = (
    list(range(36, 68, 4)) + list(range(100, 148, 4)) + list(range(149, 181, 4))
)
channels_2and5 = list(channels_2ghz + channels_5ghz)
channels_5ghz.insert(0, 0)
