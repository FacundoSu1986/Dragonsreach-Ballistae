#pragma once
#include "Astra/Core.h"
#include <span>
#include <vector>
#include <string_view>
namespace Astra {
inline constexpr std::string_view GuardStationPlugin="AstraAsedio_WhiterunTorres.esp";
// Keep all real Generate ABI arguments. The pinned CommonLib declaration is
// abbreviated; OAR's hook is the authoritative signature.
template<class Original,class Clip,class Context,class Output,class Observer>
void guardGenerateAndObserve(Original original,Clip* clip,const Context& ctx,const Output** children,Output& output,float offset,Observer observe){original(clip,ctx,children,output,offset);observe(clip,ctx);}
struct GuardCandidate {uint32_t id{};Vec position{};bool loaded{},visible{},hostile{},combat{},player{},teammate{};double halfHeight{96};bool resident{};};
struct GuardProtected {Vec feet{};double radius{},height{};};
std::optional<GuardProtected> guardBounds(Vec minimum,Vec maximum,double margin=12);
struct GuardLegPose {Vec knee;};
bool guardStation(uint32_t,uint32_t,uint32_t);
std::optional<uint32_t> selectGuardTarget(std::span<const GuardCandidate>,uint32_t,Vec,Mat,Vec);
std::optional<double> horizontalFlight(Vec,double,double,double);
std::vector<Vec> guardTrajectory(Vec,Vec,double,double,double);
bool guardPathSafe(std::span<const Vec>,std::span<const GuardProtected>,double);
Vec guardFoot(Vec,Vec,double,double,bool);
std::optional<GuardLegPose> guardLeg(Vec,Vec,Vec,Vec);
int guardClipKind(std::string_view,std::string_view,std::string_view);
std::optional<double> guardOrbit(Vec,Vec,Mat,Vec,double);
bool guardSupport(double feetZ,double floorZ,double normalZ,std::optional<double> savedFloor);
bool guardNaturalScale(double referenceScale,double effectiveScale,double baseHeight);
std::optional<Vec> guardGrip(Vec origin,Mat rotation,double yaw,bool left,double fireTime=-1);
struct GuardPoseSample {uint64_t serial{},epoch{},frame{};uintptr_t character{};int clip{};double time{},duration{},weight{};};
bool guardPoseFresh(const GuardPoseSample&,uint64_t,uintptr_t,uint64_t,int);
bool guardGripFresh(bool confirmed,uint64_t frame,uint64_t sampledFrame);
bool guardOperatorPackage(bool assigned,bool running,bool ownIdle,bool acquired,bool sheathed);
std::optional<double> guardStepPhase(double previous,double clipTime,double delta,double frameDelta);
bool guardProjectileContract(double speed,double gravity,double radius,double range,double lifetime,double proximity,double timer,double spread,bool alternativeExplosion,double flight);
// v29: the hold clip itself puts both wrists on the grips (FK of the shipped
// HKX: 0.02 u). The runtime steers mount+operator rigidly and never gates on
// animation telemetry; see docs/superpowers/specs/2026-10-11-guardias-v29-design.md.
inline constexpr double GuardTrackRate=20.;     // degrees/second of the mount
inline constexpr double GuardTrackMaxDt=.05;    // hitch frames do not jump the mount
inline constexpr double GuardEnterSeconds=.6;   // vanilla 0.5 s blend into IdleHandsBehindBack + margin
inline constexpr double GuardAimTolerance=.25;  // degrees between mount and target bearing
std::optional<double> guardTrackYaw(double yaw,double desired,double dt);
bool guardShouldFire(bool enemy,bool reachable,double yawError,double now,double nextShot);
class GuardHoldWatch {
 public:void begin(double now);void seen(double now);bool entered(double now)const;bool reissue(double now);
 private:double since_{},last_{},seen_{-1e300};
};
class GuardLease {
 public:bool begin(Key,uint32_t);Ticket ticket()const{return owner_;}void enterEffect(){++effects_;}void leaveEffect(){if(effects_)--effects_;}void cancel(){pending_=bool(owner_);}bool complete();bool current(Ticket)const;
 bool pending()const{return pending_;}uint32_t actor()const{return actor_;}
 private:Ticket owner_{};uint64_t epoch_{};uint32_t actor_{};unsigned effects_{};bool pending_{};
};
class GuardCycle {
 public:bool acquire(double);bool observeHold(double,double);bool ready()const{return ready_;}bool startFire(double);bool synchronizeFire(double,double);bool release(double,double,bool);void interrupt();double fireStart()const{return fireStart_;}
 private:bool acquired_{},ready_{},firing_{},released_{};double holdSample_{-1},holdTime_{},fireStart_{},nextFire_{};
};
}
