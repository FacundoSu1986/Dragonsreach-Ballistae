"""Preserve source animation curves, scale their time axis in the v07 copy."""
import bpy,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];cfg=json.loads((ROOT/'config.json').read_text())
parent=ROOT.with_name('Ballesta_Astra_Vanilla_SE_v06')/'source/Astra_export.blend'
bpy.ops.wm.open_mainfile(filepath=str(parent))
for name,old,new in [('Fire',.6,cfg['fire_seconds']),('Reset',4.4,cfg['reset_seconds'])]:
    action=bpy.data.actions[name];factor=new/old
    for layer in action.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                for curve in bag.fcurves:
                    for key in curve.keyframe_points:
                        for point in (key.co,key.handle_left,key.handle_right):point.x=1+(point.x-1)*factor
    action.frame_end=1+30*new
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'source/Astra_export.blend'))
print('v07 editable actions retimed; v06 file unchanged')
