#include "Astra/GuardPolicy.h"
#include <cmath>
#include <iostream>
#include <limits>
using namespace Astra;
// Integrate the parabola independently of guardArcTrajectory: where is the bolt when it is at the target's range?
static Vec flyTo(Vec muzzle,double pitchDegrees,Vec heading,double range){
 auto bore=guardBore(heading,pitchDegrees);double t=range/(GuardProjectileSpeed*std::cos(rad(pitchDegrees)));
 return muzzle+*bore*(GuardProjectileSpeed*t)+Vec{0,0,-.5*GuardProjectileGravity*t*t};
}
int main(){int n=0,fail=0;auto check=[&](bool ok){++n;if(!ok){++fail;std::cerr<<"case "<<n<<" failed\n";}};
 const double nan=std::numeric_limits<double>::quiet_NaN();
 // The solved pitch puts the bolt on the target, for targets below, level and above, near and far, with a muzzle lever.
 struct Case{Vec to;double along,up;};
 for(auto c:{Case{{0,-1200,-600},224,20},Case{{0,-3000,-600},224,20},Case{{0,-5000,-600},224,20},Case{{0,-2000,0},224,20},Case{{0,-2000,300},224,20},Case{{1500,-1500,-400},0,0},Case{{0,-800,-200},224,20}}){
  auto aim=guardAimSolution(c.to,c.along,c.up);check(aim.has_value());if(!aim)continue;
  double p=rad(aim->pitch),range=std::hypot(c.to.x,c.to.y)-(c.along*std::cos(p)-c.up*std::sin(p));
  Vec heading{c.to.x,c.to.y,0},pivot{0,0,0};
  Vec muzzle=pivot+Vec{c.to.x,c.to.y,0}*(1/std::hypot(c.to.x,c.to.y))*(c.along*std::cos(p)-c.up*std::sin(p))+Vec{0,0,c.along*std::sin(p)+c.up*std::cos(p)};
  Vec hit=flyTo(muzzle,aim->pitch,heading,range);
  check(length(hit-c.to)<1.);                                                   // less than a unit off the aim point
  check(std::abs(aim->seconds-range/(GuardProjectileSpeed*std::cos(p)))<1e-9);
 }
 // Low arc: never the lob solution.
 auto flat=guardAimSolution({0,-3000,0},0,0);check(flat&&flat->pitch>0&&flat->pitch<5);
 // Limits and reach are enforced, not clamped.
 check(!guardAimSolution({0,-3000,3000},0,0));                                    // needs ~45 deg
 check(!guardAimSolution({0,-3000,-3000},0,0));                                   // below -30
 check(guardAimSolution({0,-3000,3000},0,0,-30,60).has_value());
 check(!guardAimSolution({0,-30,0},0,0));                                         // inside the muzzle
 check(!guardAimSolution({0,-9000,0},0,0,-30,30,5400,240.345)||guardAimSolution({0,-9000,0},0,0)->pitch>0);
 check(!guardAimSolution({0,-1e6,0},0,0));                                        // beyond the parabola's reach
 for(auto bad:{Vec{nan,-1000,0},Vec{0,nan,0},Vec{0,-1000,nan}})check(!guardAimSolution(bad,0,0));
 check(!guardAimSolution({0,-1000,0},nan,0)&&!guardAimSolution({0,-1000,0},0,0,30,-30)&&!guardAimSolution({0,-1000,0},0,0,-30,30,0,240)&&!guardAimSolution({0,-1000,0},0,0,-30,30,5400,0));
 // Pitch tracking: rate limited, clamped to the range, hitches do not jump, bad input refuses.
 check(std::abs(*guardTrackPitch(0,20,.05)-GuardPitchRate*.05)<1e-9);
 check(std::abs(*guardTrackPitch(0,20,5)-GuardPitchRate*GuardTrackMaxDt)<1e-9);
 check(std::abs(*guardTrackPitch(10,-50,.05)-(10-GuardPitchRate*.05))<1e-9);
 check(std::abs(*guardTrackPitch(29.9,80,.05)-30.)<1e-9);                         // never past the limit
 check(*guardTrackPitch(5,5,.05)==5&&*guardTrackPitch(5,5,0)==5);
 check(!guardTrackPitch(31,0,.05)&&!guardTrackPitch(nan,0,.05)&&!guardTrackPitch(0,nan,.05)&&!guardTrackPitch(0,0,-1));
 // Bore: unit, matches gunDirection's heading convention, refuses a vertical or non-finite heading.
 auto bore=guardBore({3,4,99},30);check(bore&&std::abs(length(*bore)-1)<1e-12&&std::abs(bore->z-.5)<1e-12&&std::abs(bore->x/bore->y-.75)<1e-12);
 check(!guardBore({0,0,1},10)&&!guardBore({nan,1,0},10)&&!guardBore({1,0,0},nan));
 // Arc trajectory: starts at the muzzle, the flat case equals guardTrajectory, rejects non-unit bores.
 auto arc=guardArcTrajectory({1,2,3},{0,1,0},.4,5400,240.345);auto flatArc=guardTrajectory({1,2,3},{0,1,0},.4,5400,240.345);
 check(arc.size()==flatArc.size()&&!arc.empty()&&length(arc.front()-Vec{1,2,3})<1e-12&&length(arc.back()-flatArc.back())<1e-9);
 check(guardArcTrajectory({0,0,0},{0,.8,.6},.5,5400,240.345).size()>2);
 check(guardArcTrajectory({0,0,0},{0,2,0},.5,5400,240.345).empty()&&guardArcTrajectory({0,0,0},{0,1,0},0,5400,240.345).empty()&&guardArcTrajectory({0,0,0},{0,1,0},9,5400,240.345).empty());
 // Player as a target: only when the town guards are fighting them, and only through the policy switch.
 GuardCandidate player{1,{0,-300,0},true,true,true,true,true,false};                // hostile+combat but not "hunted"
 check(!guardEnemy(player));
 player.hunted=true;check(guardEnemy(player)==GuardAllowPlayerTarget);
 GuardCandidate mate=player;mate.teammate=true;check(!guardEnemy(mate));
 GuardCandidate bandit{9,{0,-1000,0},true,true,true,true,false,false};check(guardEnemy(bandit));
 bandit.hunted=true;check(guardEnemy(bandit));                                      // `hunted` is irrelevant for NPCs
 GuardCandidate calm{2,{0,-600,0},true,true,false,false,false,false};check(!guardEnemy(calm));
 // A hunted player outranks a nearer neutral and is selected like any enemy, but a calm player is still only followed.
 std::array both{calm,player};check(selectGuardTarget(both,0,{},Mat{},{0,0,136.6}).value_or(0)==1);
 player.hunted=false;std::array calmPlayer{player};check(selectGuardTarget(calmPlayer,0,{},Mat{},{0,0,136.6}).value_or(0)==1);
 GuardCandidate farPlayer{1,{0,-4000,0},true,true,true,true,true,false,90,false,false};std::array far{farPlayer};
 check(!selectGuardTarget(far,0,{},Mat{},{0,0,136.6}));                              // not hunted: no engagement past 2100 u
 // Ballistic reach extends the engagement of enemies that a flat shot cannot hit.
 GuardCandidate high{5,{0,-4000,700},true,true,true,true,false,false,90};std::array highs{high};
 check(!selectGuardTarget(highs,0,{},Mat{},{0,0,136.6}));                           // v25 behaviour kept by default
 check(selectGuardTarget(highs,0,{},Mat{},{0,0,136.6},true).value_or(0)==5);
 GuardCandidate unreachable{6,{0,-4000,5000},true,true,true,true,false,false,90};std::array nope{unreachable};
 check(!selectGuardTarget(nope,0,{},Mat{},{0,0,136.6},true));
 std::cout<<n<<" v29.2 aim assertions "<<fail<<" failures\n";return fail?1:0;}
