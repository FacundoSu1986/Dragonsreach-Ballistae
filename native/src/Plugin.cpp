#include <RE/Skyrim.h>
#include <SKSE/SKSE.h>
#include <spdlog/sinks/basic_file_sink.h>
#include "Astra/Core.h"
#include "Astra/FastShotRuntime.h"
#include "Astra/GuardRuntime.h"
#include <atomic>
#include <algorithm>
#include <chrono>
#include <optional>

namespace {
using namespace Astra;
Session session;
FastShotRuntime fastShots(session);
GuardRuntime guards;
std::atomic_bool available{false};
using UpdateFn = void (*)(RE::FirstPersonState*, RE::BSTSmartPointer<RE::TESCameraState>&);
using RotationFn = void (*)(RE::FirstPersonState*, RE::NiQuaternion&);
using TranslationFn = void (*)(RE::FirstPersonState*, RE::NiPoint3&);
using EndFn = void (*)(RE::FirstPersonState*);
using CameraUpdateFn = void (*)(RE::PlayerCamera*);
REL::Relocation<UpdateFn> originalUpdate;
REL::Relocation<RotationFn> originalRotation;
REL::Relocation<TranslationFn> originalTranslation;
REL::Relocation<EndFn> originalEnd;
REL::Relocation<CameraUpdateFn> originalCameraUpdate;

Vec from(RE::NiPoint3 p) { return {p.x,p.y,p.z}; }
Mat from(RE::NiMatrix3 m) { Mat r; for (int i=0;i<3;++i)for(int j=0;j<3;++j)r.m[3*i+j]=m.entry[i][j];return r; }
RE::NiMatrix3 into(Mat m) { RE::NiMatrix3 r;for(int i=0;i<3;++i)for(int j=0;j<3;++j)r.entry[i][j]=static_cast<float>(m.m[3*i+j]);return r; }
Transform from(RE::NiTransform t) { return {from(t.rotate),from(t.translate),t.scale}; }
Mat quatMatrix(RE::NiQuaternion q) {
 double n=std::sqrt(double(q.w)*q.w+double(q.x)*q.x+double(q.y)*q.y+double(q.z)*q.z);
 if(!std::isfinite(n)||n<1e-8)return{{NAN,0,0,0,1,0,0,0,1}};
 double w=q.w/n,x=q.x/n,y=q.y/n,z=q.z/n;
 return{{1-2*(y*y+z*z),2*(x*y-w*z),2*(x*z+w*y),2*(x*y+w*z),1-2*(x*x+z*z),2*(y*z-w*x),2*(x*z-w*y),2*(y*z+w*x),1-2*(x*x+y*y)}};
}
RE::NiQuaternion matrixQuat(Mat m) {
 double w,x,y,z,t=m.m[0]+m.m[4]+m.m[8];
 if(t>0){double s=std::sqrt(t+1)*2;w=s/4;x=(m.m[7]-m.m[5])/s;y=(m.m[2]-m.m[6])/s;z=(m.m[3]-m.m[1])/s;}
 else if(m.m[0]>m.m[4]&&m.m[0]>m.m[8]){double s=std::sqrt(1+m.m[0]-m.m[4]-m.m[8])*2;w=(m.m[7]-m.m[5])/s;x=s/4;y=(m.m[1]+m.m[3])/s;z=(m.m[2]+m.m[6])/s;}
 else if(m.m[4]>m.m[8]){double s=std::sqrt(1+m.m[4]-m.m[0]-m.m[8])*2;w=(m.m[2]-m.m[6])/s;x=(m.m[1]+m.m[3])/s;y=s/4;z=(m.m[5]+m.m[7])/s;}
 else{double s=std::sqrt(1+m.m[8]-m.m[0]-m.m[4])*2;w=(m.m[3]-m.m[1])/s;x=(m.m[2]+m.m[6])/s;y=(m.m[5]+m.m[7])/s;z=s/4;}
 double n=std::sqrt(w*w+x*x+y*y+z*z);return {float(w/n),float(x/n),float(y/n),float(z/n)};
}
double matrixDistance(Mat a,Mat b){double s=0;for(int i=0;i<9;++i)s+=std::abs(a.m[i]-b.m[i]);return s;}
bool rotationValid(Mat m){return finite({m,{0,0,0},1})&&matrixDistance(m.transpose()*m,Mat{})<0.01;}
Key key(RE::TESObjectREFR* ref,int token){return ref?Key{ref->CreateRefHandle().native_handle(),token}:Key{};}

// This cache is exclusively accessed by camera hooks on the game thread.
// NiPointers retain only the currently acquired scene; no unloaded TESObjectREFR pointer is cached.
struct Binding {
 uint64_t epoch{};
 RE::NiPointer<RE::NiAVObject> root,yaw,pitch,anchor,projectile,operatorNode,visualBolt,frontPost;
 RE::NiPointer<RE::NiNode> cameraRoot;
 RE::NiNode* cameraParent{};  // identity only, never dereferenced after acquisition
 Mat yawBase,pitchBase,adapter;
 bool translationLocal{true},rotationLocal{true};
} binding;

// v09 diagnostics. The v08 capture at yaw ~176 shows the player-eye view while this plugin
// published the sight and never dropped the session (reports/user_evidence_v08.json). These
// counters and watches record what the camera nodes actually hold one frame later, and every
// reason the sight is dropped. Game thread only, like the binding.
struct Diagnostics {
 CameraWatch rootWatch,cameraWatch;
 std::optional<Snapshot> published;          // what the last update published
 uint64_t frames{},postWrites{},postSkips{};
 double lastBeat{},suspendedAt{};
} diag;
std::atomic<uint64_t> gettersEligible{0},gettersVanilla{0};

double seconds(){return std::chrono::duration<double>(std::chrono::steady_clock::now().time_since_epoch()).count();}
int stateIndex(RE::PlayerCamera* camera,const RE::TESCameraState* state){
 if(!camera||!state)return -1;
 for(std::size_t i=0;i<RE::CameraStates::kTotal;++i)if(camera->cameraStates[i].get()==state)return static_cast<int>(i);
 return -1;
}
RE::NiAVObject* renderCamera(RE::NiNode* root){
 // The NiCamera under cameraRoot, found by Ni RTTI; no Address Library lookup is added.
 if(!root)return nullptr;
 for(auto& child:root->children)if(child&&netimmerse_cast<RE::NiCamera*>(child.get()))return child.get();
 return nullptr;
}
void resetDiagnostics(){diag=Diagnostics{};gettersEligible=0;gettersVanilla=0;}
void drop(Ticket ticket,const std::string& reason){
 if(session.invalidate(ticket)){spdlog::warn("sight dropped: {}",reason);binding={};resetDiagnostics();}
}
std::string vec(Vec v){return spdlog::fmt_lib::format("({:.1f},{:.1f},{:.1f})",v.x,v.y,v.z);}
// v09: leaving first person (TweenMenu camera, transitions) suspends instead of dropping. The lease, pose and
// any frozen shot survive; writes stop until FirstPersonState::Update runs again. Papyrus ends the session if
// the camera does not come back to first person after its menu grace (a permanent loss).
void suspendSight(Ticket ticket,const std::string& reason){
 if(session.suspend(ticket)){diag.suspendedAt=seconds();diag.published.reset();diag.rootWatch.reset();diag.cameraWatch.reset();spdlog::info("sight suspended: {}",reason);}
}

constexpr double CameraDeviationLogUnits=25.;
void recordRendered(RE::PlayerCamera* camera,RE::FirstPersonState* self){
 // Runs before this frame's composition: the nodes still hold last frame's final camera.
 if(!diag.published||!camera||!camera->cameraRoot)return;
 auto cr=camera->cameraRoot.get();auto cam=renderCamera(cr);
 Vec expected=diag.published->worldCamera.translation;
 Vec rootPos=from(cr->world.translate),camPos=cam?from(cam->world.translate):rootPos;
 double now=seconds();
 auto player=RE::PlayerCharacter::GetSingleton();
 Vec playerPos=player?from(player->GetPosition()):Vec{NAN,NAN,NAN};
 Vec eye=self&&self->firstPersonCameraObj?from(self->firstPersonCameraObj->world.translate):Vec{NAN,NAN,NAN};
 double heading=player?deg(player->data.angle.z):NAN;
 auto report=[&](const char* what,const WatchEvent& e){
  // v33.14: a fast turn always trails the published camera by a few units for one frame (2-19 u, test 2026-10-17:
  // 388 warnings in two minutes). The v09 failure this watch exists for was 140-178 u; log episodes from 25 u.
  if(e.kind==WatchEvent::kNone||e.maxDeviation<CameraDeviationLogUnits)return;
  const char* kind=e.kind==WatchEvent::kStart?"start":e.kind==WatchEvent::kEnd?"end":"ongoing";
  spdlog::warn("camera deviation {} node={} dev={:.1f} max={:.1f} for={:.2f}s yaw={:.2f} pitch={:.2f} heading={:.2f} expected={} cameraRoot={} niCamera={} vanillaEye={} player={} state={} frames={} getters(eligible/vanilla)={}/{} post(writes/skips)={}/{}",
   kind,what,e.deviation,e.maxDeviation,e.seconds,diag.published->aim.yaw,diag.published->aim.pitch,heading,vec(expected),vec(rootPos),cam?vec(camPos):"none",vec(eye),vec(playerPos),
   stateIndex(camera,camera->currentState.get()),diag.frames,gettersEligible.load(),gettersVanilla.load(),diag.postWrites,diag.postSkips);
 };
 report("cameraRoot",diag.rootWatch.observe(length(rootPos-expected),now));
 report("NiCamera",diag.cameraWatch.observe(length(camPos-expected),now));
 if(now-diag.lastBeat>=1.0){
  diag.lastBeat=now;
  spdlog::info("sight beat yaw={:.2f} pitch={:.2f} heading={:.2f} cameraToPlayer={:.1f} devRoot={:.1f} devCamera={:.1f} state={} frames={} getters(eligible/vanilla)={}/{} post(writes/skips)={}/{}",
   diag.published->aim.yaw,diag.published->aim.pitch,heading,length(expected-playerPos),length(rootPos-expected),length(camPos-expected),
   stateIndex(camera,camera->currentState.get()),diag.frames,gettersEligible.load(),gettersVanilla.load(),diag.postWrites,diag.postSkips);
 }
}

void updateWorld(RE::NiAVObject* object){
 RE::NiUpdateData data{};data.flags=RE::NiUpdateData::Flag::kDirty;
 object->UpdateWorldData(&data);
 if(auto node=object->AsNode())for(auto& child:node->children)if(child)updateWorld(child.get());
}

bool calibrateSpace(RE::PlayerCamera* camera,Mat originalRot,Vec originalPos,Mat logical) {
 auto cr=camera->cameraRoot.get(); if(!cr)return false;
 Transform parent=cr->parent?from(cr->parent->world):Transform{};
 if(!finite(parent)||!rotationValid(parent.rotation)||!rotationValid(logical)||!rotationValid(originalRot))return false;
 // TESCamera getter consumer space is observed, not inferred from declarations.
 // Without a parent the world and root-local spaces coincide, including scale.
 if(!cr->parent || (matrixDistance(parent.rotation,Mat{})<1e-5&&length(parent.translation)<1e-5&&std::abs(parent.scale-1)<1e-5)) {
  binding.translationLocal=binding.rotationLocal=true;
 } else {
  double localPos=length(originalPos-from(cr->local.translate));
  double worldPos=length(originalPos-from(cr->world.translate));
  double localRot=matrixDistance(originalRot,from(cr->local.rotate));
  double worldRot=matrixDistance(originalRot,from(cr->world.rotate));
  if(std::min(localPos,worldPos)>32 || std::min(localRot,worldRot)>0.3)return false;
  if(std::abs(localPos-worldPos)<0.1 && length(parent.translation)>0.1)return false;
  if(std::abs(localRot-worldRot)<0.01 && matrixDistance(parent.rotation,Mat{})>0.01)return false;
  binding.translationLocal=localPos<=worldPos;
  binding.rotationLocal=localRot<=worldRot;
 }
 Mat originalWorld=binding.rotationLocal?parent.rotation*originalRot:originalRot;
 binding.adapter=logical.transpose()*originalWorld;
 if(!rotationValid(binding.adapter))return false;
 spdlog::info("camera calibration epoch={} translation={} rotation={} parentScale={} parent={} parentWorld={} adapter=[{},{},{},{},{},{},{},{},{}]",binding.epoch,binding.translationLocal?"cameraRoot-local":"world",binding.rotationLocal?"cameraRoot-local":"world",parent.scale,cr->parent?cr->parent->name.c_str():"none",vec(parent.translation),binding.adapter.m[0],binding.adapter.m[1],binding.adapter.m[2],binding.adapter.m[3],binding.adapter.m[4],binding.adapter.m[5],binding.adapter.m[6],binding.adapter.m[7],binding.adapter.m[8]);
 return true;
}

void update(RE::FirstPersonState* self,RE::BSTSmartPointer<RE::TESCameraState>& next) {
 if(session.ticket())recordRendered(RE::PlayerCamera::GetSingleton(),self);
 // Engine originals may call virtual getters. Never call them while owning session mutex.
 originalUpdate(self,next);
 auto ticket=session.ticket(); if(!ticket){binding={};resetDiagnostics();return;}
 ++diag.frames;
 auto camera=RE::PlayerCamera::GetSingleton();auto player=RE::PlayerCharacter::GetSingleton();
 if(!camera||!player||player->IsDead()||!camera->cameraRoot){drop(ticket,spdlog::fmt_lib::format("camera/player unavailable (camera={} player={} dead={} cameraRoot={})",camera!=nullptr,player!=nullptr,player&&player->IsDead(),camera&&camera->cameraRoot));return;}
 if(camera->currentState.get()!=self||(next&&next.get()!=self)){suspendSight(ticket,spdlog::fmt_lib::format("first-person state left (current={} next={})",stateIndex(camera,camera->currentState.get()),next?stateIndex(camera,next.get()):-2));return;}
 RE::RefHandle handle=ticket.key.handle;RE::NiPointer<RE::TESObjectREFR> gun;RE::LookupReferenceByHandle(handle,gun);
 if(!gun||gun->IsDeleted()||!gun->Get3D()){drop(ticket,"ballesta reference or 3D unavailable");return;}
 auto root=gun->Get3D();
 if(binding.epoch==ticket.epoch&&(binding.root.get()!=root||binding.cameraRoot.get()!=camera->cameraRoot.get())){drop(ticket,"loaded3D/cameraRoot identity changed");return;}
 Transform rootWorld=from(root->world);
 double heading=player->data.angle.z,pitchAngle=player->data.angle.x;
 Vec look{std::sin(heading)*std::cos(pitchAngle),std::cos(heading)*std::cos(pitchAngle),-std::sin(pitchAngle)};
 Aim sample=aimFromWorld(rootWorld.rotation,look);
 RE::NiQuaternion vanillaRotation{};RE::NiPoint3 vanillaTranslation{};
 originalRotation(self,vanillaRotation);originalTranslation(self,vanillaTranslation);
 bool paused=RE::UI::GetSingleton()&&RE::UI::GetSingleton()->GameIsPaused();
 std::string rejected;
 bool wasSuspended=session.suspended();
 bool applied=session.update(ticket,sample,paused,[&](Aim aim)->Snapshot {
  // Scene access, acquisition, local writes, world update and snapshot publication
  // are all inside one transaction with CaptureAim(freeze) and EndSight.
  if(binding.epoch!=ticket.epoch){
   binding={};binding.epoch=ticket.epoch;binding.root.reset(root);binding.cameraRoot=camera->cameraRoot;binding.cameraParent=camera->cameraRoot->parent;
   resetDiagnostics();
   binding.yaw.reset(root->GetObjectByName("CTRL_GIRO_360"));binding.pitch.reset(root->GetObjectByName("CTRL_ELEVACION"));
   binding.anchor.reset(root->GetObjectByName("AstraSightCameraNode"));binding.projectile.reset(root->GetObjectByName("ProjectileNode"));
   binding.operatorNode.reset(root->GetObjectByName("OperatorNode"));binding.visualBolt.reset(root->GetObjectByName("VIROTE_VISUAL"));
   binding.frontPost.reset(root->GetObjectByName("AstraSightFrontPost"));
   if(!binding.yaw||!binding.pitch||!binding.anchor||!binding.projectile||!binding.operatorNode||!binding.visualBolt||!binding.frontPost){rejected="native sight missing required NIF node";return {};}
   if(binding.pitch->parent!=binding.yaw.get()||binding.anchor->parent!=binding.pitch.get()||binding.frontPost->parent!=binding.pitch.get()){rejected="native sight node hierarchy mismatch";return {};}
   // Papyrus applied initial pose before Begin. Remove that pose exactly once.
   binding.yawBase=rz(-rad(aim.yaw))*from(binding.yaw->local.rotate);
   binding.pitchBase=rx(rad(aim.pitch))*from(binding.pitch->local.rotate);
   if(!calibrateSpace(camera,quatMatrix(vanillaRotation),from(vanillaTranslation),logicalBasis(look))) {rejected="native sight camera calibration failed";return {};}
  }
  if(!finite(rootWorld)||!rotationValid(rootWorld.rotation)||!rotationValid(binding.yawBase)||!rotationValid(binding.pitchBase)){rejected="non-finite root or aim base";return {};}
  Vec foot=from(binding.operatorNode->world.translate)-rootWorld.rotation*Vec{0,0,119*rootWorld.scale};
  Vec distance=from(player->GetPosition())-foot;
  if(rootWorld.scale<=0||rootWorld.scale>100||!std::isfinite(length(distance))||distance.x*distance.x+distance.y*distance.y>160*160||std::abs(distance.z)>64){rejected=spdlog::fmt_lib::format("native sight operator out of range offset={}",vec(distance));return {};}
  binding.yaw->local.rotate=into(rz(rad(aim.yaw))*binding.yawBase);
  binding.pitch->local.rotate=into(rx(-rad(aim.pitch))*binding.pitchBase);
  // Transform-only recursion avoids replaying Fire/Reset controllers during camera update.
  updateWorld(binding.yaw.get());
  auto anchor=from(binding.anchor->world);auto projectile=from(binding.projectile->world);
  if(!finite(anchor)||!finite(projectile)||!rotationValid(anchor.rotation)){rejected="non-finite anchor or projectile";return {};}
  Vec anchorForward=anchor.rotation*Vec{0,1,0};Vec expected=rootWorld.rotation*gunDirection(aim.yaw,aim.pitch);
  if(length(anchorForward-expected)>0.02||length(anchorForward-projectile.rotation*Vec{0,1,0})>0.02){rejected="native sight anchor/projectile direction mismatch";return {};}
  // v10: the camera sits at the tail on the line rear sight (anchor) -> 75 m zero target and slides toward
  // the rear sight as elevation rises; the front post is moved onto that line. The bore checks above and
  // the player look stay on the anchor. (v09 log: the old anchor camera was pulled toward the player head
  // by the pedestal collision; v10 also lowers that collision, see build_assets.py.)
  auto pose=sightPose(anchor.translation,anchor.rotation*Vec{1,0,0},projectile.translation,projectile.rotation*Vec{0,1,0},rootWorld.translation,rootWorld.rotation*Vec{0,0,1},rootWorld.scale);
  if(!pose.valid){rejected="sight pose invalid";return {};}
  Transform pitchWorld=from(binding.pitch->world);
  if(!finite(pitchWorld)||pitchWorld.scale<=0){rejected="non-finite pitch node";return {};}
  Vec postLocal=pitchWorld.rotation.transpose()*(pose.frontPost-pitchWorld.translation)*(1/pitchWorld.scale);
  binding.frontPost->local.translate={float(postLocal.x),float(postLocal.y),float(postLocal.z)};
  updateWorld(binding.frontPost.get());
  Transform worldCamera{pose.rotation()*binding.adapter,pose.camera,1};
  auto cr=camera->cameraRoot.get();Transform parent=cr->parent?from(cr->parent->world):Transform{};
  if(!finite(parent)||!rotationValid(parent.rotation)){rejected="non-finite cameraRoot parent";return {};}
  auto local=toLocal(parent,worldCamera);
  Transform output{binding.rotationLocal?local.rotation:worldCamera.rotation,binding.translationLocal?local.translation:worldCamera.translation,1};
  if(!finite(output)||!rotationValid(output.rotation)){rejected="non-finite camera output";return {};}
  // Reconcile player logical look with the applied world direction. This prevents
  // local-Euler folding at a tilted root and discards overshoot before next input.
#if ASTRA_RUNTIME_AE17
  player->SetLooking(float(-std::asin(std::clamp(expected.z,-1.,1.))));
#else
  player->SetRotationX(float(-std::asin(std::clamp(expected.z,-1.,1.))));
#endif
#if ASTRA_RUNTIME_AE17
  player->SetHeading(float(rad(wrapDegrees(deg(std::atan2(expected.x,expected.y))))));
#else
  player->SetRotationZ(float(rad(wrapDegrees(deg(std::atan2(expected.x,expected.y))))));
#endif
  return {aim,output,true,reinterpret_cast<uintptr_t>(self),worldCamera,rootWorld,projectile,true};
 },true,reinterpret_cast<uintptr_t>(root));
 if(!session.ticket()){
  // Session::update drops the lease on a rejected apply or a non-finite look sample. A lease
  // ended elsewhere (EndSight) meanwhile is not a drop and is already logged as "sight end".
  if(!rejected.empty())spdlog::warn("sight dropped: {}",rejected);
  else if(!std::isfinite(sample.yaw)||!std::isfinite(sample.pitch))spdlog::warn("sight dropped: non-finite look sample heading={} pitch={}",heading,pitchAngle);
  binding={};resetDiagnostics();return;
 }
 if(applied){
  diag.published=session.snapshot();
  if(wasSuspended)spdlog::info("sight resumed after {:.2f}s yaw={:.2f} pitch={:.2f}",seconds()-diag.suspendedAt,diag.published?diag.published->aim.yaw:NAN,diag.published?diag.published->aim.pitch:NAN);
 }
 // Runtime evidence shows this state callback running every frame while the
 // PlayerCamera virtual Update hook is bypassed. Drive firing here, only after
 // Session::update released its lock and published the coherent scene pose.
 fastShots.tick();
}

bool eligible(RE::FirstPersonState* self,const Snapshot& snapshot){return snapshot.stateIdentity==reinterpret_cast<uintptr_t>(self)&&self->camera&&self->camera->currentState.get()==self;}
void cameraUpdate(RE::PlayerCamera* camera){
 // TESCamera finishes composing from getters before our final world-anchor write.
 // Engine code is outside the mutex: it can itself call our virtual getters.
 originalCameraUpdate(camera);
 auto ticket=session.ticket();if(!ticket)return;
 // Suspended: the camera belongs to another state (menu); never write it.
 if(session.suspended())return;
 std::string failure;bool left=false;
 bool visited=session.visitSnapshot(ticket,[&](const Snapshot& snap){
  if(camera&&camera->currentState&&(reinterpret_cast<uintptr_t>(camera->currentState.get())!=snap.stateIdentity||
     camera->currentState.get()!=camera->cameraStates[RE::CameraStates::kFirstPerson].get())){left=true;return;}
  if(!camera||!camera->cameraRoot||!camera->currentState||
     binding.epoch!=ticket.epoch||binding.cameraRoot.get()!=camera->cameraRoot.get()){
   failure=spdlog::fmt_lib::format("post-camera check failed (state={} epochMatch={} rootMatch={})",camera?stateIndex(camera,camera->currentState.get()):-1,binding.epoch==ticket.epoch,camera&&binding.cameraRoot.get()==camera->cameraRoot.get());return;}
  auto cr=camera->cameraRoot.get();auto parent=cr->parent?from(cr->parent->world):Transform{};
  if(!finite(parent)||parent.scale<=0||!rotationValid(parent.rotation)||!finite(snap.worldCamera)){failure="post-camera parent or snapshot not finite";return;}
  auto local=toLocal(parent,snap.worldCamera);
  cr->local.rotate=into(local.rotation);cr->local.translate={float(local.translation.x),float(local.translation.y),float(local.translation.z)};cr->local.scale=float(local.scale);
  // NiCamera::UpdateWorldData updates its projection/world-to-camera matrices.
  // Transform-only: never advance weapon or camera animation controllers twice.
  updateWorld(cr);
  ++diag.postWrites;
 });
 if(!visited)++diag.postSkips;
 if(left)suspendSight(ticket,spdlog::fmt_lib::format("post-camera: state={} is not first person",stateIndex(camera,camera->currentState.get())));
 if(!failure.empty())drop(ticket,failure);
}
void rotation(RE::FirstPersonState* self,RE::NiQuaternion& out){if(auto snapshot=session.snapshot();snapshot&&eligible(self,*snapshot)){++gettersEligible;out=matrixQuat(snapshot->camera.rotation);return;}if(session.ticket())++gettersVanilla;originalRotation(self,out);}
void translation(RE::FirstPersonState* self,RE::NiPoint3& out){if(auto snapshot=session.snapshot();snapshot&&eligible(self,*snapshot)){++gettersEligible;auto p=snapshot->camera.translation;out={float(p.x),float(p.y),float(p.z)};return;}if(session.ticket())++gettersVanilla;originalTranslation(self,out);}
void cameraEnd(RE::FirstPersonState* self){if(auto t=session.ticket())suspendSight(t,"FirstPersonState::End (camera left first person)");originalEnd(self);}

bool IsAvailable(RE::StaticFunctionTag*){return available.load();}
int GetAPIVersion(RE::StaticFunctionTag*){return 4;}
int GetCameraState(RE::StaticFunctionTag*){
 auto camera=RE::PlayerCamera::GetSingleton();
 // Read identity once; never dereference a state pointer on a VM tasklet.
 auto current=camera?camera->currentState.get():nullptr;
 if(!current)return -1;
 for(std::size_t i=0;i<RE::CameraStates::kTotal;++i)
  if(current==camera->cameraStates[i].get())return static_cast<int>(i);
 return -1;
}
bool BeginSight(RE::StaticFunctionTag*,RE::TESObjectREFR* gun,int token,float yaw,float pitch){auto k=key(gun,token);bool ok=available.load()&&guards.admitPlayer(k.handle,[&]{return fastShots.beginLegacy(k,yaw,pitch);});spdlog::info("sight begin token={} yaw={} pitch={} accepted={}",token,yaw,pitch,ok);return ok;}
bool IsSightReady(RE::StaticFunctionTag*,RE::TESObjectREFR* gun,int token){return available.load()&&session.ready(key(gun,token));}
bool ValidateShot(RE::StaticFunctionTag*,RE::TESObjectREFR* gun,int token,float yaw,float pitch,float pivotHeight){return session.validateShot(key(gun,token),{yaw,pitch},pivotHeight);}
std::vector<float> CaptureAim(RE::StaticFunctionTag*,RE::TESObjectREFR* gun,int token,bool freeze){auto k=key(gun,token);auto a=session.capture(k,freeze);if(a&&freeze)spdlog::info("shot freeze handle={} token={} yaw={} pitch={}",k.handle,token,a->yaw,a->pitch);return a?std::vector<float>{papyrusYaw(a->yaw),float(a->pitch)}:std::vector<float>{};}
bool SetFrozen(RE::StaticFunctionTag*,RE::TESObjectREFR* gun,int token,bool frozen){auto k=key(gun,token);bool changed=session.freeze(k,frozen);if(changed)spdlog::info("shot frozen={} handle={} token={}",frozen,k.handle,token);return changed;}
bool BeginFastSight(RE::StaticFunctionTag*,RE::TESObjectREFR* gun,int token,float yaw,float pitch,RE::TESObjectWEAP* weapon,RE::TESAmmo* ammo,RE::TESAmmo* cost,RE::TESSound* sound,std::vector<float> values,bool continuous){
 if(!available||!gun||!weapon||!ammo||!cost||values.size()!=12||!guards.stationIdle(key(gun,token).handle))return false;
 FastConfig c;c.weapon=weapon->GetFormID();c.ammo=ammo->GetFormID();c.cost=cost->GetFormID();c.sound=sound?sound->GetFormID():0;
 c.timing={values[0],values[1],values[2],values[3],continuous};c.limits={values[4],values[5],values[6],values[7]};c.pivot=values[8];c.operatorHeight=values[9];c.operatorDistance=values[10];c.operatorTolerance=values[11];
 auto k=key(gun,token);bool accepted=guards.admitPlayer(k.handle,[&]{return fastShots.begin(k,yaw,pitch,c);});spdlog::info("fast sight begin token={} accepted={} yaw_center={} yaw_half={} pitch_min={} pitch_max={}",token,accepted,c.limits.yawCenter,c.limits.yawHalf,c.limits.pitchMin,c.limits.pitchMax);return accepted;
}
bool IsFastSightReady(RE::StaticFunctionTag*,RE::TESObjectREFR* gun,int token){return fastShots.ready(key(gun,token));}
bool IsEffectsQuiescent(RE::StaticFunctionTag*,RE::TESObjectREFR* gun,int token){return fastShots.quiescent(key(gun,token));}
bool ResetIdleScene(RE::StaticFunctionTag*,RE::TESObjectREFR* gun){auto k=key(gun,0);return available.load()&&gun&&guards.admitPlayer(k.handle,[&]{return fastShots.resetIdleScene(k);});}
int GetFireMode(RE::StaticFunctionTag*,RE::TESObjectREFR* gun,int token){return fastShots.mode(key(gun,token));}
// v33.4: AstraAsedioActi.RetainMountedCombat walks this list and reasserts StartCombat on each actor.
RE::Actor* GetMountedAttacker(RE::StaticFunctionTag*,RE::TESObjectREFR* gun,int token,int index){return fastShots.mountedAttacker(key(gun,token),index);}
// v33.10: open ground in a player ballista's field of fire where a dragon fighting the mounted player is made to land
// (AstraAsedioActi.SteerLanding). The user picked the watchtower one in game on 2026-10-17 (Atalaya 14000A00 is ~35 m away).
// v33.12: decoy = where an invisible stand-in for the mounted player waits on open ground in the dragon's view (test
// 13:20: from the same spot ~670 u below, the dragon saw and breathed at the dismounted player, never at the mounted
// one: los=false). It is 20% of the way from the ballista to the landing point, on the LAND height (-5272.4) + 10.
struct LandingPoint{float x,y,z;float decoyX,decoyY,decoyZ;};
constexpr LandingPoint LandingPoints[]={{2904.75f,-16650.41f,-5406.81f,4313.38f,-15268.33f,-5262.4f}};
RE::ObjectRefHandle landingMade[std::size(LandingPoints)];RE::ObjectRefHandle decoyMade[std::size(LandingPoints)];
// v33.14: ref handles are per game session; a load or new game must not reuse one from the previous session.
void forgetLanding(){for(auto& h:landingMade)h={};for(auto& h:decoyMade)h={};}
int landingIndex(RE::TESObjectREFR* gun){
 if(!gun)return -1;auto at=gun->GetPosition();
 for(std::size_t i=0;i<std::size(LandingPoints);++i){float dx=at.x-LandingPoints[i].x,dy=at.y-LandingPoints[i].y;if(dx*dx+dy*dy<=6000.f*6000.f)return int(i);}
 return -1;}
RE::TESObjectREFR* GetLandingMarker(RE::StaticFunctionTag*,RE::TESObjectREFR* gun){
 int i=landingIndex(gun);if(i<0)return nullptr;auto& l=LandingPoints[i];
 if(auto made=landingMade[i].get();made&&!made->IsDisabled()&&!made->IsDeleted())return made.get();
 auto marker=RE::TESForm::LookupByID<RE::TESBoundObject>(0x3B);auto ref=marker?gun->PlaceObjectAtMe(marker,true):nullptr;if(!ref)return nullptr;
 ref->SetPosition(l.x,l.y,l.z);landingMade[i]=ref->GetHandle();
 spdlog::info("landing marker {:08X} placed at {:.1f},{:.1f},{:.1f} for ballista {:08X}",ref->GetFormID(),l.x,l.y,l.z,gun->GetFormID());return ref.get();}
// v33.12: the decoy is the AstraAsedio guard base (0x80F); AstraAsedioActi hides, restrains and removes it.
RE::Actor* PlaceLandingDecoy(RE::StaticFunctionTag*,RE::TESObjectREFR* gun){
 int i=landingIndex(gun);if(i<0)return nullptr;auto& l=LandingPoints[i];
 if(auto made=decoyMade[i].get()){auto a=made->As<RE::Actor>();if(a&&!a->IsDead()&&!a->IsDisabled()&&!a->IsDeleted())return a;}
 auto forms=RE::TESDataHandler::GetSingleton();auto base=forms?forms->LookupForm<RE::TESNPC>(0x80F,"DragonsreachBallistae.esp"):nullptr;
 auto ref=base?gun->PlaceObjectAtMe(base,false):nullptr;auto a=ref?ref->As<RE::Actor>():nullptr;if(!a)return nullptr;
 ref->SetPosition(l.decoyX,l.decoyY,l.decoyZ);decoyMade[i]=a->GetHandle();
 spdlog::info("landing decoy {:08X} placed at {:.1f},{:.1f},{:.1f} for ballista {:08X}",a->GetFormID(),l.decoyX,l.decoyY,l.decoyZ,gun->GetFormID());return a;}
bool EndSight(RE::StaticFunctionTag*,RE::TESObjectREFR* gun,int token){bool ended=fastShots.end(key(gun,token));spdlog::info("sight end request token={} quiescent={}",token,ended);return ended;}
bool GuardAvailable(RE::StaticFunctionTag*){return available.load()&&guards.available();}
int GuardAPIVersion(RE::StaticFunctionTag*){return 1;}
bool BeginOperation(RE::StaticFunctionTag*,RE::TESObjectREFR* gun,RE::Actor* actor,int token,RE::TESObjectWEAP* weapon,RE::TESAmmo* ammo,RE::TESSound* sound){return guards.begin(gun,actor,token,weapon,ammo,sound);}
int GetGuardStatus(RE::StaticFunctionTag*,RE::TESObjectREFR* gun,int token){return guards.status(key(gun,token));}
bool EndOperation(RE::StaticFunctionTag*,RE::TESObjectREFR* gun,int token){return guards.end(key(gun,token));}
bool NotifyCombat(RE::StaticFunctionTag*,RE::TESObjectREFR* gun,int token,RE::Actor* actor){return guards.notify(key(gun,token),actor);}
class CaptureFunction final:public RE::NativeFunction<std::vector<float>(RE::StaticFunctionTag*,RE::TESObjectREFR*,int,bool)> {
 public:
 CaptureFunction():NativeFunction("CaptureAim","AstraSightNative",CaptureAim){}
 bool MarshallAndDispatch(RE::BSScript::Variable&,RE::BSScript::Internal::VirtualMachine& vm,RE::VMStackID,RE::BSScript::Variable& out,const RE::BSScript::StackFrame& frame)const override {
  auto page=frame.GetPageForFrame();auto gun=frame.GetStackFrameVariable(0,page).Unpack<RE::TESObjectREFR*>();auto token=frame.GetStackFrameVariable(1,page).Unpack<int>();auto freeze=frame.GetStackFrameVariable(2,page).Unpack<bool>();auto values=CaptureAim(nullptr,gun,token,freeze);
  // CommonLib generic vector pack starts with untyped None on allocation failure.
  // Preserve the PSC float[] type even if the VM represents a zero array as null.
  RE::BSScript::TypeInfo floatType(RE::BSScript::TypeInfo::RawType::kFloat);
  out=RE::BSScript::Variable(RE::BSScript::TypeInfo(RE::BSScript::TypeInfo::RawType::kFloatArray));
  RE::BSTSmartPointer<RE::BSScript::Array> array;
  if(vm.CreateArray(floatType,static_cast<uint32_t>(values.size()),array)&&array){for(uint32_t i=0;i<values.size();++i)(*array)[i].SetFloat(values[i]);out.SetArray(std::move(array));}
  return true;
 }
};
bool registerPapyrus(RE::BSScript::IVirtualMachine* vm){
 vm->RegisterFunction("IsAvailable","AstraGuardNative",GuardAvailable,true);
 vm->RegisterFunction("GetAPIVersion","AstraGuardNative",GuardAPIVersion,true);
 vm->RegisterFunction("BeginOperation","AstraGuardNative",BeginOperation,false);
 vm->RegisterFunction("GetStatus","AstraGuardNative",GetGuardStatus,true);
 vm->RegisterFunction("EndOperation","AstraGuardNative",EndOperation,true);
 vm->RegisterFunction("NotifyCombat","AstraGuardNative",NotifyCombat,false);
 // These functions read identity or transact with the mutex-protected session.
 // Scene writes still occur only in FirstPersonState::Update on the game thread.
 vm->RegisterFunction("IsAvailable","AstraSightNative",IsAvailable,true);
 vm->RegisterFunction("GetAPIVersion","AstraSightNative",GetAPIVersion,true);
 vm->RegisterFunction("GetCameraState","AstraSightNative",GetCameraState,true);
 vm->RegisterFunction("BeginSight","AstraSightNative",BeginSight,true);
 vm->RegisterFunction("BeginFastSight","AstraSightNative",BeginFastSight,true);
 vm->RegisterFunction("IsFastSightReady","AstraSightNative",IsFastSightReady,true);
 vm->RegisterFunction("IsEffectsQuiescent","AstraSightNative",IsEffectsQuiescent,true);
 // Deliberately not callable from tasklets: this operation mutates loaded 3D.
 vm->RegisterFunction("ResetIdleScene","AstraSightNative",ResetIdleScene,false);
 vm->RegisterFunction("GetFireMode","AstraSightNative",GetFireMode,true);
 vm->RegisterFunction("IsSightReady","AstraSightNative",IsSightReady,true);
 vm->RegisterFunction("ValidateShot","AstraSightNative",ValidateShot,true);
 vm->BindNativeMethod(new CaptureFunction);
 vm->SetCallableFromTasklets("AstraSightNative","CaptureAim",true);
 vm->RegisterFunction("SetFrozen","AstraSightNative",SetFrozen,true);
 vm->RegisterFunction("EndSight","AstraSightNative",EndSight,true);
 vm->RegisterFunction("GetMountedAttacker","AstraSightNative",GetMountedAttacker,true);
 vm->RegisterFunction("GetLandingMarker","AstraSightNative",GetLandingMarker);
 vm->RegisterFunction("PlaceLandingDecoy","AstraSightNative",PlaceLandingDecoy);
 return true;
}
struct MenuEvents:RE::BSTEventSink<RE::MenuOpenCloseEvent>{RE::BSEventNotifyControl ProcessEvent(const RE::MenuOpenCloseEvent* e,RE::BSTEventSource<RE::MenuOpenCloseEvent>*)override{fastShots.menu(e);guards.menu(e);session.rebase();if(e&&session.ticket())spdlog::info("menu {} {}",e->menuName.c_str(),e->opening?"open":"close");return RE::BSEventNotifyControl::kContinue;}} menus;
void message(SKSE::MessagingInterface::Message* m){switch(m->type){case SKSE::MessagingInterface::kPreLoadGame:case SKSE::MessagingInterface::kPostLoadGame:case SKSE::MessagingInterface::kNewGame:if(session.ticket())spdlog::warn("sight dropped: load or new game");fastShots.invalidate();guards.invalidate();forgetLanding();break;case SKSE::MessagingInterface::kInputLoaded:RE::BSInputDeviceManager::GetSingleton()->AddEventSink(&fastShots);break;case SKSE::MessagingInterface::kDataLoaded:RE::UI::GetSingleton()->AddEventSink(&menus);guards.install();break;default:break;}}
void revert(SKSE::SerializationInterface*){if(session.ticket())spdlog::warn("sight dropped: save revert");fastShots.invalidate();guards.invalidate();forgetLanding();}
}

#if ASTRA_RUNTIME_AE17
// Skyrim AE 1.7.104 variant (alandtse CommonLibSSE-NG, GPL-3.0-or-later with exceptions). Address Library v13:
// the fork marks the plugin Address-Library-v5 compatible by default; 1.7.104 is the only accepted runtime.
constexpr REL::Version AstraRuntime{1,7,104,0};
extern "C" __declspec(dllexport) constinit SKSE::PluginVersionData SKSEPlugin_Version=[](){SKSE::PluginVersionData v;v.PluginName("AstraSight");v.PluginVersion({3,6,3,0});v.AuthorName("Dragonsreach Ballistae");v.UsesAddressLibrary();v.UsesUpdatedStructs();v.CompatibleVersions({AstraRuntime});v.MinimumRequiredXSEVersion({2,3,1,0});return v;}();
#elif ASTRA_RUNTIME_SE1597
// Skyrim SE 1.5.97 variant (SKSE 2.0.20, Address Library v1), same MIT CommonLibSSE-NG commit, SE layouts.
constexpr REL::Version AstraRuntime{1,5,97,0};
#else
constexpr REL::Version AstraRuntime{1,6,1170,0};
extern "C" __declspec(dllexport) constinit SKSE::PluginVersionData SKSEPlugin_Version=[](){SKSE::PluginVersionData v;v.PluginName("AstraSight");v.PluginVersion({3,6,3,0});v.AuthorName("Astra mounted sight");v.UsesAddressLibrary();v.UsesStructsPost629();v.CompatibleVersions({REL::Version{1,6,1170,0}});v.MinimumRequiredXSEVersion({2,2,6,0});return v;}();
#endif
extern "C" __declspec(dllexport) bool SKSEPlugin_Query(const SKSE::QueryInterface* skse,SKSE::PluginInfo* info){info->infoVersion=SKSE::PluginInfo::kVersion;info->name="AstraSight";info->version=0x03060030;return !skse->IsEditor()&&skse->RuntimeVersion()==AstraRuntime;}
extern "C" __declspec(dllexport) bool SKSEPlugin_Load(const SKSE::LoadInterface* skse){
 if(skse->IsEditor()||skse->RuntimeVersion()!=AstraRuntime)return false;
 SKSE::Init(skse);
 guards.playerLeaseProbe([](uint32_t handle){auto owner=session.ticket();return owner&&owner.key.handle==handle||!fastShots.quiescent({handle,0});});
 auto log=SKSE::log::log_directory();if(log){*log/="AstraSight.log";auto logger=std::make_shared<spdlog::logger>("AstraSight",std::make_shared<spdlog::sinks::basic_file_sink_mt>(log->string(),true));spdlog::set_default_logger(logger);spdlog::flush_on(spdlog::level::info);}
 spdlog::info("AstraSight 3.6.3 API 4 runtime 1.6.1170, native input/launch, release 66.7ms, cycle 1s, per-session sectors; v29.2 guards: hold clip grips, pose written on change, split idle re-request, supported pose before shot, active-world reset, unexpected-clip log, elevation + ballistic aim, hunted player as target, shot-refusal log, no telemetry gates; engine latency unmeasured");
 // v33.14: the banner above is pinned by the v29/v30 release contracts; this line names the build actually installed.
#if ASTRA_RUNTIME_AE17
 spdlog::info("AstraSight variant: Skyrim 1.7.104 / SKSE 2.3.1 (experimental, built with GPL-3.0 CommonLibSSE-NG)");
#elif ASTRA_RUNTIME_SE1597
 spdlog::info("AstraSight variant: Skyrim SE 1.5.97 / SKSE 2.0.20 (experimental)");
#endif
 spdlog::info("AstraSight build v33.14: N posts (towers, gate, 3 bandit camps), mounted dragon fight (attacker retention, landing marker, ground decoy), vanilla enemy health bar while mounted");
 if(!SKSE::GetPapyrusInterface()->Register(registerPapyrus))return false;
 if(!SKSE::GetMessagingInterface()->RegisterListener(message))return false;
 SKSE::GetSerializationInterface()->SetUniqueID(0x41535452);SKSE::GetSerializationInterface()->SetRevertCallback(revert);
 REL::Relocation<std::uintptr_t> vtable(RE::VTABLE_FirstPersonState[0]);
 originalEnd=vtable.write_vfunc(2,cameraEnd);originalUpdate=vtable.write_vfunc(3,update);originalRotation=vtable.write_vfunc(4,rotation);originalTranslation=vtable.write_vfunc(5,translation);
 REL::Relocation<std::uintptr_t> cameraVtable(RE::VTABLE_PlayerCamera[0]);originalCameraUpdate=cameraVtable.write_vfunc(2,cameraUpdate);
 Astra::installEnemyHealthBar();
 available=true;return true;
}
