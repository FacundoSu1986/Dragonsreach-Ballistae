#include "Astra/GuardRuntime.h"
#include "Astra/FastShotRuntime.h"
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
RE::TESFaction* faction(size_t i){auto h=RE::TESDataHandler::GetSingleton();return h?h->LookupForm<RE::TESFaction>(factionIDs[i],"DragonsreachBallistae_GuardAnims.esp"):nullptr;}
RE::TESIdleForm* idle(bool exit=false){auto h=RE::TESDataHandler::GetSingleton();return h?h->LookupForm<RE::TESIdleForm>(exit?0x803:0x802,"DragonsreachBallistae_GuardAnims.esp"):nullptr;}
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
// v33.14: TESDataHandler::LookupForm(id, plugin) walks every plugin file (strlen + _strnicmp per file) on each call.
// ownedOperator() ran it twice for every loaded actor of every scan (targets, playerHunted, shot protection: thousands
// of plugin-list walks per second on the game thread in a city), and tickPosts twice per post per frame. The post ids
// are resolved once (a function-local static is thread-safe; the load order cannot change while the game runs).
struct PostIds{RE::FormID gun{},npc{};};
const std::array<PostIds,GuardMaxPosts>& resolvedPosts(){
 static const auto ids=[]{std::array<PostIds,GuardMaxPosts> out{};auto h=RE::TESDataHandler::GetSingleton();if(!h)return out;
  for(size_t i=0;i<GuardPosts.size();++i){out[i].gun=h->LookupFormID(GuardPosts[i].gun,GuardPosts[i].plugin);out[i].npc=GuardPosts[i].npc?h->LookupFormID(GuardPosts[i].npc,GuardPosts[i].plugin):0;}
  return out;}();
 return ids;
}
bool ownedOperator(RE::Actor* actor){if(!actor)return false;auto id=actor->GetFormID();for(auto& p:resolvedPosts())if(p.npc&&p.npc==id)return true;return false;}
double referenceScale(RE::Actor* actor){return actor?actor->GetReferenceRuntimeData().refScale*.01:NAN;}
double naturalHeight(RE::Actor* actor){auto base=actor?actor->GetActorBase():nullptr;return base?base->GetHeight():NAN;}
// v29.3: ForAllActors walks every loaded actor, not just nearby ones; 512 was reachable in a busy city and
// silently emptied the target list (overflow -> target 0). Bounds only the walk; the 256 candidate cap stays.
constexpr unsigned GuardActorScanCap=4096;
// v29.2: the player is an enemy only while the town guards are fighting them (`hunted`, see playerHunted).
// v33: at a bandit camp (`camp`) the player is an enemy on sight, with no combat state required.
bool enemy(RE::Actor* a,RE::Actor* guard,bool hunted=false,bool camp=false){
 if(!alive(a)||ownedOperator(a)||a->IsPlayerTeammate())return false;
 if(a==RE::PlayerCharacter::GetSingleton())return GuardAllowPlayerTarget&&(camp||(hunted&&a->IsInCombat()));
 return guard&&a->IsInCombat()&&a->IsHostileToActor(guard);
}
bool loaded(RE::TESObjectREFR* r){return r&&!r->IsDeleted()&&!r->IsDisabled()&&r->Get3D()&&r->GetParentCell();}
bool station(RE::TESObjectREFR* gun,RE::Actor* actor){
 auto h=RE::TESDataHandler::GetSingleton();if(!h||!gun||!actor||!gun->GetBaseObject())return false;
 auto base=h->LookupForm(0xB04,"DragonsreachBallistae.esp");if(!base||gun->GetBaseObject()!=base)return false;
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
#if ASTRA_RUNTIME_AE17
 pick.rayInput.filterInfo.filter=controllerFilter.value_or(uint32_t(layer));pick.rayInput.enableShapeCollectionFilter=true;
#else
 pick.rayInput.filterInfo=controllerFilter.value_or(uint32_t(layer));pick.rayInput.enableShapeCollectionFilter=true;
#endif
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
bool visible(RE::Actor* actor,RE::TESObjectREFR* viewer,Vec origin){
 if(!alive(actor)||!loaded(viewer))return false;auto bounds=physicalBounds(actor,0);if(!bounds)return false;Vec p=bounds->feet+Vec{0,0,bounds->height*.5};Vec d=p-origin;double n=length(d);if(n<1)return true;
 auto cell=viewer->GetParentCell();auto r=ray(cell?cell->GetbhkWorld():nullptr,origin,p-d*(32/n));return r.known&&(!r.hit||r.ref==actor->GetFormID());
}
// v29.1: live wrists against the grips the hold clip was authored for (about 3 u at Nord
// height 1.03). -1 = not measurable. Measurement only; used as evidence, never as a gate.
void handErrors(RE::TESObjectREFR* gun,RE::Actor* actor,double yaw,double* out){
 out[0]=out[1]=-1;auto root=gun?gun->Get3D():nullptr;auto body=actor?actor->Get3D():nullptr;if(!root||!body)return;auto world=from(root->world);
 for(int i=0;i<2;++i){auto hand=body->GetObjectByName(i==0?"NPC L Hand [LHnd]":"NPC R Hand [RHnd]");auto grip=guardGrip(world.translation,world.rotation,yaw,i==0);if(hand&&grip)out[i]=length(from(hand->world.translate)-*grip);}
}
// v29.2: some loaded, living guard of the town is fighting the player (the operator itself has isolated AI
// and never reports combat). Unverified against the engine: logged on every change by targets().
bool playerHunted(RE::Actor* operatorGuard){
 auto player=RE::PlayerCharacter::GetSingleton();auto process=RE::ProcessLists::GetSingleton();auto forms=RE::TESDataHandler::GetSingleton();
 if(!GuardAllowPlayerTarget||!alive(player)||!player->IsInCombat()||!process||!forms)return false;
 auto town=forms->LookupForm<RE::TESFaction>(0x28172,"Skyrim.esm");auto localGuard=forms->LookupForm<RE::TESFaction>(0x2BE39,"Skyrim.esm");if(!town||!localGuard)return false;
 bool found=false;unsigned visited=0;
 process->ForAllActors([&](RE::Actor* a){if(++visited>GuardActorScanCap)return RE::BSContainer::ForEachResult::kStop;
  if(a==operatorGuard||a==player||ownedOperator(a)||!alive(a)||!(a->IsInFaction(town)||a->IsInFaction(localGuard)))return RE::BSContainer::ForEachResult::kContinue;
  if(a->IsInCombat()&&a->IsHostileToActor(player)){found=true;return RE::BSContainer::ForEachResult::kStop;}
  return RE::BSContainer::ForEachResult::kContinue;});
 return found;
}
// v32: the guard rides in a basket (OPERADOR_SOPORTE) hung from the cradle's tail by two chains and kept upright by two
// guide posts fixed to the turntable, so the basket only moves vertically. Each frame: the chain's upper eye (a point of
// CTRL_ELEVACION) is taken into the yaw frame through the pitch node's local transform, the basket is placed so that the
// lower eye (a point of the basket, which never rotates) hangs exactly ChainLength below it, and each chain node is
// re-aimed from its lower eye to its upper eye. The numbers are those of scripts/build_operador_malla.py (CADENA_A,
// CADENA_B, CADENA_L; pivot z 117, yaw node z 99.5) and colgado() there is this function; tests/test_v31_operador_malla.py
// compares both. A NIF without the chain nodes (v31.x) keeps its support where it is.
struct ChainSpec{const char* node;Vec anchor;Vec foot;};      // anchor: CTRL_ELEVACION frame; foot: basket frame
const std::array<ChainSpec,2> chains{{
 {"CADENA_I",{42.0,143.0,82.0-117.0},{42.0,143.0,50.6-99.5}},
 {"CADENA_D",{-42.0,143.0,82.0-117.0},{-42.0,143.0,50.6-99.5}}}};
constexpr double ChainLength=82.0-50.6;
Mat rotationFromZ(Vec d){
 Mat r;if(d.z>1-1e-9)return r;
 if(d.z<-1+1e-9){r.m={{1,0,0,0,-1,0,0,0,-1}};return r;}
 double vx=-d.y,vy=d.x,k=1/(1+d.z);
 r.m={{1-k*vy*vy,k*vx*vy,vy, k*vx*vy,1-k*vx*vx,-vx, -vy,vx,1-k*(vx*vx+vy*vy)}};
 return r;
}
void hangBasket(RE::NiAVObject* root){
 auto basket=root?root->GetObjectByName("OPERADOR_SOPORTE"):nullptr,pitch=root?root->GetObjectByName("CTRL_ELEVACION"):nullptr;
 if(!basket||!pitch||!root->GetObjectByName(chains[0].node))return;
 Mat rp=from(pitch->local.rotate);Vec tp=from(pitch->local.translate);           // both nodes are children of CTRL_GIRO_360
 Vec a=rp*chains[0].anchor+tp;double dy=a.y-chains[0].foot.y,h=ChainLength*ChainLength-dy*dy;if(!std::isfinite(h)||h<=0)return;
 basket->local.translate=into(Vec{0,0,a.z-std::sqrt(h)-chains[0].foot.z});transforms(basket);
 Mat rb=from(basket->local.rotate);Vec tb=from(basket->local.translate);
 for(auto& c:chains){
  auto node=root->GetObjectByName(c.node);if(!node)continue;
  Vec d=rb.transpose()*(rp*c.anchor+tp-tb)-c.foot;double n=length(d);if(!std::isfinite(n)||n<1e-6)continue;
  node->local.translate=into(c.foot);node->local.rotate=into(rotationFromZ(d*(1/n)));transforms(node);
 }
}
// v33.6: evidence for "Mirmulnir leaves while the player is on the ballista". Once a second, mounted or not, every dragon
// in combat within 20000 u of the player: its target, distance, height over the player and flight state (0 none,
// 1 take-off, 2 cruising, 3 hovering, 4 landing, 5 perching, 6 action). Mounting/dismounting is in the "fast sight
// begin" / "sight end request" lines, so both situations can be compared on the same dragon.
double nextDragonWatch=0;
void watchDragons(double now){
 // v33.14: only while a dragon fights the player on a ballista (it ran for every dragon fight of the game).
 if(now<nextDragonWatch||!mountedDragonActive())return;nextDragonWatch=now+1.;
 auto player=RE::PlayerCharacter::GetSingleton();auto process=RE::ProcessLists::GetSingleton();auto forms=RE::TESDataHandler::GetSingleton();
 if(!player||!process||!forms||!player->GetParentCell())return;
 auto dragon=forms->LookupForm<RE::BGSKeyword>(0x35D59,"Skyrim.esm");if(!dragon)return;
 Vec at=from(player->GetPosition());unsigned visited=0;
 process->ForAllActors([&](RE::Actor* a){
  if(++visited>GuardActorScanCap)return RE::BSContainer::ForEachResult::kStop;
  auto race=a?a->GetRace():nullptr;if(!race||!race->HasKeyword(dragon)||a->IsDead()||!a->IsInCombat())return RE::BSContainer::ForEachResult::kContinue;
  Vec p=from(a->GetPosition());double d=length(p-at);if(d>20000)return RE::BSContainer::ForEachResult::kContinue;
  auto target=a->GetActorRuntimeData().currentCombatTarget.get();auto state=a->AsActorState();
  // v33.8: test 2026-10-17 07:56 - mounted, Mirmulnir hovered 16 s at 2498 u without attacking and struck at once after
  // the dismount. los/detect tell whether it cannot see the mounted player or simply chooses not to attack.
  bool losArg=false;bool los=a->HasLineOfSight(player,losArg);int detect=a->RequestDetectionLevel(player);
  // v33.11: test 13:03 - landed 423-656 u from the mounted player, target=player, los=true, detect 91-310, no attack for
  // 10-12 s; dismounted it engaged at once. attack/cast say whether it tries; sit/drawn whether the player looks engageable.
  auto ps=player->AsActorState();
  spdlog::info("dragon watch actor={:08X} target={:08X} distance={:.0f} above={:.0f} fly={} los={} detect={} attacking={} attack={} cast={} playerSit={} playerDrawn={} playerCombat={}",a->GetFormID(),target?target->GetFormID():0,d,p.z-at.z,state?static_cast<int>(state->GetFlyState()):-1,los,detect,
   a->IsAttacking(),state?static_cast<int>(state->GetAttackState()):-1,a->WhoIsCasting(),ps?static_cast<int>(ps->GetSitSleepState()):-1,ps&&ps->IsWeaponDrawn(),player->IsInCombat());
  return RE::BSContainer::ForEachResult::kContinue;});
}
// v29.2: elevation that puts the bolt on `target` (world), from the live pivot/muzzle geometry. The muzzle
// swings with the elevation, so its offset is expressed at pitch 0 (ahead of / above the pivot).
std::optional<GuardAim> aimAt(RE::TESObjectREFR* gun,Vec target){
 auto root=gun?gun->Get3D():nullptr;if(!root)return {};
 auto pivot=root->GetObjectByName("CTRL_ELEVACION"),muzzle=root->GetObjectByName("ProjectileNode");if(!pivot||!muzzle)return {};
 Vec bore=from(muzzle->world.rotate)*Vec{0,1,0};double horizontal=std::hypot(bore.x,bore.y);if(!std::isfinite(horizontal)||horizontal<.3)return {};
 Vec heading{bore.x/horizontal,bore.y/horizontal,0},offset=from(muzzle->world.translate)-from(pivot->world.translate);
 double pitch=std::asin(std::clamp(bore.z,-1.,1.)),ahead=dot(offset,heading),above=offset.z;
 return guardAimSolution(target-from(pivot->world.translate),ahead*std::cos(pitch)+above*std::sin(pitch),-ahead*std::sin(pitch)+above*std::cos(pitch));
}
}
void GuardRuntime::install(){
 if(installed_)return;
 runtime=this;auto module=REX::W32::GetModuleHandleA("OpenAnimationReplacer.dll");auto request=reinterpret_cast<OAR_API::Animations::Request>(module?REX::W32::GetProcAddress(module,"RequestPluginAPI_Animations"):nullptr);
  if(request)oar_=request(OAR_API::Animations::InterfaceVersion::V1,"AstraSight",REL::Version{3,6,3,0});
 REL::Relocation<uintptr_t> playerTable(RE::VTABLE_PlayerCharacter[0]),characterTable(RE::VTABLE_Character[0]),clipTable(RE::VTABLE_hkbClipGenerator[0]);
 playerOriginal=playerTable.write_vfunc(0xAD,playerPump);characterOriginal=characterTable.write_vfunc(0xAD,actorPost);clipOriginal=clipTable.write_vfunc(0x17,clipGenerated);
 installed_=true;spdlog::info("AstraGuardNative API1 frame pump PlayerCharacter::Update (0xAD); v29 hold clip grips, mount steered rigidly, OAR samples are telemetry only; OAR Animations V1={} (module loaded={})",oar_!=nullptr,module!=nullptr);
}
bool GuardRuntime::available()const{return installed_&&oar_;}
GuardRuntime::Slot* GuardRuntime::find(Key key){for(auto& s:slots_)if(s.lease.ticket().key==key&&s.lease.ticket())return &s;return nullptr;}
bool GuardRuntime::stationIdle(uint32_t handle){std::lock_guard lock(mutex_);for(auto& s:slots_)if(s.lease.ticket()&&s.lease.ticket().key.handle==handle)return false;return true;}
bool GuardRuntime::admitPlayer(uint32_t handle,const std::function<bool()>& begin){std::lock_guard lock(mutex_);return stationIdle(handle)&&begin();}
bool GuardRuntime::begin(RE::TESObjectREFR* gun,RE::Actor* actor,int token,RE::TESObjectWEAP* weapon,RE::TESAmmo* ammo,RE::TESSound* sound){
 std::lock_guard lock(mutex_);if(!available()||token<=0||!station(gun,actor)||!weapon||!ammo||!ammo->data.projectile||!sound)return false;
 // v31: a gun whose NIF carries OPERADOR_SOPORTE is driven by tickPosts(); never lease an NPC onto it.
 if(auto r=gun->Get3D();r&&r->GetObjectByName("OPERADOR_SOPORTE"))return false;
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
void GuardRuntime::invalidate(){std::lock_guard lock(mutex_);for(auto& p:posts_){p.acquired=false;p.root=0;p.status=-1;p.target=0;}auto main=RE::Main::GetSingleton();bool gameThread=main&&main->threadID==REX::W32::GetCurrentThreadId();for(auto& s:slots_)if(s.lease.ticket()){cancel(s,false,"load/new game/revert");if(gameThread)cleanup(s);}}
// Loading invalidates; other menus retain the pose. Active-world dialogue must
// finish an existing mechanical cycle even though no new aiming/shot is admitted.
void GuardRuntime::menu(const RE::MenuOpenCloseEvent* e){if(e&&e->opening&&std::string_view(e->menuName.c_str())=="Loading Menu")invalidate();}
bool GuardRuntime::paused()const{auto ui=RE::UI::GetSingleton();auto main=RE::Main::GetSingleton();return !ui||!main||ui->GameIsPaused()||main->freezeTime||main->freezeNextFrame;}
bool GuardRuntime::blocked()const{auto ui=RE::UI::GetSingleton();if(!ui)return true;for(auto name:std::array<std::string_view,13>{"InventoryMenu","MagicMenu","MapMenu","Journal Menu","TweenMenu","Console","Dialogue Menu","Loading Menu","BarterMenu","ContainerMenu","FavoritesMenu","Sleep/Wait Menu","MessageBoxMenu"})if(ui->IsMenuOpen(name))return true;return false;}
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
bool GuardRuntime::requestClip(Slot& s,RE::Actor* actor,int clip,bool again){
 s.gripConfirmed=false;s.gripWaitSince=clock_;
 {std::lock_guard obsLock(observationsMutex_);observations_[size_t(&s-slots_.data())]={0,s.lease.ticket().epoch,frame_.load(),s.character};observedCharacters_[size_t(&s-slots_.data())].store(s.character,std::memory_order_relaxed);}
 for(size_t i=0;i<4;++i){auto f=faction(i);if(!f)return false;if(int(i)==clip||i==0)actor->AddToFaction(f,0);else actor->RemoveFromFaction(f);}
 auto api=static_cast<OAR_API::Animations::IAnimationsInterface1*>(oar_);if(!api||!idle()||!actor->GetActorRuntimeData().currentProcess)return false;
 api->ClearConditionStateData(actor);
 // v29.1: the pre-v29.1 pair (IdleForceDefaultState then PlayIdle in the same frame) asks the
 // graph for two transitions at once. The first request only plays the idle. A re-request
 // returns the graph to default now and plays the idle GuardReplayDelay s later (tick -> playHold).
 if(again){bool sent=actor->NotifyAnimationGraph("IdleForceDefaultState");s.replayAt=clock_+GuardReplayDelay;spdlog::info("guard v29.1 re-request 1/2 IdleForceDefaultState sent={} gun={:08X} actor={:08X} PlayIdle in {}s",sent,s.gun,s.actor,GuardReplayDelay);return true;}
 return playHold(s,actor);
}
bool GuardRuntime::playHold(Slot& s,RE::Actor* actor){
 auto process=actor?actor->GetActorRuntimeData().currentProcess:nullptr;auto owned=idle();if(!process||!owned)return false;
 bool played=process->PlayIdle(actor,owned,nullptr);
 spdlog::info("guard v29.1 PlayIdle gun={:08X} actor={:08X} accepted={}",s.gun,s.actor,played);return played;
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
 {std::lock_guard obsLock(observationsMutex_);auto index=size_t(&s-slots_.data());observations_[index]={0,s.lease.ticket().epoch,frame_.load(),s.character};observedCharacters_[index].store(s.character,std::memory_order_relaxed);}
 if(auto placed=pose(s,gun,actor,s.yaw,s.pitch);placed!=Pose::ok)return placed==Pose::blocked?fail(s.failure):false;
 if(!requestClip(s,actor,0))return fail("OAR / process / hold PlayIdle request rejected");
 s.acquired=true;s.phaseAt=s.lastTime=clock_;s.hold.begin(clock_);s.status=0;s.nextShot=clock_+GuardEnterSeconds;watchedActors_[size_t(&s-slots_.data())].store(s.actor);auto running=actor->GetCurrentPackage();spdlog::info("guard v26 acquired gun={:08X} actor={:08X} package={:08X} yaw={} heightOffset={} supportZ={} actorScale={} referenceScale={} baseHeight={} holdRequested=true",s.gun,s.actor,running?running->GetFormID():0,s.yaw,s.heightOffset,s.supportZ,s.actorScale,referenceScale(actor),naturalHeight(actor));return true;
}
void GuardRuntime::observe(RE::hkbClipGenerator* clip,const RE::hkbContext& ctx){
 if(!clip||!ctx.character||!oar_||!clip->animationControl||!clip->animationControl->binding||!clip->animationControl->binding->animation)return;
 size_t index=observations_.size();uint64_t epoch=0;auto character=reinterpret_cast<uintptr_t>(ctx.character);
 if(std::none_of(observedCharacters_.begin(),observedCharacters_.end(),[&](auto& c){return c.load(std::memory_order_relaxed)==character;}))return;
 {std::lock_guard lock(observationsMutex_);for(size_t i=0;i<observations_.size();++i)if(observations_[i].character==character){index=i;epoch=observations_[i].epoch;break;}}
 if(index==observations_.size())return;
 // Generate may run on a worker. Do not hold our mutex across OAR calls:
 // condition invalidation on the main thread can acquire OAR's own locks.
 auto info=static_cast<OAR_API::Animations::IAnimationsInterface1*>(oar_)->GetCurrentReplacementAnimationInfo(clip);
 int kind=guardClipKind(info.animationPath.c_str(),info.modName.c_str(),info.subModName.c_str());
 // v29: telemetry only. Any sample of the own clip proves the replacement is
 // live; blend weights vary through vanilla transitions and gate nothing.
 double weight=clip->animationControl->weight;
 if(kind<0){
  // v29.1: not one of our clips. Say which one is playing on the watched actor (vanilla
  // shows an empty animation path), once per clip every 10 s. Worker thread: only
  // observationsMutex_ and the thread-safe logger are touched.
  std::string key=std::string(info.animationPath.c_str())+"|"+info.modName.c_str()+"|"+info.subModName.c_str();
  auto now=std::chrono::steady_clock::now();bool report=false;
  {std::lock_guard lock(observationsMutex_);auto& known=loggedClips_[index];
   auto it=std::find_if(known.begin(),known.end(),[&](const LoggedClip& c){return c.key==key;});
   if(it==known.end()){if(known.size()>=16)known.erase(known.begin());known.push_back({key,now});report=true;}
   else if(now-it->at>=std::chrono::seconds(10)){it->at=now;report=true;}}
  if(report)spdlog::info("guard v29.1 unexpected clip slot={} animation='{}' project='{}' mod='{}' submod='{}' variant='{}'",index,info.animationPath.c_str(),info.projectName.c_str(),info.modName.c_str(),info.subModName.c_str(),info.variantFilename.c_str());
  return;
 }
 std::lock_guard lock(observationsMutex_);auto& o=observations_[index];
 if(o.character!=character||o.epoch!=epoch)return;
 o.clip=kind;o.time=clip->localTime;o.duration=clip->animationControl->binding->animation->duration;o.weight=weight;o.frame=frame_.load();o.serial=++observationSerial_;
}
GuardRuntime::Pose GuardRuntime::pose(Slot& s,RE::TESObjectREFR* gun,RE::Actor* actor,double yawValue,double pitchValue){
 auto invalid=[&](const char* reason){reject(s,gun,actor,reason);return Pose::invalid;};
 // v29: a refused move keeps the previous yaw, so the operator stays on the grips
 // and the lease survives. Only a broken station/operator contract ends it.
 auto refused=[&](const char* reason){s.failure=reason;return Pose::blocked;};
 auto root=gun->Get3D();auto yaw=root->GetObjectByName("CTRL_GIRO_360"),pitch=root->GetObjectByName("CTRL_ELEVACION");if(!yaw||!pitch||std::abs(yawValue)>60.001||!std::isfinite(pitchValue)||pitchValue<GuardPitchMin-.001||pitchValue>GuardPitchMax+.001)return invalid("pose node / yaw / pitch invalid");
 Transform world=from(root->world);if(!finite(world)||std::abs(world.scale-1)>.001||std::abs(world.rotation.m[8]-1)>.001||!std::isfinite(yawValue+s.heightOffset))return invalid("mounted station transform changed / nonfinite");
 Vec p=world.translation+world.rotation*rz(rad(yawValue))*Vec{0,151,0};p.z+=s.heightOffset;auto cell=gun->GetParentCell();auto physics=cell?cell->GetbhkWorld():nullptr;
#if ASTRA_RUNTIME_AE17
 auto controller=actor->GetCharController();auto bound=physicalBounds(actor,0);if(!controller||!bound)return invalid("live operator controller / physical bounds unknown");RE::CFilter cfilter{};controller->GetCollisionFilterInfo(cfilter);uint32_t filter=cfilter.filter;if(!filter)return invalid("operator collision filter unknown");
#else
 auto controller=actor->GetCharController();auto bound=physicalBounds(actor,0);if(!controller||!bound)return invalid("live operator controller / physical bounds unknown");uint32_t filter=0;controller->GetCollisionFilterInfo(filter);if(!filter)return invalid("operator collision filter unknown");
#endif
 Vec old=from(actor->GetPosition());bool move=length(old-p)>.01;
 if(!s.supportSaved||move){
  // Use the operator's actual filter, including its own collision group, as
  // Skyrim's controller support rays do. A residual self-hit never proves floor.
  auto floor=ray(physics,p+Vec{0,0,12},p-Vec{0,0,12},RE::COL_LAYER::kLOS,filter);double floorZ=p.z+12-24*floor.fraction;
  if(!floor.known||!floor.hit||floor.ref==actor->GetFormID()||!guardSupport(p.z,floorZ,floor.normal.z,s.supportSaved?std::optional<double>{s.supportZ}:std::nullopt)){
   if(!s.supportSaved)spdlog::warn("guard v26 support gun={:08X} filter={:08X} known={} hit={} hitRef={:08X} normalZ={} feetZ={} floorZ={} savedFloorZ={}",s.gun,filter,floor.known,floor.hit,floor.ref,floor.normal.z,p.z,floorZ,s.supportZ);
   return refused("floor support unknown / self-hit / slope / height changed");}
  if(!s.supportSaved){s.supportZ=floorZ;s.supportSaved=true;}
 }
 // Fenced platform clearance: rays around the moving capsule at ankle and torso.
 if(length(old-p)>5||std::abs(old.z-p.z)>2)return refused("capsule move exceeds bounded horizontal step");
 if(move){double radius=bound->radius;for(double z:std::array<double,3>{12,bound->height*.5,bound->height-12})for(int i=0;i<9;++i){Vec offset=i?Vec{radius*std::cos(2*std::numbers::pi*(i-1)/8),radius*std::sin(2*std::numbers::pi*(i-1)/8),z}:Vec{0,0,z};auto r=ray(physics,old+offset,p+offset,RE::COL_LAYER::kLOS,filter);if(!r.known||r.hit)return refused("operator swept clearance obstructed / unknown");}}
 auto ticket=s.lease.ticket();if(!s.lease.current(ticket))return Pose::invalid;
 // v29.1: write only what changed. Until v29 SetPosition/SetRotation ran on every frame even for
 // a still target: a per-frame teleport that can keep the animation graph from settling.
 Vec f=world.rotation*rz(rad(yawValue))*Vec{0,-1,0};double heading=std::atan2(f.x,f.y);
 auto writes=guardPoseWrites(old,p,actor->GetAngleZ(),heading,actor->GetAngleX());s.maxDrift=std::max(s.maxDrift,length(old-p));
 if(writes.position){
  RE::hkVector4 before{},after{};controller->GetPositionImpl(before,true);actor->SetPosition(into(p),true);controller->GetPositionImpl(after,true);
  alignas(16) float b[4],a[4];_mm_store_ps(b,before.quad);_mm_store_ps(a,after.quad);double inverseScale=RE::bhkWorld::GetWorldScaleInverse();Vec moved{(a[0]-b[0])*inverseScale,(a[1]-b[1])*inverseScale,(a[2]-b[2])*inverseScale};
  if(length(moved-(p-old))>1){actor->SetPosition(into(old),true);return refused("actor/controller displacement mismatch");}
  ++s.writesPos;
 }
#if ASTRA_RUNTIME_AE17
 if(writes.rotation){actor->SetLooking(0);actor->SetHeading(float(heading));++s.writesRot;}
#else
 if(writes.rotation){actor->SetRotationX(0);actor->SetRotationZ(float(heading));++s.writesRot;}
#endif
 if(!s.lease.current(ticket)||actor->Get3D()!=reinterpret_cast<RE::NiAVObject*>(s.actorRoot))return Pose::invalid;
 yaw->local.rotate=into(rz(rad(yawValue))*s.yawBase);pitch->local.rotate=into(rx(-rad(pitchValue))*s.pitchBase);transforms(yaw);s.yaw=yawValue;s.pitch=pitchValue;
 if(length(from(actor->GetPosition())-p)>=1||!actor->GetCharController())return refused("actor pose did not settle");return Pose::ok;
}
void GuardRuntime::postActor(RE::Actor* actor){
 // Diagnostic only: actor updates have no main-thread/post-pose guarantee.
 // Never resolve handles, touch scene/physics or acquire our slot lock here.
 if(!actor)return;auto id=actor->GetFormID();
 for(size_t i=0;i<watchedActors_.size();++i)if(watchedActors_[i].load(std::memory_order_relaxed)==id){
  auto main=RE::Main::GetSingleton();if(main&&main->threadID==REX::W32::GetCurrentThreadId())postMain_[i].fetch_add(1,std::memory_order_relaxed);else postWorker_[i].fetch_add(1,std::memory_order_relaxed);
 }
}
void GuardRuntime::poseLog(Slot& s,RE::TESObjectREFR* gun,RE::Actor* actor,const Observation& obs,double desired,double desiredPitch){
 // Measurement only: live wrists against the grips the hold clip was authored
 // for (about 3 u at Nord height 1.03). Nothing is corrected or gated on it.
 if(clock_<s.nextPoseLog)return;s.nextPoseLog=clock_+2;
 double error[2];handErrors(gun,actor,s.yaw,error);s.handError={error[0],error[1]};
 size_t index=size_t(&s-slots_.data());
 spdlog::info("guard v29 pose gun={:08X} actor={:08X} status={} yaw={:.2f} desired={:.2f} target={:08X} clip={} phase={:.3f} sampleAge={:.2f} handErrorL={:.1f} handErrorR={:.1f} moveRefused={} characterMain={} characterWorker={} writesPos={} writesRot={} maxDrift={:.3f} reissues={} held={} pitch={:.2f} desiredPitch={:.2f} hunted={}",
  s.gun,s.actor,s.status,s.yaw,desired,s.target,obs.serial?obs.clip:-1,obs.time,s.sampleAt<0?-1.:clock_-s.sampleAt,error[0],error[1],s.moveRefusal?s.moveRefusal:"none",postMain_[index].load(),postWorker_[index].load(),s.writesPos,s.writesRot,s.maxDrift,s.hold.reissues(),guardHandsHeld(error[0],error[1]),s.pitch,desiredPitch,s.hunted);
 s.writesPos=s.writesRot=0;s.maxDrift=0;
}
void GuardRuntime::reload(Slot& s,RE::TESObjectREFR* gun){
 // The mechanism's own Fire (0.2 s) then Reset (0.8 s) sequences, timed from the launch.
 double t=clock_-s.fireAt;auto root=gun->Get3D();
 if(t>=.2&&!s.resetStarted){s.resetStarted=true;if(auto fire=gun->GetSequence("Fire"))fire->Deactivate(0,false);if(auto reset=gun->GetSequence("Reset"))reset->Activate(0,true,1,0,nullptr,false);}
 if(t>=1.){if(auto reset=gun->GetSequence("Reset"))reset->SetPhase(1,true);if(auto bolt=root->GetObjectByName("VIROTE_VISUAL")){bolt->local.scale=1;transforms(bolt);}s.status=1;}
}
void GuardRuntime::targets(Slot& s,RE::TESObjectREFR* gun,RE::Actor* guard){
 auto root=gun->Get3D();auto muzzle=root->GetObjectByName("ProjectileNode");auto process=RE::ProcessLists::GetSingleton();if(!muzzle||!process){s.target=0;return;}
 auto forms=RE::TESDataHandler::GetSingleton();auto town=forms?forms->LookupForm<RE::TESFaction>(0x28172,"Skyrim.esm"):nullptr;auto localGuard=forms?forms->LookupForm<RE::TESFaction>(0x2BE39,"Skyrim.esm"):nullptr;
 if(!town||!localGuard){s.target=0;s.nextScan=clock_+.2;return;}
 // v33: whose side the post is on: the town guards (city) or the bandits (camp).
 auto bandits=forms->LookupForm<RE::TESFaction>(0x1BCC0,"Skyrim.esm");
 auto friendly=[&](RE::Actor* a){return s.camp?(bandits&&a->IsInFaction(bandits)):(a->IsInFaction(town)||a->IsInFaction(localGuard));};
 // v31: a post has no operator actor. Hostility is judged against a loaded friendly actor (cached in s.reference).
 RE::Actor* ref=guard;RE::TESObjectREFR* viewer=guard?static_cast<RE::TESObjectREFR*>(guard):gun;
 if(!ref){auto cached=RE::TESForm::LookupByID<RE::Actor>(s.reference);auto self=RE::PlayerCharacter::GetSingleton();
  // v33.14: a camp's bandit must be at the camp (GuardCampReferenceRadius); a city keeps any loaded town guard.
  auto atCamp=[&](RE::Actor* a){return !s.camp||length(from(a->GetPosition())-from(root->world.translate))<=GuardCampReferenceRadius;};
  auto usable=[&](RE::Actor* a){return a&&a!=self&&!ownedOperator(a)&&alive(a)&&friendly(a)&&atCamp(a);};
  if(usable(cached))ref=cached;
  else{double best=1e300;unsigned seen=0;process->ForAllActors([&](RE::Actor* a){if(++seen>GuardActorScanCap)return RE::BSContainer::ForEachResult::kStop;
    if(usable(a)){double d=length(from(a->GetPosition())-from(root->world.translate));if(d<best){best=d;ref=a;}}return RE::BSContainer::ForEachResult::kContinue;});
   s.reference=ref?ref->GetFormID():0;}}
 // v33: a camp shoots the player on sight; a city only while its guards fight them.
 bool hunted=s.camp||playerHunted(guard);if(hunted!=s.hunted){s.hunted=hunted;spdlog::info("guard v29.2 player-hostile gun={:08X} hunted={}",s.gun,hunted);}
 // v31.2: a post judges whether a candidate can be engaged from the muzzle where it WOULD be once the mount has turned
 // and elevated onto that candidate, not from where it happens to be now. The live muzzle sinks into the mount's own
 // surroundings (the parapet in front of it) when the barrel is depressed, so a verdict taken from the live muzzle
 // depended on the pitch the mount itself was commanding and the gun bounced between targets (log 2026-10-12 17:54,
 // tower B80), and it kept pointing the barrel into the wall at targets far below. The predicted-muzzle test is
 // independent of the current pose and also drops what the barrel cannot reach past the wall.
 Mat R0=from(root->world.rotate);Vec rootT=from(root->world.translate);
 auto yawNode=root->GetObjectByName("CTRL_GIRO_360"),pitchNode=root->GetObjectByName("CTRL_ELEVACION");
 const bool havePost=s.post&&yawNode&&pitchNode;
 Vec tPitch{},tMuzzle{},pYaw=rootT,pivot=rootT;double ahead=0,above=0;
 if(havePost){tPitch=from(pitchNode->local.translate);tMuzzle=from(muzzle->local.translate);pYaw=from(yawNode->world.translate);pivot=pYaw+R0*tPitch;
  Vec bl=from(muzzle->local.rotate)*Vec{0,1,0};double h=std::hypot(bl.x,bl.y);ahead=h>.3?(tMuzzle.x*bl.x+tMuzzle.y*bl.y)/h:0;above=tMuzzle.z;}
 auto muzzleAt=[&](double yawDeg,double pitchDeg){return pYaw+R0*(rz(rad(yawDeg))*(tPitch+rx(-rad(pitchDeg))*tMuzzle));};
 Vec eye=havePost?muzzleAt(s.yaw,0):from(muzzle->world.translate);
 auto engageable=[&](RE::Actor* a,Vec c,bool ballistic){
  if(!havePost)return visible(a,viewer,from(muzzle->world.translate));
  double yawDeg=std::remainder(aimFromWorld(R0,c-rootT).yaw,360.);if(!std::isfinite(yawDeg)||std::abs(yawDeg)>GuardYawLimit)return false;
  Vec to=c-pivot;double pitchDeg=aimFromWorld(R0,to).pitch;
  if(ballistic)if(auto sol=guardAimSolution(to,ahead,above))pitchDeg=sol->pitch;
  if(!std::isfinite(pitchDeg))return false;
  return visible(a,viewer,muzzleAt(yawDeg,std::clamp(pitchDeg,GuardPitchMin,GuardPitchMax)));};
 // The current target keeps its verdict for 0.8 s after a single failed ray.
 auto look=[&](RE::Actor* a,Vec c,bool ballistic){bool v=engageable(a,c,ballistic);if(a->GetFormID()==s.target){if(v)s.targetSeenAt=clock_;else if(s.post&&clock_-s.targetSeenAt<.8)v=true;}return v;};
 std::vector<GuardCandidate> candidates;bool overflow=false;unsigned visited=0;process->ForAllActors([&](RE::Actor* a){if(++visited>GuardActorScanCap||candidates.size()>=256){overflow=true;return RE::BSContainer::ForEachResult::kStop;}if((guard&&a==guard)||ownedOperator(a)||!alive(a))return RE::BSContainer::ForEachResult::kContinue;
  Vec p=from(a->GetPosition());if(length(p-from(root->world.translate))>6200||a->GetParentCell()->GetbhkWorld()!=gun->GetParentCell()->GetbhkWorld())return RE::BSContainer::ForEachResult::kContinue;
  auto bounds=physicalBounds(a,0);if(!bounds)return RE::BSContainer::ForEachResult::kContinue;p=bounds->feet+Vec{0,0,bounds->height*.5};
  bool isPlayer=a==RE::PlayerCharacter::GetSingleton();
  candidates.push_back({a->GetFormID(),p,true,look(a,p,isPlayer?hunted:(ref&&a->IsHostileToActor(ref)&&a->IsInCombat())),isPlayer?hunted:(ref&&a->IsHostileToActor(ref)),isPlayer?hunted:a->IsInCombat(),isPlayer,a->IsPlayerTeammate(),bounds->height*.5,friendly(a),isPlayer&&hunted});return RE::BSContainer::ForEachResult::kContinue;});
 // Player may not occur in ProcessLists::ForAllActors.
 auto player=RE::PlayerCharacter::GetSingleton();if(alive(player)&&std::none_of(candidates.begin(),candidates.end(),[&](auto& c){return c.id==player->GetFormID();})){auto bounds=physicalBounds(player,0);if(bounds)candidates.push_back({player->GetFormID(),bounds->feet+Vec{0,0,bounds->height*.5},true,look(player,bounds->feet+Vec{0,0,bounds->height*.5},hunted),hunted,hunted,true,false,bounds->height*.5,false,hunted});}
 s.target=overflow?0:selectGuardTarget(candidates,s.target,from(root->world.translate),from(root->world.rotate),eye,true,!s.post).value_or(0);s.nextScan=clock_+.2;s.advisory=0;
 // v29.3 diagnostic: why the player is or is not picked; every filter of selectGuardTarget is evaluated separately.
 // v33.14: only while the player IS an enemy of this post (hunted / camp) and still nobody is selected, once per 5 s
 // (it was every 1.5 s whenever the post was idle, i.e. all the time).
 if(player&&hunted&&!s.target&&clock_>=s.nextTargetLog){
  s.nextTargetLog=clock_+5;auto cit=std::find_if(candidates.begin(),candidates.end(),[&](auto& c){return c.id==player->GetFormID();});
  auto controller=player->GetCharController();auto pcell=player->GetParentCell();auto pworld=pcell?pcell->GetbhkWorld():nullptr;
  auto bounds=physicalBounds(player,0);Vec o=from(root->world.translate),m=eye;
  if(!bounds)spdlog::info("guard v29.3 diag gun={:08X} hunted={} candidates={} overflow={} player: bounds=FAIL controller={} world={} shape0={} shape1={} alive={}",s.gun,hunted,candidates.size(),overflow,controller!=nullptr,pworld!=nullptr,controller&&controller->shapes[0]!=nullptr,controller&&controller->shapes[1]!=nullptr,alive(player));
  else {
   Vec c=bounds->feet+Vec{0,0,bounds->height*.5},d=c-o;double dist=length(d),yaw=std::remainder(aimFromWorld(from(root->world.rotate),d).yaw,360.);
   Vec toMuzzle=c-m;double n=length(toMuzzle);Ray r=n>=1?ray(pworld,m,c-toMuzzle*(32/n)):Ray{true};
   bool aim=guardAimSolution(c-m,0,0).has_value();
   // Where a blocked ray stopped, in the gun frame (x right, y forward along the bore at yaw 0, z up).
   Vec hitLocal=r.hit?from(root->world.rotate).transpose()*(m+(c-toMuzzle*(32/std::max(n,1.))-m)*r.fraction-m):Vec{};
   spdlog::info("guard v29.3 diag gun={:08X} hunted={} visited={} overflow={} candidates={} inList={} dist={:.0f} yaw={:.1f} height={:.0f} ray(known={} hit={} ref={:08X} frac={:.2f}) hitLocal=({:.0f},{:.0f},{:.0f}) normal=({:.2f},{:.2f},{:.2f}) pitch={:.1f} muzzleZ={:.0f} visible={} teammate={} aim={} inCombat={}",
    s.gun,hunted,visited,overflow,candidates.size(),cit!=candidates.end(),dist,yaw,bounds->height,r.known,r.hit,r.ref,r.fraction,hitLocal.x,hitLocal.y,hitLocal.z,r.normal.x,r.normal.y,r.normal.z,s.pitch,m.z,cit!=candidates.end()&&cit->visible,player->IsPlayerTeammate(),aim,player->IsInCombat());
  }
 }
}
bool GuardRuntime::shoot(Slot& s,RE::TESObjectREFR* gun,RE::Actor* guard){
 // Everything below is in the main-thread effects scope. Resolve forms/handles
 // afresh and validate immediately adjacent to Projectile::Launch. v29: no body
 // clip synchronisation; every target, path and protection check is unchanged.
 // v29.2: the bore may be elevated (solved by aimAt), the player may be the target while hunted, and
 // every refusal records its reason in s.shotRefusal for the log.
 s.shotRefusal="";s.shotDetail.clear();auto refuse=[&](const char* reason){s.shotRefusal=reason;return false;};
 auto target=RE::TESForm::LookupByID<RE::Actor>(s.target);auto ammo=RE::TESForm::LookupByID<RE::TESAmmo>(s.ammo);auto weapon=RE::TESForm::LookupByID<RE::TESObjectWEAP>(s.weapon);auto sound=RE::TESForm::LookupByID<RE::TESSound>(s.sound);
 auto player=RE::PlayerCharacter::GetSingleton();bool targetIsPlayer=target&&target==player;bool hunted=targetIsPlayer&&(s.camp||playerHunted(guard));
 // v31: a post credits the shot to a loaded town guard (the engine needs a real Actor as shooter).
 RE::Actor* shooter=guard?guard:RE::TESForm::LookupByID<RE::Actor>(s.reference);RE::TESObjectREFR* viewer=guard?static_cast<RE::TESObjectREFR*>(guard):gun;
 if(!shooter||!alive(shooter))return refuse("no loaded town guard to credit the shot to");
 if(!enemy(target,shooter,hunted,s.camp)||!ammo||!weapon||!sound||!ammo->data.projectile)return refuse("target is no enemy / ammo, weapon or sound missing");
 if(!loaded(target)||target->GetParentCell()->GetbhkWorld()!=gun->GetParentCell()->GetbhkWorld())return refuse("target not loaded / other physics world");
 auto proj=ammo->data.projectile;if(std::abs(proj->data.speed-5400)>.01||std::abs(proj->data.gravity*9.81*70-240.345)>.1||!proj->IsArrow()||proj->data.flags.any(RE::BGSProjectileData::BGSProjectileFlags::kHitScan))return refuse("projectile record is not the authored arrow");
 double blast=0;if(proj->data.flags.any(RE::BGSProjectileData::BGSProjectileFlags::kExplosion)){auto explosion=proj->data.explosionType;if(!explosion||explosion->data.spawnProjectile||explosion->data.flags.any(RE::BGSExplosionData::Flag::kChain)||explosion->data.verticalOffsetMult!=0)return refuse("explosion record not allowed");blast=explosion->data.radius;if(!std::isfinite(blast)||blast<0)return refuse("explosion radius unknown");}
 auto root=gun->Get3D();auto node=root->GetObjectByName("ProjectileNode");auto targetBounds=physicalBounds(target,0);if(!node||!finite(from(node->world))||!targetBounds)return refuse("muzzle or target bounds unknown");Vec muzzle=from(node->world.translate),bore=from(node->world.rotate)*Vec{0,1,0};Vec center=targetBounds->feet+Vec{0,0,targetBounds->height*.5},delta=center-muzzle;
 auto aim=aimAt(gun,center);if(!aim)return refuse("no elevation reaches the target");
 if(!visible(target,viewer,muzzle)){
  // Say what the ray hit: the muzzle of a depressed barrel can start inside the mount's own surroundings.
  auto vc=gun->GetParentCell();auto vw=vc?vc->GetbhkWorld():nullptr;double vn=length(delta);
  if(vw&&vn>=1){auto r=ray(vw,muzzle,center-delta*(32/vn));s.shotDetail=fmt::format("ray known={} hit={} ref={:08X} frac={:.3f} dist={:.0f} muzzleZ={:.0f} pitch={:.1f}",r.known,r.hit,r.ref,r.fraction,vn,muzzle.z,s.pitch);}
  return refuse("target not visible from the muzzle");}
 // Flight time along the real bore (its horizontal component), not along an assumed flat one.
 double borePlane=std::hypot(bore.x,bore.y);double seconds=borePlane>.3?std::hypot(delta.x,delta.y)/(5400*borePlane):NAN;
 if(!guardProjectileContract(proj->data.speed,proj->data.gravity*9.81*70,proj->data.collisionRadius,proj->data.range,proj->data.lifetime,proj->data.explosionProximity,proj->data.explosionTimer,proj->data.coneSpread,proj->data.flags.any(RE::BGSProjectileData::BGSProjectileFlags::kExplosionAltTrigger),seconds))return refuse("projectile contract / flight time outside limits");
 Vec horizontal{delta.x,delta.y,0};if(length(horizontal)<64)return refuse("target inside the minimum range");
 auto expected=guardBore(horizontal,aim->pitch);
 if(!expected||length(bore-*expected)>GuardBoreTolerance){s.shotDetail=fmt::format("|bore-solved|={:.4f} (limit {}) pitch={:.2f} solved={:.2f}",expected?length(bore-*expected):-1.,GuardBoreTolerance,s.pitch,aim->pitch);return refuse("bore not yet on the solved elevation / heading");}
 auto path=guardArcTrajectory(muzzle,bore,seconds,5400,240.345);auto cell=gun->GetParentCell();auto world=cell?cell->GetbhkWorld():nullptr;if(!world||path.size()<2)return refuse("trajectory or physics world unknown");
 std::vector<GuardProtected> protect;std::vector<RE::FormID> protectIds;auto process=RE::ProcessLists::GetSingleton();if(!process)return refuse("process lists unknown");bool unknown=false;unsigned visited=0;unsigned approximated=0;
 // v31.2: only actors that can be on the path matter (same physics world, within the flight range), and an actor whose
 // controller cannot be measured is protected by a conservative capsule instead of vetoing every shot: in a city
 // there is always one of the ~2000 loaded actors without a measurable controller (log 2026-10-12 17:57).
 process->ForAllActors([&](RE::Actor* a){if(++visited>GuardActorScanCap||protect.size()>=512){unknown=true;return RE::BSContainer::ForEachResult::kStop;}if(!alive(a)||a==target||enemy(a,shooter))return RE::BSContainer::ForEachResult::kContinue;
  Vec where=from(a->GetPosition());auto acell=a->GetParentCell();if(!acell||acell->GetbhkWorld()!=world||length(where-muzzle)>6500)return RE::BSContainer::ForEachResult::kContinue;
  auto bounds=physicalBounds(a);if(!bounds){bounds=GuardProtected{where,60.,170.};++approximated;}protect.push_back(*bounds);protectIds.push_back(a->GetFormID());return RE::BSContainer::ForEachResult::kContinue;});
 if(!alive(player))return refuse("player unknown");auto playerBounds=physicalBounds(player);std::optional<GuardProtected> guardBounds=guard?physicalBounds(guard):std::optional<GuardProtected>{};if(!playerBounds||(guard&&!guardBounds)||unknown)return refuse("protected actor bounds unknown");
 // A hunted player is the target, not a bystander; every other actor stays protected.
 if(!targetIsPlayer){protect.push_back(*playerBounds);protectIds.push_back(player->GetFormID());}if(guardBounds){protect.push_back(*guardBounds);protectIds.push_back(guard->GetFormID());}
 // Follow the entire predicted trajectory to its first live target contact.
 // Any earlier obstruction or an unobserved impact leaves safety unknown.
 bool impact=false;for(size_t i=1;i<path.size();++i){auto r=ray(world,path[i-1],path[i],RE::COL_LAYER::kProjectile);if(!r.known)return refuse("collision query unknown");if(r.hit){Vec hit=path[i-1]+(path[i]-path[i-1])*r.fraction;Vec feet=targetBounds->feet;if(r.ref!=target->GetFormID()||std::hypot(hit.x-feet.x,hit.y-feet.y)>targetBounds->radius||hit.z<feet.z||hit.z>feet.z+targetBounds->height){
   s.shotDetail=fmt::format("segment {}/{} frac={:.3f} ref={:08X} fromMuzzle={:.0f} hit=({:.0f},{:.0f},{:.0f}) muzzleZ={:.0f} targetDist={:.0f} pitch={:.1f}",i,path.size()-1,r.fraction,r.ref,length(hit-muzzle),hit.x,hit.y,hit.z,muzzle.z,length(delta),s.pitch);
   return refuse("path blocked before the target");}path[i]=hit;path.resize(i+1);impact=true;break;}}
 if(!impact)return refuse("path does not reach the target");
 if(!guardPathSafe(path,protect,blast)){
  for(size_t i=0;i<protect.size();++i)if(!guardPathSafe(path,std::span<const GuardProtected>(&protect[i],1),blast)){s.shotDetail=fmt::format("actor {:08X} ({} protected, {} approximated)",i<protectIds.size()?protectIds[i]:0,protect.size(),approximated);break;}
  return refuse("a protected actor is on the path");}
 RE::NiPointer<RE::TESObjectREFR> liveGun;RE::NiPointer<RE::Actor> liveGuard;bool still=guard?(context(s,liveGun,liveGuard)&&liveGun.get()==gun&&liveGuard.get()==guard):(loaded(gun)&&reinterpret_cast<uintptr_t>(gun->Get3D())==s.root);
 if(!still||!enemy(target,shooter,hunted,s.camp)||!visible(target,viewer,muzzle))return refuse("lease or target changed during validation");
 auto liveTargetBounds=physicalBounds(target,0);if(!liveTargetBounds||length(liveTargetBounds->feet-targetBounds->feet)>.01||std::abs(liveTargetBounds->height-targetBounds->height)>.01||std::abs(liveTargetBounds->radius-targetBounds->radius)>.01)return refuse("target moved during validation");
 auto liveMuzzle=gun->Get3D()->GetObjectByName("ProjectileNode");if(!liveMuzzle||length(from(liveMuzzle->world.translate)-muzzle)>.01||length(from(liveMuzzle->world.rotate)*Vec{0,1,0}-bore)>.001)return refuse("muzzle moved during validation");
 // v32: the bolt is launched with the bore's real pitch. Up to v31.4 angleX was 0: the engine builds the projectile
 // flat and its delayed 3D initialisation recomputes the velocity from that orientation, so a bolt fired at -39 deg
 // left the muzzle downwards and then turned flat ("rebotaban en el piso de la ballesta", test 2026-10-14). Same
 // convention as the player's shot (FastShotRuntime.cpp, game-tested): angleX = -asin(forward.z), positive = down.
 RE::ProjectileHandle handle;RE::Projectile::ProjectileRot angles{float(-std::asin(std::clamp(bore.z,-1.,1.))),float(std::atan2(bore.x,bore.y))};RE::Projectile::LaunchData launch(shooter,into(muzzle),angles,ammo,weapon);
 launch.autoAim=false;launch.alwaysHit=false;launch.useOrigin=true;launch.forceConeOfFire=false;launch.desiredTarget=nullptr;
 // Nothing that can queue another VM action intervenes between lease/pose/
 // target safety revalidation above and the real engine commitment.
 RE::Projectile::Launch(&handle,launch);auto projectile=handle.get();if(!projectile){if(guard)cancel(s,true,"engine launch returned no projectile");else s.shotRefusal="engine launch returned no projectile";return false;}
 auto& data=projectile->GetProjectileRuntimeData();auto corrected=speedMultiplierCorrection(5400,projectile->GetSpeed(),data.speedMult);if(!corrected){if(guard)cancel(s,true,"projectile speed scalar unknown");return true;}data.speedMult=float(*corrected);data.linearVelocity=into(bore*5400);
 if(!guard){s.flight=handle;s.flightOrigin=muzzle;s.flightBore=bore;s.flightAt=clock_;s.flightStage=0;}
 if(guard&&!s.lease.current(s.lease.ticket()))return true;
 // The mechanism's own Fire sequence starts with the real launch; reload() runs Reset.
 if(auto fire=gun->GetSequence("Fire")){if(auto reset=gun->GetSequence("Reset"))reset->Deactivate(0,false);fire->Deactivate(0,false);fire->Activate(0,true,1,0,nullptr,false);}
#if ASTRA_RUNTIME_AE17
 auto bolt=root->GetObjectByName("VIROTE_VISUAL");if(bolt){bolt->local.scale=0;transforms(bolt);}RE::BSSoundHandle snd;auto audio=RE::BSAudioManager::GetSingleton();if(audio&&sound->descriptor&&audio->GetSoundHandle(snd,sound->descriptor)){snd.SetPosition(into(muzzle));snd.SetObjectToFollow(root);snd.Play();}
#else
 auto bolt=root->GetObjectByName("VIROTE_VISUAL");if(bolt){bolt->local.scale=0;transforms(bolt);}RE::BSSoundHandle snd;auto audio=RE::BSAudioManager::GetSingleton();if(audio&&sound->descriptor&&audio->BuildSoundDataFromDescriptor(snd,sound->descriptor)){snd.SetPosition(into(muzzle));snd.SetObjectToFollow(root);snd.Play();}
#endif
 Vec velocity=from(data.linearVelocity);
 spdlog::info("guard real projectile gun={:08X} guard={:08X} target={:08X} token={} epoch={} handle={} yaw={:.2f} pitch={:.2f} solvedPitch={:.2f} speed=5400 velocityZ={:.1f} expectedZ={:.1f} angleX={:.2f} blast={} player={}",s.gun,s.actor,s.target,s.lease.ticket().key.token,s.lease.ticket().epoch,handle.native_handle(),s.yaw,s.pitch,aim->pitch,velocity.z,bore.z*5400,angles.x*180/3.14159265358979,blast,targetIsPlayer);return true;
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
 {std::lock_guard obsLock(observationsMutex_);observations_[size_t(&s-slots_.data())]={};observedCharacters_[size_t(&s-slots_.data())].store(0,std::memory_order_relaxed);}s.retired=s.lease.ticket().key;s.lease.leaveEffect();s.lease.complete();s.status=s.fault?-2:-1;s.character=0;s.root=s.actorRoot=0;s.flagsSaved=false;
}
// v31: posts. The operator is geometry of the gun NIF (OPERADOR_SOPORTE under CTRL_GIRO_360), so it turns with the
// mount by construction and has no AI to wander off. The DLL only aims, tracks and fires; no OAR / package / clip.
bool GuardRuntime::postPose(Slot& s,RE::TESObjectREFR* gun,double yawValue,double pitchValue){
 auto root=gun->Get3D();auto yaw=root?root->GetObjectByName("CTRL_GIRO_360"):nullptr,pitch=root?root->GetObjectByName("CTRL_ELEVACION"):nullptr;
 if(!yaw||!pitch||!std::isfinite(yawValue+pitchValue)||std::abs(yawValue)>60.001||pitchValue<GuardPitchMin-.001||pitchValue>GuardPitchMax+.001)return false;
 yaw->local.rotate=into(rz(rad(yawValue))*s.yawBase);pitch->local.rotate=into(rx(-rad(pitchValue))*s.pitchBase);transforms(yaw);hangBasket(root);s.yaw=yawValue;s.pitch=pitchValue;return true;
}
bool GuardRuntime::postAcquire(Slot& s,RE::TESObjectREFR* gun,size_t index){
 auto h=RE::TESDataHandler::GetSingleton();auto root=gun->Get3D();
 auto fail=[&](const char* reason){if(clock_>=s.nextPostLog){s.nextPostLog=clock_+10;spdlog::warn("guard v31 post gun={:08X} not acquired: {}",gun->GetFormID(),reason);}return false;};
 if(!h||!root)return fail("no scene");
 auto weapon=h->LookupForm<RE::TESObjectWEAP>(0x804,"DragonsreachBallistae.esp");auto ammo=h->LookupForm<RE::TESAmmo>(0xB01,"DragonsreachBallistae.esp");auto sound=h->LookupForm<RE::TESSound>(0x80D,"DragonsreachBallistae.esp");
 if(!weapon||!ammo||!sound||!ammo->data.projectile)return fail("weapon / ammo / sound form missing");
 if(!root->GetObjectByName("CTRL_GIRO_360")||!root->GetObjectByName("CTRL_ELEVACION")||!root->GetObjectByName("ProjectileNode")||!root->GetObjectByName("VIROTE_VISUAL"))return fail("required low-rig node missing");
 if(!gun->GetSequence("Fire")||!gun->GetSequence("Reset"))return fail("weapon Fire/Reset sequence missing");
 auto world=from(root->world);if(!finite(world)||std::abs(world.scale-1)>.001||std::abs(world.rotation.m[8]-1)>.001)return fail("station transform is not upright / finite");
 double nextPostLog=s.nextPostLog;
 s=Slot{};s.post=true;s.camp=GuardPosts[index].kind==GuardPostKind::camp;s.gun=gun->GetFormID();s.weapon=weapon->GetFormID();s.ammo=ammo->GetFormID();s.sound=sound->GetFormID();s.nextPostLog=nextPostLog;
 s.yawBase=Mat{};s.pitchBase=Mat{};s.root=reinterpret_cast<uintptr_t>(root);s.acquired=true;s.status=0;s.entered=clock_;s.nextShot=clock_+GuardEnterSeconds;
 postPose(s,gun,0,0);
 spdlog::info("guard v31 post acquired gun={:08X} slot={} (the operator is part of the model)",s.gun,index);
 return true;
}
// v32: where the post's bolt really is 0.05 / 0.25 / 0.5 s after the launch, against the arc it was launched on
// (muzzle + bore*5400*t - 240.345*t^2/2). Up to v31.4 the bolt left with angleX = 0 and the log only showed the
// velocity written right after Launch, before the engine's own initialisation could change it.
void GuardRuntime::sampleFlight(Slot& s){
 constexpr std::array<double,3> at{.05,.25,.5};
 if(!s.flight||s.flightStage>=int(at.size())||clock_-s.flightAt<at[s.flightStage])return;
 double t=clock_-s.flightAt;auto projectile=s.flight.get();
 if(!projectile){spdlog::info("guard flight sample gun={:08X} stage={} t={:.3f} gone (impact or unload)",s.gun,s.flightStage,t);s.flight={};return;}
 auto& rt=projectile->GetProjectileRuntimeData();Vec p=from(projectile->GetPosition()),v=from(rt.linearVelocity);
 Vec expected=s.flightOrigin+s.flightBore*(GuardProjectileSpeed*t)+Vec{0,0,-.5*GuardProjectileGravity*t*t};
 double speed=length(v);Vec dir=speed>1e-6?v*(1/speed):Vec{};
 spdlog::info("guard flight sample gun={:08X} stage={} t={:.3f} travelled={:.0f} offArc={:.1f} velocity=({:.0f},{:.0f},{:.0f}) speed={:.0f} dirZ={:.3f} boreZ={:.3f}",
  s.gun,s.flightStage,t,length(p-s.flightOrigin),length(p-expected),v.x,v.y,v.z,speed,dir.z,s.flightBore.z);
 if(++s.flightStage>=int(at.size()))s.flight={};
}
void GuardRuntime::tickPosts(double step,bool actions){
 auto h=RE::TESDataHandler::GetSingleton();if(!h)return;
 for(size_t i=0;i<posts_.size();++i){
  auto& s=posts_[i];auto& ids=resolvedPosts()[i];auto gun=ids.gun?RE::TESForm::LookupByID<RE::TESObjectREFR>(ids.gun):nullptr;
  auto root=loaded(gun)?gun->Get3D():nullptr;
  if(!root||!root->GetObjectByName("OPERADOR_SOPORTE")){if(s.acquired){s.acquired=false;s.root=0;s.status=-1;s.target=0;}continue;}
  // v33.14: the city towers are also player stations (AstraAsedioStation). While the player owns the gun the post
  // neither aims nor shoots (both wrote the same nodes); it takes the gun back from the centre once the player leaves.
  if(playerOwns_&&playerOwns_(gun->CreateRefHandle().native_handle())){if(s.acquired){s.acquired=false;s.root=0;s.status=-1;s.target=0;spdlog::info("guard v31 post gun={:08X} yields to the player",gun->GetFormID());}continue;}
  if(s.acquired&&s.root!=reinterpret_cast<uintptr_t>(root)){s.acquired=false;s.root=0;s.status=-1;s.target=0;}   // scene rebuilt (cell reload)
  // The NPC operator of this station is retired in favour of the mesh one; saves made before v31 still have it enabled.
  if(auto npc=ids.npc?RE::TESForm::LookupByID<RE::Actor>(ids.npc):nullptr;npc&&!npc->IsDisabled()&&!npc->IsDeleted()){npc->Disable();spdlog::info("guard v31 post gun={:08X}: NPC operator {:08X} disabled",gun->GetFormID(),npc->GetFormID());}
  if(!s.acquired){if(clock_<s.nextAcquire)continue;s.nextAcquire=clock_+1;if(!postAcquire(s,gun,i))continue;}
  sampleFlight(s);
  if(s.status==3)reload(s,gun);
  if(!actions)continue;
  if(s.status==0&&clock_-s.entered>=GuardEnterSeconds){s.status=1;spdlog::info("guard v31 post holding gun={:08X}",s.gun);}
  if(clock_>=s.nextScan)targets(s,gun,nullptr);
  auto target=RE::TESForm::LookupByID<RE::Actor>(s.target);auto ref=RE::TESForm::LookupByID<RE::Actor>(s.reference);
  std::optional<GuardProtected> bounds;double desired=s.yaw,desiredPitch=s.pitch;std::optional<GuardAim> aim;
  if(s.status>=1&&alive(target)){bounds=physicalBounds(target,0);if(bounds){auto rootRotation=from(root->world.rotate);desired=std::remainder(aimFromWorld(rootRotation,bounds->feet-from(root->world.translate)).yaw,360.);
   Vec center=bounds->feet+Vec{0,0,bounds->height*.5};aim=aimAt(gun,center);
   // Line of sight is taken from the elevation pivot (what the barrel actually swings about), like targets() does.
   auto pivotNode=root->GetObjectByName("CTRL_ELEVACION");Vec pivotAt=pivotNode?from(pivotNode->world.translate):from(root->world.translate);
   if(aim&&enemy(target,ref,s.hunted,s.camp))desiredPitch=aim->pitch;else desiredPitch=aimFromWorld(rootRotation,center-pivotAt).pitch;}else s.target=0;}
  if(!bounds)desiredPitch=0;
  // v31.1: with nobody to follow for a few seconds the mount goes back to the centre line (the guard rides on it).
  if(bounds)s.lastTargetAt=clock_;else if(s.lastTargetAt>0&&clock_-s.lastTargetAt>4.)desired=0;
  if(!std::isfinite(desired)){desired=s.yaw;bounds.reset();}
  if(!std::isfinite(desiredPitch)){desiredPitch=s.pitch;aim.reset();}
  auto next=guardTrackYaw(s.yaw,desired,step);auto nextPitch=guardTrackPitch(s.pitch,desiredPitch,step);
  bool placed=next&&nextPitch&&postPose(s,gun,*next,*nextPitch);
  if(s.status==1&&bounds&&placed){
   bool reachable=aim.has_value()&&std::abs(desiredPitch-s.pitch)<=GuardAimTolerance;
   if(guardShouldFire(enemy(target,ref,s.hunted,s.camp),reachable,desired-s.yaw,clock_,s.nextShot,true)){
    if(shoot(s,gun,nullptr)){s.status=3;s.fireAt=clock_;s.resetStarted=false;s.nextShot=clock_+2.5;}
    else{s.nextShot=clock_+.5;if(clock_>=s.nextRefusalLog){s.nextRefusalLog=clock_+5;spdlog::info("guard v31 post shot refused gun={:08X} target={:08X} yaw={:.2f} pitch={:.2f} desiredPitch={:.2f} reason={} detail={}",s.gun,s.target,s.yaw,s.pitch,desiredPitch,s.shotRefusal?s.shotRefusal:"?",s.shotDetail);}}
   }
  }
  // v33.14: on change, plus a 30 s heartbeat (was every 2 s per loaded post, for as long as the post was loaded).
  if(s.status!=s.loggedStatus||s.target!=s.loggedTarget||s.hunted!=s.loggedHunted||clock_>=s.nextPostLog){
   s.loggedStatus=s.status;s.loggedTarget=s.target;s.loggedHunted=s.hunted;s.nextPostLog=clock_+30;
   spdlog::info("guard v31 post gun={:08X} status={} yaw={:.2f} desired={:.2f} pitch={:.2f} desiredPitch={:.2f} target={:08X} reference={:08X} hunted={}",s.gun,s.status,s.yaw,desired,s.pitch,desiredPitch,s.target,s.reference,s.hunted);}
 }
}
void GuardRuntime::tick(float dt){
 auto main=RE::Main::GetSingleton();if(!main||main->threadID!=REX::W32::GetCurrentThreadId())return;
 std::lock_guard lock(mutex_);++frame_;auto frame=guardFrame(paused(),blocked(),dt);bool pause=frame.elapsed<=0;
 double step=frame.elapsed;clock_+=step;
 mountedAirborneTick();                      // v33.7: give dragons their landing back once the player dismounts
 if(!pause){watchDragons(clock_);tickPosts(step,frame.actions);}
 for(auto& s:slots_){if(!s.lease.ticket())continue;if(s.lease.pending()){cleanup(s);continue;}
  if(pause)continue;
  RE::NiPointer<RE::TESObjectREFR> gun;RE::NiPointer<RE::Actor> actor;if(!context(s,gun,actor)){cancel(s,false,s.failure);cleanup(s);continue;}
  s.lease.enterEffect();
  if(s.acquired&&s.status==3)reload(s,gun.get());
  if(!frame.actions){s.lease.leaveEffect();continue;}
  if(!s.acquired){
   if(auto failure=operatorFailure(actor.get())){
    if(!s.packageRequested){s.packageRequested=true;actor->DrawWeaponMagicHands(false);actor->EvaluatePackage(true,false);}
    if(!operatorPackage()||clock_-s.entered>3){reject(s,gun.get(),actor.get(),failure);cancel(s,true,s.failure);}
   }else if(!acquire(s,gun.get(),actor.get()))cancel(s,true,s.failure);
   s.lease.leaveEffect();continue;}
  // Telemetry: any sample of the own hold clip keeps the watch quiet. It never gates.
  Observation obs;{std::lock_guard obsLock(observationsMutex_);obs=observations_[size_t(&s-slots_.data())];}
  if(obs.serial&&obs.serial!=s.seen&&obs.epoch==s.lease.ticket().epoch&&obs.character==s.character){s.seen=obs.serial;s.sampleAt=clock_;if(obs.clip==0)s.hold.seen(clock_);}
  // v29.1: wrists on the grips prove the pose is held even when no OAR sample is seen.
  if(clock_>=s.nextHandCheck){s.nextHandCheck=clock_+.25;handErrors(gun.get(),actor.get(),s.yaw,s.handError.data());if(s.replayAt<0&&guardHandsHeld(s.handError[0],s.handError[1]))s.hold.seen(clock_);}
  // Second step of a re-request: the graph has had GuardReplayDelay s to leave the hold.
  if(s.replayAt>=0&&clock_>=s.replayAt){s.replayAt=-1;if(!playHold(s,actor.get())){cancel(s,true,"hold PlayIdle re-request rejected");s.lease.leaveEffect();continue;}s.hold.restart(clock_);}
  if(s.replayAt<0&&s.hold.reissue(clock_)){spdlog::info("guard v29 hold re-request gun={:08X} actor={:08X}: no own clip sample and wrists not on the grips for 3 s (try {}/{})",s.gun,s.actor,s.hold.reissues(),GuardMaxReissues);if(!requestClip(s,actor.get(),0,true)){cancel(s,true,"hold PlayIdle re-request rejected");s.lease.leaveEffect();continue;}}
  if(s.hold.exhausted()&&!s.holdGaveUp&&s.replayAt<0&&s.hold.stale(clock_)){s.holdGaveUp=true;spdlog::warn("guard v29.1 hold unresolved gun={:08X} actor={:08X} reissues={} handErrorL={:.1f} handErrorR={:.1f}: keeping the pose, no more re-requests",s.gun,s.actor,s.hold.reissues(),s.handError[0],s.handError[1]);}
  if(s.status==0&&s.hold.entered(clock_)){s.status=1;spdlog::info("guard v29 holding gun={:08X} actor={:08X} yaw={:.2f}",s.gun,s.actor,s.yaw);}
  if(clock_>=s.nextScan)targets(s,gun.get(),actor.get());
  // Steer mount and operator together; the hold clip keeps both hands on the grips.
  auto target=RE::TESForm::LookupByID<RE::Actor>(s.target);std::optional<GuardProtected> bounds;double desired=s.yaw,desiredPitch=s.pitch;std::optional<GuardAim> aim;
  if(s.status>=1&&alive(target)){bounds=physicalBounds(target,0);if(bounds){auto rootRotation=from(gun->Get3D()->world.rotate);desired=std::remainder(aimFromWorld(rootRotation,bounds->feet-from(gun->Get3D()->world.translate)).yaw,360.);
   // v29.2: an enemy gets the ballistic elevation; anyone else (a passer-by) is followed along the line of sight.
   Vec center=bounds->feet+Vec{0,0,bounds->height*.5};aim=aimAt(gun.get(),center);
   if(aim&&enemy(target,actor.get(),s.hunted))desiredPitch=aim->pitch;else desiredPitch=aimFromWorld(rootRotation,center-from(gun->Get3D()->world.translate)).pitch;}else s.target=0;}
  // v29.3: with nobody to follow the barrel returns to level. A depressed muzzle sits in the mount's own
  // collision, which hid every candidate and froze the gun there for good (log 2026-10-12 15:20).
  if(!bounds)desiredPitch=0;
  if(!std::isfinite(desired)){desired=s.yaw;bounds.reset();}
  if(!std::isfinite(desiredPitch)){desiredPitch=s.pitch;aim.reset();}
  auto next=guardTrackYaw(s.yaw,desired,step);auto nextPitch=guardTrackPitch(s.pitch,desiredPitch,step);
  auto placed=next&&nextPitch?pose(s,gun.get(),actor.get(),*next,*nextPitch):Pose::invalid;const char* refusal=nullptr;
  if(placed==Pose::blocked&&next&&nextPitch&&(*next!=s.yaw||*nextPitch!=s.pitch)){refusal=s.failure;placed=pose(s,gun.get(),actor.get(),s.yaw,s.pitch);}
  s.moveRefusal=refusal?refusal:placed==Pose::ok?nullptr:s.failure;
  if(placed==Pose::invalid){cancel(s,true,next&&nextPitch?s.failure:"mount yaw / pitch outside its range");s.lease.leaveEffect();continue;}
  if(placed==Pose::ok)s.blockedSince=-1;
  else if(s.blockedSince<0)s.blockedSince=clock_;
  else if(clock_-s.blockedSince>2){cancel(s,true,"operator cannot be held on the mount");s.lease.leaveEffect();continue;}
  if(s.status==1&&bounds&&s.hold.entered(clock_)){
   // Fire only with a reachable elevation that the mount has already reached (yaw is checked by guardShouldFire).
   bool reachable=aim.has_value()&&std::abs(desiredPitch-s.pitch)<=GuardAimTolerance;
   if(guardShouldFire(enemy(target,actor.get(),s.hunted),reachable,desired-s.yaw,clock_,s.nextShot,placed==Pose::ok)){
    if(shoot(s,gun.get(),actor.get())){s.status=3;s.fireAt=clock_;s.resetStarted=false;s.nextShot=clock_+2.5;}
    else{s.nextShot=clock_+.5;if(clock_>=s.nextRefusalLog){s.nextRefusalLog=clock_+5;spdlog::info("guard v29.2 shot refused gun={:08X} target={:08X} yaw={:.2f} pitch={:.2f} desiredPitch={:.2f} reason={}",s.gun,s.target,s.yaw,s.pitch,desiredPitch,s.shotRefusal?s.shotRefusal:"?");}}
   }
  }
  poseLog(s,gun.get(),actor.get(),obs,desired,desiredPitch);
  s.lease.leaveEffect();
 }
}
}
