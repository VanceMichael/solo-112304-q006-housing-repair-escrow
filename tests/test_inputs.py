import unittest

from source_fixture import load


class ExchangeInputs(unittest.TestCase):
    def test_related_source_records(self):
        exchange = load()
        initial = exchange["initial"]
        changes = exchange["changes"]
        self.assertGreater(initial["/repairs/applications"]["body"]["records"][0]["funds"][0][1], 0)
        changed = changes[1]["routes"]["/registry/units"]["body"]["records"]
        self.assertEqual(changed[1]["fund"], changed[2]["fund"])
        self.assertLess(changed[1]["effective"], initial["/repairs/applications"]["body"]["records"][0]["signed"])
        self.assertEqual({x["state"] for x in changes[0]["routes"]["/escrow/effective"]["body"]["reservations"]}, {"frozen","paid"})
