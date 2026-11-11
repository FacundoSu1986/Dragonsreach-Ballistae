#include "Astra/Core.h"
#include <iostream>
using namespace Astra;
// v08 sight zero: the optical axis is 20.4 u above and parallel to the bore; the view dips by
// delta(pitch) so the reticle meets the modelled trajectory at 75 m for any elevation.
int main(){
 int checks=0,failures=0; auto check=[&](bool ok,const char* name){++checks;if(!ok){++failures;std::cerr<<name<<'\n';}};
 check(std::abs(deg(sightZeroRadians(0))+1.38198)<1e-4,"flat zero is 1.382 degrees down");
 check(std::abs(deg(sightZeroRadians(45))+1.03898)<2e-4,"45 degrees scales the drop by cos");
 check(std::abs(deg(sightZeroRadians(80))+0.41393)<2e-4,"80 degrees keeps parallax with little drop");
 // Gravity across the line of fire is g*cos(elevation): depression and elevation of the same angle match.
 check(std::isfinite(sightZeroRadians(-5))&&sightZeroRadians(-5)<0,"lowest elevation still dips the view");
 check(std::abs(sightZeroRadians(-5)-sightZeroRadians(5))<1e-15,"symmetric about level fire");
 double previous=sightZeroRadians(0);
 for(double p=5;p<=80;p+=5){double z=sightZeroRadians(p);check(std::isfinite(z)&&z<0,"finite downward zero");check(z>previous,"zero shrinks as elevation rises");previous=z;}
 for(double yaw:{0.,179.,180.,240.})for(double pitch:{-5.,0.,35.,80.}){
  Mat anchor=rz(rad(yaw))*rx(rad(-pitch))*rz(rad(180));
  Mat view=sightCameraRotation(anchor,Mat{},pitch);
  Vec bore=anchor*Vec{0,1,0},forward=view*Vec{0,1,0};
  double dot=bore.x*forward.x+bore.y*forward.y+bore.z*forward.z;
  check(std::abs(dot-std::cos(sightZeroRadians(pitch)))<1e-9,"view differs from bore by exactly the zero");
  Vec local=anchor.transpose()*forward;
  check(local.z<0&&std::abs(local.x)<1e-12,"tilt is a pure downward pitch in the anchor frame");
  check(std::abs(length(forward)-1)<1e-12&&matrixNear(view.transpose()*view,Mat{}),"view stays a rotation");
 }
 Mat adapter=rz(rad(90))*rx(rad(-90));
 check(matrixNear(sightCameraRotation(Mat{},adapter,0),rx(sightZeroRadians(0))*adapter),"adapter composes after the tilt");
 std::cout<<(failures?"FAILED ":"PASS ")<<checks<<" v08 assertions, "<<failures<<" failures\n";return failures?1:0;
}
