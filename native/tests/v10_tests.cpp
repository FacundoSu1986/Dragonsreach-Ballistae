#include "Astra/Core.h"
#include <cmath>
#include <iostream>
using namespace Astra;
// v10: tail camera on the rear-sight -> 75 m zero line (user choice 2026-10-05), front post on that line.
// Geometry of the packaged NIF: pitch pivot 153 u above the root, rear sight (anchor) (0,80,40), muzzle
// (0,-224,19.6), bore local -Y; pitch node = translate(0,0,153) * rz(yaw) * rx(-elevation).
int main(){
 int checks=0,failures=0; auto check=[&](bool ok,const char* name){++checks;if(!ok){++failures;std::cerr<<name<<'\n';}};
 auto pivot=Vec{0,0,153};
 for(double scale:{1.,2.})for(double yaw:{0.,90.,179.,180.,240.,359.}){
  double previous=1e9;
  for(double elevation:{-20.,-15.,-10.,-5.,0.,10.,20.,35.,45.,60.,70.,80.}){
   Mat frame=rz(rad(yaw))*rx(rad(-elevation));
   auto world=[&](Vec local){return (pivot+frame*local)*scale;};
   Vec rear=world({0,80,40}),muzzle=world({0,-224,19.6});
   Vec bore=frame*Vec{0,-1,0},right=frame*Vec{-1,0,0};
   auto p=sightPose(rear,right,muzzle,bore,{0,0,0},{0,0,1},scale);
   check(p.valid,"pose valid");
   Vec toPost=p.frontPost-p.camera,toTarget=p.target-p.camera;
   check(length(cross(toPost*(1/length(toPost)),toTarget*(1/length(toTarget))))<1e-9,"camera, front post and zero target are collinear");
   check(length(cross(p.forward,(rear-p.camera)))<1e-6*scale+1e-9||p.distance<1e-9,"the rear sight is on the camera line");
   // The bolt flies in world units: the zero (5250 u, 113.589 u drop) does not scale with the model.
   Vec drop=muzzle+bore*5250-p.target;
   check(std::abs(drop.z-113.589)<1e-6&&std::abs(drop.x)<1e-9&&std::abs(drop.y)<1e-9,"zero target is the 75 m bolt position, gravity straight down, unscaled");
   check(p.distance<=120*scale+1e-9&&p.distance>=-1e-12,"camera between the rear sight and the tail");
   check(p.camera.z>=65*scale-1e-6||std::abs(p.distance-120*scale)<1e-9,"camera never below 65 u above the root while it slides");
   check(p.distance<=previous+1e-9,"the camera only slides forward as elevation rises");previous=p.distance;
   Mat r=p.rotation();check(matrixNear(r.transpose()*r,Mat{}),"camera rotation is orthonormal");
   check(std::abs(dot(p.forward,bore))>0.999,"view stays within the zero angle of the bore");
   check(dot(p.up,{0,0,1})>0,"camera keeps the weapon roll (up stays up)");
   Vec postLocal=frame.transpose()*(p.frontPost*(1/scale)-pivot);
   check(std::abs(postLocal.y+150)<1e-6&&std::abs(postLocal.x)<1e-9,"front post stays at local y -150 on the centreline");
   if(scale==1.){
    // Golden values shared with tests/test_v10_sight.py (scripts/sight_pose.py at scale 1).
    check(postLocal.z>34.3&&postLocal.z<38.4,"front post tip moves only 34.4..38.3 u (zero correction)");
    if(elevation==0){
     Vec camLocal=frame.transpose()*(p.camera*(1/scale)-pivot);
     check(std::abs(camLocal.y-200)<0.05&&std::abs(camLocal.z-42.9)<0.1,"flat fire: camera at the tail (0,200,42.9)");
     check(std::abs(postLocal.z-34.451)<0.001,"flat fire: post tip 34.451");
    }
    if(elevation==45)check(std::abs(p.distance-86.048)<0.001&&std::abs(postLocal.z-35.768)<0.001&&std::abs(p.camera.z-65)<1e-6,"+45: camera 86.048 behind the rear sight at 65 u, post 35.768");
    if(elevation==80)check(std::abs(p.distance-16.432)<0.001&&std::abs(postLocal.z-38.304)<0.001&&std::abs(p.camera.z-65)<1e-6,"+80: camera 16.432 behind the rear sight at 65 u, post 38.304");
   }
   if(elevation==80)check(p.distance<20*scale,"at +80 the camera is close to the rear sight");
  }
 }
 check(!sightPose({0,0,0},{1,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,1},1).valid,"a zero bore is rejected");
 check(!sightPose({0,0,0},{0,5250,-113.589},{0,0,0},{0,1,0},{0,0,0},{0,0,1},1).valid,"a right axis along the sight line is rejected");
 check(!sightPose({0,0,0},{1,0,0},{0,10,0},{0,1,0},{0,0,0},{0,0,1},0).valid,"zero scale is rejected");
 std::cout<<(failures?"FAILED ":"PASS ")<<checks<<" v10 assertions, "<<failures<<" failures\n";return failures?1:0;
}
