"""3.19 regressions without writing to a running game."""
import ast
import os
from pathlib import Path
import unittest
from unittest.mock import Mock, patch

import PVZ_data as data
import PVZ_Hybrid as pvz
import editor_runtime

ROOT = Path(__file__).resolve().parents[1]


class Memory:
    process_handle = 1

    def __init__(self):
        self.bytes = {}
        self.writes = []

    def read_bytes(self, address, size):
        return bytes(self.bytes.get(address + i, 0) for i in range(size))

    def write_bytes(self, address, value, size):
        assert len(value) == size
        self.bytes.update({address + i: b for i, b in enumerate(value)})
        self.writes.append((address, value))

    def read_uint(self, address):
        return int.from_bytes(self.read_bytes(address, 4), "little")

    def read_uchar(self, address):
        return self.read_bytes(address, 1)[0]

    def read_bool(self, address):
        return bool(self.read_uchar(address))

    def write_int(self, address, value):
        self.write_bytes(address, value.to_bytes(4, "little"), 4)

    def write_uchar(self, address, value):
        self.write_bytes(address, bytes([value]), 1)


def ui_function(name, **scope):
    tree = ast.parse((ROOT / "editor.py").read_text(encoding="utf-8-sig"))
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
    namespace = {"PVZ_data": data, "os": os, **scope}
    exec(compile(ast.Module(body=[node], type_ignores=[]), "editor-function", "exec"), namespace)
    return namespace[name]


class Hybrid319Tests(unittest.TestCase):
    def setUp(self):
        previous = data.PVZ_version
        previous_hp = data.zombies_HP_addresses
        self.addCleanup(setattr, data, "PVZ_version", previous)
        self.addCleanup(setattr, data, "zombies_HP_addresses", previous_hp)
        self.addCleanup(data.update_PVZ_version, previous if isinstance(previous, (int, float)) else 3.18)
        data.update_PVZ_version(3.19)

    def test_titles_and_card_offsets(self):
        for text, version, offset in [("v3.19", 3.19, 512), ("v3.18", 3.18, 512),
                                     ("v3.1", 3.1, 256), ("v3.1.5", 3.15, 256)]:
            self.assertEqual(editor_runtime.detect_game_version("植物大战僵尸杂交版" + text), version)
            data.update_PVZ_version(version)
            self.assertEqual(data.zombie_card_offset(), offset)

    def test_entities_and_reconnect(self):
        plants = data.plantsType
        self.assertEqual(plants[368:371], list(data.HYBRID_319_PLANTS))
        self.assertEqual(plants[651:], list(data.HYBRID_319_ZOMBIES))
        self.assertEqual(data.zombiesType[139:], list(data.HYBRID_319_ZOMBIES))
        self.assertEqual(len(data.bulletType), 135)
        self.assertEqual(len(data.zombieSpaw), 146)
        data.update_PVZ_version(3.18)
        self.assertEqual(plants[368:371], ["占位"] * 3)
        self.assertEqual(len(data.zombiesType), 139)
        self.assertEqual(len(data.bulletType), 134)
        data.update_PVZ_version(3.19)
        self.assertIs(plants, data.plantsType)
        self.assertEqual(len(plants), 654)

    def test_random_endpoints(self):
        self.assertEqual(pvz.get_zombie_num(), 142)
        with patch.object(pvz.random, "randint", side_effect=lambda low, high: high):
            self.assertEqual(pvz.getRandomZombie(), 141)
            self.assertEqual(pvz.getRandomPlant(), 370)

    def test_characteristic_and_spawn_tables(self):
        memory = Memory()
        with patch.object(data, "PVZ_memory", memory):
            self.assertEqual(data.plantCharacteristic(370).addr, 0xEF4010 + 370 * 0x24)
            self.assertEqual(data.plantCharacteristic(653).addr, 0x88B1A9 + 141 * 4)
            zombie = data.zombieType(141)
            zombie.setWeight(23)
            self.assertEqual(memory.read_uint(0x7A8000 + 141 * 0x1C + 0x14), 23)
            zombie.setLevel(7)
            self.assertEqual(memory.read_uint(zombie.addr + 8), 7)
            for i, address in enumerate(data.SPAWN_PROBABILITY_ADDRESSES_319):
                data.zombieType(142 + i).setWeight(30 + i)
                self.assertEqual(memory.read_uchar(address), 30 + i)

    def test_old_version_rejects_new_placements_before_writes(self):
        data.update_PVZ_version(3.18)
        with patch.object(data, "PVZ_memory", Mock()) as memory, patch.object(pvz.asm, "runThread") as run:
            for name, args in [("putPlant", (0, 1, 370)), ("putZombie", (0, 8, 141)),
                               ("putcard", (0, 0, 653)), ("changeSlot", (1, 653)), ("selectCard", (370,))]:
                with self.assertRaises(ValueError):
                    getattr(pvz, name)(*args)
            self.assertEqual(memory.mock_calls, [])
            run.assert_not_called()

    def test_spawn_argument_is_not_sign_extended(self):
        with patch.object(pvz.asm, "runThread") as run:
            pvz.putZombie(0, 8, 141)
        code = run.call_args.args[0].creat_asm(0x100000)
        self.assertEqual(bytes(code.code[:7]), bytes.fromhex("6a 08 68 8d 00 00 00"))

    def test_new_bullet_creation_argument(self):
        with patch.object(pvz.asm, "runThread") as run:
            pvz.creatBullet([(134, 300, 200, 1.0, 0.0)])
        code = run.call_args.args[0].creat_asm(0x100000)
        self.assertEqual(bytes(code.code[:6]), bytes.fromhex("60 68 86 00 00 00"))

    def test_random_zombie_slots_use_modern_offset(self):
        memory = Mock()
        memory.read_uint.return_value = 0x100000
        with patch.object(data, "PVZ_memory", memory), patch.object(pvz, "getRandomZombie", return_value=139):
            event = Mock()
            event.is_set.side_effect = [False, True]
            pvz.randomZombieSlots_operstion(event, 1, 1)
            memory.write_int.assert_called_once_with(0x10005C, 651)
            memory.write_int.reset_mock()
            event.is_set.side_effect = [False, True]
            pvz.randomSlots_operstion(event, True)
            self.assertEqual(memory.write_int.call_count, 16)
            self.assertTrue(all(call.args[1] == 651 for call in memory.write_int.call_args_list))

    def test_bullet_hooks_restore_modern_address(self):
        memory = Memory()
        with patch.object(data, "PVZ_memory", memory), \
             patch.object(pvz.pymem.memory, "allocate_memory", return_value=0x10000000), \
             patch.object(pvz.pymem.memory, "free_memory"):
            for function, args in [(pvz.setAllBullet, (134,)), (pvz.randomBullet, (False, False, False))]:
                function(True, *args)
                self.assertEqual(memory.read_bytes(0x9815F6, 5), b"\x90" * 5)
                function(False, *args)
                self.assertEqual(memory.read_bytes(0x9815F6, 5), bytes.fromhex("e8 b5 d6 ae ff"))
            self.assertNotIn(0x88CE91, [a for a, _ in memory.writes])

    def test_large_plant_comparison(self):
        memory = Memory()
        with patch.object(data, "PVZ_memory", memory), \
             patch.object(pvz.pymem.memory, "allocate_memory", return_value=0x10000000):
            pvz.setPlantBullet(True, 370, 134, 0)
        code = memory.writes[0][1]
        self.assertEqual(code[:7], bytes.fromhex("81 7d 24 72 01 00 00"))
        target = 9 + code[8]
        self.assertEqual(code[target:target + 4], bytes.fromhex("8b 54 24 3c"))

    def test_spawn_hook_roundtrip_and_reapply(self):
        memory = Memory()
        originals = {0x425855: b"\x7f", 0x42584E: bytes.fromhex("e9 ad f7 60 00"),
                     0x8230C1: bytes.fromhex("0f 85 0c 00 00 00"),
                     0x5A9A47: bytes.fromhex("f7 74 24 04 8b c2"),
                     0x41C078: b"\x74", 0x40D91F: b"\x74"}
        for address, code in originals.items():
            memory.write_bytes(address, code, len(code))
        with patch.object(data, "PVZ_memory", memory), patch.object(pvz, "_spawn_patch_319", None), \
             patch.object(pvz.pymem.memory, "allocate_memory", return_value=0x10000000), \
             patch.object(pvz.pymem.memory, "free_memory") as free:
            pvz.globalSpawModify(True, ["141"])
            code = memory.read_bytes(0x10000000, 142 * 7)
            self.assertEqual(code[-7:], bytes.fromhex("c6 82 61 58 00 00 01"))
            reconnected = Memory()
            reconnected.bytes = memory.bytes
            data.PVZ_memory = reconnected
            pvz.globalSpawModify(True, ["140"])
            pvz.globalSpawModify(True, [])
            self.assertEqual(memory.read_bytes(0x5A9A47, 1), b"\xe9")
            pvz.globalSpawModify(False, [])
            self.assertEqual(free.call_count, 3)
        for address, code in originals.items():
            self.assertEqual(memory.read_bytes(address, len(code)), code)
        self.assertNotIn(0x8240BB, [a for a, _ in memory.writes])

    def test_hero_patch_roundtrip(self):
        memory = Memory()
        original = bytes.fromhex("56 50 51 52 6a 00")
        memory.write_bytes(0x9F10A4, original, 6)
        with patch.object(data, "PVZ_memory", memory), patch.object(pvz, "_more_hero_319_process", None), \
             patch.object(pvz, "newmem_more_hero", None), \
             patch.object(pvz.pymem.memory, "allocate_memory", return_value=0x10000000) as allocate, \
             patch.object(pvz.pymem.memory, "free_memory") as free:
            pvz.more_hero(True)
            pvz.more_hero(True)
            reconnected = Memory()
            reconnected.bytes = memory.bytes
            data.PVZ_memory = reconnected
            pvz.more_hero(False)
            pvz.more_hero(False)
            allocate.assert_called_once()
            free.assert_called_once()
        self.assertEqual(memory.read_bytes(0x9F10A4, 6), original)

    def test_spawn_signature_failure_leaves_memory_untouched(self):
        memory = Memory()
        with patch.object(data, "PVZ_memory", memory), patch.object(pvz, "_spawn_patch_319", None), \
             patch.object(pvz.pymem.memory, "allocate_memory") as allocate:
            with self.assertRaises(ValueError):
                pvz.globalSpawModify(True, ["141"])
            allocate.assert_not_called()
        self.assertEqual(memory.writes, [])

    def test_spawn_restore_does_not_overwrite_another_patch(self):
        memory = Memory()
        memory.write_bytes(0x425855, b"\xcc", 1)
        memory.writes.clear()
        state = ((0, None), 0x10000000, {0x425855: b"\xeb"})
        with patch.object(data, "PVZ_memory", memory), patch.object(pvz, "_spawn_patch_319", state), \
             patch.object(pvz.pymem.memory, "free_memory") as free:
            with self.assertRaises(ValueError):
                pvz.globalSpawModify(False, [])
            free.assert_not_called()
        self.assertEqual(memory.writes, [])

    def test_card_images_filter_and_decode(self):
        from PIL import Image
        images = ui_function("available_card_images", resource_path=lambda p: str(ROOT / p))
        self.assertIn("370.png", images("plants"))
        self.assertIn("141.png", images("zombies"))
        for kind, ids in [("plants", range(368, 371)), ("zombies", range(139, 142))]:
            for entity_id in ids:
                with Image.open(ROOT / f"res/cards/pvzhe_{kind}/{entity_id}.png") as card:
                    self.assertEqual(card.size, (50, 70))
                    card.verify()
        data.update_PVZ_version(3.18)
        self.assertNotIn("370.png", images("plants"))
        self.assertNotIn("141.png", images("zombies"))

    def test_tk_reconnect_keeps_translations_and_selection(self):
        import tkinter as tk
        import ttkbootstrap as ttk
        import i18n
        i18n.install_tk_i18n(ttk, tk)
        root = ttk.Window()
        root.withdraw()
        self.addCleanup(root.destroy)
        data.update_PVZ_version(3.18)
        combo = ttk.Combobox(root, values=data.zombiesType)
        combo.current(138)
        update = ui_function("set_game_version", main_window=root, i18n=i18n)
        update(3.19)
        self.assertEqual(combo.current(), 138)
        self.assertEqual(len(combo["values"]), 142)
        combo.current(141)
        self.assertEqual(combo.get(), "读报伽刚特尔")
        update(3.18)
        self.assertEqual(len(combo["values"]), 139)
        self.assertEqual(combo.get(), "")


if __name__ == "__main__":
    unittest.main()
