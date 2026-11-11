#include "Astra/Core.h"
#include <cmath>
#include <iostream>
using namespace Astra;
// v09: the yaw Papyrus receives, and the hysteresis watch that records the rendered camera.
int main(){
 int checks=0,failures=0; auto check=[&](bool ok,const char* name){++checks;if(!ok){++failures;std::cerr<<name<<'\n';}};
 // 07:30:03 in reports/user_evidence_v08.json: heading float(pi) > pi gives this native yaw.
 double h=static_cast<float>(rad(180.0));
 double sampled=wrapDegrees(deg(std::atan2(std::sin(h),-std::cos(h))));
 check(sampled<360.0&&static_cast<float>(sampled)==360.f,"the v08 sample rounds to float 360 (the reproduced fault)");
 check(papyrusYaw(sampled)==0.f,"papyrusYaw hands that sample to Papyrus as 0");
 for(double y:{0.,1e-9,0.5,90.,179.999,180.,270.25,359.99,359.999999,360.,-1e-9,-90.,720.5}){
  float p=papyrusYaw(y);
  check(p>=0.f&&p<360.f,"papyrusYaw is always in [0,360) as float");
  double d=std::abs(std::remainder(double(p)-y,360.));
  check(d<1e-4,"papyrusYaw keeps the direction");
 }
 CameraWatch w;
 check(w.observe(1.9,0).kind==WatchEvent::kNone&&!w.deviating(),"below the start threshold nothing is reported");
 auto s=w.observe(150.,1.);
 check(s.kind==WatchEvent::kStart&&w.deviating()&&s.deviation==150.,"a jump to the player eye starts a deviation");
 check(w.observe(149.,1.2).kind==WatchEvent::kNone,"no repeat inside half a second");
 auto o=w.observe(160.,1.6);
 check(o.kind==WatchEvent::kOngoing&&o.maxDeviation==160.&&std::abs(o.seconds-.6)<1e-12,"ongoing reports max and duration");
 check(w.observe(1.5,1.7).kind==WatchEvent::kNone&&w.deviating(),"hysteresis: 1.5 u does not end it");
 auto e=w.observe(.2,2.);
 check(e.kind==WatchEvent::kEnd&&!w.deviating()&&e.maxDeviation==160.&&std::abs(e.seconds-1.)<1e-12,"returning under 1 u ends it with max and duration");
 check(w.observe(NAN,3.).kind==WatchEvent::kNone&&w.observe(3.,INFINITY).kind==WatchEvent::kNone,"non-finite input is ignored");
 auto again=w.observe(5.,4.);
 check(again.kind==WatchEvent::kStart&&again.maxDeviation==5.,"a new deviation starts with a fresh maximum");
 w.reset();check(!w.deviating()&&w.observe(.5,5.).kind==WatchEvent::kNone,"reset clears the state");
 // v09: a menu camera suspends the sight; the lease, readiness and a frozen shot survive (07:32:21 in the v08 log).
 Session sess;Key k{77,5};
 check(sess.begin(k,0,0),"begin");
 Ticket t=sess.ticket();
 auto apply=[](Aim a)->Snapshot{Snapshot n;n.aim=a;n.valid=true;n.camera=Transform{};n.worldCamera=Transform{};n.poseValid=true;return n;};
 check(sess.update(t,{0,0},false,apply,true)&&sess.ready(k),"first update publishes");
 check(sess.capture(k,true).has_value(),"a shot freezes");
 check(sess.suspend(t)&&sess.suspended(),"leaving first person suspends");
 check(!sess.suspend(t),"a second suspend is not new");
 check(sess.ticket().epoch==t.epoch&&sess.ready(k),"suspension keeps the lease and readiness");
 check(sess.freeze(k,false),"the frozen shot can still be thawed while suspended");
 check(sess.capture(k,false).has_value(),"the last pose is still readable");
 check(sess.update(t,{0,0},false,apply,true)&&!sess.suspended(),"the next first-person update resumes");
 Ticket stale{k,t.epoch+7};
 check(!sess.suspend(stale)&&!sess.suspended(),"a stale ticket cannot suspend");
 check(sess.suspend(t),"suspend again");sess.invalidate();
 check(!sess.suspended()&&!sess.ready(k)&&!sess.ticket(),"invalidation clears the suspension");
 check(sess.begin(k,0,0)&&!sess.suspended(),"a new lease starts unsuspended");
 check(sess.suspend(sess.ticket())&&sess.end(k)&&!sess.suspended(),"EndSight clears the suspension");
 std::cout<<(failures?"FAILED ":"PASS ")<<checks<<" v09 assertions, "<<failures<<" failures\n";return failures?1:0;
}
