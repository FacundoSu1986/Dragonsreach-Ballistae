#include "Astra/GuardPolicy.h"
#include <algorithm>
#include <limits>
#include <numbers>
#include <string>
#include <cctype>
namespace Astra {
bool guardNaturalScale(double referenceScale,double effectiveScale,double baseHeight){
 // GetScale includes the NPC/race's natural height. The authored contract
 // requires an unscaled reference, not a Nord whose natural height is 1.00.
 return std::isfinite(referenceScale+effectiveScale+baseHeight)&&std::abs(referenceScale-1)<=.001&&baseHeight>=.9&&baseHeight<=1.1&&std::abs(effectiveScale-referenceScale*baseHeight)<=.001;
}
std::optional<Vec> guardGrip(Vec origin,Mat rotation,double yaw,bool left,double fireTime){
 if(!finite({rotation,origin,1})||std::abs(rotation.m[8]-1)>.001||!std::isfinite(yaw+fireTime)||std::abs(yaw)>60.001||(fireTime!=-1&&(fireTime<0||fireTime>1.05)))return {};
 Vec hand{left?33.6:-33.6,143.8,100.5};
 if(!left&&fireTime>=0){
  constexpr std::array<std::pair<double,double>,6> keys{{{0,0},{2./30.,1},{4./30.,.7},{.2,.35},{.45,0},{1,0}}};
  for(size_t i=1;i<keys.size();++i)if(fireTime<=keys[i].first){double u=(fireTime-keys[i-1].first)/(keys[i].first-keys[i-1].first);u=u*u*(3-2*u);double impulse=keys[i-1].second+(keys[i].second-keys[i-1].second)*u;hand.y-=.75*impulse;hand.z-=.8*impulse;break;}
 }
 return origin+rotation*rz(rad(yaw))*hand;
}
bool guardPoseFresh(const GuardPoseSample& o,uint64_t epoch,uintptr_t character,uint64_t frame,int expected){
 constexpr std::array<double,4> duration{2,1,.8,.8};
 return character&&o.character==character&&epoch&&o.epoch==epoch&&o.serial&&o.frame<=frame&&frame-o.frame<=2&&expected>=0&&expected<4&&o.clip==expected&&std::isfinite(o.time+o.duration+o.weight)&&o.time>=0&&o.time<=duration[expected]+.05&&std::abs(o.duration-duration[expected])<=.04&&o.weight>=.99&&o.weight<=1.001;
}
bool guardGripFresh(bool confirmed,uint64_t frame,uint64_t sampledFrame){return confirmed&&sampledFrame<=frame&&frame-sampledFrame<=2;}
bool guardOperatorPackage(bool assigned,bool running,bool ownIdle,bool acquired,bool sheathed){
 // Measured on 1.6.1170 (v26 session log, 93 acquire->cancel cycles): PlayIdle's
 // run-once wrapper takes over GetRunningPackage() and high->currentProcessIdle
 // stays null the whole time (idle=00000000, runningPackage=FFxxxx), so the old
 // clause (running||ownIdle-after-acquire) was unsatisfiable on this route.
 // Post-acquisition the lease therefore tolerates the transient wrapper and the
 // owned-idle identity is arbitrated by the OAR clip-observation hook instead
 // (exact project/submod/path/duration/weight; hold timeout cancels bounded).
 return assigned&&sheathed&&(running||acquired);
}
bool guardProjectileContract(double speed,double gravity,double radius,double range,double lifetime,double proximity,double timer,double spread,bool alt,double flight){
 return std::isfinite(speed+gravity+radius+range+lifetime+proximity+timer+spread+flight)&&std::abs(speed-5400)<=.01&&std::abs(gravity-240.345)<=.1&&radius>0&&radius<=12&&flight>0&&flight<=6000./5400&&range>=flight*speed&&lifetime>=0&&(lifetime==0||lifetime>flight)&&proximity==0&&timer==0&&spread==0&&!alt;
}
std::optional<double> guardStepPhase(double previous,double clipTime,double delta,double dt){
 if(!std::isfinite(previous+clipTime+delta+dt)||previous<0||previous>1||clipTime<0||clipTime>.85||std::abs(delta)>12||dt<=0||dt>.1)return {};
 double phase=std::clamp(clipTime/.8,0.,1.);
 if(phase<previous){if(previous<.9||clipTime>.05)return {};phase=1;}
 if(std::abs(delta*(phase-previous))>15*dt+1e-5)return {};return phase;
}
std::optional<GuardProtected> guardBounds(Vec lo,Vec hi,double margin){
 if(!std::isfinite(length(lo)+length(hi)+margin)||margin<0||hi.x<=lo.x||hi.y<=lo.y||hi.z<=lo.z)return {};
 return GuardProtected{{(lo.x+hi.x)/2,(lo.y+hi.y)/2,lo.z-margin},std::hypot((hi.x-lo.x)/2,(hi.y-lo.y)/2)+margin,hi.z-lo.z+2*margin};
}
bool guardStation(uint32_t gun,uint32_t actor,uint32_t base){return base==0xB04&&((gun==0xB70&&actor==0xB71)||(gun==0xB80&&actor==0xB81));}
std::optional<double> horizontalFlight(Vec d,double speed,double gravity,double tolerance){
 if(!std::isfinite(length(d))||!std::isfinite(speed)||!std::isfinite(gravity)||!std::isfinite(tolerance)||speed<=0||gravity<=0||tolerance<0)return {};
 double t=std::hypot(d.x,d.y)/speed;if(t<=0||t>6000./speed)return {};
 return std::abs(d.z+.5*gravity*t*t)<=tolerance?std::optional<double>{t}:std::nullopt;
}
bool guardEnemy(const GuardCandidate& a){return a.hostile&&a.combat&&!a.teammate&&(!a.player||(GuardAllowPlayerTarget&&a.hunted));}
std::optional<uint32_t> selectGuardTarget(std::span<const GuardCandidate> actors,uint32_t cached,Vec origin,Mat root,Vec muzzle,bool ballistic){
 const GuardCandidate* stable=nullptr;const GuardCandidate* best=nullptr;double bestDistance=std::numeric_limits<double>::infinity();
 for(auto& a:actors){Vec d=a.position-origin;bool enemy=guardEnemy(a);
  double yaw=std::remainder(aimFromWorld(root,d).yaw,360.);
  if(!a.id||!a.loaded||!a.visible||!std::isfinite(length(d))||length(d)>(enemy?6000.:2100.)||std::abs(yaw)>60.)continue;
  if(a.resident&&!a.player&&!enemy)continue;
  // Nearby enemies may be followed visually at any visible height. Extending
  // the engagement beyond the visual radius requires a reachable shot (flat, or
  // elevated when the caller can aim: the muzzle swing is solved later).
  if(enemy&&length(d)>2100&&!(ballistic?guardAimSolution(a.position-muzzle,0,0).has_value():horizontalFlight(a.position-muzzle,5400,240.345,a.halfHeight).has_value()))continue;
  if(a.id==cached)stable=&a;
  bool bestEnemy=best&&guardEnemy(*best);
  double distance=dot(d,d);if(!best||(enemy&&!bestEnemy)||(enemy==bestEnemy&&(distance<bestDistance||(distance==bestDistance&&a.id<best->id)))){best=&a;bestDistance=distance;}
 }
 if(stable){bool stableEnemy=guardEnemy(*stable);bool bestEnemy=best&&guardEnemy(*best);if(stableEnemy||!bestEnemy)return stable->id;}
 return best?std::optional<uint32_t>{best->id}:std::nullopt;
}
std::vector<Vec> guardTrajectory(Vec muzzle,Vec bore,double seconds,double speed,double gravity){
 if(!std::isfinite(length(muzzle))||!std::isfinite(length(bore))||std::abs(length(bore)-1)>.001||std::abs(bore.z)>.001||seconds<=0||seconds>6000./speed||speed<=0||gravity<=0)return {};
 int n=int(std::ceil(seconds/.02));std::vector<Vec> result;result.reserve(n+1);for(int i=0;i<=n;++i){double t=seconds*i/n;result.push_back(muzzle+bore*(speed*t)+Vec{0,0,-.5*gravity*t*t});}return result;
}
bool guardPathSafe(std::span<const Vec> path,std::span<const GuardProtected> protectedActors,double blast){
 if(path.size()<2||path.size()>128||!std::isfinite(blast)||blast<0)return false;
 for(auto p:path)if(!std::isfinite(length(p)))return false;
 for(auto& a:protectedActors){if(!std::isfinite(length(a.feet)+a.radius+a.height)||a.radius<=0||a.height<=0)return false;
  Vec center=a.feet+Vec{0,0,a.height*.5};if(length(path.back()-center)<=blast+a.height*.5+a.radius)return false;
  for(size_t i=1;i<path.size();++i){Vec p=path[i-1]-a.feet,d=path[i]-path[i-1];double lo=0,hi=1;
   // Clip against the vertical slab first, then minimize horizontal distance
   // on that interval. A closest point to the 3D center can miss an oblique
   // segment that crosses the edge of a tall cylinder.
   if(std::abs(d.z)<1e-9){if(p.z< -12||p.z>a.height+12)continue;}
   else {double x=(-12-p.z)/d.z,y=(a.height+12-p.z)/d.z;lo=std::max(lo,std::min(x,y));hi=std::min(hi,std::max(x,y));if(lo>hi)continue;}
   double horizontal=d.x*d.x+d.y*d.y,t=horizontal>0?std::clamp(-(p.x*d.x+p.y*d.y)/horizontal,lo,hi):lo;
   if(std::hypot(p.x+d.x*t,p.y+d.y*t)<=a.radius+12)return false;}
 }return true;
}
Vec guardFoot(Vec start,Vec pivot,double delta,double phase,bool lead){
 phase=std::clamp(phase,0.,1.);Vec end=pivot+rz(rad(delta))*(start-pivot);double u=lead?std::clamp(2*phase,0.,1.):std::clamp(2*phase-1,0.,1.);double smooth=u*u*(3-2*u);return start+(end-start)*smooth+Vec{0,0,4*std::sin(std::acos(-1.)*u)};
}
std::optional<GuardLegPose> guardLeg(Vec hip,Vec knee,Vec foot,Vec target){
 double a=length(knee-hip),b=length(foot-knee),c=length(target-hip);if(!std::isfinite(a+b+c)||a<1||b<1||c<1)return {};
 if(length(target-foot)<.001)return GuardLegPose{knee};
 if(c>a+b-.001||c<std::abs(a-b)+.001)return {};
 Vec axis=(target-hip)*(1/c),bend=knee-hip-axis*dot(knee-hip,axis);double l=length(bend);if(l<.001)return {};
 double x=(a*a-b*b+c*c)/(2*c),y=std::sqrt(std::max(0.,a*a-x*x));return GuardLegPose{hip+axis*x+bend*(y/l)};
}
std::optional<double> guardTrackYaw(double yaw,double desired,double dt){
 if(!std::isfinite(yaw+desired+dt)||dt<0||std::abs(yaw)>60.001)return {};
 double step=GuardTrackRate*std::min(dt,GuardTrackMaxDt);
 return yaw+std::clamp(std::clamp(desired,-60.,60.)-yaw,-step,step);
}
std::optional<GuardAim> guardAimSolution(Vec to,double along,double up,double pitchMin,double pitchMax,double speed,double gravity){
 if(!std::isfinite(length(to)+along+up+pitchMin+pitchMax+speed+gravity)||speed<=0||gravity<=0||pitchMin>pitchMax)return {};
 const double distance=std::hypot(to.x,to.y);double pitch=0;
 for(int i=0;i<12;++i){
  // Muzzle swing: (along,up) rotated by the elevation, then range and drop measured from the muzzle.
  double c=std::cos(pitch),s=std::sin(pitch),range=distance-(along*c-up*s),drop=to.z-(along*s+up*c);
  if(range<64)return {};
  double k=gravity*range*range/(2*speed*speed),disc=range*range-4*k*(drop+k);if(disc<0)return {};
  double tangent=(range-std::sqrt(disc))/(2*k),next=std::atan(tangent);
  if(!std::isfinite(next))return {};
  bool done=std::abs(next-pitch)<1e-9;pitch=next;if(done)break;
 }
 double degrees=deg(pitch);if(degrees<pitchMin||degrees>pitchMax)return {};
 double range=distance-(along*std::cos(pitch)-up*std::sin(pitch)),seconds=range/(speed*std::cos(pitch));
 if(!std::isfinite(seconds)||seconds<=0)return {};
 return GuardAim{degrees,seconds};
}
std::optional<double> guardTrackPitch(double pitch,double desired,double dt){
 if(!std::isfinite(pitch+desired+dt)||dt<0||pitch<GuardPitchMin-.001||pitch>GuardPitchMax+.001)return {};
 double step=GuardPitchRate*std::min(dt,GuardTrackMaxDt);
 return pitch+std::clamp(std::clamp(desired,GuardPitchMin,GuardPitchMax)-pitch,-step,step);
}
std::optional<Vec> guardBore(Vec horizontal,double pitchDegrees){
 double h=std::hypot(horizontal.x,horizontal.y);if(!std::isfinite(h+pitchDegrees)||h<1e-9)return {};
 double p=rad(pitchDegrees);return Vec{horizontal.x/h*std::cos(p),horizontal.y/h*std::cos(p),std::sin(p)};
}
std::vector<Vec> guardArcTrajectory(Vec muzzle,Vec bore,double seconds,double speed,double gravity){
 if(!std::isfinite(length(muzzle)+length(bore)+seconds+speed+gravity)||std::abs(length(bore)-1)>.001||seconds<=0||seconds>6000./speed||speed<=0||gravity<=0)return {};
 int n=int(std::ceil(seconds/.02));std::vector<Vec> result;result.reserve(n+1);for(int i=0;i<=n;++i){double t=seconds*i/n;result.push_back(muzzle+bore*(speed*t)+Vec{0,0,-.5*gravity*t*t});}return result;
}
bool guardShouldFire(bool enemy,bool reachable,double yawError,double now,double nextShot){
 return enemy&&reachable&&std::isfinite(yawError+now+nextShot)&&std::abs(yawError)<=GuardAimTolerance&&now>=nextShot;
}
void GuardHoldWatch::begin(double now){since_=last_=now;seen_=-1e300;reissues_=0;}
void GuardHoldWatch::seen(double now){if(std::isfinite(now))seen_=now;}
bool GuardHoldWatch::entered(double now)const{return std::isfinite(now)&&now-since_>=GuardEnterSeconds;}
bool GuardHoldWatch::reissue(double now){
 // Samples are optional telemetry (an off-screen actor may not generate). Only a
 // clip silent for 3 s is re-requested, at most every 6 s and GuardMaxReissues times
 // per lease; it never cancels.
 if(!std::isfinite(now)||now-std::max(seen_,last_)<=3.||now-last_<6.||exhausted())return false;
 since_=last_=now;++reissues_;return true;
}
void GuardHoldWatch::restart(double now){if(std::isfinite(now))since_=last_=now;}
bool GuardHoldWatch::stale(double now)const{return std::isfinite(now)&&now-std::max(seen_,last_)>3.;}
GuardPoseWrites guardPoseWrites(Vec current,Vec desired,double currentHeading,double desiredHeading,double currentPitch){
 if(!std::isfinite(length(current)+length(desired)+currentHeading+desiredHeading+currentPitch))return {true,true};
 double turn=std::abs(std::remainder(desiredHeading-currentHeading,2*std::numbers::pi));
 return {length(desired-current)>GuardPoseEpsilonPosition,turn>GuardPoseEpsilonAngle||std::abs(currentPitch)>GuardPoseEpsilonAngle};
}
bool guardHandsHeld(double leftError,double rightError){
 // A negative error is "not measured" (hand node or grip unavailable): no evidence.
 return std::isfinite(leftError+rightError)&&leftError>=0&&rightError>=0&&leftError<=GuardHeldHandError&&rightError<=GuardHeldHandError;
}
bool GuardLease::begin(Key key,uint32_t actor){if(owner_||effects_||pending_||!key.handle||key.token<=0||!actor)return false;owner_={key,++epoch_};actor_=actor;return true;}
std::optional<double> guardOrbit(Vec feet,Vec gun,Mat root,Vec facing,double scale){
 if(!finite({root,gun,scale})||std::abs(scale-1)>.001||!std::isfinite(length(feet)+length(facing))||std::abs(root.m[8]-1)>.001)return {};
 // A free NPC's heading is not owned yet. Acquisition sets it after support
 // validation, rather than requiring the vanilla AI to face the bore first.
 Vec local=root.transpose()*(feet-gun);double yaw=deg(std::atan2(-local.x,local.y));if(std::abs(yaw)>60.001||std::abs(std::hypot(local.x,local.y)-151)>2||std::abs(local.z)>8)return {};return yaw;
}
bool guardSupport(double feetZ,double floorZ,double normalZ,std::optional<double> savedFloor){
 if(!std::isfinite(feetZ+floorZ+normalZ)||(savedFloor&&!std::isfinite(*savedFloor)))return false;
 double gap=feetZ-floorZ;
 return normalZ>=.7&&normalZ<=1.001&&gap>=-2&&gap<=8&&(!savedFloor||std::abs(floorZ-*savedFloor)<=2);
}
int guardClipKind(std::string_view pathIn,std::string_view modIn,std::string_view subIn){
 auto normalize=[](std::string_view input){std::string s(input);std::transform(s.begin(),s.end(),s.begin(),[](unsigned char c){return char(std::tolower(c));});std::replace(s.begin(),s.end(),'\\','/');return s;};
 auto path=normalize(pathIn),mod=normalize(modIn),sub=normalize(subIn);if(mod!="astraasedio guard")return -1;
 constexpr std::array<std::string_view,4> folders{"operate","fire","turnleft","turnright"};
 for(int i=0;i<4;++i){std::string expected="animations/openanimationreplacer/astraasedioguard/"+std::string(folders[i])+"/";
  if(sub!="astra guard "+std::string(folders[i]))continue;
  if(path.ends_with(expected+"idlehandsbehindback.hkx")||path.ends_with(expected+"idlehandsbehindback_enter.hkx"))return i;
 }return -1;
}
bool GuardLease::current(Ticket t)const{return t&&owner_.epoch==t.epoch&&owner_.key==t.key&&!pending_;}
bool GuardLease::complete(){if(!pending_||effects_)return false;owner_={};actor_=0;pending_=false;return true;}
bool GuardCycle::acquire(double now){if(!std::isfinite(now))return false;acquired_=true;interrupt();holdTime_=now;return true;}
bool GuardCycle::observeHold(double now,double phase){if(!acquired_||firing_||!std::isfinite(now+phase)||phase<0||phase>2.05)return false;
 if(holdSample_>=0&&now>holdTime_&&phase!=holdSample_&&now-holdTime_<.25)ready_=true;holdSample_=phase;holdTime_=now;return true;}
bool GuardCycle::startFire(double now){if(!ready_||firing_||!std::isfinite(now)||now<nextFire_)return false;ready_=false;firing_=true;released_=false;fireStart_=now;nextFire_=now+2.5;return true;}
bool GuardCycle::synchronizeFire(double now,double phase){if(!firing_||released_||!std::isfinite(now+phase)||phase<0||phase>.05||now-phase<fireStart_-.01||now-fireStart_>.25)return false;fireStart_=now-phase;nextFire_=fireStart_+2.5;return true;}
bool GuardCycle::release(double now,double bodyTime,bool safe){if(!firing_||released_||!safe||!std::isfinite(now+bodyTime)||bodyTime<2./30.||bodyTime>2./30.+.05||std::abs((now-fireStart_)-bodyTime)>.05)return false;released_=true;return true;}
void GuardCycle::interrupt(){ready_=false;firing_=false;released_=false;holdSample_=-1;}
}
