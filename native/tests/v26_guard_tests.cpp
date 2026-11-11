#include "Astra/GuardPolicy.h"
#include <iostream>
using namespace Astra;
int main(){
 int checks=0,failures=0;auto check=[&](bool value,const char* text){++checks;if(!value){++failures;std::cerr<<text<<'\n';}};
 check(guardOperatorPackage(true,true,false,false,true),"station AI must run normally before acquisition");
 check(guardOperatorPackage(true,false,true,true,true),"owned special idle must not revoke its permanent assigned station AI");
 check(!guardOperatorPackage(true,false,true,false,true),"idle override before acquisition cannot confer station ownership");
 check(!guardOperatorPackage(false,true,true,true,true),"another assigned package must revoke the station even if effective package matches");
 check(guardOperatorPackage(true,false,false,true,true),"measured 1.6.1170 run-once wrapper (currentProcessIdle stays null) is tolerated post-acquisition; OAR clip observation arbitrates owned-idle identity");
 check(!guardOperatorPackage(true,false,true,true,false),"owned idle does not authorize a personal weapon pose");
 check(!guardOperatorPackage(true,true,true,true,false),"normal station package still requires sheathed hands");
 check(guardOperatorPackage(true,true,false,true,true),"normal station execution remains valid without a transient idle");
 check(!guardOperatorPackage(false,false,false,true,true),"missing process/package is never valid");
 std::cout<<checks<<" v26 assertions "<<failures<<" failures\n";return failures?1:0;
}
