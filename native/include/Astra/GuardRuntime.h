#pragma once
#include <RE/Skyrim.h>
#include <SKSE/SKSE.h>
#include "Astra/FastShot.h"
#include "Astra/GuardPolicy.h"
#include <string>
#include <atomic>
namespace Astra {
// Separate API1. No player camera or player ValidateShot is involved.
class GuardRuntime {
 public:
 void install();bool available()const;
 bool begin(RE::TESObjectREFR*,RE::Actor*,int,RE::TESObjectWEAP*,RE::TESAmmo*,RE::TESSound*);
 int status(Key);bool end(Key);bool notify(Key,RE::Actor*);
 bool stationIdle(uint32_t);void invalidate();void menu(const RE::MenuOpenCloseEvent*);
 bool admitPlayer(uint32_t,const std::function<bool()>&);
 void tick(float);void postActor(RE::Actor*);
 void observe(RE::hkbClipGenerator*,const RE::hkbContext&);
 void playerLeaseProbe(std::function<bool(uint32_t)> probe){playerOwns_=std::move(probe);}
 private:
 using Observation=GuardPoseSample;
 struct Slot {
  GuardLease lease;GuardCycle cycle;RE::FormID gun{},actor{},weapon{},ammo{},sound{},target{},advisory{};
  int status{-1};Key retired{};bool acquired{},fault{},flagsSaved{},movement{},head{},graphHead{},graphHeadSaved{};std::array<int,4> ranks{{-1,-1,-1,-1}};
  uintptr_t root{},actorRoot{},character{};uint64_t seen{},gripFrame{};double entered{},phaseAt{},nextScan{},lastTime{},yaw{},stepStart{},stepDelta{},stepPhase{},fireStart{};
   int recoveries{};bool fireObserved{},launched{},resetStarted{},packageRequested{},supportSaved{};Mat yawBase{},pitchBase{};
   double heightOffset{},supportZ{},actorScale{},gripWaitSince{},nextPoseLog{};bool gripConfirmed{};const char* failure{"acquisition not evaluated"};
   std::array<Vec,2> feet{};std::array<Mat,2> footRotation{};
  };
 mutable std::recursive_mutex mutex_;std::mutex observationsMutex_;std::array<Slot,2> slots_{};std::array<Observation,2> observations_{};
 std::array<std::atomic<RE::FormID>,2> watchedActors_{};std::array<std::atomic<uint64_t>,2> postMain_{},postWorker_{};
 std::atomic<uint64_t> frame_{};uint64_t observationSerial_{};double clock_{};std::atomic_bool installed_{};void* oar_{};
 std::function<bool(uint32_t)> playerOwns_;
 Slot* find(Key);void cancel(Slot&,bool,const char*);void cleanup(Slot&);bool context(Slot&,RE::NiPointer<RE::TESObjectREFR>&,RE::NiPointer<RE::Actor>&);
 bool acquire(Slot&,RE::TESObjectREFR*,RE::Actor*);bool pose(Slot&,RE::TESObjectREFR*,RE::Actor*,double);bool feetIK(Slot&,RE::Actor*);
 bool settleGrip(Slot&,RE::TESObjectREFR*,RE::Actor*,const Observation&);
 bool observationFresh(const Slot&,const Observation&)const;bool gripIK(Slot&,RE::TESObjectREFR*,RE::Actor*,const Observation&);
 bool reject(Slot&,RE::TESObjectREFR*,RE::Actor*,const char*);
  bool requestClip(Slot&,RE::Actor*,int);void targets(Slot&,RE::TESObjectREFR*,RE::Actor*);bool shoot(Slot&,RE::TESObjectREFR*,RE::Actor*,double);
 bool blocked()const;
};
}
