#pragma once
#include <RE/Skyrim.h>
#include <SKSE/SKSE.h>
#include "Astra/FastShot.h"
namespace Astra {
struct FastConfig {
 RE::FormID weapon{},ammo{},cost{},sound{};ShotTiming timing;AimLimits limits;
 double pivot{153},operatorHeight{119},operatorDistance{160},operatorTolerance{64};
};
class FastShotRuntime final:public RE::BSTEventSink<RE::InputEvent*> {
 public:
 explicit FastShotRuntime(Session& s):session_(s){}
 bool begin(Key,double,double,FastConfig);
 bool beginLegacy(Key,double,double);
 bool end(Key);void invalidate();
 bool ready(Key);bool quiescent(Key);int mode(Key);
 bool resetIdleScene(Key);
 void tick();void menu(const RE::MenuOpenCloseEvent*);
 RE::BSEventNotifyControl ProcessEvent(RE::InputEvent* const*,RE::BSTEventSource<RE::InputEvent*>*)override;
 private:
 Session& session_;EffectsBarrier effects_;EffectsFence fence_;FastShot shots_;FastConfig config_{};Ticket owner_{};
 bool armed_{};uintptr_t rootIdentity_{};double entered_{},lastArmWaitLog_{};
 RE::ProjectileHandle flightHandle_;Ticket flightTicket_{};Vec flightOrigin_{};double flightAt_{};int flightStage_{};
 std::array<uint32_t,6> mapping_{{255,255,255,255,255,255}};
 std::array<std::array<bool,256>,2> physical_{};
 void mappings();std::array<bool,4> physicalHolds();
 bool context(RE::NiPointer<RE::TESObjectREFR>&,Snapshot&)const;
 bool blocked()const;bool current(Ticket)const;
 bool sequence(RE::TESObjectREFR*,const char*,const char*);
 void cleanup(Ticket,FastConfig,uintptr_t);void requestEnd();
};
}
