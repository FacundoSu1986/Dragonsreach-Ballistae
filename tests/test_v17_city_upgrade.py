"""Fresh city bindings and save repair; source fixtures are not Skyrim VM proof."""
from pathlib import Path
import struct
from types import SimpleNamespace
import pytest
from test_control_lease import SessionSourceEvaluator
from test_v15_placements import records
from test_v15_station import StationFixture, count
from build_modular_v13 import subs
import build_plugin as B

ROOT=Path(__file__).resolve().parents[1]

def test_new_station_ids_have_complete_scripts_and_old_refs_are_disabled():
    r=records()
    for old,new in [(0x04000B40,0x04000B70),(0x04000B50,0x04000B80)]:
        assert new in r, 'saved refs retain prior bindings; replacement must be a fresh ref'
        for n in range(5):
            assert struct.unpack_from('<I',r[old+n],8)[0]&0x800
            assert not struct.unpack_from('<I',r[new+n],8)[0]&0x800
        scripts=B.read_vmad(subs(r[new])['VMAD'])['scripts']
        player,guard=[s['properties'] for s in scripts]
        assert player['Guard']['value']['form_id']==new
        assert guard['AllowPlayerTakeover']['value'] is True
        assert guard['Standby']['value']['form_id']==new+3
        assert guard['Puesto']['value']['form_id']==new+2
        assert guard['Artillero']['value']['form_id']==new+1

class Ref:
    def __init__(self):self.disabled=False;self.quiet=True;self.busy=False;self.retired=False
    def RetireStation(self):self.retired=True;return not self.busy
    def Disable(self,fade=False):self.disabled=True

def alias():
    vm=SessionSourceEvaluator((ROOT/'mod/scripts/source/AstraAsedioPlayerAlias.psc').read_text())
    refs={i:Ref() for i in [0xB70,*range(0xB40,0xB45)]};disabled=[]
    vm.state.update(Game=SimpleNamespace(GetFormFromFile=lambda i,f:refs.get(i)),
                    SKSE=SimpleNamespace(GetPluginVersion=lambda name: 0x03050040),
                    AstraSightNative=SimpleNamespace(IsEffectsQuiescent=lambda r,t:r.quiet),
                    Debug=SimpleNamespace(Trace=lambda *a:None))
    return vm,refs

@pytest.mark.parametrize('fence',['native','guard'])
def test_saved_station_is_not_disabled_before_old_effects_drain(fence):
    vm,refs=alias();gun=refs[0xB40]
    if fence=='native':gun.quiet=False
    else:gun.busy=True
    assert not vm.run('RetireLegacyCity',0xB40,0xB70)
    assert not any(refs[n].disabled for n in range(0xB40,0xB45))
    gun.quiet=True;gun.busy=False
    assert vm.run('RetireLegacyCity',0xB40,0xB70)
    assert gun.retired and all(refs[n].disabled for n in range(0xB40,0xB45))
    assert not refs[0xB70].disabled

def test_no_city_addon_leaves_all_existing_refs_untouched():
    vm,refs=alias();del refs[0xB70]
    assert vm.run('RetireLegacyCity',0xB40,0xB70)
    assert not any(r.disabled or r.retired for r in refs.values())

def test_native_preparation_that_returns_after_four_seconds_can_enter():
    f=StationFixture()
    f.hooks['guard:PreparePlayerLease:after']=lambda:setattr(f.parent.vm,'now',f.parent.vm.now+4.)
    f.enter()
    assert count(f,'parent:OnActivate')==1
    assert f.parent.vm.state['operating']

def test_retirement_cancels_pending_guard_and_prevents_recovery():
    from test_v13_guard import GuardFixture
    f=GuardFixture();f.load();f.vm.state['pinBusy']=True
    assert not f.run('RetireStation')
    assert f.vm.state['stationRetired'] and not f.vm.state['running']
    f.vm.state['pinBusy']=False
    assert f.run('RetireStation')
    f.load()
    assert not f.vm.state['running'] and not f.guard.pinned

def test_restored_alias_mutation_slot_keeps_polling_until_old_call_returns():
    vm,refs=alias();updates=[]
    vm.native['RegisterForSingleUpdate']=updates.append
    vm.state.update(cityRetirementPending=True,cityRetirementBusy=True)
    vm.run('OnUpdate')
    assert updates==[.2] and not any(r.disabled for r in refs.values())
