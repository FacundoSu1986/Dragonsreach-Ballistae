#pragma once
#include <RE/Skyrim.h>
#include <SKSE/SKSE.h>
#include "Astra/FastShot.h"
#include <mutex>
#include <vector>
namespace Astra {
struct FastConfig {
 RE::FormID weapon{},ammo{},cost{},sound{};ShotTiming timing;AimLimits limits;
 double pivot{153},operatorHeight{119},operatorDistance{160},operatorTolerance{64};
};
// v33.10: the dragon a mounted scan keeps (Keep) feeds the health bar; Tick drops it 1.5 s after the last scan. The
// v33.7 combat-style change (no landing) is gone: it kept Mirmulnir in the air down to no health (test 2026-10-17 12:18).
void mountedAirborneKeep(RE::Actor*);
void mountedAirborneTick();
// v33.14: a dragon is fighting the player on a ballista right now (gates the dragon-watch diagnostics).
bool mountedDragonActive();
// v33.9: the vanilla enemy health bar for the dragon fighting the mounted player (the sight camera keeps it off the
// crosshair, so the HUD hid it). Hooks EnemyHealth::Update and drives HUDMovieBaseInstance.EnemyHealthMeter.SetPercent.
void installEnemyHealthBar();
class FastShotRuntime final:public RE::BSTEventSink<RE::InputEvent*> {
 public:
 explicit FastShotRuntime(Session& s):session_(s){}
 bool begin(Key,double,double,FastConfig);
 bool beginLegacy(Key,double,double);
 bool end(Key);void invalidate();
 bool ready(Key);bool quiescent(Key);int mode(Key);
 bool resetIdleScene(Key);
 // v33.4: the n-th hostile retained while the player owns `Key` (nullptr past the end / another owner).
 RE::Actor* mountedAttacker(Key,int);
 void tick();void menu(const RE::MenuOpenCloseEvent*);
 RE::BSEventNotifyControl ProcessEvent(RE::InputEvent* const*,RE::BSTEventSource<RE::InputEvent*>*)override;
 private:
 Session& session_;EffectsBarrier effects_;EffectsFence fence_;FastShot shots_;FastConfig config_{};Ticket owner_{};
 bool armed_{};uintptr_t rootIdentity_{};double entered_{},lastArmWaitLog_{};
 RE::ProjectileHandle flightHandle_;Ticket flightTicket_{};Vec flightOrigin_{};double flightAt_{};int flightStage_{};
 std::array<uint32_t,6> mapping_{{255,255,255,255,255,255}};
 std::mutex threatsMutex_;Key threatsKey_{};std::vector<RE::ActorHandle> threats_;double nextThreatScan_{},nextThreatLog_{};
 void scanThreats();
 std::array<std::array<bool,256>,2> physical_{};
 void mappings();std::array<bool,4> physicalHolds();
 bool context(RE::NiPointer<RE::TESObjectREFR>&,Snapshot&)const;
 bool blocked()const;bool current(Ticket)const;
 bool sequence(RE::TESObjectREFR*,const char*,const char*);
 void cleanup(Ticket,FastConfig,uintptr_t);void requestEnd();
};
}
