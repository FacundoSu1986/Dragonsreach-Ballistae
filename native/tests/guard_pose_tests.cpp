#include "Astra/GuardPolicy.h"
#include <cmath>
#include <iostream>
#include <limits>
#include <numbers>
using namespace Astra;
int main(){int n=0,fail=0;auto check=[&](bool ok){++n;if(!ok){++fail;std::cerr<<"case "<<n<<" failed\n";}};
 const double nan=std::numeric_limits<double>::quiet_NaN(),pi=std::numbers::pi;
 const Vec at{18400,-6300,-3636.2};
 // Write only on change: a held pose with a stationary target writes nothing.
 auto idleWrites=guardPoseWrites(at,at,1.2,1.2,0);
 check(!idleWrites.position&&!idleWrites.rotation);
 auto floatNoise=guardPoseWrites(at,at+Vec{.004,-.003,.002},1.2,1.2+2e-7,0);   // float32 round-trip of GetPosition/GetAngleZ
 check(!floatNoise.position&&!floatNoise.rotation);
 auto edge=guardPoseWrites(at,at+Vec{.05,0,0},1.2,1.2,0);                      // exactly at the epsilon: still no write
 check(!edge.position);
 auto moved=guardPoseWrites(at,at+Vec{.06,0,0},1.2,1.2,0);
 check(moved.position&&!moved.rotation);
 auto tracking=guardPoseWrites(at,at+Vec{0,.88,0},1.2,1.2+.0058,0);            // 20 deg/s * 0.05 s on the 151 u orbit
 check(tracking.position&&tracking.rotation);
 auto turned=guardPoseWrites(at,at,1.2,1.2+.0011,0);
 check(!turned.position&&turned.rotation);
 auto tilted=guardPoseWrites(at,at,1.2,1.2,.01);                                // pitch must be levelled once
 check(!tilted.position&&tilted.rotation);
 // Headings compare modulo a full turn: 3.1415 and -3.1415 are the same bearing.
 auto wrapped=guardPoseWrites(at,at,pi-1e-4,-pi+1e-4,0);
 check(!wrapped.rotation);
 auto wrappedFar=guardPoseWrites(at,at,pi-1e-4,-pi+2e-3,0);
 check(wrappedFar.rotation);
 auto zeroWrap=guardPoseWrites(at,at,2*pi-1e-4,1e-4,0);
 check(!zeroWrap.rotation);
 // Unknown inputs fail towards writing (the previous behaviour), never towards silence.
 for(auto w:{guardPoseWrites(Vec{nan,0,0},at,0,0,0),guardPoseWrites(at,Vec{0,nan,0},0,0,0),guardPoseWrites(at,at,nan,0,0),guardPoseWrites(at,at,0,nan,0),guardPoseWrites(at,at,0,0,nan)})check(w.position&&w.rotation);
 // Held evidence: both wrists measured and close to their grips.
 check(guardHandsHeld(3,3.4));
 check(guardHandsHeld(12,12));
 check(!guardHandsHeld(12.1,3));
 check(!guardHandsHeld(3,29));                                                  // blend start was ~29 u
 check(!guardHandsHeld(-1,3));                                                  // hand node not found: no evidence
 check(!guardHandsHeld(3,-1));
 check(!guardHandsHeld(nan,3));
 check(!guardHandsHeld(3,std::numeric_limits<double>::infinity()));
 // Re-requests are capped per lease; held evidence and a fresh lease reset nothing but the budget.
 GuardHoldWatch w;w.begin(0);
 check(!w.exhausted()&&w.reissues()==0);
 check(w.reissue(6.1));check(w.reissues()==1);
 check(w.reissue(12.2));check(w.reissues()==2);
 check(w.reissue(18.3));check(w.reissues()==3);
 check(w.exhausted());
 check(!w.reissue(100));                                                        // budget spent: keep the pose, do not cycle forever
 check(w.stale(100));                                                           // ...but the watch can still report it as unresolved
 w.begin(200);
 check(!w.exhausted()&&w.reissues()==0&&!w.stale(201));                         // new lease, new budget
 // Held evidence silences the watch exactly like an OAR sample.
 GuardHoldWatch held;held.begin(0);
 bool quiet=true;for(int i=0;i<400;++i){double t=.1*i;if(guardHandsHeld(3,3))held.seen(t);quiet=quiet&&!held.reissue(t);}
 check(quiet&&held.reissues()==0&&!held.stale(39.9));
 // Two-phase re-request: the entry blend restarts when the idle is actually played, after the delay.
 GuardHoldWatch two;two.begin(0);
 check(two.reissue(6.1));                                                       // step 1: IdleForceDefaultState
 check(!two.entered(6.1+GuardReplayDelay+.1));                                  // not in the hold yet
 two.restart(6.1+GuardReplayDelay);                                             // step 2: PlayIdle
 check(!two.entered(6.1+GuardReplayDelay+GuardEnterSeconds-.05));
 check(two.entered(6.1+GuardReplayDelay+GuardEnterSeconds+.01));
 check(!two.reissue(6.1+GuardReplayDelay+5.9));                                 // 6 s spacing counts from the PlayIdle
 two.restart(nan);                                                              // a bad clock changes nothing
 check(two.entered(6.1+GuardReplayDelay+GuardEnterSeconds+.01));
 check(GuardReplayDelay>=.2&&GuardReplayDelay<GuardEnterSeconds);               // longer than the 0.2 s vanilla exit blend
 std::cout<<n<<" v29.1 pose assertions "<<fail<<" failures\n";return fail?1:0;}
