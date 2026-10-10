#include "Astra/Core.h"
#include <algorithm>
#include <numbers>
// Portable math uses column vectors and row-major storage; all angles at API boundaries are degrees.
namespace Astra {
Vec Vec::operator+(Vec v)const{return {x+v.x,y+v.y,z+v.z};} Vec Vec::operator-(Vec v)const{return{x-v.x,y-v.y,z-v.z};} Vec Vec::operator*(double s)const{return{x*s,y*s,z*s};}
Mat Mat::transpose()const { Mat r; for(int i=0;i<3;++i)for(int j=0;j<3;++j)r.m[3*i+j]=m[3*j+i];return r; }
Mat Mat::operator*(Mat b)const {Mat r;for(int i=0;i<3;++i)for(int j=0;j<3;++j){r.m[3*i+j]=0;for(int k=0;k<3;++k)r.m[3*i+j]+=m[3*i+k]*b.m[3*k+j];}return r;}
Vec Mat::operator*(Vec v)const {return {m[0]*v.x+m[1]*v.y+m[2]*v.z,m[3]*v.x+m[4]*v.y+m[5]*v.z,m[6]*v.x+m[7]*v.y+m[8]*v.z};}
double rad(double d){return d*std::numbers::pi/180;} double deg(double r){return r*180/std::numbers::pi;}
double wrapDegrees(double d){d=std::fmod(d,360);return d<0?d+360:d;}
double length(Vec v){return std::sqrt(v.x*v.x+v.y*v.y+v.z*v.z);}
Mat rz(double r){double c=std::cos(r),s=std::sin(r);return{{c,-s,0,s,c,0,0,0,1}};}
Mat rx(double r){double c=std::cos(r),s=std::sin(r);return{{1,0,0,0,c,-s,0,s,c}};}
Vec gunDirection(double y,double p){y=rad(y);p=rad(p);return{std::sin(y)*std::cos(p),-std::cos(y)*std::cos(p),std::sin(p)};}
Aim aimFromWorld(Mat root,Vec d){auto l=root.transpose()*d;double n=length(l);if(!std::isfinite(n)||n<1e-9)return{NAN,NAN};l=l*(1/n);return{wrapDegrees(deg(std::atan2(l.x,-l.y))),deg(std::asin(std::clamp(l.z,-1.,1.)))};}
Mat logicalBasis(Vec d){double n=length(d);if(!std::isfinite(n)||n<1e-9)return{{NAN,0,0,0,1,0,0,0,1}};d=d*(1/n);double h=std::hypot(d.x,d.y);if(h<1e-7)return{{NAN,0,0,0,1,0,0,0,1}};Vec right{d.y/h,-d.x/h,0};Vec up{right.y*d.z,-right.x*d.z,right.x*d.y-right.y*d.x};return{{right.x,d.x,up.x,right.y,d.y,up.y,right.z,d.z,up.z}};}
Transform toLocal(Transform parent,Transform w){return{parent.rotation.transpose()*w.rotation,parent.rotation.transpose()*(w.translation-parent.translation)*(1/parent.scale),w.scale/parent.scale};}
// v08 sight zero. The optical axis sits 20.4 u above and parallel to the bore (NIF camera (0,80,40),
// muzzle (0,-224,19.6), both Rz180). Modelled drop at 75 m (5250 u): 0.5*g*t^2, g = 0.35*9.81*70 u/s^2
// (PROJ gravity), t = 5250/5400 s (PROJ speed); range from the camera 5250+304 u. Gravity across the
// line of fire scales with cos(elevation). tests/test_v08_sight_zero.py re-derives the three constants.
// Legacy since v10: Plugin.cpp no longer calls sightZeroRadians/sightCameraRotation (sightPose below
// replaced them); they and their v08 tests are kept only as the record of the v08 zero.
constexpr double kSightParallax=20.4,kSightZeroDrop=113.589,kSightZeroRange=5554.;
double sightZeroRadians(double pitchDegrees){return -std::atan((kSightParallax+kSightZeroDrop*std::cos(rad(pitchDegrees)))/kSightZeroRange);}
Mat sightCameraRotation(Mat anchor,Mat adapter,double pitchDegrees){return anchor*rx(sightZeroRadians(pitchDegrees))*adapter;}
// v10 sight (user choice 2026-10-05: camera at the tail, sliding forward with elevation; rear ring + front post).
// The zero target is where the bolt is after flying kPoseZeroRange along the bore: gravity pulls it kPoseZeroDrop
// straight down (world -Z) in that time, at any elevation. tests/test_v10_sight.py re-derives the constants.
// The bolt flies in world units whatever the model scale: range and drop are not scaled; the sight
// geometry (post, tail, camera floor over the pedestal collision) scales with the model.
constexpr double kPoseZeroRange=5250.,kPoseZeroDrop=113.589,kFrontPostAlong=230.,kTailDistance=120.,kMinCameraHeight=65.,kMinCameraDistance=0.;
double dot(Vec a,Vec b){return a.x*b.x+a.y*b.y+a.z*b.z;}
Vec cross(Vec a,Vec b){return {a.y*b.z-a.z*b.y,a.z*b.x-a.x*b.z,a.x*b.y-a.y*b.x};}
Mat SightPose::rotation()const{return {{right.x,forward.x,up.x,right.y,forward.y,up.y,right.z,forward.z,up.z}};}
SightPose sightPose(Vec rear,Vec anchorRight,Vec muzzle,Vec bore,Vec rootPos,Vec rootUp,double scale){
 SightPose p;double bl=length(bore);if(!std::isfinite(bl)||bl<1e-9||!std::isfinite(scale)||scale<=0)return p;
 bore=bore*(1/bl);
 p.target=muzzle+bore*kPoseZeroRange+Vec{0,0,-kPoseZeroDrop};
 Vec line=p.target-rear;double ll=length(line);if(!std::isfinite(ll)||ll<1e-6)return p;
 p.forward=line*(1/ll);double along=dot(p.forward,bore);if(along<0.9)return p;
 p.frontPost=rear+p.forward*(kFrontPostAlong*scale/along);
 double height=dot(rear-rootPos,rootUp),rise=dot(p.forward,rootUp);
 p.distance=kTailDistance*scale;
 if(rise>1e-9)p.distance=std::min(p.distance,(height-kMinCameraHeight*scale)/rise);
 p.distance=std::max(p.distance,kMinCameraDistance*scale);
 p.camera=rear-p.forward*p.distance;
 Vec r=anchorRight-p.forward*dot(anchorRight,p.forward);double rl=length(r);if(!std::isfinite(rl)||rl<1e-6)return p;
 p.right=r*(1/rl);p.up=cross(p.right,p.forward);
 p.valid=std::isfinite(p.camera.x)&&std::isfinite(p.camera.y)&&std::isfinite(p.camera.z)&&std::isfinite(p.frontPost.x)&&std::isfinite(p.frontPost.z);
 return p;
}
float papyrusYaw(double yawDegrees){float y=static_cast<float>(wrapDegrees(yawDegrees));return y<360.f?y:0.f;}
WatchEvent CameraWatch::observe(double deviation,double now){
 if(!std::isfinite(deviation)||!std::isfinite(now))return {};
 if(!deviating_){
  if(deviation<=kStartUnits)return {};
  deviating_=true;since_=lastLog_=now;max_=deviation;
  return {WatchEvent::kStart,deviation,max_,0};
 }
 max_=std::max(max_,deviation);
 if(deviation<kEndUnits){deviating_=false;return {WatchEvent::kEnd,deviation,max_,now-since_};}
 if(now-lastLog_>=kRepeatSeconds){lastLog_=now;return {WatchEvent::kOngoing,deviation,max_,now-since_};}
 return {};
}
void CameraWatch::reset(){deviating_=false;since_=lastLog_=max_=0;}
bool matrixNear(Mat a,Mat b){for(int i=0;i<9;++i)if(std::abs(a.m[i]-b.m[i])>1e-6)return false;return true;}
bool finite(Transform t){for(auto v:t.rotation.m)if(!std::isfinite(v))return false;return std::isfinite(t.translation.x)&&std::isfinite(t.translation.y)&&std::isfinite(t.translation.z)&&std::isfinite(t.scale)&&std::abs(t.scale)>1e-9;}
bool validLimits(AimLimits l){return std::isfinite(l.yawCenter)&&std::isfinite(l.yawHalf)&&std::isfinite(l.pitchMin)&&std::isfinite(l.pitchMax)&&l.yawHalf>0&&l.yawHalf<=180&&l.pitchMin>=-20&&l.pitchMax<=80&&l.pitchMin<=l.pitchMax;}
Aim limitAim(Aim a,AimLimits l){return {wrapDegrees(l.yawCenter+std::clamp(std::remainder(a.yaw-l.yawCenter,360.),-l.yawHalf,l.yawHalf)),std::clamp(a.pitch,l.pitchMin,l.pitchMax)};}
bool Session::begin(Key k,double yaw,double pitch){return begin(k,yaw,pitch,AimLimits{});}
bool Session::begin(Key k,double yaw,double pitch,AimLimits limits){std::lock_guard l(mutex_);if(active_||!k.handle||k.token<=0||!std::isfinite(yaw)||!std::isfinite(pitch)||!validLimits(limits))return false;key_=k;limits_=limits;aim_=limitAim({yaw,pitch},limits);active_=true;ready_=frozen_=sampled_=suspended_=false;snapshot_={};sceneTicket_={};sceneIdentity_=0;++epoch_;return true;}
bool Session::ready(Key k)const{std::lock_guard l(mutex_);return active_&&ready_&&key_==k;}
std::optional<Aim> Session::capture(Key k,bool freeze){std::lock_guard l(mutex_);if(!active_||!ready_||key_!=k)return{};if(freeze)frozen_=true;return snapshot_.aim;}
bool Session::freeze(Key k,bool freeze){std::lock_guard l(mutex_);if(!active_||!ready_||key_!=k)return false;if(frozen_!=freeze)sampled_=false;frozen_=freeze;return true;}
bool Session::end(Key k){std::lock_guard l(mutex_);if(!active_||key_!=k)return false;active_=ready_=suspended_=false;snapshot_={};++epoch_;return true;}
void Session::invalidate(){std::lock_guard l(mutex_);active_=ready_=suspended_=false;snapshot_={};++epoch_;}
bool Session::invalidate(Ticket t){std::lock_guard l(mutex_);if(!active_||t.epoch!=epoch_||t.key!=key_)return false;active_=ready_=suspended_=false;snapshot_={};++epoch_;return true;}
// v09: the camera left first person (a menu camera such as TweenMenu). Keep the lease, pose, readiness and
// freeze; only scene and camera writes stop until FirstPersonState::Update runs again. Papyrus decides a
// permanent loss (camera state not back to first person after its menu grace).
bool Session::suspend(Ticket t){std::lock_guard l(mutex_);if(!active_||t.epoch!=epoch_||t.key!=key_)return false;bool newly=!suspended_;suspended_=true;sampled_=false;return newly;}
bool Session::suspended()const{std::lock_guard l(mutex_);return active_&&suspended_;}
void Session::rebase(){std::lock_guard l(mutex_);sampled_=false;}
Ticket Session::ticket()const{std::lock_guard l(mutex_);return active_?Ticket{key_,epoch_}:Ticket{};}
uintptr_t Session::invalidateScene(Ticket t){
 std::lock_guard l(mutex_);uintptr_t identity=0;
 if(sceneTicket_.epoch==t.epoch&&sceneTicket_.key==t.key){identity=sceneIdentity_;sceneTicket_={};sceneIdentity_=0;}
 if(active_&&epoch_==t.epoch&&key_==t.key){active_=ready_=suspended_=false;snapshot_={};++epoch_;}
 return identity;
}
bool Session::update(Ticket t,Aim sample,bool paused,const std::function<Snapshot(Aim)>& apply,bool reconcileInput,uintptr_t sceneIdentity){
 std::lock_guard l(mutex_);
 if(!active_||t.epoch!=epoch_||t.key!=key_)return false;
 // Record acquisition in the same transaction as pose writes. Even a failed
 // first apply or End before FastShot arms must clean this original scene.
 if(sceneIdentity){sceneTicket_=t;sceneIdentity_=sceneIdentity;}
 if(!std::isfinite(sample.yaw)||!std::isfinite(sample.pitch)){active_=ready_=suspended_=false;snapshot_={};++epoch_;return false;}
 // Consume player-look increments even during pause/freeze, discarding concealed motion.
 if(sampled_&&!frozen_&&!paused){double dy=std::remainder(sample.yaw-last_.yaw,360);aim_=limitAim({aim_.yaw+dy,aim_.pitch+sample.pitch-last_.pitch},limits_);}
 last_=sample;sampled_=true;
 // Apply, world update and publish are inside the same mutex as Freeze/End.
 auto next=apply(aim_);
 if(!next.valid||!finite(next.camera)){active_=ready_=suspended_=false;snapshot_={};++epoch_;return false;}
 if(reconcileInput)last_=next.aim;
 snapshot_=next;ready_=true;suspended_=false;return true;
}
std::optional<Snapshot> Session::snapshot()const{std::lock_guard l(mutex_);return active_&&ready_?std::optional<Snapshot>{snapshot_}:std::nullopt;}
bool Session::visitSnapshot(Ticket t,const std::function<void(const Snapshot&)>& visitor)const{
 std::lock_guard l(mutex_);if(!active_||!ready_||t.epoch!=epoch_||t.key!=key_)return false;
 visitor(snapshot_);return true;
}
bool Session::validateShot(Key k,Aim pose,double pivotHeight)const{
 std::lock_guard l(mutex_);
 if(!active_||!ready_||!frozen_||k!=key_||!snapshot_.poseValid)return false;
 const auto& s=snapshot_;
 if(!std::isfinite(pose.yaw)||!std::isfinite(pose.pitch)||!std::isfinite(pivotHeight)||
    std::abs(std::remainder(pose.yaw-s.aim.yaw,360.))>.01||std::abs(pose.pitch-s.aim.pitch)>.01||
    !finite(s.root)||!finite(s.muzzle)||s.root.scale<=0||s.root.scale>100)return false;
 auto orthogonal=[](Mat m){auto unit=m.transpose()*m;for(int i=0;i<9;++i)if(std::abs(unit.m[i]-Mat{}.m[i])>.002)return false;return true;};
 if(!orthogonal(s.root.rotation)||!orthogonal(s.muzzle.rotation))return false;
 Vec expected=s.root.rotation*gunDirection(pose.yaw,pose.pitch),forward=s.muzzle.rotation*Vec{0,1,0};
 double dot=expected.x*forward.x+expected.y*forward.y+expected.z*forward.z;
 if(dot<.999||std::abs(length(forward)-1)>.001)return false;
 double p=rad(pose.pitch),y=rad(pose.yaw),ly=-224*std::cos(p)+19.6*std::sin(p);
 Vec local{-ly*std::sin(y),ly*std::cos(y),pivotHeight+224*std::sin(p)+19.6*std::cos(p)};
 return length(s.root.translation+s.root.rotation*local*s.root.scale-s.muzzle.translation)<=1.;
}
}
