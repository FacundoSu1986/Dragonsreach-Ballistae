#include "Astra/Core.h"
#include <iostream>
#include <future>
#include <chrono>
using namespace Astra;
int main(){
 int checks=0,failures=0; auto check=[&](bool ok,const char* name){++checks;if(!ok){++failures;std::cerr<<name<<'\n';}};
 for(double yaw:{0.,179.,180.,181.,240.,359.})for(double pitch:{-20.,-5.,0.,35.,80.}){
  Session s;Key k{800,1};s.begin(k,yaw,pitch);auto ticket=s.ticket();
  Transform root{rz(rad(37))*rx(rad(12)),{3000,-4000,600},1.25};
  double p=rad(pitch),y=rad(yaw),ly=-224*std::cos(p)+19.6*std::sin(p);
  Vec local{-ly*std::sin(y),ly*std::cos(y),153+224*std::sin(p)+19.6*std::cos(p)};
  Transform muzzle{root.rotation*rz(y)*rx(-p)*rz(rad(180)),root.translation+root.rotation*local*root.scale,root.scale};
  Transform desired{muzzle.rotation,muzzle.translation+Vec{0,0,20.4},1};
  s.update(ticket,{yaw,pitch},false,[&](Aim a){Snapshot v{a,{},true,1};v.worldCamera=desired;v.root=root;v.muzzle=muzzle;v.poseValid=true;return v;});
  check(!s.validateShot(k,{yaw,pitch},153),"unfrozen snapshot cannot launch");
  s.capture(k,true);check(s.validateShot(k,{yaw,pitch},153),"frozen posed muzzle under tilted scaled root");
  check(!s.validateShot({800,2},{yaw,pitch},153),"wrong lease denied");
  check(!s.validateShot(k,{yaw+4,pitch},153),"stale yaw denied");
  check(!s.validateShot(k,{yaw,pitch},160),"wrong muzzle position denied");
  // Simulate vanilla late composition driven by body and then a changed parent.
  Transform parent{rz(rad(yaw+21))*rx(rad(-8)),{920,350,-12},.7};
  Transform cameraLocal{rz(rad(12)),{400,300,80},1};
  check(s.visitSnapshot(ticket,[&](const Snapshot& v){cameraLocal=toLocal(parent,v.worldCamera);}),"active post-camera visitor accepted");
  check(length(parent.translation+parent.rotation*cameraLocal.translation*parent.scale-desired.translation)<1e-6,"late vanilla position replaced at current parent");
  check(matrixNear(parent.rotation*cameraLocal.rotation,desired.rotation),"late vanilla rotation replaced beyond 180");
  s.end(k);bool touched=false;
  check(!s.visitSnapshot(ticket,[&](const Snapshot&){touched=true;})&&!touched,"ended camera transaction cannot write scene");
  s.begin(k,0,0);auto fresh=s.ticket();s.update(fresh,{0,0},false,[](Aim a){return Snapshot{a,{},true};});
  check(!s.visitSnapshot(ticket,[&](const Snapshot&){touched=true;})&&!touched,"renewed same-key stale epoch cannot write");
 }
 Session race;Key key{901,1};race.begin(key,0,0);auto t=race.ticket();race.update(t,{0,0},false,[](Aim a){return Snapshot{a,{},true};});
 std::promise<void> entered,release;auto done=release.get_future();
 auto writer=std::async(std::launch::async,[&]{race.visitSnapshot(t,[&](const Snapshot&){entered.set_value();done.wait();});});
 entered.get_future().wait();auto end=std::async(std::launch::async,[&]{return race.end(key);});
 check(end.wait_for(std::chrono::milliseconds(30))==std::future_status::timeout,"EndSight serializes with post-camera write");
 release.set_value();writer.get();check(end.get()&&!race.snapshot(),"no post-camera write after EndSight returns");
 std::cout<<(failures?"FAILED ":"PASS ")<<checks<<" v07 assertions, "<<failures<<" failures\n";return failures?1:0;
}
