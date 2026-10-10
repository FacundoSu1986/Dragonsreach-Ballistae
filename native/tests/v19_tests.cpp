#include "Astra/FastShot.h"
#include <iostream>
using namespace Astra;
int main(){
 int checks=0,failures=0;
 auto check=[&](bool x,const char* s){++checks;if(!x){++failures;std::cerr<<s<<'\n';}};
 Key gun{100,0}; Ticket owner{{100,7},2},other{{200,8},3};
 check(idleResetAllowed(gun,{},{},true,false),"idle gun may reset");
 check(!idleResetAllowed({0,0},{},{},true,false),"missing ref rejected");
 check(!idleResetAllowed({100,1},{},{},true,false),"wildcard required");
 check(!idleResetAllowed(gun,owner,{},true,false),"legacy sight owner protected");
 check(!idleResetAllowed(gun,{},owner,true,false),"fast sight owner protected");
 check(!idleResetAllowed(gun,{},{},false,false),"effect in progress protected");
 check(!idleResetAllowed(gun,{},{},true,true),"cleanup in progress protected");
 check(idleResetAllowed(gun,other,other,true,false),"other gun owner untouched");
 std::cout<<checks<<" v19 assertions "<<failures<<" failures\n";return failures?1:0;
}
