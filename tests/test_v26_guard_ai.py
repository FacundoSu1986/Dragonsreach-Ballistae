"""Check real saved-actor migration and the v25 interruption evidence."""
import hashlib
import json
import unittest
from tests import test_v25_guard_ai as V25

ROOT=V25.ROOT


class GuardAI26(V25.GuardAI25):
    def test_migration_runs_after_draining_v23_and_refreshes_packages(self):
        text=(ROOT/'mod/scripts/source/AstraAsedioGuard.psc').read_text()
        for required in ('v23PlacementVersion < 26','v23PlacementVersion >= 26',
                         'v23PlacementVersion = 26','actorRef.EvaluatePackage()'):
            self.assertTrue(required in text,required+' missing')
        self.assertNotIn('actorRef.RemoveAllItems(',text)
        self.assertNotIn('actorRef.EnableAI(false)',text)
        self.assertNotIn('actorRef.SetScale(',text)
        pump=text.split('Function PumpV23()',1)[1]
        self.assertIn('v23PlacementVersion < 26 && v23Token == 0',pump)
        self.assertLess(pump.index('AstraGuardNative.EndOperation('),pump.index('MigrateV23('))

    def test_shield_is_prepared_on_owned_operator_before_new_native_token(self):
        text=(ROOT/'mod/scripts/source/AstraAsedioGuard.psc').read_text()
        self.assertTrue('Function PrepareShieldV26(' in text,'left hand preparation absent')
        prep=text.split('Function PrepareShieldV26(',1)[1].split('EndFunction',1)[0]
        self.assertIn('actorRef != ResolveV23Operator()',prep)
        self.assertIn('actorRef.GetEquippedShield()',prep)
        self.assertIn('actorRef.UnequipItem(shield, true, true)',prep)
        self.assertNotIn('RemoveItem(',prep)
        self.assertNotIn('UnequipAll(',prep)
        pump=text.split('Function PumpV23()',1)[1]
        self.assertLess(pump.index('PrepareShieldV26('),pump.index('AstraGuardNative.BeginOperation('))
        # A shield request must yield to a later update before native scene
        # identity is captured; it may rebuild the actor's equipment geometry.
        self.assertIn('if !PrepareShieldV26(actorRef, expected)',pump)
        self.assertIn('FinishPumpV23(expected, 0.2)',pump)

    def test_observed_v25_acquisition_is_followed_by_context_cancellation(self):
        data=json.loads((ROOT/'reports/diagnosis_v25_context.json').read_text())
        snapshot=ROOT/'build/guard-v26/observed_v25_AstraSight.log'
        self.assertEqual(hashlib.sha256(snapshot.read_bytes()).hexdigest(),data['log_sha256'])
        self.assertGreater(data['acquired_count'],0)
        self.assertEqual(data['acquired_count'],data['cancel_count'])
        self.assertFalse(data['hold_observed'])
        self.assertFalse(data['grip_observed'])
        self.assertFalse(data['v26_in_game_tested'])
        self.assertEqual(set(k.strip() for k in data['cancel_reasons']),{'death/stagger/unload/owner/context'})


if __name__=='__main__':unittest.main()
