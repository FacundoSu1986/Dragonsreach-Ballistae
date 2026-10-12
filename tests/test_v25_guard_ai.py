"""Release contracts for the measured v24 scale rejection and saved actors."""
import hashlib
import json
import unittest
from tests import test_v24_guard_ai as V24

ROOT=V24.ROOT


class GuardAI25(V24.GuardAI24):
    def test_migration_runs_after_draining_v23_and_refreshes_packages(self):
        text=(ROOT/'mod/scripts/source/AstraAsedioGuard.psc').read_text()
        for required in ('v23PlacementVersion < 25','v23PlacementVersion >= 25',
                         'v23PlacementVersion = 25','actorRef.EvaluatePackage()'):
            self.assertTrue(required in text,required+' missing')
        self.assertNotIn('actorRef.RemoveAllItems(',text)
        self.assertNotIn('actorRef.EnableAI(false)',text)
        self.assertNotIn('actorRef.SetScale(',text)
        pump=text.split('Function PumpV23()',1)[1]
        self.assertIn('v23PlacementVersion < 25 && v23Token == 0',pump)
        self.assertLess(pump.index('AstraGuardNative.EndOperation('),pump.index('MigrateV23('))

    def test_observed_diagnosis_snapshot_is_preserved(self):
        data=json.loads((ROOT/'reports/diagnosis_v24_scale.json').read_text())
        snapshot=ROOT/'build/guard-v25/observed_v24_AstraSight.log'
        self.assertEqual(hashlib.sha256(snapshot.read_bytes()).hexdigest(),data['log_sha256'])
        text=snapshot.read_text()
        self.assertIn('actorScale=1.03',text)
        self.assertIn('clause=station / actor scale differs from 1',text)
        self.assertNotIn('guard v24 hold confirmed by OAR',text)
        self.assertFalse(data['v25_in_game_tested'])


if __name__=='__main__':unittest.main()
