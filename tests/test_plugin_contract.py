"""Contract checks on the bytes the game will consume; deliberately corrupt files too."""
import collections,importlib.util,json,struct,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
sys.path.insert(0,str(ROOT/'scripts/vendor'))
from parser_esm import Plugin

class PluginContract(unittest.TestCase):
 def setUp(self):
  self.assertTrue((ROOT/'mod/AstraAsedio.esp').exists(),'missing generated ESP')
  self.p=Plugin(ROOT/'mod/AstraAsedio.esp')
  self.records={}
  for t,o,n,d in self.p.recorrer():
   if t!='GRUP':self.records[self.p.form_id(o)]=(t,o,dict(self.p.subrecords(self.p.datos(o))))
 def test_three_masters_regular_esp_and_every_record_version_44(self):
  ss=self.p.subrecords(self.p.datos(0));masters=[v.rstrip(b'\0').decode() for k,v in ss if k=='MAST']
  self.assertEqual(masters,['Skyrim.esm','Update.esm','Dawnguard.esm'])
  self.assertEqual(struct.unpack_from('<I',self.p.d,8)[0],0)
  for t,o,s in self.records.values():self.assertEqual(struct.unpack_from('<H',self.p.d,o+20)[0],44)
 def test_seq_resolves_start_enabled_quest_in_final_plugin(self):
  seq=(ROOT/'mod/seq/AstraAsedio.seq').read_bytes()
  self.assertTrue(seq and len(seq)%4==0)
  quests=[fid for fid,(t,o,s) in self.records.items() if t=='QUST' and struct.unpack_from('<H',s['DNAM'])[0]&1]
  self.assertEqual(list(struct.unpack('<'+'I'*(len(seq)//4),seq)),quests)
 def test_validator_rejects_none_session_property(self):
  from build_plugin import validate_plugin
  b=bytearray(self.p.d);o=self.records[0x03000801][1];vmad=self.records[0x03000801][2]['VMAD']
  pos=b.find(vmad,o+24)+vmad.index(b'Session')+len('Session')+2+4
  struct.pack_into('<I',b,pos,0)
  with tempfile.TemporaryDirectory() as td:
   q=Path(td)/'missing_session.esp';q.write_bytes(b)
   with self.assertRaisesRegex(ValueError,'Session'):validate_plugin(q)
 def test_test_cell_has_neutral_imagespace_and_no_visible_distance_fog(self):
  cell=self.records[0x03000807][2];light=cell['XCLL']
  self.assertEqual(cell['XCIM'],struct.pack('<I',0x167))
  self.assertEqual(len(light),92)
  self.assertEqual(light[0],light[1]);self.assertEqual(light[1],light[2])
  self.assertGreaterEqual(light[0],100)
  self.assertEqual(struct.unpack_from('<f',light,76)[0],0.)
  self.assertGreater(struct.unpack_from('<f',light,12)[0],10000.)
 def test_four_native_lights_cover_tower_and_targets_without_shadows(self):
  lights={fid:ss for fid,(t,o,ss) in self.records.items() if t=='LIGH'}
  refs=[s for t,o,s in self.records.values() if t=='REFR' and struct.unpack('<I',s['NAME'])[0] in lights]
  self.assertEqual(len(refs),4)
  positions=[struct.unpack('<6f',r['DATA'])[:3] for r in refs]
  self.assertEqual(sum(p[1]<-800 for p in positions),2)
  for s in lights.values():
   data=s['DATA'];self.assertEqual(len(data),48)
   self.assertEqual(data[8],data[9]);self.assertEqual(data[9],data[10])
   self.assertEqual(struct.unpack_from('<I',data,12)[0],0,'light must not cast shadows, flicker, pulse or be carried')
 def test_target_front_normals_face_the_ballesta(self):
  import math
  # Face identified from the vanilla DDS render; NiMatrix3 Skyrim heading is CW.
  front=(-0.94,0.,0.34)
  # Each named tripod is followed by its paired vanilla target in stable v01 IDs.
  refs=[self.records[fid+1][2] for fid,(t,o,s) in self.records.items() if t=='REFR' and s.get('EDID',b'').startswith(b'AstraAsedioTarget')]
  self.assertEqual(len(refs),2)
  for s in refs:
   angle=struct.unpack('<6f',s['DATA'])[5]
   normal=(math.cos(angle)*front[0]+math.sin(angle)*front[1],-math.sin(angle)*front[0]+math.cos(angle)*front[1],front[2])
   self.assertGreater(normal[1],.9);self.assertLess(abs(normal[0]),.001)
 def test_v08_siege_ballistics_on_final_bytes(self):
  import build_plugin,nif_fisica,nif_nodos
  V=build_plugin.V08;donors=json.loads((ROOT/'build/Dawnguard.esm.donors.json').read_text())
  weap=[s for t,o,s in self.records.values() if t=='WEAP'][0]
  ammo=[s for t,o,s in self.records.values() if t=='AMMO'][0]
  proj=[s for t,o,s in self.records.values() if t=='PROJ'][0]
  # Weapon: donor DNAM except the stagger float; siege damage; no attack sound (Papyrus plays exactly one).
  dnam=bytearray(bytes.fromhex(dict(donors['DLC1TrapCrossbowWeapon01']['subs'])['DNAM']));struct.pack_into('<f',dnam,96,V['weapon_stagger'])
  self.assertEqual(weap['DNAM'],bytes(dnam))
  self.assertEqual(len(weap['DATA']),10);self.assertEqual(struct.unpack('<IfH',weap['DATA'])[2],V['weapon_damage'])
  self.assertEqual(weap['NNAM'],b'ProjectileNode\0');self.assertNotIn('SNAM',weap);self.assertNotIn('XNAM',weap)
  self.assertEqual(weap['FULL'],(V['names']['launcher']+'\0').encode('cp1252'))
  # Projectile: donor gravity/speed/range; only flags, explosion, impact force and radius change.
  self.assertEqual(self.records[struct.unpack_from('<I',ammo['DATA'])[0]][0],'PROJ')
  donor=bytes.fromhex(dict(donors['DLC1BoltSteelProjectile']['subs'])['DATA']);data=proj['DATA']
  changed={i for i in range(len(data)) if data[i]!=donor[i]}
  self.assertLessEqual(changed,set(range(0,2))|set(range(36,40))|set(range(52,56))|set(range(72,76)))
  self.assertEqual(struct.unpack_from('<3f',data,4),struct.unpack_from('<3f',donor,4))
  flags=struct.unpack_from('<H',data)[0];self.assertFalse(flags&0x40);self.assertTrue(flags&0x02);self.assertTrue(flags&0x80)
  self.assertEqual(struct.unpack_from('<f',data,52)[0],V['impact_force'])
  t,o,expl=self.records[struct.unpack_from('<I',data,36)[0]];self.assertEqual(t,'EXPL')
  self.assertEqual(struct.unpack_from('<3f',expl['DATA'],24),(V['explosion_force'],V['explosion_damage'],V['explosion_radius']))
  self.assertEqual(expl['MODT'],bytes.fromhex('020000000000000000000000'),'formVersion 39 MODT triples must not ship under 44')
  box=nif_fisica.cuerpos_caja(nif_nodos.leer(str(ROOT/'mod/meshes/AstraAsedio/virote.nif')))[0]
  self.assertAlmostEqual(struct.unpack_from('<f',data,72)[0],min(box['semiejes_hk'][0],box['semiejes_hk'][2])*nif_fisica.HK,places=3)
  self.assertEqual(proj['MODL'],b'AstraAsedio\\virote.nif\0')
  self.assertEqual(proj['FULL'],(V['names']['projectile']+'\0').encode('cp1252'))
  # Ammo: donor damage, never playable.
  self.assertEqual(struct.unpack_from('<f',ammo['DATA'],8)[0],10.)
  self.assertTrue(struct.unpack_from('<I',ammo['DATA'],4)[0]&0x02)
  self.assertEqual(ammo['FULL'],(V['names']['ammo']+'\0').encode('cp1252'))
 def test_every_projectile_and_ammo_is_siege_only(self):
  kinds=collections.Counter()
  for fid,(t,o,s) in self.records.items():
   if t=='PROJ':kinds[t]+=1;self.assertFalse(struct.unpack_from('<H',s['DATA'])[0]&0x40,hex(fid))
   if t=='AMMO':kinds[t]+=1;self.assertTrue(struct.unpack_from('<I',s['DATA'],4)[0]&0x02,hex(fid))
  self.assertEqual(kinds,{'PROJ':2,'AMMO':2})
 def test_shot_sound_is_bound_to_dawnguard_crossbow_fire(self):
  from build_plugin import read_vmad
  props=read_vmad(self.records[0x03000801][2]['VMAD'])['scripts'][0]['properties']
  sound=props['ShotSound']['value']['form_id'];self.assertEqual(self.records[sound][0],'SOUN')
  fire=json.loads((ROOT/'build/Dawnguard.esm.donors.json').read_text())['WPNCrossbowFire']
  self.assertEqual(fire['type'],'SNDR')
  self.assertEqual(self.records[sound][2]['SDSC'],struct.pack('<I',fire['fid']))
 def test_validator_rejects_pickable_projectile_playable_ammo_and_missing_sound(self):
  from build_plugin import validate_plugin
  def mutated(fid,sub,offset,fmt,value):
   b=bytearray(self.p.d);o=self.records[fid][1];data=self.records[fid][2][sub]
   struct.pack_into(fmt,b,b.find(data,o+24)+offset,value);return b
  vmad=self.records[0x03000801][2]['VMAD']
  cases=[(mutated(0x03000802,'DATA',0,'<H',0x00C2),'non-pickable'),
         (mutated(0x03000803,'DATA',4,'<I',0),'non-playable'),
         (mutated(0x03000801,'VMAD',vmad.index(b'ShotSound')+len('ShotSound')+2+4,'<I',0),'ShotSound'),
         # Review finding: the build validator alone accepted these.
         (mutated(0x03000802,'DATA',4,'<f',0.8),'ballistics'),
         (mutated(0x03000802,'DATA',8,'<f',2800.),'ballistics'),
         (mutated(0x03000802,'DATA',72,'<f',0.5),'radius'),
         (mutated(0x0300080C,'MODT',4,'<I',1),'MODT'),
         (mutated(0x03000804,'DNAM',4,'<f',2.0),'only damage and stagger')]
  with tempfile.TemporaryDirectory() as td:
   for i,(b,message) in enumerate(cases):
    q=Path(td)/f'bad{i}.esp';q.write_bytes(b)
    with self.assertRaisesRegex(ValueError,message):validate_plugin(q)
 def test_navmesh_capsule_clearance_against_final_collision_boxes(self):
  import build_plugin
  self.assertTrue(hasattr(build_plugin,'triangle_blocked'),'missing collision clipping check')
  data=json.loads((ROOT/'reports/collision_walkable.json').read_text())
  boxes=[dict(b,nav_step_units=16.) if b.get('name','').startswith(('Vigueta_', 'Viga_borde_')) else b for b in data['solid_boxes_units']]
  boxes += [dict(b,nav_step_units=16.) for b in data['floors_units']]
  for b in data.get('stair_edge_barriers_units',[]):
   ramp=next(r for r in data['ramps'] if abs(r['y'][0]-b['min'][1])<.01 and abs(r['y'][1]-b['max'][1])<.01)
   slope=(ramp['z'][1]-ramp['z'][0])/(ramp['y'][1]-ramp['y'][0])
   boxes=boxes+[dict(b,slope_y=slope,z_intercept=ramp['z'][0]-slope*ramp['y'][0],rail_height=b['max'][2]-ramp['z'][1])]
  z=json.loads((ROOT/'config.json').read_text())['tower_top_units']
  local=data['ballesta_fixed_box_units'];boxes=boxes+[{'min':[local['min'][0],local['min'][1],local['min'][2]+z],'max':[local['max'][0],local['max'][1],local['max'][2]+z]}]
  nv=self.records[0x03000809][2]['NVNM'];n=struct.unpack_from('<I',nv,16)[0]
  verts=[struct.unpack_from('<3f',nv,20+12*i) for i in range(n)];off=20+n*12;tcount=struct.unpack_from('<I',nv,off)[0];off+=4
  for i in range(tcount):
   ids=struct.unpack_from('<3H',nv,off+i*16);tri=[verts[j] for j in ids]
   for b in boxes:self.assertFalse(build_plugin.triangle_blocked(tri,b),f'triangle {i} collides with expanded wall/railing/pedestal')
 def test_triangle_box_clip_catches_crossing_without_inside_vertices(self):
  import build_plugin
  self.assertTrue(hasattr(build_plugin,'triangle_blocked'),'missing exact polygon clipping')
  b={'min':[-.5,-.5,-1.],'max':[.5,.5,1.]}
  self.assertTrue(build_plugin.triangle_blocked([(-2.,0.,0.),(2.,0.,0.),(0.,2.,0.)],b,0.,0.))
  self.assertFalse(build_plugin.triangle_blocked([(-2.,0.,2.),(2.,0.,2.),(0.,2.,2.)],b,0.,0.))
 def test_sloped_rail_does_not_block_higher_landing_but_blocks_ramp(self):
  import build_plugin
  b={'min':[20.,0.,0.],'max':[27.,100.,160.],'slope_y':1.,'z_intercept':0.,'rail_height':60.}
  self.assertFalse(build_plugin.triangle_blocked([(22.,0.,140.),(25.,0.,140.),(23.,4.,140.)],b))
  self.assertTrue(build_plugin.triangle_blocked([(22.,50.,50.),(25.,50.,50.),(23.,54.,54.)],b))
 def test_plugin_bounds_come_from_final_nif_measurements(self):
  assets=json.loads((ROOT/'reports/assets.json').read_text())
  baseline=Plugin(ROOT.with_name('Ballesta_Astra_Vanilla_SE_v11')/'mod/AstraAsedio.esp')
  old={baseline.form_id(o):dict(baseline.subrecords(baseline.datos(o))) for t,o,n,d in baseline.recorrer() if t!='GRUP'}
  for fid,asset in [(0x03000800,'torre'),(0x03000801,'ballesta'),(0x03000802,'virote')]:
   import math
   if asset=='torre':
    bbox=assets[asset]['bbox_units'];expected=[math.floor(x) for x in bbox['min']]+[math.ceil(x) for x in bbox['max']]
   else:
    # v12 preserves the user's proven weapon/projectile records. Historical v11 OBND
    # differs from its latest amarra mesh measurement by one unit on the weapon X axis.
    expected=list(struct.unpack('<6h',old[fid]['OBND']))
   self.assertEqual(list(struct.unpack('<6h',self.records[fid][2]['OBND'])),expected)
 def test_new_cell_and_valid_navmesh(self):
  from build_plugin import validate_plugin
  result=validate_plugin(ROOT/'mod/AstraAsedio.esp')
  self.assertTrue(result['structural_valid']);self.assertGreater(result['navmesh_triangles'],10)
  self.assertFalse(result['ck_finalized_verified'])
 def test_interior_groups_follow_vanilla_decimal_block_convention(self):
  stack=[];interiores=0
  for t,o,n,d in self.p.recorrer():
   stack=stack[:d]
   if t=='GRUP':stack.append((struct.unpack_from('<i',self.p.d,o+8)[0],struct.unpack_from('<i',self.p.d,o+12)[0]));continue
   # la convencion decimal es de las celdas INTERIORES (GRUP CELL); la celda exterior del
   # mundo cuelga de WRLD>1>4>5 y la cubre tests/test_v11_mundo_esp.py
   if t=='CELL' and struct.pack('<i',stack[0][0])==b'CELL':
    local=self.p.form_id(o)&0xffffff
    self.assertEqual(stack[1],(local%10,2));self.assertEqual(stack[2],((local//10)%10,3));interiores+=1
  self.assertGreaterEqual(interiores,1,'el filtro dejo el control sin celdas que mirar')
 def test_navmesh_connects_ground_to_collision_rooftop(self):
  from build_plugin import validate_plugin
  result=validate_plugin(ROOT/'mod/AstraAsedio.esp')
  self.assertIn('navmesh_components',result);self.assertEqual(result['navmesh_components'],1)
  deck=json.loads((ROOT/'config.json').read_text())['tower_v11']['platform']['deck_top']
  self.assertAlmostEqual(result['navmesh_max_z'],deck+2,places=2)
 def test_validator_rejects_wrong_ammo_projectile_and_truncation(self):
  from build_plugin import validate_plugin
  b=bytearray(self.p.d); ammo=next((o,s) for t,o,s in self.records.values() if t=='AMMO')
  o,s=ammo;offset=b.find(s['DATA'],o+24);struct.pack_into('<I',b,offset,0x0300FFFF)
  with tempfile.TemporaryDirectory() as td:
   q=Path(td)/'bad.esp';q.write_bytes(b)
   with self.assertRaises(ValueError):validate_plugin(q)
   q.write_bytes(self.p.d[:-2])
   with self.assertRaises((ValueError,Exception)):validate_plugin(q)

if __name__=='__main__':unittest.main()


