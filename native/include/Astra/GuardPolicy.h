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
// v29.2: `hunted` marks a player whom the town guards are fighting; only then (and only with
// GuardAllowPlayerTarget) can the player be an enemy. Any other player stays a visual target.
struct GuardCandidate {uint32_t id{};Vec position{};bool loaded{},visible{},hostile{},combat{},player{},teammate{};double halfHeight{96};bool resident{};bool hunted{};};
struct GuardProtected {Vec feet{};double radius{},height{};};
std::optional<GuardProtected> guardBounds(Vec minimum,Vec maximum,double margin=12);
struct GuardLegPose {Vec knee;};
bool guardStation(uint32_t,uint32_t,uint32_t);
bool guardEnemy(const GuardCandidate&);
// `ballistic` (v29.2): enemies beyond the visual radius need an elevated shot instead of a flat one.
std::optional<uint32_t> selectGuardTarget(std::span<const GuardCandidate>,uint32_t,Vec,Mat,Vec,bool ballistic=false);
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
// v29.2 (docs/superpowers/specs/2026-10-12-guardia-apuntado-disparo.md). Unproven in game.
// Elevation: CTRL_ELEVACION is driven as in the player sight (rx(-pitch)*base, Plugin.cpp), so the bore
// is gunDirection(yaw,pitch). The hands stay on the rest-pose grips (the hold clip is fixed), hence
// the narrow pitch range.
inline constexpr double GuardPitchRate=25.;     // degrees/second of the elevation
inline constexpr double GuardPitchMin=-30.;     // degrees, negative = down
inline constexpr double GuardPitchMax=30.;
inline constexpr double GuardBoreTolerance=.008; // |actual bore - solved bore| (unit vectors) allowed at launch
inline constexpr bool GuardAllowPlayerTarget=true; // policy switch: shoot a player the guards are fighting
inline constexpr double GuardProjectileSpeed=5400.,GuardProjectileGravity=240.345;
struct GuardAim {double pitch{},seconds{};};
// Low-arc pitch (degrees) for a target at `toTarget` from the pitch pivot. The muzzle sits `along`
// ahead of the pivot and `up` above it at pitch 0 and swings with the elevation. nullopt: out of
// reach or outside [pitchMin,pitchMax] or non-finite.
std::optional<GuardAim> guardAimSolution(Vec toTarget,double along,double up,double pitchMin=GuardPitchMin,double pitchMax=GuardPitchMax,double speed=GuardProjectileSpeed,double gravity=GuardProjectileGravity);
std::optional<double> guardTrackPitch(double pitch,double desired,double dt);
// Unit bore for a horizontal heading (any length) and an elevation in degrees.
std::optional<Vec> guardBore(Vec horizontal,double pitchDegrees);
// Parabola from the muzzle along a unit bore with any elevation (guardTrajectory is the flat case).
std::vector<Vec> guardArcTrajectory(Vec muzzle,Vec bore,double seconds,double speed,double gravity);
// v29.1 (docs/superpowers/specs/2026-10-12-guardia-pose-fixes.md). Unproven in game:
// these remove three engine interferences that fit "arms keep trying to rise, no reaction".
// 1) Write the actor transform only when it differs from the target. A redundant
//    SetPosition/SetRotation every frame is a per-frame teleport.
inline constexpr double GuardPoseEpsilonPosition=.05;  // units
inline constexpr double GuardPoseEpsilonAngle=.001;    // radians
struct GuardPoseWrites {bool position{},rotation{};};
// Unknown (non-finite) inputs fail towards writing, i.e. the pre-v29.1 behaviour.
GuardPoseWrites guardPoseWrites(Vec current,Vec desired,double currentHeading,double desiredHeading,double currentPitch);
// 2) Wrists this close to their grips prove the pose is held, whatever OAR telemetry says
//    (expected about 3 u at Nord height 1.03); a held pose is never re-requested.
inline constexpr double GuardHeldHandError=12.;        // units
bool guardHandsHeld(double leftError,double rightError);
// 3) A re-request returns the graph to default first and plays the idle later, never in the
//    same frame, and gives up after a few tries (the pose is then kept, not cancelled).
inline constexpr double GuardReplayDelay=.35;          // seconds after IdleForceDefaultState
inline constexpr int GuardMaxReissues=3;
class GuardHoldWatch {
 public:void begin(double now);void seen(double now);bool entered(double now)const;bool reissue(double now);
 // The idle was (re)played at `now`: the entry blend and the 6 s spacing restart there.
 void restart(double now);
 // No evidence of the pose for more than 3 s, whatever the reissue budget.
 bool stale(double now)const;bool exhausted()const{return reissues_>=GuardMaxReissues;}int reissues()const{return reissues_;}
 private:double since_{},last_{},seen_{-1e300};int reissues_{};
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
