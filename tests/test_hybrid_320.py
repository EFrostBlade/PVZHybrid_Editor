import unittest
from unittest.mock import patch
import PVZ_data as data
import PVZ_Hybrid as pvz
import editor_runtime as runtime
from test_hybrid_319 import Memory

class Hybrid320Tests(unittest.TestCase):
    def setUp(self):
        previous = data.PVZ_version
        self.addCleanup(data.update_PVZ_version, previous if isinstance(previous, float) else 3.19)
        data.update_PVZ_version(3.920)

    def test_version_and_catalog(self):
        self.assertEqual(runtime.detect_game_version("v3.20"), 3.920)
        self.assertEqual(runtime.detect_game_version("v3.2"), 3.2)
        self.assertIn("3.20", runtime.main_window_title("0.76", 3.920))
        self.assertEqual(data.plantsType[371:379], list(data.HYBRID_320_PLANTS))
        self.assertEqual(data.bulletType[135:], list(data.HYBRID_320_BULLETS))
        self.assertEqual(len(data.plantsType), 654)
        self.assertEqual(pvz.get_zombie_num(), 142)
        with patch.object(pvz.random, "randint", side_effect=lambda low, high: high):
            self.assertEqual(pvz.getRandomPlant(), 378)
        data.update_PVZ_version(3.19)
        with self.assertRaises(ValueError):
            data.require_supported_entity("plant", 371)
        with self.assertRaises(ValueError):
            pvz.setAllBullet(True, 135)
        data.require_supported_entity("plant", 370)

    def test_attribute_table_and_card_images(self):
        from PIL import Image
        from pathlib import Path
        root = Path(__file__).resolve().parents[1]
        with patch.object(data, "PVZ_memory", Memory()):
            for identifier in range(371, 379):
                self.assertEqual(data.plantCharacteristic(identifier).addr, 0xEF4010 + identifier * 0x24)
                with Image.open(root / f"res/cards/pvzhe_plants/{identifier}.png") as image:
                    self.assertEqual(image.size, (50, 70))
                    image.verify()
