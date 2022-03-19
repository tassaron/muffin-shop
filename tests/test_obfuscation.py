from muffin_shop.helpers.shop.util import obfuscate_number, deobfuscate_number


def test_obfuscation():
    for i in range(1, 4500):
        assert deobfuscate_number(obfuscate_number(i)) == i
