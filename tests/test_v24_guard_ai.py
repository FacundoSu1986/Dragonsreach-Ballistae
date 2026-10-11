"""Regression evidence for the in-game v23 acquisition/combat failure."""
from pathlib import Path
import struct
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'scripts'),str(ROOT/'scripts/vendor')]
from parser_esm import Plugin


class GuardAI24(unittest.TestCase):
    def test_only_owned_operators_receive_exclusive_package(self):
        p = Plugin(ROOT/'addons/WhiterunTorres/AstraAsedio_WhiterunTorres.esp')
        records = {p.form_id(o):(t,p.subrecords(p.datos(o))) for t,o,n,d in p.recorrer()
                   if t not in ('GRUP','TES4')}
        package = 0x04000B90
        self.assertTrue(package in records,'operator package absent: actor uses vanilla combat AI')
        typ,subs = records[package]
        self.assertEqual(typ,'PACK')
        self.assertEqual(dict(subs)['PKCU'],struct.pack('<III',3,0x00016FAA,3))
        self.assertEqual(dict(subs)['PLDT'],struct.pack('<III',12,0,0))
        flags = struct.unpack_from('<I',dict(subs)['PKDT'])[0]
        self.assertEqual(flags & ((1<<20)|(1<<21)|(1<<27)),(1<<20)|(1<<21)|(1<<27))
        self.assertFalse(flags & (1<<23),'operator must not draw a personal weapon')
        self.assertEqual(struct.unpack_from('<H',dict(subs)['PKDT'],8)[0],0)
        self.assertFalse(any(k in ('VMAD','CTDA') for k,v in subs))
        for npc in (0x04000B00,0x04000B01):
            packages = [struct.unpack('<I',v)[0] for k,v in records[npc][1] if k=='PKID']
            self.assertEqual(packages[0],package)

    def test_saved_generated_actor_bases_are_covered_by_alias(self):
        p = Plugin(ROOT/'addons/GuardAnim/AstraAsedio_GuardAnim.esp')
        quest = next(p.subrecords(p.datos(o)) for t,o,n,d in p.recorrer() if t=='QUST')
        self.assertEqual(dict(quest)['DNAM'][2],100)
        self.assertEqual([struct.unpack('<I',v)[0] for k,v in quest if k=='ALPC'],[0x02000B90]*2)
        self.assertEqual([struct.unpack('<I',v)[0] for k,v in quest if k=='FNAM'],[0x92]*2)

    def test_migration_runs_after_draining_v23_and_refreshes_packages(self):
        text = (ROOT/'mod/scripts/source/AstraAsedioGuard.psc').read_text()
        for required in ('v23PlacementVersion < 24','v23PlacementVersion >= 24',
                         'v23PlacementVersion = 24','actorRef.EvaluatePackage()'):
            self.assertTrue(required in text,required+' missing')
        self.assertNotIn('actorRef.RemoveAllItems(',text)
        self.assertNotIn('actorRef.EnableAI(false)',text)

    def test_alias_packages_are_refilled_on_existing_save_load(self):
        text=(ROOT/'mod/scripts/source/AstraAsedioPlayerAlias.psc').read_text()
        self.assertIn('operatorAlias.Clear()',text)
        self.assertIn('operatorAlias.ForceRefTo(operatorRef)',text)
        bootstrap=text.split('Function BootstrapGuardV23()',1)[1]
        self.assertLess(bootstrap.index('controller.StartV23()'),bootstrap.index('operatorAlias.Clear()'))


if __name__ == '__main__':unittest.main()
