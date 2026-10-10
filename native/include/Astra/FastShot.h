#pragma once
#include "Astra/Core.h"
#include <array>
#include <functional>
#include <mutex>

namespace Astra {
// A mounted gun supplies its own initial impulse; the operator's equipped bow
// and draw animation do not define the velocity at the muzzle.
std::optional<Vec> muzzleVelocity(Vec bore,double speed);
std::optional<double> speedMultiplierCorrection(double desired,double calculated,double currentMultiplier);
bool idleResetAllowed(Key gun,Ticket sessionOwner,Ticket effectsOwner,bool effectsIdle,bool cleanupPending);
struct ShotTiming { double fire{.2},release{1./15.},reset{.8},cycle{1.}; bool continuous{}; };
enum class ShotAction { None,Prepare,Launch,Reset,Restore };
enum class InputResult { Ignored,Accepted,ModeChanged };
struct ShotRequest { Ticket ticket; uint64_t sequence{}; double admitted{}; bool repeated{}; };
// Plain deterministic state; the adapter serializes it with EffectsBarrier.
class FastShot {
 public:
 bool begin(Ticket,ShotTiming,std::array<bool,4>);
 InputResult edge(Ticket,int slot,bool down,double now,bool context);
 void pause(std::array<bool,4>);
 void invalidate();
 ShotAction next(double now,bool context);
 void prepared(double now,bool success);
 void launched(double now,bool success);
 void reset(double now);
 void restored();
 bool continuous()const{return timing_.continuous;}
 bool active()const{return bool(ticket_);}
 ShotRequest request()const{return request_;}
 private:
 Ticket ticket_{};ShotTiming timing_{};std::array<bool,4> held_{},releaseGate_{};
 ShotRequest request_{};uint64_t sequence_{};int phase_{};
 bool repeatArmed_{},committed_{},resetNeeded_{};
 double releaseAt_{},resetAt_{},restoreAt_{},cooldownUntil_{};
};
// Engine effects never own Session's mutex. End/Begin wait here for an old
// effect block; reentrant engine callbacks invalidate but cannot begin anew.
class EffectsBarrier {
 public:
 using Lock=std::unique_lock<std::recursive_mutex>;
 Lock lock(){return Lock(mutex_);}
 bool quiescent()const{return depth_==0;}
 void enter(){++depth_;}
 void leave(){--depth_;}
 private: std::recursive_mutex mutex_;unsigned depth_{};
};
struct AmmoOutcome { bool launched{},charged{},refunded{};int before{},after{}; };
// Task-queue cleanup handshake, also used by PSC/guard readiness queries.
class EffectsFence {
 public:
 bool begin(Ticket);void requestEnd(Ticket);void complete(Ticket);
 bool pending()const{return pending_;}bool quiescent(Key)const;
 private:Ticket owner_{};bool pending_{};
};
AmmoOutcome transactAmmo(const std::function<int()>& count,const std::function<void()>& remove,
 const std::function<bool()>& launch,const std::function<void()>& refund);
}
