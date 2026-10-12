#include "Astra/GuardPolicy.h"
#include <iostream>
using namespace Astra;
int main(){
 int checks=0,failures=0;auto check=[&](bool value,const char* text){++checks;if(!value){++failures;std::cerr<<text<<'\n';}};
 check(guardNaturalScale(1,1.03,1.03),"real v24 Nord scale1.03 at reference1 must acquire");
 check(guardNaturalScale(1,1,1),"unit natural actor remains valid");
 check(!guardNaturalScale(1.03,1.0609,1.03),"intentional reference resizing remains outside mounted contract");
 check(!guardNaturalScale(1,1.03,1),"unexplained effective scale is not treated as race height");
 check(!guardNaturalScale(1,NAN,1.03)&&!guardNaturalScale(1,1.03,NAN),"unknown scale cannot certify geometry");
 auto left=guardGrip({},Mat{},0,true),right=guardGrip({},Mat{},0,false);
 check(left&&length(*left-Vec{33.6,143.8,100.5})<.00001,"left hand matches approved physical handle");
 check(right&&length(*right-Vec{-33.6,143.8,100.5})<.00001,"right hand matches approved physical handle");
 for(double yaw:std::array{-60.,0.,60.}){
  auto actual=guardGrip({100,200,300},rz(rad(30)),yaw,true);
  Vec expected={100,200,300};expected=expected+rz(rad(30+yaw))*Vec{33.6,143.8,100.5};
  check(actual&&length(*actual-expected)<.00001,"hand stays attached throughout horizontal station rotation");
 }
 auto trigger=guardGrip({},Mat{},0,false,2./30.);
 check(trigger&&length(*trigger-Vec{-33.6,143.05,99.7})<.00001,"Fire trigger displacement agrees with observed release phase");
 auto reset=guardGrip({},Mat{},0,false,1);
 check(reset&&right&&length(*reset-*right)<.00001,"Fire returns right hand to canonical handle");
 check(!guardGrip({},Mat{},61,true)&&!guardGrip({},Mat{},0,false,NAN),"invalid pose cannot move a hand");
 check(!guardGripFresh(false,100,100),"PlayIdle request alone does not prove physical grip");
 check(guardGripFresh(true,102,100),"recent observed canonical grip is usable");
 check(!guardGripFresh(true,103,100)&&!guardGripFresh(true,99,100),"stale or future grip cannot authorize launch");
 GuardCandidate resident{2,{0,-200,80},true,true,false,false,false,false,80,true};
 GuardCandidate visitor{3,{0,-600,80},true,true,false,false,false,false,80,false};
 std::array candidates{resident,visitor};
 check(selectGuardTarget(candidates,2,{},Mat{},{0,0,136.6}).value_or(0)==3,"cached local does not displace an eligible visitor");
 candidates[0].hostile=true;candidates[0].combat=true;
 check(selectGuardTarget(candidates,3,{},Mat{},{0,0,136.6}).value_or(0)==2,"hostile local in combat has enemy priority");
 candidates[0].position.z=400;
 check(selectGuardTarget(candidates,3,{},Mat{},{0,0,136.6}).value_or(0)==2,"near enemy can be visually tracked above the horizontal firing line");
 check(!horizontalFlight(candidates[0].position-Vec{0,0,136.6},5400,240.345,80),"visual enemy tracking still cannot authorize an elevated launch");
 candidates[0].position.y=-3000;
 check(selectGuardTarget(candidates,2,{},Mat{},{0,0,136.6}).value_or(0)==3,"unreachable enemy beyond visual radius cannot extend engagement range");
 candidates[0].position={0,-300,80};candidates[0].player=true;
 check(selectGuardTarget(candidates,3,{},Mat{},{0,0,136.6}).value_or(0)==3,"cached valid visitor remains stable when protected player enters");
 candidates[1].visible=false;
 check(selectGuardTarget(candidates,3,{},Mat{},{0,0,136.6}).value_or(0)==2,"player remains visual target even with a local faction tag");
 std::cout<<checks<<" v25 assertions "<<failures<<" failures\n";return failures?1:0;
}
