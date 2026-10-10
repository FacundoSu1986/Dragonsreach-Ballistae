#include "Astra/FastShotRuntime.h"
#include <algorithm>
#include <chrono>

namespace Astra {
namespace {
double clockNow(){return std::chrono::duration<double>(std::chrono::steady_clock::now().time_since_epoch()).count();}
constexpr std::array<std::string_view,13> menus={"InventoryMenu","MagicMenu","MapMenu","Journal Menu","TweenMenu","Console","Dialogue Menu","Loading Menu","BarterMenu","ContainerMenu","FavoritesMenu","Sleep/Wait Menu","MessageBoxMenu"};
bool match(Ticket a,Ticket b){return a.epoch==b.epoch&&a.key==b.key;}
Vec vector(RE::NiPoint3 p){return {p.x,p.y,p.z};}
void transforms(RE::NiAVObject* o){if(!o)return;RE::NiUpdateData d{};d.flags=RE::NiUpdateData::Flag::kDirty;o->UpdateWorldData(&d);if(auto n=o->AsNode())for(auto&c:n->children)if(c)transforms(c.get());}
struct EffectScope {EffectsBarrier& b;EffectScope(EffectsBarrier&x):b(x){b.enter();}~EffectScope(){b.leave();}};
}
bool FastShotRuntime::begin(Key k,double yaw,double pitch,FastConfig c){
 auto lock=effects_.lock();
 if(!effects_.quiescent()||fence_.pending()||owner_||!validLimits(c.limits)||!std::isfinite(c.pivot)||!std::isfinite(c.operatorHeight)||
 !std::isfinite(c.operatorDistance)||!std::isfinite(c.operatorTolerance)||c.operatorDistance<=0||c.operatorTolerance<=0)return false;
 // IDs outlive cells; no retained actor/reference/scene pointers cross VM boundaries.
 auto w=RE::TESForm::LookupByID<RE::TESObjectWEAP>(c.weapon);auto a=RE::TESForm::LookupByID<RE::TESAmmo>(c.ammo);auto cost=RE::TESForm::LookupByID<RE::TESAmmo>(c.cost);
 FastShot probe;if(!w||!a||!a->data.projectile||!cost||!probe.begin({k,1},c.timing,{}))return false;
 if(!session_.begin(k,yaw,pitch,c.limits))return false;
 owner_=session_.ticket();fence_.begin(owner_);config_=c;armed_=false;rootIdentity_=0;entered_=clockNow();lastArmWaitLog_=0;return true;
}
bool FastShotRuntime::current(Ticket t)const{return t&&match(session_.ticket(),t)&&!session_.suspended();}
bool FastShotRuntime::beginLegacy(Key k,double yaw,double pitch){auto lock=effects_.lock();if(!effects_.quiescent()||owner_||fence_.pending())return false;return session_.begin(k,yaw,pitch);}
bool FastShotRuntime::blocked()const{auto ui=RE::UI::GetSingleton();if(!ui||ui->GameIsPaused())return true;for(auto name:menus)if(ui->IsMenuOpen(name))return true;return false;}
bool FastShotRuntime::context(RE::NiPointer<RE::TESObjectREFR>& gun,Snapshot& s)const{
 if(!owner_||!current(owner_)||blocked())return false;
 auto p=RE::PlayerCharacter::GetSingleton();auto camera=RE::PlayerCamera::GetSingleton();
 if(!p||p->IsDead()||!camera||camera->currentState.get()!=camera->cameraStates[RE::CameraStates::kFirstPerson].get())return false;
 RE::RefHandle h=owner_.key.handle;RE::LookupReferenceByHandle(h,gun);
 if(!gun||gun->IsDeleted()||gun->IsDisabled()||!gun->Get3D()||(rootIdentity_&&reinterpret_cast<uintptr_t>(gun->Get3D())!=rootIdentity_))return false;
 auto snap=session_.snapshot();if(!snap||!snap->poseValid||!finite(snap->muzzle)||!finite(snap->root)||snap->root.scale<=0||snap->root.scale>100)return false;s=*snap;
 auto op=gun->Get3D()->GetObjectByName("OperatorNode");auto muzzle=gun->Get3D()->GetObjectByName("ProjectileNode");
 if(!op||!muzzle||!gun->GetSequence("Fire")||!gun->GetSequence("Reset")||!gun->Get3D()->GetObjectByName("VIROTE_VISUAL"))return false;
 Vec feet=vector(op->world.translate)-s.root.rotation*Vec{0,0,config_.operatorHeight*s.root.scale};Vec d=vector(p->GetPosition())-feet;
 return std::isfinite(length(d))&&d.x*d.x+d.y*d.y<=config_.operatorDistance*config_.operatorDistance&&std::abs(d.z)<=config_.operatorTolerance;
}
void FastShotRuntime::mappings(){auto c=RE::ControlMap::GetSingleton();if(!c)return;for(int device=0;device<2;++device){auto d=device==0?RE::INPUT_DEVICE::kKeyboard:RE::INPUT_DEVICE::kMouse;mapping_[device]=c->GetMappedKey("Right Attack/Block",d);mapping_[2+device]=c->GetMappedKey("Sprint",d);mapping_[4+device]=c->GetMappedKey("Activate",d);}}
std::array<bool,4> FastShotRuntime::physicalHolds(){
 mappings();auto inputs=RE::BSInputDeviceManager::GetSingleton();
 for(int slot=0;slot<4;++slot){int device=slot%2;auto id=mapping_[slot];if(id>=255)continue;
 if(inputs&&device==0){auto k=inputs->GetKeyboard();if(k)physical_[0][id]=(k->curState[id]&0x80)!=0;}
 if(inputs&&device==1&&id<8){auto m=inputs->GetMouse();if(m)physical_[1][id]=(m->dInputNextState.rgbButtons[id]&0x80)!=0;}
 }
 std::array<bool,4> held{};for(int slot=0;slot<4;++slot)if(mapping_[slot]<255)held[slot]=physical_[slot%2][mapping_[slot]];return held;
}
bool FastShotRuntime::ready(Key k){auto lock=effects_.lock();return owner_.key==k&&armed_&&!fence_.pending()&&match(owner_,session_.ticket())&&session_.ready(k);}
bool FastShotRuntime::quiescent(Key k){auto lock=effects_.lock();return effects_.quiescent()&&fence_.quiescent(k);}
bool FastShotRuntime::resetIdleScene(Key k){
 // Default (non-tasklet) Papyrus binding: all scene effects run on the game
 // thread. Retain scene/sequence ownership locally, never across VM returns.
 auto lock=effects_.lock();
 if(!idleResetAllowed(k,session_.ticket(),owner_,effects_.quiescent(),fence_.pending()))return false;
 RE::RefHandle h=k.handle;RE::NiPointer<RE::TESObjectREFR> gun;RE::LookupReferenceByHandle(h,gun);
 if(!gun||gun->IsDeleted()||gun->IsDisabled()||!gun->Get3D())return false;
 RE::NiPointer<RE::NiAVObject> scene{gun->Get3D()};
 RE::NiPointer<RE::NiControllerSequence> fire{gun->GetSequence("Fire")},reset{gun->GetSequence("Reset")};
 RE::NiPointer<RE::NiAVObject> bolt{scene->GetObjectByName("VIROTE_VISUAL")};
 if(!fire||!reset||!bolt||!scene->GetObjectByName("CTRL_GIRO_360")||!scene->GetObjectByName("CTRL_ELEVACION"))return false;
 EffectScope scope(effects_);
 auto valid=[&]{return !gun->IsDeleted()&&!gun->IsDisabled()&&gun->Get3D()==scene.get()&&
  idleResetAllowed(k,session_.ticket(),owner_,true,fence_.pending());};
 fire->Deactivate(0,false);if(!valid())return false;
 reset->Deactivate(0,false);if(!valid())return false;
 if(!reset->Activate(0,true,1,0,nullptr,false)||!valid())return false;
 // Same settled Reset pose used by native player cleanup, without restarting
 // a full legacy reference animation during guard/player handoff.
 reset->SetPhase(1,true);if(!valid())return false;
 bolt->local.scale=1;transforms(bolt.get());
 bool ok=valid();spdlog::info("station idle scene restored handle={} stable3D={}",k.handle,ok);return ok;
}
int FastShotRuntime::mode(Key k){auto lock=effects_.lock();return owner_.key==k&&armed_?int(shots_.continuous()):-1;}
bool FastShotRuntime::sequence(RE::TESObjectREFR* gun,const char* to,const char* from){
 auto t=owner_;RE::NiPointer<RE::NiControllerSequence> dst{gun->GetSequence(to)},src{gun->GetSequence(from)};if(!dst||!src)return false;
 auto valid=[&]{RE::NiPointer<RE::TESObjectREFR> checkGun;Snapshot s;return !fence_.pending()&&match(owner_,t)&&context(checkGun,s);};
 src->Deactivate(0,false);if(!valid())return false;
 dst->Deactivate(0,false);if(!valid())return false;
 return dst->Activate(0,true,1.f,0.f,nullptr,false)&&valid();
}
void FastShotRuntime::cleanup(Ticket t,FastConfig,uintptr_t identity){
 auto lock=effects_.lock();if(!fence_.pending()||!match(owner_,t))return;EffectScope scope(effects_);
 RE::RefHandle h=t.key.handle;RE::NiPointer<RE::TESObjectREFR> gun;RE::LookupReferenceByHandle(h,gun);
 if(gun&&!gun->IsDeleted()&&gun->Get3D()&&reinterpret_cast<uintptr_t>(gun->Get3D())==identity){
 RE::NiPointer<RE::NiAVObject> scene{gun->Get3D()};
 RE::NiPointer<RE::NiControllerSequence> fire{gun->GetSequence("Fire")},reset{gun->GetSequence("Reset")};
 if(fire)fire->Deactivate(0,false);
 if(reset){reset->Deactivate(0,false);if(reset->Activate(0,true,1,0,nullptr,false))reset->SetPhase(1,true);}
 // Both own NIF aim controls have identity rest rotation. Restore one neutral
 // pose, so a later Begin never strips stale Papyrus angles from live nodes.
 if(RE::NiPointer<RE::NiAVObject> yaw{scene->GetObjectByName("CTRL_GIRO_360")}){yaw->local.rotate=RE::NiMatrix3{};
 if(RE::NiPointer<RE::NiAVObject> pitch{scene->GetObjectByName("CTRL_ELEVACION")})pitch->local.rotate=RE::NiMatrix3{};transforms(yaw.get());}
 if(RE::NiPointer<RE::NiAVObject> bolt{scene->GetObjectByName("VIROTE_VISUAL")}){bolt->local.scale=1;transforms(bolt.get());}
 }
 fence_.complete(t);owner_={};rootIdentity_=0;spdlog::info("shot effects quiescent epoch={} token={}",t.epoch,t.key.token);
}
void FastShotRuntime::requestEnd(){
 if(!owner_||fence_.pending())return;auto t=owner_;shots_.invalidate();armed_=false;flightHandle_={};flightTicket_={};
 if(auto acquired=session_.invalidateScene(t))rootIdentity_=acquired;
 if(!rootIdentity_){fence_.requestEnd(t);fence_.complete(t);owner_={};return;}
 fence_.requestEnd(t);auto c=config_;auto id=rootIdentity_;SKSE::GetTaskInterface()->AddTask([this,t,c,id]{cleanup(t,c,id);});
}
bool FastShotRuntime::end(Key k){auto lock=effects_.lock();if(owner_&&owner_.key==k)requestEnd();else session_.end(k);return effects_.quiescent()&&(!fence_.pending()||owner_.key!=k);}
void FastShotRuntime::invalidate(){auto lock=effects_.lock();requestEnd();session_.invalidate();}
void FastShotRuntime::menu(const RE::MenuOpenCloseEvent* e){if(!e||std::find(menus.begin(),menus.end(),std::string_view(e->menuName.c_str()))==menus.end())return;auto lock=effects_.lock();if(armed_){shots_.pause(physicalHolds());session_.freeze(owner_.key,false);}session_.rebase();}
RE::BSEventNotifyControl FastShotRuntime::ProcessEvent(RE::InputEvent* const* list,RE::BSTEventSource<RE::InputEvent*>*){
 if(!list)return RE::BSEventNotifyControl::kContinue;auto lock=effects_.lock();mappings();
 for(auto e=*list;e;e=e->next){auto b=e->AsButtonEvent();if(!b)continue;int d=b->GetDevice()==RE::INPUT_DEVICE::kKeyboard?0:b->GetDevice()==RE::INPUT_DEVICE::kMouse?1:-1;if(d<0||b->GetIDCode()>=255||(d==1&&b->GetIDCode()>=10))continue;
 auto raw=b->GetIDCode();physical_[d][raw]=b->IsPressed();if(!armed_||fence_.pending())continue;
 RE::NiPointer<RE::TESObjectREFR> gun;Snapshot s;bool valid=context(gun,s);double now=clockNow();
 if(raw==mapping_[4+d]&&b->IsDown()&&valid&&now>=entered_+.35){spdlog::info("shot input exit epoch={} token={}",owner_.epoch,owner_.key.token);requestEnd();continue;}
 for(int slot=d;slot<4;slot+=2){if(raw!=mapping_[slot])continue;auto result=shots_.edge(owner_,slot,b->IsPressed(),now,valid);
 if(result==InputResult::Accepted){session_.capture(owner_.key,true);auto r=shots_.request();spdlog::info("shot input admitted t={:.6f} epoch={} token={} seq={} device={} raw={}",now,owner_.epoch,owner_.key.token,r.sequence,d,raw);}
 else if(result==InputResult::ModeChanged){spdlog::info("shot mode continuous={} epoch={} token={}",shots_.continuous(),owner_.epoch,owner_.key.token);}
 else if(b->IsDown())spdlog::info("shot input rejected t={:.6f} epoch={} token={} device={} raw={} context={}",now,owner_.epoch,owner_.key.token,d,raw,valid);
 }
 }
 return RE::BSEventNotifyControl::kContinue;
}
void FastShotRuntime::tick(){
 auto lock=effects_.lock();if(!owner_||fence_.pending())return;
 if(!match(owner_,session_.ticket())){requestEnd();return;}
 constexpr std::array<double,3> flightSamples{.05,.25,.5};
 if(flightHandle_&&match(flightTicket_,owner_)&&!blocked()&&clockNow()-flightAt_>=flightSamples[flightStage_]){
  auto projectile=flightHandle_.get();double dt=clockNow()-flightAt_;
  if(projectile){auto& rt=projectile->GetProjectileRuntimeData();
   spdlog::info("shot flight sample handle={} stage={} elapsed_ms={:.3f} distance={:.3f} velocity={:.3f} calculated_speed={:.3f} power={:.3f} speed_mult={:.3f} loaded3D={} flags={:08X} distance_moved={:.3f}",flightHandle_.native_handle(),flightStage_,dt*1000,length(vector(projectile->GetPosition())-flightOrigin_),length(vector(rt.linearVelocity)),projectile->GetSpeed(),rt.power,rt.speedMult,projectile->Get3D()!=nullptr,rt.flags,rt.distanceMoved);
  }else spdlog::info("shot flight sample handle={} elapsed_ms={:.3f} unavailable (impact/unload)",flightHandle_.native_handle(),dt*1000);
  if(!projectile||++flightStage_>=int(flightSamples.size())){flightHandle_={};flightTicket_={};}
 }
 RE::NiPointer<RE::TESObjectREFR> gun;Snapshot s;bool valid=context(gun,s);
 if(!armed_){
  if(!valid){
   double now=clockNow();
   if(now>=lastArmWaitLog_+1){lastArmWaitLog_=now;auto snap=session_.snapshot();
    spdlog::warn("shot frame pump waiting epoch={} token={} suspended={} modal={} snapshot={} loaded3D={} Fire={} Reset={}",owner_.epoch,owner_.key.token,session_.suspended(),blocked(),snap&&snap->poseValid,gun&&gun->Get3D(),gun&&gun->GetSequence("Fire"),gun&&gun->GetSequence("Reset"));}
   return;
  }
  rootIdentity_=reinterpret_cast<uintptr_t>(gun->Get3D());armed_=shots_.begin(owner_,config_.timing,physicalHolds());if(armed_)spdlog::info("shot armed epoch={} token={} release_ms={:.3f} cycle_s={}",owner_.epoch,owner_.key.token,config_.timing.release*1000,config_.timing.cycle);return;
 }
 EffectScope scope(effects_);
 for(int step=0;step<3;++step){double now=clockNow();valid=context(gun,s);auto action=shots_.next(now,valid);if(action==ShotAction::None){if(!valid)session_.freeze(owner_.key,false);break;}
 auto r=shots_.request();
 if(action==ShotAction::Prepare){
 bool froze=session_.capture(owner_.key,true).has_value();bool started=froze&&sequence(gun.get(),"Fire","Reset");shots_.prepared(clockNow(),started);
 if(!started){if(match(owner_,r.ticket))session_.freeze(r.ticket.key,false);spdlog::warn("shot Fire failed epoch={} token={} seq={}",r.ticket.epoch,r.ticket.key.token,r.sequence);}continue;
 }
 if(action==ShotAction::Launch){
 // Commitment is serialized by the effects barrier. Engine calls stay outside
 // Session mutex; End cannot release a new owner before this block completes.
 auto p=RE::PlayerCharacter::GetSingleton();auto ammo=RE::TESForm::LookupByID<RE::TESAmmo>(config_.ammo);auto cost=RE::TESForm::LookupByID<RE::TESAmmo>(config_.cost);auto weapon=RE::TESForm::LookupByID<RE::TESObjectWEAP>(config_.weapon);
 bool preflight=valid&&p&&ammo&&ammo->data.projectile&&cost&&weapon&&muzzleVelocity(s.muzzle.rotation*Vec{0,1,0},ammo->data.projectile->data.speed)&&session_.validateShot(owner_.key,s.aim,config_.pivot);
 RE::ProjectileHandle handle;double launchedAt=now;
 AmmoOutcome outcome;
 if(preflight){auto count=[&]{auto items=p->GetInventoryCounts([&](RE::TESBoundObject& o){return &o==cost;});auto it=items.find(cost);return it==items.end()?0:it->second;};
 outcome=transactAmmo(count,[&]{p->RemoveItem(cost,1,RE::ITEM_REMOVE_REASON::kRemove,nullptr,nullptr);},[&]{
 // Inventory callbacks may synchronously invalidate this lease. Recheck at
 // the actual engine commitment after RemoveItem, refunding on cancellation.
 Snapshot committedSnapshot;RE::NiPointer<RE::TESObjectREFR> committedGun;
 if(fence_.pending()||!match(owner_,r.ticket)||!context(committedGun,committedSnapshot)||
    !session_.validateShot(r.ticket.key,committedSnapshot.aim,config_.pivot))return false;
 s=committedSnapshot;gun=committedGun;
 auto velocity=muzzleVelocity(s.muzzle.rotation*Vec{0,1,0},ammo->data.projectile->data.speed);if(!velocity)return false;
 Vec forward=*velocity*(1./length(*velocity));RE::NiPoint3 origin{float(s.muzzle.translation.x),float(s.muzzle.translation.y),float(s.muzzle.translation.z)};
 RE::Projectile::ProjectileRot angles{float(-std::asin(std::clamp(forward.z,-1.,1.))),float(std::atan2(forward.x,forward.y))};
 RE::Projectile::LaunchData data(p,origin,angles,ammo,weapon);RE::Projectile::Launch(&handle,data);
 auto projectile=handle.get();if(!projectile)return false;
 auto& rt=projectile->GetProjectileRuntimeData();double engineVelocity=length(vector(rt.linearVelocity));
 double calculatedBefore=projectile->GetSpeed();auto corrected=speedMultiplierCorrection(ammo->data.projectile->data.speed,calculatedBefore,rt.speedMult);
 // Launch creates a pending projectile; its later 3D initialization computes
 // velocity again from GetSpeed(). Fix that stored scalar before assigning
 // the initial vector, so initialization does not replace 5400 with 756.
 if(corrected)rt.speedMult=float(*corrected);
 else spdlog::warn("shot speed normalization unavailable handle={} calculated={} multiplier={}",handle.native_handle(),calculatedBefore,rt.speedMult);
 rt.linearVelocity={float(velocity->x),float(velocity->y),float(velocity->z)};
 launchedAt=clockNow();flightHandle_=handle;flightTicket_=r.ticket;flightOrigin_=s.muzzle.translation;flightAt_=launchedAt;flightStage_=0;
 spdlog::info("shot speed normalization handle={} calculated_before={:.3f} calculated_after={:.3f} speed_mult={:.6f}",handle.native_handle(),calculatedBefore,projectile->GetSpeed(),rt.speedMult);
 spdlog::info("shot ballistics handle={} base_speed={:.3f} engine_velocity={:.3f} muzzle_velocity={:.3f} calculated_speed={:.3f} power={:.3f} speed_mult={:.3f} direction={:.5f},{:.5f},{:.5f}",handle.native_handle(),ammo->data.projectile->data.speed,engineVelocity,length(vector(rt.linearVelocity)),projectile->GetSpeed(),rt.power,rt.speedMult,forward.x,forward.y,forward.z);
 return true;
 },[&]{p->AddObjectToContainer(cost,nullptr,1,nullptr);});}
 shots_.launched(launchedAt,outcome.launched);session_.freeze(owner_.key,false);
 spdlog::info("shot launch t={:.6f} input_to_launch_ms={:.3f} epoch={} token={} seq={} repeated={} handle={} valid={} charged={} refund={} ammo_before={} ammo_after={} preflight={}",launchedAt,(launchedAt-r.admitted)*1000,r.ticket.epoch,r.ticket.key.token,r.sequence,r.repeated,handle.native_handle(),outcome.launched,outcome.charged,outcome.refunded,outcome.before,outcome.after,preflight);
 RE::NiPointer<RE::TESObjectREFR> effectGun;Snapshot effectSnapshot;
 if(outcome.launched&&!fence_.pending()&&match(owner_,r.ticket)&&context(effectGun,effectSnapshot)){
 RE::NiPointer<RE::NiAVObject> scene{effectGun->Get3D()};
 if(RE::NiPointer<RE::NiAVObject> bolt{scene->GetObjectByName("VIROTE_VISUAL")}){bolt->local.scale=0;transforms(bolt.get());}
 auto snd=RE::TESForm::LookupByID<RE::TESSound>(config_.sound);auto audio=RE::BSAudioManager::GetSingleton();RE::BSSoundHandle sound;
 if(snd&&snd->descriptor&&audio&&audio->BuildSoundDataFromDescriptor(sound,snd->descriptor)&&
    !fence_.pending()&&match(owner_,r.ticket)&&context(effectGun,effectSnapshot)){
 sound.SetPosition({float(s.muzzle.translation.x),float(s.muzzle.translation.y),float(s.muzzle.translation.z)});
 sound.SetObjectToFollow(scene.get());if(!sound.Play())spdlog::warn("shot sound failed seq={}",r.sequence);}
 }
 break; // At most one projectile per frame, even after a slow frame.
 }
 if(action==ShotAction::Reset){bool ok=sequence(gun.get(),"Reset","Fire");shots_.reset(clockNow());if(!ok){spdlog::warn("shot Reset failed epoch={} token={}",owner_.epoch,owner_.key.token);requestEnd();break;}continue;}
 if(action==ShotAction::Restore){if(auto bolt=gun->Get3D()->GetObjectByName("VIROTE_VISUAL")){bolt->local.scale=1;transforms(bolt);}shots_.restored();continue;}
 }
}
}
