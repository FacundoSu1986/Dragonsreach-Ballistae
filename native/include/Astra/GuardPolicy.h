#pragma once
#include "Astra/Core.h"
#include <span>
#include <vector>
#include <string_view>
#include <array>
namespace Astra {
inline constexpr std::string_view GuardStationPlugin="DragonsreachBallistae_WhiterunTowers.esp";
// v33: the posts the runtime drives, by the FormID (in the entry's own plugin) of the gun reference. A post whose
// reference is not in the load order (or not loaded) is simply skipped, so the table can name sites the plugin
// does not carry yet. `npc` is the retired NPC operator of the v30 stations (0 = none).
//  city : engages what the town guards fight; the player only while the guards are fighting them (`hunted`). Crime
//         tolerance (minor crimes, Thane) is inherited: those guards do not fight the player. v33.3: the house
//         exemption was removed -- GLOB HPWhiterun is the house PRICE (5000), not an ownership flag, so it silenced
//         every city post for every player.
//  camp : friends are bandits; the player is a target on sight, always.
enum class GuardPostKind{city,camp};
struct GuardPostSpec{uint32_t gun,npc;GuardPostKind kind;std::string_view plugin;};
inline constexpr std::string_view GuardPuestosPlugin="DragonsreachBallistae_Outposts.esp";
inline constexpr size_t GuardMaxPosts=6;
// v33.14: a camp post only counts bandits this close to it as its own (it credits its shot to one and judges hostility
// against it). Without the limit a cleared camp kept shooting the player for any bandit loaded elsewhere.
inline constexpr double GuardCampReferenceRadius=6000.;
inline constexpr std::array<GuardPostSpec,GuardMaxPosts> GuardPosts{{
 {0xB70,0xB71,GuardPostKind::city,GuardStationPlugin},   // east tower
 {0xB80,0xB81,GuardPostKind::city,GuardStationPlugin},   // west tower
 {0xBA0,0,GuardPostKind::city,GuardPuestosPlugin},       // above the gate
 {0xBB0,0,GuardPostKind::camp,GuardPuestosPlugin},                       // White River Watch
 {0xBC0,0,GuardPostKind::camp,GuardPuestosPlugin},                       // Halted Stream Camp
 {0xBD0,0,GuardPostKind::camp,GuardPuestosPlugin}}};                     // Silent Moons Camp
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
// v33.4: `watchVisitors=false` (the posts): a calm actor that is not the player is never even watched. The khajiit
// caravan camped at the Whiterun gate held the gate and tower posts on itself (test 2026-10-16).
std::optional<uint32_t> selectGuardTarget(std::span<const GuardCandidate>,uint32_t,Vec,Mat,Vec,bool ballistic=false,bool watchVisitors=true);
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
bool guardShouldFire(bool enemy,bool reachable,double yawError,double now,double nextShot,bool placed=true);
struct GuardFrame {double elapsed{};bool actions{};};
GuardFrame guardFrame(bool paused,bool menu,double dt);
// v29.2 (docs/superpowers/specs/2026-10-12-guardia-apuntado-disparo.md). Unproven in game.
// Elevation: CTRL_ELEVACION is driven as in the player sight (rx(-pitch)*base, Plugin.cpp), so the bore
// is gunDirection(yaw,pitch). The hands stay on the rest-pose grips (the hold clip is fixed), hence
// the narrow pitch range.
inline constexpr double GuardPitchRate=25.;     // degrees/second of the elevation
inline constexpr double GuardYawLimit=60.;       // degrees either side of the mount's centre line
// v31.3: the depression follows the geometry, measured on the shipped NIFs (scripts/verify_gun_sweep_v31.py):
// at -42 the barrel assembly clears the bastion prow by 9 u and its own pedestal feet by 6 u (they touch at
// -45). The 2026-10-12 19:3x log had the player 35-39 degrees below the east gun and NPCs at -44.
inline constexpr double GuardPitchMin=-42.;     // degrees, negative = down
// v32: the guard rides in a basket hung from the cradle's tail (scripts/build_operador_malla.py). Elevating the barrel
// lowers the tail and the basket with it: at +16 its floor comes within 1.5 u of the base of its guide posts
// (scripts/verify_canasta_v32.py), at +15 it keeps >= 2.3 u. In every log so far (2026-10-12/14) the targets were below the gun.
inline constexpr double GuardPitchMax=15.;
inline constexpr double GuardBoreTolerance=.008; // |actual bore - solved bore| (unit vectors) allowed at launch
inline constexpr bool GuardAllowPlayerTarget=true; // policy switch: shoot a player the guards are fighting
inline constexpr double GuardProjectileSpeed=5400.,GuardProjectileGravity=240.345;
struct GuardAim {double pitch{},seconds{};};
// Low-arc pitch (degrees) for a target at `toTarget` from the pitch pivot. The muzzle sits `along`
// ahead of the pivot and `up` above it at pitch 0 and swings with the elevation. nullopt: out of
// reach or outside [pitchMin,pitchMax] or non-finite.
std::optional<GuardAim> guardAimSolution(Vec toTarget,double along,double up,double pitchMin=GuardPitchMin,double pitchMax=GuardPitchMax,double speed=GuardProjectileSpeed,double gravity=GuardProjectileGravity);
std::optional<double> guardTrackPitch(double pitch,double desired,double dt);
// v33.4: the player's own mount. Taking the fighting controls sheathes the player's weapon and a dragon then drops the
// player as its target (MQ104 at the Western Watchtower, test 2026-10-16: Mirmulnir flew off while the player was on
// the ballista and came back when they stepped off). While a player session owns a gun, every hostile actor that targets
// the player -- or a dragon in combat nearby -- is retained, and Papyrus reasserts StartCombat on it twice a second.
// v33.5: kept to 30000 u -- in the 2026-10-16 test Mirmulnir passed 12000 u ten seconds after the player mounted and
// was dropped from the list for good.
inline constexpr double MountedThreatCapture=8000.,MountedThreatRelease=30000.,MountedThreatPeriod=.25;
bool mountedThreatCaptured(bool alive,bool teammate,bool hostile,bool sameWorld,double distance,bool targetsPlayer,bool dragonInCombat);
bool mountedThreatKept(bool alive,bool hostile,bool sameWorld,double distance);
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
