#include "Astra/GuardRuntime.h"
#include "Astra/OARAnimations.h"
#include <REX/W32/KERNEL32.h>
#include <algorithm>
#include <numbers>
#include <cctype>
namespace RE {class hkbGeneratorOutput;}
namespace Astra {
namespace {
GuardRuntime* runtime{};
using ActorUpdate=void (*)(RE::Actor*,float);
using ClipGenerate=void (*)(RE::hkbClipGenerator*,const RE::hkbContext&,const RE::hkbGeneratorOutput**,RE::hkbGeneratorOutput&,float);
REL::Relocation<ActorUpdate> playerOriginal,characterOriginal;
REL::Relocation<ClipGenerate> clipOriginal;
void playerPump(RE::Actor* actor,float dt){playerOriginal(actor,dt);if(runtime)runtime->tick(dt);}
void actorPost(RE::Actor* actor,float dt){characterOriginal(actor,dt);if(runtime)runtime->postActor(actor);}
void clipGenerated(RE::hkbClipGenerator* clip,const RE::hkbContext& context,const RE::hkbGeneratorOutput** children,RE::hkbGeneratorOutput& output,float offset){
 guardGenerateAndObserve(clipOriginal,clip,context,children,output,offset,[offset](auto* c,const auto& ctx){if(runtime&&offset==0)runtime->observe(c,ctx);});
}
Vec from(RE::NiPoint3 p){return {p.x,p.y,p.z};}
Mat from(RE::NiMatrix3 m){Mat r;for(int i=0;i<3;++i)for(int j=0;j<3;++j)r.m[3*i+j]=m.entry[i][j];return r;}
RE::NiPoint3 into(Vec v){return {float(v.x),float(v.y),float(v.z)};}
RE::NiMatrix3 into(Mat m){RE::NiMatrix3 r;for(int i=0;i<3;++i)for(int j=0;j<3;++j)r.entry[i][j]=float(m.m[3*i+j]);return r;}
Transform from(RE::NiTransform t){return {from(t.rotate),from(t.translate),t.scale};}
void transforms(RE::NiAVObject* o){if(!o)return;RE::NiUpdateData d{};d.flags=RE::NiUpdateData::Flag::kDirty;o->UpdateWorldData(&d);if(auto n=o->AsNode())for(auto& c:n->children)if(c)transforms(c.get());}
constexpr std::array<uint32_t,4> factionIDs{0x800,0x801,0x804,0x805};
constexpr std::array<double,4> durations{2.,1.,.8,.8};
RE::TESFaction* faction(size_t i){auto h=RE::TESDataHandler::GetSingleton();return h?h->LookupForm<RE::TESFaction>(factionIDs[i],"AstraAsedio_GuardAnim.esp"):nullptr;}
RE::TESIdleForm* idle(bool exit=false){auto h=RE::TESDataHandler::GetSingleton();return h?h->LookupForm<RE::TESIdleForm>(exit?0x803:0x802,"AstraAsedio_GuardAnim.esp"):nullptr;}
RE::TESPackage* operatorPackage(){auto h=RE::TESDataHandler::GetSingleton();return h?h->LookupForm<RE::TESPackage>(0xB90,GuardStationPlugin):nullptr;}
const char* operatorFailure(RE::Actor* actor,bool acquired=false){
 auto p=operatorPackage();auto process=actor?actor->GetActorRuntimeData().currentProcess:nullptr;auto state=actor?actor->AsActorState():nullptr;auto ownedIdle=idle();
 if(!p)return "owned operator package missing";
 if(!process||!state)return "operator process / actor state missing";
 if(process->currentPackage.package!=p)return "assigned operator package changed";
 if(state->GetWeaponState()!=RE::WEAPON_STATE::kSheathed)return "operator personal weapon not fully sheathed";
 // The assigned station package and the running special-idle package are
 // separate engine fields. Measured on 1.6.1170: while the own PlayIdle runs,
 // the running package is the run-once wrapper and currentProcessIdle stays
 // null, so an acquired lease tolerates that override (see GuardPolicy).
 if(!guardOperatorPackage(true,actor->GetCurrentPackage()==p,
  ownedIdle&&process->high&&process->high->currentProcessIdle==ownedIdle,acquired,true))return "assigned package / weapon-state contract broken";
 return nullptr;
}
RE::TESObjectARMO* actorShield(RE::Actor* actor){return actor?actor->GetWornArmor(RE::BGSBipedObjectForm::BipedObjectSlot::kShield,true):nullptr;}
bool alive(RE::Actor* a){return a&&!a->IsDead()&&!a->IsDeleted()&&!a->IsDisabled()&&a->Get3D()&&a->GetParentCell()&&a->AsActorValueOwner()->GetActorValue(RE::ActorValue::kHealth)>0;}
bool interrupted(RE::Actor* a){auto s=a->AsActorState();return !s||s->actorState2.staggered||s->GetKnockState()!=RE::KNOCK_STATE_ENUM::kNormal||s->GetLifeState()!=RE::ACTOR_LIFE_STATE::kAlive||a->IsInKillMove();}
bool ownedOperator(RE::Actor* actor){auto h=RE::TESDataHandler::GetSingleton();return h&&actor&&(h->LookupForm(0xB71,GuardStationPlugin)==actor||h->LookupForm(0xB81,GuardStationPlugin)==actor);}
double referenceScale(RE::Actor* actor){return actor?actor->GetReferenceRuntimeData().refScale*.01:NAN;}
double naturalHeight(RE::Actor* actor){auto base=actor?actor->GetActorBase():nullptr;return base?base->GetHeight():NAN;}
bool enemy(RE::Actor* a,RE::Actor* guard){return alive(a)&&!ownedOperator(a)&&a!=RE::PlayerCharacter::GetSingleton()&&!a->IsPlayerTeammate()&&a->IsInCombat()&&a->IsHostileToActor(guard);}
bool loaded(RE::TESObjectREFR* r){return r&&!r->IsDeleted()&&!r->IsDisabled()&&r->Get3D()&&r->GetParentCell();}
bool station(RE::TESObjectREFR* gun,RE::Actor* actor){
 auto h=RE::TESDataHandler::GetSingleton();if(!h||!gun||!actor||!gun->GetBaseObject())return false;
 auto base=h->LookupForm(0xB04,"AstraAsedio.esp");if(!base||gun->GetBaseObject()!=base)return false;
 for(auto [g,a]:std::array<std::pair<uint32_t,uint32_t>,2>{{{0xB70,0xB71},{0xB80,0xB81}}})if(h->LookupForm(g,GuardStationPlugin)==gun&&h->LookupForm(a,GuardStationPlugin)==actor&&guardStation(g,a,0xB04))return true;
 return false;
}
struct Ray {bool known{},hit{};double fraction{1};RE::FormID ref{};Vec normal{};};
Ray ray(RE::bhkWorld* world,Vec a,Vec b,RE::COL_LAYER layer=RE::COL_LAYER::kLOS,std::optional<uint32_t> controllerFilter={}){
 if(!world||!std::isfinite(length(a)+length(b)))return {};
 double scale=RE::bhkWorld::GetWorldScale();if(!std::isfinite(scale)||scale<=0)return {};
 RE::bhkPickData pick{};pick.rayOutput.Reset();pick.rayInput.from=RE::hkVector4(into(a*scale));pick.rayInput.to=RE::hkVector4(into(b*scale));
 // World pick applies the live Havok collision filter. Dynamic actor protection
 // is additionally conservative capsule/path math; unclassified hits block.
 pick.rayInput.filterInfo=controllerFilter.value_or(uint32_t(layer));pick.rayInput.enableShapeCollectionFilter=true;
 RE::BSReadLockGuard lock(world->worldLock);world->PickObject(pick);
 bool hit=pick.rayOutput.HasHit();double fraction=hit?pick.rayOutput.hitFraction:1.;RE::FormID ref=0;Vec normal{};
 if(hit){if(!pick.rayOutput.rootCollidable)return {};auto refr=RE::TESHavokUtilities::FindCollidableRef(*pick.rayOutput.rootCollidable);if(refr)ref=refr->GetFormID();alignas(16) float n[4];_mm_store_ps(n,pick.rayOutput.normal.quad);normal={n[0],n[1],n[2]};}
 return {std::isfinite(fraction)&&fraction>=0&&fraction<=1&&(!hit||std::isfinite(length(normal))),hit,fraction,ref,normal};
}
std::optional<GuardProtected> physicalBounds(RE::Actor* actor,double margin=12){
 // Query the live Havok shapes with their live controller transform. Race
 // dimensions and a fixed human capsule are insufficient for scaled actors.
 auto controller=actor?actor->GetCharController():nullptr;auto cell=actor?actor->GetParentCell():nullptr;auto world=cell?cell->GetbhkWorld():nullptr;
 double scale=RE::bhkWorld::GetWorldScaleInverse();if(!controller||!world||!std::isfinite(scale)||scale<=0)return {};
 Vec lo{INFINITY,INFINITY,INFINITY},hi{-INFINITY,-INFINITY,-INFINITY};bool found=false;
 RE::BSReadLockGuard lock(world->worldLock);RE::hkTransform transform{};controller->GetTransformImpl(transform);
 // Query the shape held by the typed controller wrapper. userData is not an
 // additional ownership certificate for these runtime-created Havok shapes.
 for(auto& wrapper:controller->shapes){if(!wrapper||!wrapper->referencedObject)continue;auto shape=static_cast<RE::hkpShape*>(wrapper->referencedObject.get());
  RE::hkAabb bounds{};shape->GetAabbImpl(transform,0,bounds);alignas(16) float min[4],max[4];_mm_store_ps(min,bounds.min.quad);_mm_store_ps(max,bounds.max.quad);
  Vec minimum{min[0]*scale,min[1]*scale,min[2]*scale},maximum{max[0]*scale,max[1]*scale,max[2]*scale};if(!guardBounds(minimum,maximum,0))return {};
  lo={std::min(lo.x,minimum.x),std::min(lo.y,minimum.y),std::min(lo.z,minimum.z)};hi={std::max(hi.x,maximum.x),std::max(hi.y,maximum.y),std::max(hi.z,maximum.z)};found=true;
 }
 if(!found)return {};Vec feet=from(actor->GetPosition());
 // These limits validate the unit conversion/controller origin, and fail
 // closed for unobservable or unrelated shape data rather than guessing.
 if(feet.x<lo.x-16||feet.x>hi.x+16||feet.y<lo.y-16||feet.y>hi.y+16||std::abs(feet.z-lo.z)>64||length(hi-lo)>4000)return {};
 return guardBounds(lo,hi,margin);
}
bool visible(RE::Actor* actor,RE::Actor* guard,Vec origin){
 if(!alive(actor)||!loaded(guard))return false;auto bounds=physicalBounds(actor,0);if(!bounds)return false;Vec p=bounds->feet+Vec{0,0,bounds->height*.5};Vec d=p-origin;double n=length(d);if(n<1)return true;
 auto cell=guard->GetParentCell();auto r=ray(cell?cell->GetbhkWorld():nullptr,origin,p-d*(32/n));return r.known&&(!r.hit||r.ref==actor->GetFormID());
}
Mat align(Vec a,Vec b){
 a=a*(1/length(a));b=b*(1/length(b));Vec v=cross(a,b);double c=dot(a,b);if(c>.999999)return {};if(c<-.9999)return {{NAN,0,0,0,1,0,0,0,1}};
 Mat k{{0,-v.z,v.y,v.z,0,-v.x,-v.y,v.x,0}},k2=k*k,r;for(int i=0;i<9;++i)r.m[i]+=k.m[i]+k2.m[i]/(1+c);return r;
}
bool rotateBone(RE::NiAVObject* bone,Vec fromDir,Vec toDir){
 if(!bone||!bone->parent||length(fromDir)<.1||length(toDir)<.1)return false;Mat correction=align(fromDir,toDir),parent=from(bone->parent->world.rotate);
 Mat local=parent.transpose()*correction*parent*from(bone->local.rotate);if(!finite({local,{},1}))return false;bone->local.rotate=into(local);transforms(bone);return true;
}
}
void GuardRuntime::install(){
 if(installed_)return;
 runtime=this;auto module=REX::W32::GetModuleHandleA("OpenAnimationReplacer.dll");auto request=reinterpret_cast<OAR_API::Animations::Request>(module?REX::W32::GetProcAddress(module,"RequestPluginAPI_Animations"):nullptr);
  if(request)oar_=request(OAR_API::Animations::InterfaceVersion::V1,"AstraSight",REL::Version{3,5,9,0});
 REL::Relocation<uintptr_t> playerTable(RE::VTABLE_PlayerCharacter[0]),characterTable(RE::VTABLE_Character[0]),clipTable(RE::VTABLE_hkbClipGenerator[0]);
 playerOriginal=playerTable.write_vfunc(0xAD,playerPump);characterOriginal=characterTable.write_vfunc(0xAD,actorPost);clipOriginal=clipTable.write_vfunc(0x17,clipGenerated);
 installed_=true;spdlog::info("AstraGuardNative API1 frame pump PlayerCharacter::Update (0xAD), main station pump pose/IK; Character::Update telemetry only; OAR Animations V1={} (module loaded={})",oar_!=nullptr,module!=nullptr);
}
bool GuardRuntime::available()const{return installed_&&oar_;}
GuardRuntime::Slot* GuardRuntime::find(Key key){for(auto& s:slots_)if(s.lease.ticket().key==key&&s.lease.ticket())return &s;return nullptr;}
bool GuardRuntime::stationIdle(uint32_t handle){std::lock_guard lock(mutex_);for(auto& s:slots_)if(s.lease.ticket()&&s.lease.ticket().key.handle==handle)return false;return true;}
bool GuardRuntime::admitPlayer(uint32_t handle,const std::function<bool()>& begin){std::lock_guard lock(mutex_);return stationIdle(handle)&&begin();}
bool GuardRuntime::begin(RE::TESObjectREFR* gun,RE::Actor* actor,int token,RE::TESObjectWEAP* weapon,RE::TESAmmo* ammo,RE::TESSound* sound){
 std::lock_guard lock(mutex_);if(!available()||token<=0||!station(gun,actor)||!weapon||!ammo||!ammo->data.projectile||!sound)return false;
 Key key{gun->CreateRefHandle().native_handle(),token};if(!stationIdle(key.handle)||(playerOwns_&&playerOwns_(key.handle)))return false;
 for(auto& s:slots_)if(s.lease.ticket()&&s.actor==actor->GetFormID())return false;
 for(size_t i=0;i<slots_.size();++i){auto& s=slots_[i];if(s.lease.ticket())continue;auto lease=s.lease;s=Slot{};s.lease=lease;if(!s.lease.begin(key,actor->CreateRefHandle().native_handle()))return false;
  s.gun=gun->GetFormID();s.actor=actor->GetFormID();s.weapon=weapon->GetFormID();s.ammo=ammo->GetFormID();s.sound=sound->GetFormID();s.status=0;s.entered=clock_;s.cycle.acquire(clock_);return true;}
 return false;
}
int GuardRuntime::status(Key key){std::lock_guard lock(mutex_);auto s=find(key);if(s)return s->status;for(auto& old:slots_)if(old.retired==key)return old.status;return -1;}
bool GuardRuntime::end(Key key){std::lock_guard lock(mutex_);auto s=find(key);if(!s){for(auto& old:slots_)if(old.retired==key)old.status=-1;return true;}cancel(*s,false,"end request");return false;}
bool GuardRuntime::notify(Key key,RE::Actor* target){std::lock_guard lock(mutex_);auto s=find(key);if(!s||s->lease.pending()||!target)return false;s->advisory=target->GetFormID();return true;}
void GuardRuntime::cancel(Slot& s,bool fault,const char* reason){if(s.lease.pending())return;s.fault=fault;s.status=fault?-2:4;s.cycle.interrupt();s.lease.cancel();spdlog::info("guard cancel gun={:08X} token={} epoch={} fault={} reason={}",s.gun,s.lease.ticket().key.token,s.lease.ticket().epoch,fault,reason);}
void GuardRuntime::invalidate(){std::lock_guard lock(mutex_);auto main=RE::Main::GetSingleton();bool gameThread=main&&main->threadID==REX::W32::GetCurrentThreadId();for(auto& s:slots_)if(s.lease.ticket()){cancel(s,false,"load/new game/revert");if(gameThread)cleanup(s);}}
void GuardRuntime::menu(const RE::MenuOpenCloseEvent* e){if(e&&e->opening)invalidate();}
bool GuardRuntime::blocked()const{auto ui=RE::UI::GetSingleton();if(!ui||ui->GameIsPaused())return true;for(auto name:std::array<std::string_view,13>{"InventoryMenu","MagicMenu","MapMenu","Journal Menu","TweenMenu","Console","Dialogue Menu","Loading Menu","BarterMenu","ContainerMenu","FavoritesMenu","Sleep/Wait Menu","MessageBoxMenu"})if(ui->IsMenuOpen(name))return true;auto main=RE::Main::GetSingleton();return !main||main->freezeTime||main->freezeNextFrame;}
bool GuardRuntime::context(Slot& s,RE::NiPointer<RE::TESObjectREFR>& gun,RE::NiPointer<RE::Actor>& actor){
 auto t=s.lease.ticket();RE::RefHandle g=t.key.handle,a=s.lease.actor();RE::NiPointer<RE::TESObjectREFR> refr;RE::LookupReferenceByHandle(g,gun);RE::LookupReferenceByHandle(a,refr);if(refr){if(auto p=refr->As<RE::Actor>())actor.reset(p);}
 auto fail=[&](const char* reason){
  s.failure=reason;auto process=actor?actor->GetActorRuntimeData().currentProcess:nullptr;auto state=actor?actor->AsActorState():nullptr;
  auto assigned=process?process->currentPackage.package:nullptr;auto running=process?process->GetRunningPackage():nullptr;
  auto once=process&&process->middleHigh?process->middleHigh->runOncePackage.package:nullptr;auto activeIdle=process&&process->high?process->high->currentProcessIdle:nullptr;
  auto shield=actorShield(actor.get());auto gunCell=gun?gun->GetParentCell():nullptr;auto actorCell=actor?actor->GetParentCell():nullptr;
  spdlog::warn("guard v26 context gun={:08X} actor={:08X} token={} clause={} acquired={} assignedPackage={:08X} runningPackage={:08X} runOncePackage={:08X} idle={:08X} weaponDrawn={} weaponState={} shield={:08X} gunCell={:08X} actorCell={:08X} gunRootStable={} actorRootStable={} actorScale={} referenceScale={} baseHeight={}",
   s.gun,s.actor,t.key.token,reason,s.acquired,assigned?assigned->GetFormID():0,running?running->GetFormID():0,once?once->GetFormID():0,activeIdle?activeIdle->GetFormID():0,state?state->IsWeaponDrawn():false,state?int(state->GetWeaponState()):-1,shield?shield->GetFormID():0,
   gunCell?gunCell->GetFormID():0,actorCell?actorCell->GetFormID():0,gun&&(!s.root||s.root==reinterpret_cast<uintptr_t>(gun->Get3D())),actor&&(!s.actorRoot||s.actorRoot==reinterpret_cast<uintptr_t>(actor->Get3D())),actor?actor->GetScale():NAN,referenceScale(actor.get()),naturalHeight(actor.get()));
  return false;
 };
 if(!s.lease.current(t))return fail("lease no longer current");
 if(!loaded(gun.get()))return fail("station unloaded / disabled / deleted");
 if(!alive(actor.get()))return fail("operator dead / unloaded / disabled / deleted / zero health");
 if(interrupted(actor.get()))return fail("operator stagger / knock / life state / killmove");
 if(!station(gun.get(),actor.get()))return fail("station / operator ownership pair changed");
 if(gun->GetParentCell()!=actor->GetParentCell())return fail("operator and station cells differ");
 if(s.root&&s.root!=reinterpret_cast<uintptr_t>(gun->Get3D()))return fail("station scene identity changed");
 if(s.actorRoot&&s.actorRoot!=reinterpret_cast<uintptr_t>(actor->Get3D()))return fail("operator scene identity changed");
 if(actorShield(actor.get()))return fail("operator shield equipped");
 if(s.acquired)if(auto failure=operatorFailure(actor.get(),true))return fail(failure);
 if(s.acquired&&!guardNaturalScale(referenceScale(actor.get()),actor->GetScale(),naturalHeight(actor.get())))return fail("reference scale / natural height contract changed");
 if(s.acquired&&std::abs(actor->GetScale()-s.actorScale)>.001)return fail("effective actor scale changed during lease");
 if(playerOwns_&&playerOwns_(t.key.handle))return fail("player owns station");
 return true;
}
bool GuardRuntime::reject(Slot& s,RE::TESObjectREFR* gun,RE::Actor* actor,const char* reason){
 s.failure=reason;auto p=from(actor->GetPosition());auto g=from(gun->Get3D()->world.translate);auto pkg=actor->GetCurrentPackage();
 spdlog::warn("guard v26 reject gun={:08X} actor={:08X} token={} clause={} actorXYZ=({:.3f},{:.3f},{:.3f}) gunXYZ=({:.3f},{:.3f},{:.3f}) actorScale={} referenceScale={} baseHeight={} rootScale={} package={:08X} weaponDrawn={} weaponState={}",s.gun,s.actor,s.lease.ticket().key.token,reason,p.x,p.y,p.z,g.x,g.y,g.z,actor->GetScale(),referenceScale(actor),naturalHeight(actor),gun->Get3D()->world.scale,pkg?pkg->GetFormID():0,actor->AsActorState()->IsWeaponDrawn(),int(actor->AsActorState()->GetWeaponState()));
 return false;
}
bool GuardRuntime::requestClip(Slot& s,RE::Actor* actor,int clip){
 s.gripConfirmed=false;s.gripWaitSince=clock_;
 {std::lock_guard obsLock(observationsMutex_);observations_[size_t(&s-slots_.data())]={0,s.lease.ticket().epoch,frame_.load(),s.character};}
 for(size_t i=0;i<4;++i){auto f=faction(i);if(!f)return false;if(int(i)==clip||i==0)actor->AddToFaction(f,0);else actor->RemoveFromFaction(f);}
 auto api=static_cast<OAR_API::Animations::IAnimationsInterface1*>(oar_);if(!api||!idle()||!actor->GetActorRuntimeData().currentProcess)return false;
 api->ClearConditionStateData(actor);actor->NotifyAnimationGraph("IdleForceDefaultState");return actor->GetActorRuntimeData().currentProcess->PlayIdle(actor,idle(),nullptr);
}
bool GuardRuntime::acquire(Slot& s,RE::TESObjectREFR* gun,RE::Actor* actor){
 auto fail=[&](const char* reason){return reject(s,gun,actor,reason);};
 auto root=gun->Get3D();auto yaw=root->GetObjectByName("CTRL_GIRO_360"),pitch=root->GetObjectByName("CTRL_ELEVACION");auto muzzle=root->GetObjectByName("ProjectileNode"),bolt=root->GetObjectByName("VIROTE_VISUAL");
 if(auto failure=operatorFailure(actor))return fail(failure);
 if(actorShield(actor))return fail("operator shield equipped before acquisition");
 if(!yaw||!pitch||!muzzle||!bolt)return fail("required low-rig node missing");
 if(!gun->GetSequence("Fire")||!gun->GetSequence("Reset"))return fail("weapon Fire/Reset sequence missing");
 if(std::abs(root->world.scale-1)>.001||!guardNaturalScale(referenceScale(actor),actor->GetScale(),naturalHeight(actor)))return fail("station / reference scale or natural actor height invalid");
 s.actorScale=actor->GetScale();
 if(!actor->GetCharController())return fail("actor character controller absent");
 auto world=from(root->world);if(!finite(world)||std::abs(world.rotation.m[8]-1)>.001)return fail("station transform is not upright / finite");
 Vec facing{std::sin(actor->GetAngleZ()),std::cos(actor->GetAngleZ()),0};auto orbit=guardOrbit(from(actor->GetPosition()),world.translation,world.rotation,facing,referenceScale(actor));if(!orbit)return fail("actor outside radius151 / sector60 / support8");s.yaw=*orbit;
 // Both controlled nodes have identity rest rotations in the low NIF. Do
 // not use a saved live turn as the next lease's rest rotation.
 s.yawBase=Mat{};s.pitchBase=Mat{};
 yaw->local.rotate=into(s.yawBase);pitch->local.rotate=into(s.pitchBase);transforms(yaw);
 if(!finite(from(muzzle->world))||length(from(muzzle->world.rotate)*Vec{0,1,0}-world.rotation*gunDirection(0,0))>.001)return fail("muzzle rest orientation disagrees with horizontal bore");
 Vec feet=world.translation+world.rotation*rz(rad(s.yaw))*Vec{0,151,0};s.heightOffset=actor->GetPosition().z-feet.z;feet.z+=s.heightOffset;if(length(from(actor->GetPosition())-feet)>2)return fail("actor not on operator orbit");
 if(std::abs(actor->GetAngleX())>.01||std::abs(actor->GetAngleY())>.01)return fail("actor tilted away from upright posture");
 for(size_t i=0;i<4;++i){auto f=faction(i);if(!f)return fail("owned animation faction missing");s.ranks[i]=actor->IsInFaction(f)?actor->GetFactionRank(f,false):-1;}
 s.movement=actor->GetActorRuntimeData().boolFlags.all(RE::Actor::BOOL_FLAGS::kMovementBlocked);s.head=actor->AsActorState()->actorState2.headTracking;
 s.graphHeadSaved=actor->GetGraphVariableBool("bHeadTracking",s.graphHead);s.flagsSaved=true;actor->GetActorRuntimeData().boolFlags.set(RE::Actor::BOOL_FLAGS::kMovementBlocked);actor->AsActorState()->actorState2.headTracking=false;if(s.graphHeadSaved)actor->SetGraphVariableBool("bHeadTracking",false);
 RE::BSTSmartPointer<RE::BSAnimationGraphManager> manager;if(!actor->GetAnimationGraphManager(manager)||!manager||manager->graphs.empty())return fail("animation graph manager / graphs absent");
 {RE::BSSpinLockGuard graphLock(manager->GetRuntimeData().updateLock);auto index=manager->GetRuntimeData().activeGraph;if(index>=manager->graphs.size()||!manager->graphs[index])return fail("active animation graph absent");s.character=reinterpret_cast<uintptr_t>(&manager->graphs[index]->characterInstance);}
 s.root=reinterpret_cast<uintptr_t>(root);s.actorRoot=reinterpret_cast<uintptr_t>(actor->Get3D());
 {std::lock_guard obsLock(observationsMutex_);auto index=size_t(&s-slots_.data());observations_[index]={0,s.lease.ticket().epoch,frame_.load(),s.character};}
 if(!pose(s,gun,actor,s.yaw))return false;
 if(!requestClip(s,actor,0))return fail("OAR / process / hold PlayIdle request rejected");
 s.acquired=true;s.phaseAt=s.lastTime=clock_;watchedActors_[size_t(&s-slots_.data())].store(s.actor);auto running=actor->GetCurrentPackage();spdlog::info("guard v26 acquired gun={:08X} actor={:08X} package={:08X} yaw={} heightOffset={} supportZ={} actorScale={} referenceScale={} baseHeight={} holdRequested=true",s.gun,s.actor,running?running->GetFormID():0,s.yaw,s.heightOffset,s.supportZ,s.actorScale,referenceScale(actor),naturalHeight(actor));return true;
}
void GuardRuntime::observe(RE::hkbClipGenerator* clip,const RE::hkbContext& ctx){
 if(!clip||!ctx.character||!oar_||!clip->animationControl||!clip->animationControl->binding||!clip->animationControl->binding->animation)return;
 size_t index=observations_.size();uint64_t epoch=0;auto character=reinterpret_cast<uintptr_t>(ctx.character);
 {std::lock_guard lock(observationsMutex_);for(size_t i=0;i<observations_.size();++i)if(observations_[i].character==character){index=i;epoch=observations_[i].epoch;break;}}
 if(index==observations_.size())return;
 // Generate may run on a worker. Do not hold our mutex across OAR calls:
 // condition invalidation on the main thread can acquire OAR's own locks.
 auto info=static_cast<OAR_API::Animations::IAnimationsInterface1*>(oar_)->GetCurrentReplacementAnimationInfo(clip);
 int kind=guardClipKind(info.animationPath.c_str(),info.modName.c_str(),info.subModName.c_str());
 double weight=clip->animationControl->weight;
 if(kind<0||!std::isfinite(weight)||weight<.99||weight>1.001)return;
 std::lock_guard lock(observationsMutex_);auto& o=observations_[index];
 if(o.character!=character||o.epoch!=epoch)return;
 o.clip=kind;o.time=clip->localTime;o.duration=clip->animationControl->binding->animation->duration;o.weight=weight;o.frame=frame_.load();o.serial=++observationSerial_;
}
bool GuardRuntime::pose(Slot& s,RE::TESObjectREFR* gun,RE::Actor* actor,double yawValue){
 auto fail=[&](const char* reason){return reject(s,gun,actor,reason);};
 auto root=gun->Get3D();auto yaw=root->GetObjectByName("CTRL_GIRO_360"),pitch=root->GetObjectByName("CTRL_ELEVACION");if(!yaw||!pitch||std::abs(yawValue)>60)return fail("pose node / yaw invalid");
 Transform world=from(root->world);if(!finite(world)||std::abs(world.scale-1)>.001||std::abs(world.rotation.m[8]-1)>.001||!std::isfinite(yawValue+s.heightOffset))return fail("mounted station transform changed / nonfinite");
 Vec p=world.translation+world.rotation*rz(rad(yawValue))*Vec{0,151,0};p.z+=s.heightOffset;auto cell=gun->GetParentCell();auto physics=cell?cell->GetbhkWorld():nullptr;
 auto controller=actor->GetCharController();auto bound=physicalBounds(actor,0);if(!controller||!bound)return fail("live operator controller / physical bounds unknown");uint32_t filter=0;controller->GetCollisionFilterInfo(filter);if(!filter)return fail("operator collision filter unknown");
 // Use the operator's actual filter, including its own collision group, as
 // Skyrim's controller support rays do. A residual self-hit never proves floor.
 auto floor=ray(physics,p+Vec{0,0,12},p-Vec{0,0,12},RE::COL_LAYER::kLOS,filter);double floorZ=p.z+12-24*floor.fraction;
 if(!floor.known||!floor.hit||floor.ref==actor->GetFormID()||!guardSupport(p.z,floorZ,floor.normal.z,s.supportSaved?std::optional<double>{s.supportZ}:std::nullopt)){
  spdlog::warn("guard v26 support gun={:08X} filter={:08X} known={} hit={} hitRef={:08X} normalZ={} feetZ={} floorZ={} savedFloorZ={}",s.gun,filter,floor.known,floor.hit,floor.ref,floor.normal.z,p.z,floorZ,s.supportZ);return fail("floor support unknown / self-hit / slope / height changed");}
 if(!s.supportSaved){s.supportZ=floorZ;s.supportSaved=true;}
 // Fenced platform clearance: rays around the moving capsule at ankle and torso.
 Vec old=from(actor->GetPosition());if(length(old-p)>5||std::abs(old.z-p.z)>2)return fail("capsule move exceeds bounded horizontal step");
 if(length(old-p)>.01){double radius=bound->radius;for(double z:std::array<double,3>{12,bound->height*.5,bound->height-12})for(int i=0;i<9;++i){Vec offset=i?Vec{radius*std::cos(2*std::numbers::pi*(i-1)/8),radius*std::sin(2*std::numbers::pi*(i-1)/8),z}:Vec{0,0,z};auto r=ray(physics,old+offset,p+offset,RE::COL_LAYER::kLOS,filter);if(!r.known||r.hit)return fail("operator swept clearance obstructed / unknown");}}
 auto ticket=s.lease.ticket();if(!s.lease.current(ticket))return false;
 RE::hkVector4 before{},after{};controller->GetPositionImpl(before,true);actor->SetPosition(into(p),true);controller->GetPositionImpl(after,true);
 alignas(16) float b[4],a[4];_mm_store_ps(b,before.quad);_mm_store_ps(a,after.quad);double inverseScale=RE::bhkWorld::GetWorldScaleInverse();Vec moved{(a[0]-b[0])*inverseScale,(a[1]-b[1])*inverseScale,(a[2]-b[2])*inverseScale};if(length(moved-(p-old))>1)return fail("actor/controller displacement mismatch");
 Vec f=world.rotation*rz(rad(yawValue))*Vec{0,-1,0};actor->SetRotationX(0);actor->SetRotationZ(float(std::atan2(f.x,f.y)));
 if(!s.lease.current(ticket)||actor->Get3D()!=reinterpret_cast<RE::NiAVObject*>(s.actorRoot))return false;
 yaw->local.rotate=into(rz(rad(yawValue))*s.yawBase);pitch->local.rotate=into(s.pitchBase);transforms(yaw);s.yaw=yawValue;
 if(length(from(actor->GetPosition())-p)>=1||!actor->GetCharController())return fail("actor pose did not settle");return true;
}
bool GuardRuntime::feetIK(Slot& s,RE::Actor* actor){
 if(s.status!=2)return true;auto root=actor->Get3D();if(!root||reinterpret_cast<uintptr_t>(root)!=s.actorRoot)return false;
 auto gun=RE::TESForm::LookupByID<RE::TESObjectREFR>(s.gun);if(!loaded(gun)||reinterpret_cast<uintptr_t>(gun->Get3D())!=s.root)return false;Vec pivot=from(gun->Get3D()->world.translate);
 for(int i=0;i<2;++i){bool lead=(s.stepDelta>0)?i==0:i==1;Vec target=guardFoot(s.feet[i],pivot,s.stepDelta,s.stepPhase,lead);
  auto hip=root->GetObjectByName(i==0?"NPC L Thigh [LThg]":"NPC R Thigh [RThg]"),knee=root->GetObjectByName(i==0?"NPC L Calf [LClf]":"NPC R Calf [RClf]"),foot=root->GetObjectByName(i==0?"NPC L Foot [Lft ]":"NPC R Foot [Rft ]");if(!hip||!knee||!foot)return false;
  Vec h=from(hip->world.translate),k=from(knee->world.translate),f=from(foot->world.translate);auto solution=guardLeg(h,k,f,target);if(!solution||!rotateBone(hip,k-h,solution->knee-h))return false;
  k=from(knee->world.translate);f=from(foot->world.translate);if(!rotateBone(knee,f-k,target-k)||!foot->parent)return false;
  double u=lead?std::clamp(2*s.stepPhase,0.,1.):std::clamp(2*s.stepPhase-1,0.,1.);double smooth=u*u*(3-2*u);Mat rotation=rz(rad(s.stepDelta*smooth))*s.footRotation[i];foot->local.rotate=into(from(foot->parent->world.rotate).transpose()*rotation);transforms(foot);
  if(length(from(foot->world.translate)-target)>1)return false;
 }return true;
}
bool GuardRuntime::observationFresh(const Slot& s,const Observation& obs)const{
 return guardPoseFresh(obs,s.lease.ticket().epoch,s.character,frame_.load(),obs.clip);
}
bool GuardRuntime::gripIK(Slot& s,RE::TESObjectREFR* gun,RE::Actor* actor,const Observation& obs){
 auto root=actor->Get3D();if(!root||reinterpret_cast<uintptr_t>(root)!=s.actorRoot||!loaded(gun)||reinterpret_cast<uintptr_t>(gun->Get3D())!=s.root)return false;
 auto world=from(gun->Get3D()->world);
 for(int i=0;i<2;++i){
  auto shoulder=root->GetObjectByName(i==0?"NPC L UpperArm [LUar]":"NPC R UpperArm [RUar]");
  auto elbow=root->GetObjectByName(i==0?"NPC L Forearm [LLar]":"NPC R Forearm [RLar]");
  auto hand=root->GetObjectByName(i==0?"NPC L Hand [LHnd]":"NPC R Hand [RHnd]");
  auto target=guardGrip(world.translation,world.rotation,s.yaw,i==0,obs.clip==1?obs.time:-1);
  if(!shoulder||!elbow||!hand||!hand->parent||!target)return reject(s,gun,actor,"canonical hand / arm bones unavailable");
  Vec h=from(shoulder->world.translate),k=from(elbow->world.translate),f=from(hand->world.translate);double error=length(*target-f);
  // Only correct the small natural-height discrepancy of the authored pose.
  // Never pull a vanilla, weapon, stagger or transitional pose onto a handle.
  if(!std::isfinite(error)||error>16){spdlog::warn("guard v26 grip mismatch gun={:08X} actor={:08X} side={} error={} phase={} clip={}",s.gun,s.actor,i,error,obs.time,obs.clip);return reject(s,gun,actor,"canonical grip correction exceeds 16 units");}
  Mat rotation=from(hand->world.rotate);auto solution=guardLeg(h,k,f,*target);
  if(!solution||!rotateBone(shoulder,k-h,solution->knee-h))return reject(s,gun,actor,"upper arm grip IK unreachable");
  k=from(elbow->world.translate);f=from(hand->world.translate);
  if(!rotateBone(elbow,f-k,*target-k))return reject(s,gun,actor,"forearm grip IK unreachable");
  hand->local.rotate=into(from(hand->parent->world.rotate).transpose()*rotation);transforms(hand);
  if(length(from(hand->world.translate)-*target)>1)return reject(s,gun,actor,"hand did not settle on crank");
 }
 return true;
}
void GuardRuntime::postActor(RE::Actor* actor){
 // Diagnostic only: actor updates have no main-thread/post-pose guarantee.
 // Never resolve handles, touch scene/physics or acquire our slot lock here.
 if(!actor)return;auto id=actor->GetFormID();
 for(size_t i=0;i<watchedActors_.size();++i)if(watchedActors_[i].load(std::memory_order_relaxed)==id){
  auto main=RE::Main::GetSingleton();if(main&&main->threadID==REX::W32::GetCurrentThreadId())postMain_[i].fetch_add(1,std::memory_order_relaxed);else postWorker_[i].fetch_add(1,std::memory_order_relaxed);
 }
}
bool GuardRuntime::settleGrip(Slot& s,RE::TESObjectREFR* gun,RE::Actor* actor,const Observation& obs){
 // Called only by the existing main-thread station pump, before aim/fire.
 // OAR identity alone is insufficient: the live hands must settle within the
 // same bounded geometry contract. No Character::Update callback is required.
 bool wasGrip=s.gripConfirmed;s.gripConfirmed=false;
 int expected=s.status==3?1:s.status==2?(s.stepDelta>0?2:3):0;
 size_t index=size_t(&s-slots_.data());auto frame=frame_.load();
 if(clock_>=s.nextPoseLog){
  auto left=actor->Get3D()->GetObjectByName("NPC L Hand [LHnd]");auto right=actor->Get3D()->GetObjectByName("NPC R Hand [RHnd]");auto world=from(gun->Get3D()->world);
  auto lt=guardGrip(world.translation,world.rotation,s.yaw,true,obs.clip==1?obs.time:-1);auto rt=guardGrip(world.translation,world.rotation,s.yaw,false,obs.clip==1?obs.time:-1);
  spdlog::info("guard v28 pose pump gun={:08X} actor={:08X} frame={} sampleFrame={} serial={} expected={} clip={} phase={} characterMain={} characterWorker={} handErrorL={} handErrorR={}",s.gun,s.actor,frame,obs.frame,obs.serial,expected,obs.clip,obs.time,postMain_[index].load(),postWorker_[index].load(),left&&lt?length(from(left->world.translate)-*lt):-1,right&&rt?length(from(right->world.translate)-*rt):-1);
  s.nextPoseLog=clock_+2;
 }
 if(!guardPoseFresh(obs,s.lease.ticket().epoch,s.character,frame,expected)){
  if(clock_-s.gripWaitSince>1.5){cancel(s,true,"main pose pump: expected OAR clip unavailable before grip deadline");return false;}
  return true;
 }
 if(!feetIK(s,actor)){cancel(s,true,"main pose pump: lower skeleton IK unreachable");return false;}
 if(!gripIK(s,gun,actor,obs)){cancel(s,true,s.failure);return false;}
 s.gripConfirmed=true;s.gripFrame=frame;s.gripWaitSince=clock_;
 if(!wasGrip)spdlog::info("guard v28 grip confirmed on main pump gun={:08X} actor={:08X} epoch={} clip={} phase={} frame={}",s.gun,s.actor,s.lease.ticket().epoch,obs.clip,obs.time,frame);
 return true;
}
void GuardRuntime::targets(Slot& s,RE::TESObjectREFR* gun,RE::Actor* guard){
 auto root=gun->Get3D();auto muzzle=root->GetObjectByName("ProjectileNode");auto process=RE::ProcessLists::GetSingleton();if(!muzzle||!process){s.target=0;return;}
 auto forms=RE::TESDataHandler::GetSingleton();auto town=forms?forms->LookupForm<RE::TESFaction>(0x28172,"Skyrim.esm"):nullptr;auto localGuard=forms?forms->LookupForm<RE::TESFaction>(0x2BE39,"Skyrim.esm"):nullptr;
 if(!town||!localGuard){s.target=0;s.nextScan=clock_+.2;return;}
 std::vector<GuardCandidate> candidates;bool overflow=false;unsigned visited=0;process->ForAllActors([&](RE::Actor* a){if(++visited>512||candidates.size()>=256){overflow=true;return RE::BSContainer::ForEachResult::kStop;}if(a==guard||ownedOperator(a)||!alive(a))return RE::BSContainer::ForEachResult::kContinue;
  Vec p=from(a->GetPosition());if(length(p-from(root->world.translate))>6200||a->GetParentCell()->GetbhkWorld()!=gun->GetParentCell()->GetbhkWorld())return RE::BSContainer::ForEachResult::kContinue;
  auto bounds=physicalBounds(a,0);if(!bounds)return RE::BSContainer::ForEachResult::kContinue;p=bounds->feet+Vec{0,0,bounds->height*.5};
  candidates.push_back({a->GetFormID(),p,true,visible(a,guard,from(muzzle->world.translate)),a->IsHostileToActor(guard),a->IsInCombat(),a==RE::PlayerCharacter::GetSingleton(),a->IsPlayerTeammate(),bounds->height*.5,a->IsInFaction(town)||a->IsInFaction(localGuard)});return RE::BSContainer::ForEachResult::kContinue;});
 // Player may not occur in ProcessLists::ForAllActors.
 auto player=RE::PlayerCharacter::GetSingleton();if(alive(player)&&std::none_of(candidates.begin(),candidates.end(),[&](auto& c){return c.id==player->GetFormID();})){auto bounds=physicalBounds(player,0);if(bounds)candidates.push_back({player->GetFormID(),bounds->feet+Vec{0,0,bounds->height*.5},true,visible(player,guard,from(muzzle->world.translate)),false,false,true,false,bounds->height*.5});}
 s.target=overflow?0:selectGuardTarget(candidates,s.target,from(root->world.translate),from(root->world.rotate),from(muzzle->world.translate)).value_or(0);s.nextScan=clock_+.2;s.advisory=0;
}
bool GuardRuntime::shoot(Slot& s,RE::TESObjectREFR* gun,RE::Actor* guard,double bodyTime){
 // Everything below is in the main-thread effects scope. Resolve forms/handles
 // afresh and validate immediately adjacent to Projectile::Launch.
 auto target=RE::TESForm::LookupByID<RE::Actor>(s.target);auto ammo=RE::TESForm::LookupByID<RE::TESAmmo>(s.ammo);auto weapon=RE::TESForm::LookupByID<RE::TESObjectWEAP>(s.weapon);auto sound=RE::TESForm::LookupByID<RE::TESSound>(s.sound);
 if(s.launched||s.status!=3||!s.fireObserved||!guardGripFresh(s.gripConfirmed,frame_.load(),s.gripFrame)||!enemy(target,guard)||!ammo||!weapon||!sound||!ammo->data.projectile)return false;
 if(!loaded(target)||target->GetParentCell()->GetbhkWorld()!=gun->GetParentCell()->GetbhkWorld())return false;
 auto proj=ammo->data.projectile;if(std::abs(proj->data.speed-5400)>.01||std::abs(proj->data.gravity*9.81*70-240.345)>.1||!proj->IsArrow()||proj->data.flags.any(RE::BGSProjectileData::BGSProjectileFlags::kHitScan))return false;
 double blast=0;if(proj->data.flags.any(RE::BGSProjectileData::BGSProjectileFlags::kExplosion)){auto explosion=proj->data.explosionType;if(!explosion||explosion->data.spawnProjectile||explosion->data.flags.any(RE::BGSExplosionData::Flag::kChain)||explosion->data.verticalOffsetMult!=0)return false;blast=explosion->data.radius;if(!std::isfinite(blast)||blast<0)return false;}
 auto root=gun->Get3D();auto node=root->GetObjectByName("ProjectileNode");auto targetBounds=physicalBounds(target,0);if(!node||!finite(from(node->world))||!targetBounds)return false;Vec muzzle=from(node->world.translate),bore=from(node->world.rotate)*Vec{0,1,0};Vec delta=targetBounds->feet+Vec{0,0,targetBounds->height*.5}-muzzle;
 double seconds=std::hypot(delta.x,delta.y)/5400;if(!horizontalFlight(delta,5400,240.345,targetBounds->height*.5)||!visible(target,guard,muzzle))return false;
 if(!guardProjectileContract(proj->data.speed,proj->data.gravity*9.81*70,proj->data.collisionRadius,proj->data.range,proj->data.lifetime,proj->data.explosionProximity,proj->data.explosionTimer,proj->data.coneSpread,proj->data.flags.any(RE::BGSProjectileData::BGSProjectileFlags::kExplosionAltTrigger),seconds))return false;
 Vec horizontal{delta.x,delta.y,0};if(length(horizontal)<64)return false;horizontal=horizontal*(1/length(horizontal));if(length(bore-horizontal)>.006||std::abs(bore.z)>.001)return false;
 auto path=guardTrajectory(muzzle,bore,seconds,5400,240.345);auto cell=gun->GetParentCell();auto world=cell?cell->GetbhkWorld():nullptr;if(!world||path.size()<2)return false;
 std::vector<GuardProtected> protect;auto process=RE::ProcessLists::GetSingleton();if(!process)return false;bool unknown=false;unsigned visited=0;
 process->ForAllActors([&](RE::Actor* a){if(++visited>512||protect.size()>=256){unknown=true;return RE::BSContainer::ForEachResult::kStop;}if(!alive(a)||a==target||enemy(a,guard))return RE::BSContainer::ForEachResult::kContinue;
  auto bounds=physicalBounds(a);if(!bounds){unknown=true;return RE::BSContainer::ForEachResult::kStop;}protect.push_back(*bounds);return RE::BSContainer::ForEachResult::kContinue;});
 auto player=RE::PlayerCharacter::GetSingleton();if(!alive(player))return false;auto playerBounds=physicalBounds(player),guardBounds=physicalBounds(guard);if(!playerBounds||!guardBounds||unknown)return false;protect.push_back(*playerBounds);protect.push_back(*guardBounds);
 // Follow the entire predicted trajectory to its first live target contact.
 // Any earlier obstruction or an unobserved impact leaves safety unknown.
 bool impact=false;for(size_t i=1;i<path.size();++i){auto r=ray(world,path[i-1],path[i],RE::COL_LAYER::kProjectile);if(!r.known)return false;if(r.hit){Vec hit=path[i-1]+(path[i]-path[i-1])*r.fraction;Vec feet=targetBounds->feet;if(r.ref!=target->GetFormID()||std::hypot(hit.x-feet.x,hit.y-feet.y)>targetBounds->radius||hit.z<feet.z||hit.z>feet.z+targetBounds->height)return false;path[i]=hit;path.resize(i+1);impact=true;break;}}
 if(!impact||!guardPathSafe(path,protect,blast))return false;
 RE::NiPointer<RE::TESObjectREFR> liveGun;RE::NiPointer<RE::Actor> liveGuard;if(!context(s,liveGun,liveGuard)||liveGun.get()!=gun||liveGuard.get()!=guard||!guardGripFresh(s.gripConfirmed,frame_.load(),s.gripFrame)||!enemy(target,guard)||!visible(target,guard,muzzle)||s.stepPhase!=0)return false;
 auto liveTargetBounds=physicalBounds(target,0);if(!liveTargetBounds||length(liveTargetBounds->feet-targetBounds->feet)>.01||std::abs(liveTargetBounds->height-targetBounds->height)>.01||std::abs(liveTargetBounds->radius-targetBounds->radius)>.01)return false;
 auto liveMuzzle=gun->Get3D()->GetObjectByName("ProjectileNode");if(!liveMuzzle||length(from(liveMuzzle->world.translate)-muzzle)>.01||length(from(liveMuzzle->world.rotate)*Vec{0,1,0}-bore)>.001)return false;
 auto fire=gun->GetSequence("Fire");if(!fire||!fire->Animating()||!std::isfinite(fire->lastScaledTime)||std::abs(double(fire->lastScaledTime)-bodyTime)>.05||!s.cycle.release(clock_,bodyTime,true))return false;
 RE::ProjectileHandle handle;RE::Projectile::ProjectileRot angles{0,float(std::atan2(bore.x,bore.y))};RE::Projectile::LaunchData launch(guard,into(muzzle),angles,ammo,weapon);
 launch.autoAim=false;launch.alwaysHit=false;launch.useOrigin=true;launch.forceConeOfFire=false;launch.desiredTarget=nullptr;
 // Nothing that can queue another VM action intervenes between lease/pose/
 // target safety revalidation above and the real engine commitment.
 RE::Projectile::Launch(&handle,launch);s.launched=true;auto projectile=handle.get();if(!projectile){cancel(s,true,"engine launch returned no projectile");return false;}
 auto& data=projectile->GetProjectileRuntimeData();auto corrected=speedMultiplierCorrection(5400,projectile->GetSpeed(),data.speedMult);if(!corrected){cancel(s,true,"projectile speed scalar unknown");return false;}data.speedMult=float(*corrected);data.linearVelocity=into(bore*5400);
 if(!s.lease.current(s.lease.ticket()))return true;auto bolt=root->GetObjectByName("VIROTE_VISUAL");if(bolt){bolt->local.scale=0;transforms(bolt);}RE::BSSoundHandle snd;auto audio=RE::BSAudioManager::GetSingleton();if(audio&&sound->descriptor&&audio->BuildSoundDataFromDescriptor(snd,sound->descriptor)){snd.SetPosition(into(muzzle));snd.SetObjectToFollow(root);snd.Play();}
 spdlog::info("guard real projectile gun={:08X} guard={:08X} target={:08X} token={} epoch={} handle={} phase={:.6f} speed=5400 blast={}",s.gun,s.actor,s.target,s.lease.ticket().key.token,s.lease.ticket().epoch,handle.native_handle(),bodyTime,blast);return true;
}
void GuardRuntime::cleanup(Slot& s){
 watchedActors_[size_t(&s-slots_.data())].store(0);
 s.lease.enterEffect();auto actor=RE::TESForm::LookupByID<RE::Actor>(s.actor);auto gun=RE::TESForm::LookupByID<RE::TESObjectREFR>(s.gun);
 if(actor&&s.flagsSaved){for(size_t i=0;i<4;++i)if(auto f=faction(i)){if(s.ranks[i]<0)actor->RemoveFromFaction(f);else actor->AddToFaction(f,int8_t(s.ranks[i]));}
  if(s.movement)actor->GetActorRuntimeData().boolFlags.set(RE::Actor::BOOL_FLAGS::kMovementBlocked);else actor->GetActorRuntimeData().boolFlags.reset(RE::Actor::BOOL_FLAGS::kMovementBlocked);
  actor->AsActorState()->actorState2.headTracking=s.head;if(s.graphHeadSaved&&actor->Get3D())actor->SetGraphVariableBool("bHeadTracking",s.graphHead);
  if(alive(actor)&&!interrupted(actor)){auto p=actor->GetActorRuntimeData().currentProcess;if(p&&idle(true))p->PlayIdle(actor,idle(true),nullptr);else actor->NotifyAnimationGraph("IdleForceDefaultState");}
 }
 if(loaded(gun)&&reinterpret_cast<uintptr_t>(gun->Get3D())==s.root){auto root=gun->Get3D();auto fire=gun->GetSequence("Fire"),reset=gun->GetSequence("Reset");if(fire)fire->Deactivate(0,false);if(reset){reset->Deactivate(0,false);if(reset->Activate(0,true,1,0,nullptr,false))reset->SetPhase(1,true);}
  if(auto yaw=root->GetObjectByName("CTRL_GIRO_360")){yaw->local.rotate=into(s.yawBase);if(auto pitch=root->GetObjectByName("CTRL_ELEVACION"))pitch->local.rotate=into(s.pitchBase);transforms(yaw);}if(auto bolt=root->GetObjectByName("VIROTE_VISUAL")){bolt->local.scale=1;transforms(bolt);}
 }
 {std::lock_guard obsLock(observationsMutex_);observations_[size_t(&s-slots_.data())]={};}s.retired=s.lease.ticket().key;s.lease.leaveEffect();s.lease.complete();s.status=s.fault?-2:-1;s.character=0;s.root=s.actorRoot=0;s.flagsSaved=false;
}
void GuardRuntime::tick(float dt){
 auto main=RE::Main::GetSingleton();if(!main||main->threadID!=REX::W32::GetCurrentThreadId())return;
 std::lock_guard lock(mutex_);++frame_;bool pause=blocked();if(!pause&&std::isfinite(dt)&&dt>0&&dt<=.1)clock_+=dt;
 for(auto& s:slots_){if(!s.lease.ticket())continue;if(pause)cancel(s,false,"menu/pause");else if(!std::isfinite(dt)||dt<=0||dt>.1)cancel(s,true,"frame delta cannot preserve clip phase");if(s.lease.pending()){cleanup(s);continue;}
   RE::NiPointer<RE::TESObjectREFR> gun;RE::NiPointer<RE::Actor> actor;if(!context(s,gun,actor)){cancel(s,false,s.failure);cleanup(s);continue;}
  s.lease.enterEffect();if(!s.acquired){
   if(auto failure=operatorFailure(actor.get())){
    if(!s.packageRequested){s.packageRequested=true;actor->DrawWeaponMagicHands(false);actor->EvaluatePackage(true,false);}
    if(!operatorPackage()||clock_-s.entered>3){reject(s,gun.get(),actor.get(),failure);cancel(s,true,s.failure);}
   }else if(!acquire(s,gun.get(),actor.get()))cancel(s,true,s.failure);
   s.lease.leaveEffect();continue;}
  if(!pose(s,gun.get(),actor.get(),s.yaw)){cancel(s,true,s.failure);s.lease.leaveEffect();continue;}
  Observation obs;{std::lock_guard obsLock(observationsMutex_);obs=observations_[size_t(&s-slots_.data())];}
  if(!settleGrip(s,gun.get(),actor.get(),obs)){s.lease.leaveEffect();continue;}
  bool fresh=observationFresh(s,obs)&&obs.serial!=s.seen;
  if(fresh)s.seen=obs.serial;
  if(clock_>=s.nextScan&&s.status!=3)targets(s,gun.get(),actor.get());
  if(s.status==0||s.status==1){
   if(fresh&&obs.clip==0){bool wasReady=s.cycle.ready();s.cycle.observeHold(clock_,obs.time);s.lastTime=clock_;s.status=s.cycle.ready()?1:0;if(!wasReady&&s.cycle.ready())spdlog::info("guard v26 hold confirmed by OAR gun={:08X} actor={:08X} epoch={} phase={}",s.gun,s.actor,s.lease.ticket().epoch,obs.time);}
   else if(clock_-s.lastTime>.25){s.cycle.interrupt();s.status=0;if(clock_-s.phaseAt>1.5){if(s.recoveries++<2&&requestClip(s,actor.get(),0))s.phaseAt=clock_;else cancel(s,true,"hold replacement not observable");}}
   auto target=RE::TESForm::LookupByID<RE::Actor>(s.target);if(s.status==1&&guardGripFresh(s.gripConfirmed,frame_.load(),s.gripFrame)&&alive(target)){
    auto bounds=physicalBounds(target,0);if(!bounds){s.target=0;s.lease.leaveEffect();continue;}double desired=std::remainder(aimFromWorld(from(gun->Get3D()->world.rotate),bounds->feet-from(gun->Get3D()->world.translate)).yaw,360.);double error=desired-s.yaw;
    if(std::abs(error)>.25){s.stepStart=s.yaw;s.stepDelta=std::clamp(error,-12.,12.);s.stepPhase=0;bool limbs=true;for(int i=0;i<2;++i){auto foot=actor->Get3D()->GetObjectByName(i==0?"NPC L Foot [Lft ]":"NPC R Foot [Rft ]");if(!foot){limbs=false;break;}s.feet[i]=from(foot->world.translate);s.footRotation[i]=from(foot->world.rotate);}
     s.status=2;s.phaseAt=clock_;s.lastTime=-1;if(!limbs||!requestClip(s,actor.get(),s.stepDelta>0?2:3))cancel(s,true,"turn clip/feet unavailable");}
    else {auto muzzle=gun->Get3D()->GetObjectByName("ProjectileNode");bool reachable=muzzle&&horizontalFlight(bounds->feet+Vec{0,0,bounds->height*.5}-from(muzzle->world.translate),5400,240.345,bounds->height*.5).has_value();
     if(enemy(target,actor.get())&&reachable&&s.cycle.startFire(clock_)){s.status=3;s.phaseAt=clock_;s.fireObserved=false;s.launched=false;s.resetStarted=false;s.stepPhase=0;if(!requestClip(s,actor.get(),1))cancel(s,true,"body Fire request failed");}}
   }
  }else if(s.status==2){
   int kind=s.stepDelta>0?2:3;if(fresh&&obs.clip==kind){auto phase=guardStepPhase(s.stepPhase,obs.time,s.stepDelta,dt);if(s.lastTime<0&&obs.time>.05)cancel(s,true,"turn start missed");else if(!phase)cancel(s,true,"turn phase jump exceeds 15 degrees/s");else if(!pose(s,gun.get(),actor.get(),s.stepStart+s.stepDelta**phase)){cancel(s,true,"capsule floor/collision movement rejected");}else{s.stepPhase=*phase;s.lastTime=clock_;if(!feetIK(s,actor.get()))cancel(s,true,"partial turn IK rejected");
    if(*phase==1){s.stepPhase=0;s.status=0;s.cycle.interrupt();s.phaseAt=s.lastTime=clock_;if(!requestClip(s,actor.get(),0))cancel(s,true,"return hold failed");}}}
   if(clock_-s.phaseAt>1.2||(s.lastTime>=0&&clock_-s.lastTime>.2))cancel(s,true,"turn playback timeout");
  }else if(s.status==3){
   if(fresh&&obs.clip==1){if(!s.fireObserved){if(obs.time>.05||!s.cycle.synchronizeFire(clock_,obs.time))cancel(s,true,"body Fire start missed");else {s.fireObserved=true;s.fireStart=s.cycle.fireStart();
     auto fire=gun->GetSequence("Fire"),reset=gun->GetSequence("Reset");if(!fire||!reset||!std::isfinite(fire->endKeyTime+fire->beginKeyTime+reset->endKeyTime+reset->beginKeyTime)||std::abs((fire->endKeyTime-fire->beginKeyTime)-.2)>.01||std::abs((reset->endKeyTime-reset->beginKeyTime)-.8)>.01)cancel(s,true,"NIF Fire/Reset duration mismatch");else {reset->Deactivate(0,false);fire->Deactivate(0,false);if(!fire->Activate(0,true,1,0,nullptr,false))cancel(s,true,"NIF Fire activation failed");else fire->SetPhase(float(obs.time/.2),true);}
    }}
    if(s.fireObserved&&!s.lease.pending()){double t=clock_-s.fireStart;auto fire=gun->GetSequence("Fire");if(std::abs(t-obs.time)>.05)cancel(s,true,"body Fire game clock mismatch");else if(obs.time>=2./30.&&!s.launched&&obs.time<=2./30.+.05){if(!shoot(s,gun.get(),actor.get(),obs.time))s.launched=true;}
     if(t>=.2&&!s.resetStarted){auto reset=gun->GetSequence("Reset");if(fire)fire->Deactivate(0,false);if(!reset||!reset->Activate(0,true,1,0,nullptr,false))cancel(s,true,"NIF Reset failed");else s.resetStarted=true;}
     if(obs.time>=.96){if(auto reset=gun->GetSequence("Reset"))reset->SetPhase(1,true);if(auto bolt=gun->Get3D()->GetObjectByName("VIROTE_VISUAL")){bolt->local.scale=1;transforms(bolt);}s.cycle.interrupt();s.status=0;s.phaseAt=s.lastTime=clock_;if(!requestClip(s,actor.get(),0))cancel(s,true,"Fire recovery hold failed");}
    }
   }
   if(clock_-s.phaseAt>1.4||(!fresh&&clock_-s.phaseAt>.25))cancel(s,true,"body Fire playback unavailable");
  }
  s.lease.leaveEffect();
 }
}
}
