#include "Astra/FastShot.h"
#include <limits>
namespace Astra {
bool idleResetAllowed(Key gun,Ticket sessionOwner,Ticket effectsOwner,bool effectsIdle,bool cleanupPending){
 return gun.handle&&gun.token==0&&effectsIdle&&!cleanupPending&&
  (!sessionOwner||sessionOwner.key.handle!=gun.handle)&&(!effectsOwner||effectsOwner.key.handle!=gun.handle);
}
std::optional<double> speedMultiplierCorrection(double desired,double calculated,double currentMultiplier){
 if(!std::isfinite(desired)||!std::isfinite(calculated)||!std::isfinite(currentMultiplier)||desired<=0||calculated<=0||currentMultiplier<=0)return {};
 double corrected=currentMultiplier*(desired/calculated);
 if(!std::isfinite(corrected)||corrected<std::numeric_limits<float>::min()||corrected>std::numeric_limits<float>::max())return {};
 return corrected;
}
std::optional<Vec> muzzleVelocity(Vec bore,double speed){
 if(!std::isfinite(bore.x)||!std::isfinite(bore.y)||!std::isfinite(bore.z)||!std::isfinite(speed)||speed<=0)return {};
 double n=length(bore);if(!std::isfinite(n)||n<1e-6)return {};
 Vec v=bore*(speed/n);if(!std::isfinite(v.x)||!std::isfinite(v.y)||!std::isfinite(v.z))return {};
 return v;
}
bool EffectsFence::begin(Ticket t){if(owner_||!t)return false;owner_=t;pending_=false;return true;}
void EffectsFence::requestEnd(Ticket t){if(owner_&&owner_.epoch==t.epoch&&owner_.key==t.key)pending_=true;}
void EffectsFence::complete(Ticket t){if(pending_&&owner_.epoch==t.epoch&&owner_.key==t.key){owner_={};pending_=false;}}
bool EffectsFence::quiescent(Key k)const{if(k.token==0)return !owner_||owner_.key.handle!=k.handle;return !pending_||owner_.key!=k;}
bool FastShot::begin(Ticket t,ShotTiming timing,std::array<bool,4> held){
 if(!t||!std::isfinite(timing.fire)||!std::isfinite(timing.release)||!std::isfinite(timing.reset)||!std::isfinite(timing.cycle)||
 timing.release<0||timing.release>timing.fire||timing.fire<=0||timing.reset<=0||timing.cycle+1e-5<timing.fire+timing.reset)return false;
 invalidate();ticket_=t;timing_=timing;held_=releaseGate_=held;return true;
}
InputResult FastShot::edge(Ticket t,int slot,bool down,double now,bool context){
 if(!active()||t.epoch!=ticket_.epoch||t.key!=ticket_.key||slot<0||slot>=4||!std::isfinite(now))return InputResult::Ignored;
 bool wasHeld=held_[slot];held_[slot]=down;
 if(!down){releaseGate_[slot]=false;if(!held_[0]&&!held_[1])repeatArmed_=false;return InputResult::Ignored;}
 if(wasHeld||releaseGate_[slot]||!context)return InputResult::Ignored;
 if(slot>=2){timing_.continuous=!timing_.continuous;repeatArmed_=false;return InputResult::ModeChanged;}
 if(phase_!=0||now<cooldownUntil_)return InputResult::Ignored;
 repeatArmed_=timing_.continuous;request_={ticket_,++sequence_,now,false};phase_=1;return InputResult::Accepted;
}
void FastShot::pause(std::array<bool,4> held){
 held_=releaseGate_=held;repeatArmed_=false;
 if(phase_==1){phase_=0;request_={};}
 else if(phase_==2&&!committed_){phase_=3;resetNeeded_=true;request_={};}
}
void FastShot::invalidate(){ticket_={};held_={};releaseGate_={};request_={};phase_=0;repeatArmed_=committed_=resetNeeded_=false;releaseAt_=resetAt_=restoreAt_=cooldownUntil_=0;sequence_=0;}
ShotAction FastShot::next(double now,bool context){
 if(!active()||!std::isfinite(now))return ShotAction::None;
 if(!context){pause(held_);return ShotAction::None;}
 if(phase_==0&&timing_.continuous&&repeatArmed_&&(held_[0]||held_[1])&&now>=cooldownUntil_){request_={ticket_,++sequence_,now,true};phase_=1;}
 if(phase_==1)return ShotAction::Prepare;
 if(phase_==2){if(!committed_&&now>=releaseAt_)return ShotAction::Launch;if(now>=resetAt_)return ShotAction::Reset;}
 if(phase_==3){if(resetNeeded_)return ShotAction::Reset;if(now>=restoreAt_&&now>=cooldownUntil_)return ShotAction::Restore;}
 return ShotAction::None;
}
void FastShot::prepared(double now,bool success){
 if(phase_!=1)return;committed_=false;
 if(!success){repeatArmed_=false;phase_=3;resetNeeded_=true;return;}
 phase_=2;releaseAt_=now+timing_.release;resetAt_=now+timing_.fire;
}
void FastShot::launched(double now,bool success){if(phase_!=2||committed_)return;committed_=true;if(success)cooldownUntil_=now+timing_.cycle;else repeatArmed_=false;}
void FastShot::reset(double now){phase_=3;resetNeeded_=false;restoreAt_=now+timing_.reset;}
void FastShot::restored(){phase_=0;request_={};committed_=false;resetNeeded_=false;}
AmmoOutcome transactAmmo(const std::function<int()>& count,const std::function<void()>& remove,
 const std::function<bool()>& launch,const std::function<void()>& refund){
 AmmoOutcome o;o.before=o.after=count();if(o.before<1)return o;
 remove();o.after=count();o.charged=o.after==o.before-1;if(!o.charged)return o;
 o.launched=launch();if(!o.launched){refund();o.after=count();o.refunded=o.after==o.before;}return o;
}
}
