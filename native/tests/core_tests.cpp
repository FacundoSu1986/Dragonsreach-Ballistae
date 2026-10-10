#include "Astra/Core.h"
#include <atomic>
#include <cmath>
#include <future>
#include <iostream>
#include <limits>
#include <thread>

using namespace Astra;
static int failures = 0;
static int checks = 0;
void check(bool b, const char* name) { ++checks; if (!b) { std::cerr << "FAIL: " << name << '\n'; ++failures; } }
bool near(double a, double b) { return std::abs(a-b) < 1e-6; }
int main() {
    try {
    check(near(wrapDegrees(-1),359) && near(wrapDegrees(721),1), "continuous 360 wrap");
    for (double yaw : {0.,47.,180.,359.}) for (double pitch : {-20.,-5.,0.,45.,80.}) {
        auto root = rz(rad(33))*rx(rad(19));
        auto d = root * gunDirection(yaw,pitch);
        auto a = aimFromWorld(root,d);
        check(near(a.yaw,yaw) && near(a.pitch,pitch),"world/root transpose roundtrip");
        auto logical = logicalBasis(d);
        check(length(logical*Vec{0,1,0}-d)<1e-6,"camera +Y optical logical forward");
        auto original = root*rx(rad(11))*rz(rad(22));
        auto adapter = logical.transpose()*original;
        check(matrixNear(logical*adapter,original),"calibrated camera adapter preserves original basis");
        Transform parent{root,{130,-85,66},2.5};
        Transform world{logical,{210,30,181},1};
        auto local = toLocal(parent,world);
        check(length(parent.rotation*(local.translation*parent.scale)+parent.translation-world.translation)<1e-6,"scaled parent camera translation");
        check(matrixNear(parent.rotation*local.rotation,world.rotation),"parent camera rotation");
    }
    // v13: both BeginSight and incremental input admit depression down to -20.
    for (double initial : {-90.,-20.,-10.,0.,80.,90.}) {
        Session limits; Key key{90,1};
        check(limits.begin(key,15,initial),"finite initial pitch accepted");
        limits.update(limits.ticket(),{15,initial},false,[](Aim a){return Snapshot{a,{},true};});
        double expected=initial<-20?-20:initial>80?80:initial;
        check(near(limits.capture(key,false)->pitch,expected),"begin clamps to -20..80 and retains allowed depression");
    }
    Session session;
    check(!session.begin({1,1},0,std::numeric_limits<double>::quiet_NaN()),"reject nonfinite begin");
    check(session.begin({100,7},359,80),"first begin accepted");
    if (!session.ticket()) return 1;
    check(!session.begin({101,8},0,0),"second begin rejected");
    auto ticket = session.ticket();
    int writes=0;
    session.update(ticket,{359,80},false,[&](Aim aim){ ++writes; return Snapshot{aim,{},true}; });
    check(session.ready({100,7}),"ready only after committed scene snapshot");
    session.update(ticket,{359,89},false,[&](Aim aim){ ++writes; return Snapshot{aim,{},true}; });
    session.update(ticket,{359,88},false,[&](Aim aim){ ++writes; return Snapshot{aim,{},true}; });
    check(near(session.capture({100,7},false)->yaw,359) && near(session.capture({100,7},false)->pitch,79),"immediate reverse after upper overshoot");
    check(!session.capture({100,6},true),"old token cannot freeze");
    auto frozen=session.capture({100,7},true);
    session.update(ticket,{100,10},false,[&](Aim aim){ ++writes; return Snapshot{aim,{},true}; });
    check(near(session.capture({100,7},false)->pitch,79),"freeze discards motion");
    session.freeze({100,7},false);
    session.update(ticket,{99,9},false,[&](Aim aim){ ++writes; return Snapshot{aim,{},true}; });
    check(near(session.capture({100,7},false)->pitch,79),"unfreeze first sample rebases");
    session.update(ticket,{98,8},false,[&](Aim aim){ ++writes; return Snapshot{aim,{},true}; });
    check(near(session.capture({100,7},false)->pitch,78),"freeze rebased samples prevent resume jump");
    session.update(ticket,{200,20},true,[&](Aim aim){ ++writes; return Snapshot{aim,{},true}; });
    session.update(ticket,{201,21},false,[&](Aim aim){ ++writes; return Snapshot{aim,{},true}; });
    check(near(session.capture({100,7},false)->pitch,79),"menu pause rebases hidden motion");
    check(!session.end({100,6}),"old end harmless");
    check(session.end({100,7}),"matching end accepted");
    int previous=writes;
    session.update(ticket,{0,0},false,[&](Aim aim){ ++writes; return Snapshot{aim,{},true}; });
    check(writes==previous && !session.ready({100,7}),"stale frame cannot write after End");
    session.begin({100,8},20,5);
    session.update(ticket,{1,1},false,[&](Aim aim){ ++writes; return Snapshot{aim,{},true}; });
    check(writes==previous,"old epoch cannot affect next lease");
    ticket=session.ticket();
    std::promise<void> applying, release;
    auto releaseFuture=release.get_future();
    auto worker=std::async(std::launch::async,[&]{ session.update(ticket,{20,5},false,[&](Aim aim){applying.set_value();releaseFuture.wait();++writes;return Snapshot{aim,{},true};}); });
    applying.get_future().wait();
    auto ender=std::async(std::launch::async,[&]{ return session.end({100,8}); });
    check(ender.wait_for(std::chrono::milliseconds(30))==std::future_status::timeout,"End waits for in-flight apply transaction");
    release.set_value(); worker.get(); check(ender.get(),"End completes after apply");
    previous=writes;
    session.update(ticket,{21,6},false,[&](Aim aim){++writes;return Snapshot{aim,{},true};});
    check(writes==previous,"no native write after End returns");
    session.begin({100,9},0,0); ticket=session.ticket();
    session.invalidate();
    session.update(ticket,{0,0},false,[&](Aim aim){++writes;return Snapshot{aim,{},true};});
    check(writes==previous && !session.ready({100,9}),"load/revert invalidates epoch");
    Session freezeSession;
    freezeSession.begin({200,1},359,-20);auto freezeTicket=freezeSession.ticket();
    freezeSession.update(freezeTicket,{359,-20},false,[](Aim a){return Snapshot{a,{},true};});
    freezeSession.update(freezeTicket,{1,-35},false,[](Aim a){return Snapshot{a,{},true};});
    check(near(freezeSession.capture({200,1},false)->pitch,-20),"incremental lower overshoot clamps at -20");
    freezeSession.update(freezeTicket,{2,-34},false,[](Aim a){return Snapshot{a,{},true};});
    check(near(freezeSession.capture({200,1},false)->yaw,2)&&near(freezeSession.capture({200,1},false)->pitch,-19),"wrap and immediate lower-limit reverse at -20");
    // A frame's player-look sample may have been prepared before VM freeze.
    Aim prepared={100,50};auto committed=freezeSession.capture({200,1},true);
    freezeSession.update(freezeTicket,prepared,false,[](Aim a){return Snapshot{a,{},true};});
    check(near(freezeSession.capture({200,1},false)->yaw,committed->yaw)&&near(freezeSession.capture({200,1},false)->pitch,committed->pitch),"prepared frame cannot overwrite frozen aim");
    freezeSession.rebase();freezeSession.freeze({200,1},false);
    freezeSession.update(freezeTicket,{220,70},false,[](Aim a){return Snapshot{a,{},true};});
    check(near(freezeSession.capture({200,1},false)->yaw,committed->yaw),"menu close/unfreeze discards unsampled motion");
    std::promise<void> freezeApplying,freezeRelease;auto freezeReleaseFuture=freezeRelease.get_future();
    auto updater=std::async(std::launch::async,[&]{freezeSession.update(freezeTicket,{221,71},false,[&](Aim a){freezeApplying.set_value();freezeReleaseFuture.wait();return Snapshot{a,{},true};});});
    freezeApplying.get_future().wait();
    auto capturer=std::async(std::launch::async,[&]{return freezeSession.capture({200,1},true);});
    check(capturer.wait_for(std::chrono::milliseconds(30))==std::future_status::timeout,"CaptureAim freeze waits for in-flight world apply");
    freezeRelease.set_value();updater.get();auto captured=capturer.get();
    freezeSession.update(freezeTicket,{30,-1},false,[](Aim a){return Snapshot{a,{},true};});
    check(near(freezeSession.capture({200,1},false)->yaw,captured->yaw),"frozen result is same published applied transaction");
    freezeSession.freeze({200,1},false);
    freezeSession.update(freezeTicket,{30,-1},false,[](Aim){return Snapshot{};});
    check(!freezeSession.ready({200,1})&&!freezeSession.snapshot(),"missing geometry/camera invalidates readiness and override");
    freezeSession.begin({200,2},0,0);freezeTicket=freezeSession.ticket();
    freezeSession.update(freezeTicket,{NAN,0},false,[](Aim a){return Snapshot{a,{},true};});
    check(!freezeSession.snapshot(),"nonfinite player look invalidates override");
    Session reconciled;
    reconciled.begin({300,1},15,80);auto reconciledTicket=reconciled.ticket();
    reconciled.update(reconciledTicket,{15,80},false,[](Aim a){return Snapshot{a,{},true};},true);
    reconciled.update(reconciledTicket,{15,85},false,[](Aim a){return Snapshot{a,{},true};},true);
    // Engine player look was restored to the applied 80 after overshoot.
    reconciled.update(reconciledTicket,{15,79},false,[](Aim a){return Snapshot{a,{},true};},true);
    check(near(reconciled.capture({300,1},false)->pitch,79),"reconciled look rebases over-limit sample before reverse");
    Session lowerReconciled; Key lowerKey{301,1};
    lowerReconciled.begin(lowerKey,15,-20);auto lowerTicket=lowerReconciled.ticket();
    lowerReconciled.update(lowerTicket,{15,-20},false,[](Aim a){return Snapshot{a,{},true};},true);
    lowerReconciled.update(lowerTicket,{15,-25},false,[](Aim a){return Snapshot{a,{},true};},true);
    lowerReconciled.update(lowerTicket,{15,-19},false,[](Aim a){return Snapshot{a,{},true};},true);
    check(near(lowerReconciled.capture(lowerKey,false)->pitch,-19),"reconciled look reverses immediately after -20 overshoot");
    Session validationRace;
    validationRace.begin({400,1},2,3);auto ticketA=validationRace.ticket();
    validationRace.update(ticketA,{2,3},false,[](Aim a){return Snapshot{a,{},true};});
    validationRace.end({400,1});validationRace.begin({400,2},40,30);auto ticketB=validationRace.ticket();
    Transform cameraB{rz(rad(10)),{7,8,9},1};
    validationRace.update(ticketB,{40,30},false,[&](Aim a){return Snapshot{a,cameraB,true};});
    check(!validationRace.invalidate(ticketA),"stale A validation cannot invalidate B");
    auto preservedB=validationRace.snapshot();
    check(validationRace.ready({400,2})&&validationRace.ticket().epoch==ticketB.epoch,"B readiness and epoch survive stale A failure");
    check(preservedB&&near(preservedB->aim.yaw,40)&&near(preservedB->aim.pitch,30)&&length(preservedB->camera.translation-cameraB.translation)<1e-6,"B applied snapshot survives stale A failure");
    Session matchingFailure;
    matchingFailure.begin({500,1},0,0);auto matchingTicket=matchingFailure.ticket();
    matchingFailure.update(matchingTicket,{0,0},false,[](Aim a){return Snapshot{a,{},true};});
    Ticket wrongKey=matchingTicket;wrongKey.key.token=2;
    check(!matchingFailure.invalidate(wrongKey)&&matchingFailure.ready({500,1}),"same epoch wrong key cannot invalidate lease");
    check(matchingFailure.invalidate(matchingTicket)&&!matchingFailure.ready({500,1})&&!matchingFailure.snapshot(),"matching frame failure invalidates its lease");
    Session repeatedKey;
    repeatedKey.begin({600,1},0,0);auto priorEpoch=repeatedKey.ticket();
    repeatedKey.end({600,1});repeatedKey.begin({600,1},0,0);auto newEpoch=repeatedKey.ticket();
    repeatedKey.update(newEpoch,{0,0},false,[](Aim a){return Snapshot{a,{},true};});
    check(!repeatedKey.invalidate(priorEpoch)&&repeatedKey.ready({600,1}),"same key stale epoch cannot invalidate renewed lease");
    std::cout << (failures?"FAILED ":"PASS ") << checks << " assertions, " << failures << " failures\n";
    return failures?1:0;
    } catch(const std::exception& e) { std::cerr<<"TEST EXCEPTION: "<<e.what()<<'\n';return 2; }
}
