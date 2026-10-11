#include "Astra/GuardPolicy.h"
#include <iostream>
#include <limits>
using namespace Astra;
int main(){int n=0,fail=0;auto check=[&](bool ok){++n;if(!ok){++fail;std::cerr<<"case "<<n<<" failed\n";}};
 GuardPoseSample o{1,42,100,1234,0,.5,2,1};
 check(guardPoseFresh(o,42,1234,101,0)); // Works without any Character callback input.
 check(!guardPoseFresh(o,43,1234,101,0));
 check(!guardPoseFresh(o,42,5678,101,0));
 check(!guardPoseFresh(o,42,1234,103,0));
 check(!guardPoseFresh(o,42,1234,99,0));
 check(!guardPoseFresh(o,42,1234,101,1));
 check(!guardPoseFresh(o,42,1234,101,4));
 auto bad=o;bad.serial=0;check(!guardPoseFresh(bad,42,1234,101,0));
 bad=o;bad.duration=1;check(!guardPoseFresh(bad,42,1234,101,0));
 bad=o;bad.weight=.5;check(!guardPoseFresh(bad,42,1234,101,0));
 bad=o;bad.time=std::numeric_limits<double>::quiet_NaN();check(!guardPoseFresh(bad,42,1234,101,0));
 check(!guardGripFresh(false,101,101)); // Request/cancel invalidation vetoes fire.
 o.clip=1;o.duration=1;o.time=2./30.;check(guardPoseFresh(o,42,1234,101,1));
 check(!guardGripFresh(true,105,101));
 std::cout<<n<<" v28 assertions "<<fail<<" failures\n";return fail?1:0;}
