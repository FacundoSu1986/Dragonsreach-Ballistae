#include "Astra/GuardPolicy.h"
#include <cmath>
#include <iostream>
#include <limits>
using namespace Astra;
int main(){int n=0,fail=0;auto check=[&](bool ok){++n;if(!ok){++fail;std::cerr<<"case "<<n<<" failed\n";}};
 auto near=[](std::optional<double> v,double e){return v&&std::abs(*v-e)<1e-9;};
 const double nan=std::numeric_limits<double>::quiet_NaN();
 // Tracking: rate-limited toward the desired yaw, inside the +-60 degree mount.
 check(near(guardTrackYaw(0,10,.05),1));        // 20 deg/s * 0.05 s
 check(near(guardTrackYaw(0,-10,.05),-1));
 check(near(guardTrackYaw(9.5,10,.05),10));     // reaches the target exactly, no overshoot
 check(near(guardTrackYaw(0,10,.5),1));         // a hitch frame is clamped to 0.05 s
 check(near(guardTrackYaw(59.5,90,.05),60));    // sector clamp
 check(near(guardTrackYaw(-59.5,-90,.05),-60));
 check(near(guardTrackYaw(5,5,.05),5));
 check(near(guardTrackYaw(5,7,0),5));           // a paused frame does not move the mount
 check(!guardTrackYaw(nan,0,.05));
 check(!guardTrackYaw(0,nan,.05));
 check(!guardTrackYaw(0,0,nan));
 check(!guardTrackYaw(0,0,-.01));
 check(!guardTrackYaw(61,0,.05));               // current yaw outside the mount
 // Hold watch: enter after the vanilla 0.5 s blend; reissue only when samples stop, rate limited.
 GuardHoldWatch w;w.begin(10);
 check(!w.entered(10.5));check(w.entered(10.61));
 check(!w.reissue(12.9));                       // 3 s grace after the request
 check(!w.reissue(15.9));                       // ... and 6 s between requests
 check(w.reissue(16.1));                        // stale and spaced: exactly one reissue
 check(!w.reissue(16.2));
 w.seen(17);
 check(!w.reissue(19.9));                       // fresh sample restarts the grace
 check(!w.reissue(20.5));                       // stale again but only 4.4 s since the reissue
 check(w.reissue(22.2));
 check(!w.entered(22.5));                       // a reissue replays the entry blend
 check(w.entered(22.9));
 GuardHoldWatch v;v.begin(0);bool quiet=true;
 for(int i=0;i<600;++i){double t=.1*i;v.seen(t);quiet=quiet&&!v.reissue(t);}
 check(quiet);                                  // a healthy clip is never re-requested
 GuardHoldWatch u;u.begin(0);check(!u.reissue(nan));u.seen(nan);check(!u.reissue(3.5));check(u.reissue(6));
 // Fire decision: hostile, reachable, aligned and cooled down. Never on a NaN error.
 check(guardShouldFire(true,true,.2,10,9));
 check(guardShouldFire(true,true,-.25,10,10));
 check(!guardShouldFire(false,true,0,10,9));
 check(!guardShouldFire(true,false,0,10,9));
 check(!guardShouldFire(true,true,.3,10,9));
 check(!guardShouldFire(true,true,0,8.9,9));
 check(!guardShouldFire(true,true,nan,10,9));
 check(!guardShouldFire(true,true,0,nan,9));
 std::cout<<n<<" v29 assertions "<<fail<<" failures\n";return fail?1:0;}
