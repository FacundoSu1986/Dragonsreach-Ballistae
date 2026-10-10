#include "Astra/FastShot.h"
#include <iostream>
#include <limits>
using namespace Astra;
int main(){
 int checks=0,failures=0;
 auto check=[&](bool ok,const char* message){++checks;if(!ok){++failures;std::cerr<<message<<'\n';}};
 for(double pitch:{-20.,0.,80.}){
  Vec bore=gunDirection(35,pitch);auto v=muzzleVelocity(bore*2.5,5400);
  check(bool(v),"valid muzzle");
  check(v&&std::abs(length(*v)-5400)<1e-6,"projectile data speed independent of draw state");
  check(v&&dot(*v,bore)>5399.99,"direction matches bore, including depression");
 }
 check(!muzzleVelocity({},5400),"zero direction");
 for(double s:{0.,-1.,std::numeric_limits<double>::infinity(),std::numeric_limits<double>::quiet_NaN()})
  check(!muzzleVelocity({0,1,0},s),"invalid speed rejected before ammo consumption");
 check(!muzzleVelocity({0,std::numeric_limits<double>::quiet_NaN(),0},5400),"invalid direction rejected");
 std::cout<<checks<<" v17 assertions "<<failures<<" failures\n";return failures?1:0;
}
