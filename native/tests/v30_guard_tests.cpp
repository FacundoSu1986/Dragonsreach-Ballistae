#include "Astra/GuardPolicy.h"
#include <cmath>
#include <iostream>
#include <limits>
using namespace Astra;
int main(){int n=0,fail=0;auto check=[&](bool ok){++n;if(!ok){++fail;std::cerr<<"case "<<n<<" failed\n";}};
 // A blocked placement may recover for two seconds, but cannot authorize a shot.
 check(!guardShouldFire(true,true,0,10,9,false));
 check(guardShouldFire(true,true,0,10,9,true));
 check(!guardShouldFire(false,true,0,10,9,true));
 check(!guardShouldFire(true,false,0,10,9,true));
 check(!guardShouldFire(true,true,1,10,9,true));
 check(!guardShouldFire(true,true,0,8,9,true));
 // A dialogue suppresses new actions without stopping an existing Fire/Reset.
 double elapsed=0;bool actions=false;
 for(int i=0;i<100;++i){auto frame=guardFrame(false,true,.01);elapsed+=frame.elapsed;actions=actions||frame.actions;}
 check(std::abs(elapsed-1)<1e-9);check(!actions);
 for(bool menu:{false,true}){auto frame=guardFrame(true,menu,.1);check(frame.elapsed==0);check(!frame.actions);}
 auto active=guardFrame(false,false,.02);check(active.elapsed==.02);check(active.actions);
 for(double dt:{0.,-1.,std::numeric_limits<double>::quiet_NaN(),std::numeric_limits<double>::infinity()}){
  auto invalid=guardFrame(false,false,dt);check(invalid.elapsed==0);check(!invalid.actions);
 }
 check(guardFrame(false,false,2).elapsed==.25);
 std::cout<<n<<" v30 assertions "<<fail<<" failures\n";return fail?1:0;
}
