#pragma once
#include <RE/Skyrim.h>
#include <SKSE/SKSE.h>
#include "Astra/FastShot.h"
#include "Astra/GuardPolicy.h"
#include <string>
#include <atomic>
#include <chrono>
#include <vector>
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
 // ok: mount+operator placed. blocked: this move is refused, previous yaw kept.
 // invalid: the station/operator contract is broken and the lease must end.
 enum class Pose {ok,blocked,invalid};
 struct Slot {
  GuardLease lease;GuardCycle cycle;RE::FormID gun{},actor{},weapon{},ammo{},sound{},target{},advisory{};
  int status{-1};Key retired{};bool acquired{},fault{},flagsSaved{},movement{},head{},graphHead{},graphHeadSaved{};std::array<int,4> ranks{{-1,-1,-1,-1}};
  uintptr_t root{},actorRoot{},character{};uint64_t seen{},gripFrame{};double entered{},phaseAt{},nextScan{},lastTime{},yaw{},stepStart{},stepDelta{},stepPhase{},fireStart{};
   int recoveries{};bool fireObserved{},launched{},resetStarted{},packageRequested{},supportSaved{};Mat yawBase{},pitchBase{};
   double heightOffset{},supportZ{},actorScale{},gripWaitSince{},nextPoseLog{};bool gripConfirmed{};const char* failure{"acquisition not evaluated"};
   // v29.1: two-phase re-request, held-pose evidence and write counters (poseLog).
   double replayAt{-1},nextHandCheck{},maxDrift{};std::array<double,2> handError{{-1,-1}};bool holdGaveUp{};unsigned writesPos{},writesRot{};
   // v29.2: elevation of CTRL_ELEVACION (degrees), the town guards are fighting the player, last shot refusal.
   double pitch{},nextRefusalLog{},nextTargetLog{};bool hunted{};const char* shotRefusal{""};
   // v31: a post is a station whose operator is part of the NIF (node OPERADOR_SOPORTE); no actor, no lease.
   bool post{},camp{};RE::FormID reference{};double nextAcquire{},nextPostLog{},lastTargetAt{},targetSeenAt{};std::string shotDetail;
   // v33.14: the post status line is written when status/target/hunted change, and as a 30 s heartbeat otherwise.
   int loggedStatus{-99};RE::FormID loggedTarget{};bool loggedHunted{};
   std::array<Vec,2> feet{};std::array<Mat,2> footRotation{};
   GuardHoldWatch hold;double nextShot{},fireAt{},blockedSince{-1},sampleAt{-1};const char* moveRefusal{};
   // v32: the last bolt of a post, sampled in flight (position and velocity against the launch arc).
   RE::ProjectileHandle flight;Vec flightOrigin{},flightBore{};double flightAt{};int flightStage{};
  };
 mutable std::recursive_mutex mutex_;std::mutex observationsMutex_;std::array<Slot,2> slots_{};std::array<Slot,GuardMaxPosts> posts_{};std::array<Observation,2> observations_{};
 // v33.14: lock-free mirror of observations_[i].character, read by observe() before it takes the mutex. observe() runs
 // for every clip of every animated actor (possibly on animation workers) and the list is empty unless an NPC guard
 // lease is live (never, since the v31 posts). A missed sample is harmless: the observation is telemetry only.
 std::array<std::atomic<uintptr_t>,2> observedCharacters_{};
 std::array<std::atomic<RE::FormID>,2> watchedActors_{};std::array<std::atomic<uint64_t>,2> postMain_{},postWorker_{};
 std::atomic<uint64_t> frame_{};uint64_t observationSerial_{};double clock_{};std::atomic_bool installed_{};void* oar_{};
 std::function<bool(uint32_t)> playerOwns_;
 // v29.1: clips seen on a watched actor that are not the owned ones (worker thread; observationsMutex_).
 struct LoggedClip{std::string key;std::chrono::steady_clock::time_point at{};};
 std::array<std::vector<LoggedClip>,2> loggedClips_{};
 Slot* find(Key);void cancel(Slot&,bool,const char*);void cleanup(Slot&);bool context(Slot&,RE::NiPointer<RE::TESObjectREFR>&,RE::NiPointer<RE::Actor>&);
 bool acquire(Slot&,RE::TESObjectREFR*,RE::Actor*);Pose pose(Slot&,RE::TESObjectREFR*,RE::Actor*,double,double);
 void reload(Slot&,RE::TESObjectREFR*);void poseLog(Slot&,RE::TESObjectREFR*,RE::Actor*,const Observation&,double,double);
 bool reject(Slot&,RE::TESObjectREFR*,RE::Actor*,const char*);
  void tickPosts(double,bool);bool postAcquire(Slot&,RE::TESObjectREFR*,size_t);bool postPose(Slot&,RE::TESObjectREFR*,double,double);void sampleFlight(Slot&);
  bool requestClip(Slot&,RE::Actor*,int,bool again=false);bool playHold(Slot&,RE::Actor*);void targets(Slot&,RE::TESObjectREFR*,RE::Actor*);bool shoot(Slot&,RE::TESObjectREFR*,RE::Actor*);
 bool blocked()const;
 bool paused()const;
};
}
