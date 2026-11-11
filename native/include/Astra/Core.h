#pragma once
#include <array>
#include <cmath>
#include <cstdint>
#include <functional>
#include <mutex>
#include <optional>
namespace Astra {
struct Vec { double x{},y{},z{}; Vec operator+(Vec) const; Vec operator-(Vec) const; Vec operator*(double) const; };
struct Mat { std::array<double,9> m{1,0,0,0,1,0,0,0,1}; Mat transpose() const; Mat operator*(Mat) const; Vec operator*(Vec) const; };
struct Transform { Mat rotation; Vec translation; double scale{1}; };
struct Aim { double yaw{},pitch{}; };
struct AimLimits { double yawCenter{},yawHalf{180},pitchMin{-20},pitchMax{80}; };
bool validLimits(AimLimits); Aim limitAim(Aim,AimLimits);
struct Snapshot { Aim aim; Transform camera; bool valid{}; uintptr_t stateIdentity{}; Transform worldCamera,root,muzzle; bool poseValid{}; };
struct Key { uint32_t handle{}; int token{}; bool operator==(const Key&) const = default; };
struct Ticket { Key key; uint64_t epoch{}; explicit operator bool() const { return epoch!=0; } };
double rad(double); double deg(double); double wrapDegrees(double); double length(Vec);
Mat rz(double); Mat rx(double); Vec gunDirection(double,double); Aim aimFromWorld(Mat,Vec); Mat logicalBasis(Vec); Transform toLocal(Transform,Transform); bool matrixNear(Mat,Mat); bool finite(Transform);
// v08 sight zero: downward view tilt (radians) that meets the modelled trajectory at 75 m; elevation in degrees.
double sightZeroRadians(double pitchDegrees); Mat sightCameraRotation(Mat anchor,Mat adapter,double pitchDegrees);
// v10: tail camera on the line rear sight -> 75 m zero target; front post on that line (scripts/sight_pose.py).
struct SightPose { Vec camera,forward,right,up,frontPost,target; double distance{}; bool valid{}; Mat rotation() const; };
SightPose sightPose(Vec rear,Vec anchorRight,Vec muzzle,Vec bore,Vec rootPos,Vec rootUp,double scale);
Vec cross(Vec,Vec); double dot(Vec,Vec);
// v09: yaw handed to Papyrus as float. A double in [0,360) can round to 360.0f, which Papyrus rejected.
float papyrusYaw(double yawDegrees);
// v09: hysteresis watch of a rendered camera against the camera AstraSight published (units of distance).
struct WatchEvent { enum Kind { kNone, kStart, kOngoing, kEnd } kind{kNone}; double deviation{},maxDeviation{},seconds{}; };
class CameraWatch {
 public:
  static constexpr double kStartUnits=2.0,kEndUnits=1.0,kRepeatSeconds=0.5;
  WatchEvent observe(double deviation,double now);
  void reset();
  bool deviating() const { return deviating_; }
 private:
  bool deviating_{}; double since_{},lastLog_{},max_{};
};
class Session {
 public:
  bool begin(Key,double,double); bool ready(Key) const; std::optional<Aim> capture(Key,bool); bool freeze(Key,bool); bool end(Key); void invalidate(); bool invalidate(Ticket); void rebase(); Ticket ticket() const;
  bool begin(Key,double,double,AimLimits);
  // v09: camera left first person; keep the lease. Returns true when newly suspended.
  bool suspend(Ticket); bool suspended() const;
  bool update(Ticket,Aim,bool,const std::function<Snapshot(Aim)>&,bool reconcileInput=false,uintptr_t sceneIdentity=0);
  uintptr_t invalidateScene(Ticket);
  std::optional<Snapshot> snapshot() const;
  // Visitor must not call Session or engine originals; serializes final scene writes with EndSight.
  bool visitSnapshot(Ticket,const std::function<void(const Snapshot&)>&) const;
  bool validateShot(Key,Aim,double pivotHeight) const;
 private:
  mutable std::mutex mutex_; Key key_{}; uint64_t epoch_{1}; bool active_{},ready_{},frozen_{},sampled_{},suspended_{}; Aim aim_{},last_{}; Snapshot snapshot_{}; AimLimits limits_{};
  Ticket sceneTicket_{};uintptr_t sceneIdentity_{};
};
}
