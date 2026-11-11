#include "Astra/FastShot.h"
#include <iostream>
#include <limits>
using namespace Astra;
int main(){
 int checks=0,failures=0;
 auto check=[&](bool x,const char* s){++checks;if(!x){++failures;std::cerr<<s<<'\n';}};
 // Actual v17 engine: full PROJ speed 5400, clamped draw power .35,
 // weapon factor .4, speedMult 1; deferred init replaced the impulse by 756.
 auto mult=speedMultiplierCorrection(5400,756,1);
 check(mult&&std::abs(*mult-1./(.35*.4))<1e-5,"actual v17 speed mismatch");
 check(mult&&std::abs(5400*.35*.4*(*mult)-5400)<1e-4,"deferred init retains the mounted speed");
 auto normal=speedMultiplierCorrection(5400,5400,1);check(normal&&*normal==1,"normal shot unchanged");
 auto modded=speedMultiplierCorrection(8000,3200,2);check(modded&&*modded==5,"own PROJ overrides honored");
 for(double x:{0.,-1.,std::numeric_limits<double>::infinity(),std::numeric_limits<double>::quiet_NaN()}){
  check(!speedMultiplierCorrection(5400,x,1),"bad measured speed rejected");
  check(!speedMultiplierCorrection(x,756,1),"bad base speed rejected");
  check(!speedMultiplierCorrection(5400,756,x),"bad multiplier rejected");
 }
 std::cout<<checks<<" v18 assertions "<<failures<<" failures\n";return failures?1:0;
}
