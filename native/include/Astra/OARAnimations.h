#pragma once
// ABI transcribed from the public OAR Animations API V1. API structures only;
// no OAR implementation or assets are redistributed.
// https://github.com/ersh1/OpenAnimationReplacer/blob/main/src/API/OpenAnimationReplacerAPI-Animations.h
namespace OAR_API::Animations {
enum class InterfaceVersion: uint8_t { V1,Latest=V1 };
struct ReplacementAnimationInfo {RE::BSString animationPath{},projectName{},variantFilename{},subModName{},modName{};};
class IAnimationsInterface1 {
 public:
 virtual ReplacementAnimationInfo GetCurrentReplacementAnimationInfo(RE::hkbClipGenerator*)noexcept=0;
 virtual void ClearConditionStateData(RE::hkbClipGenerator*)noexcept=0;
 virtual void ClearConditionStateData(RE::TESObjectREFR*)noexcept=0;
};
using Request=IAnimationsInterface1* (*)(InterfaceVersion,const char*,REL::Version);
}
