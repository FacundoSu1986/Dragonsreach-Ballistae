import unittest,json,hashlib,struct,sys,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/vendor')]
from parser_esm import Plugin
import patch_plugin_v12 as P
from build_modular_v13 import subs
from nav_clearance_v21 import check

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

class NavigationProxy(unittest.TestCase):
    nav=np.array([[[-50.,-50.,0.],[50.,-50.,0.],[0.,50.,0.]]])
    def triangle(self,z):return np.array([[[-5.,-5.,z],[5.,-5.,z],[0.,5.,z]]])
    def test_inside_prism_detected_without_boundary_crossing(self):
        self.assertTrue(check(self.triangle(30),self.nav))
    def test_above_headroom_is_clear(self):
        self.assertFalse(check(self.triangle(180),self.nav))
    def test_below_ground_is_clear(self):
        self.assertFalse(check(self.triangle(-10),self.nav))
    def test_vertical_face_horizontal_radius(self):
        tri=np.array([[[52.,-50.,10.],[52.,-50.,70.],[52.,-49.,50.]]])
        self.assertTrue(check(tri,self.nav,radius=24))
        self.assertFalse(check(tri,self.nav,radius=1))
    def test_continuous_crossing_between_vertices(self):
        tri=np.array([[[-5.,-5.,-10.],[5.,-5.,180.],[0.,5.,180.]]])
        self.assertTrue(check(tri,self.nav))

class ReleaseContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records=P.record_map(Plugin(str(ROOT/'addons/Atalaya/AstraAsedio_Atalaya.esp')))
    def test_core_and_city_payload_preserved(self):
        parent=ROOT.with_name('Ballesta_Astra_Vanilla_SE_v20')
        # Mounting sheathes the player and drops the dragon. Recompiling stamps
        # every PEX. The quiescence guard also changes Guard, PlayerAlias,
        # Session and Station sources.
        exempt={Path('scripts')/name for name in (
            'AstraAsedioActi.pex','AstraAsedioGuard.pex','AstraAsedioPlayerAlias.pex',
            'AstraAsedioSession.pex','AstraAsedioStation.pex','AstraSightNative.pex',
            'source/AstraAsedioActi.psc','source/AstraAsedioGuard.psc',
            'source/AstraAsedioPlayerAlias.psc','source/AstraAsedioSession.psc',
            'source/AstraAsedioStation.psc')}
        for folder in ['mod','addons/WhiterunTorres']:
            a={p.relative_to(ROOT/folder):sha(p) for p in (ROOT/folder).rglob('*') if p.is_file()}
            b={p.relative_to(parent/folder):sha(p) for p in (parent/folder).rglob('*') if p.is_file()}
            if folder!='mod':
                self.assertEqual(a,b,folder); continue
            self.assertEqual(set(a), set(b))
            changed={rel for rel in a if a[rel]!=b[rel]}
            self.assertEqual(changed, exempt)
    def test_stable_owned_identities(self):
        before=P.record_map(Plugin(str(ROOT.with_name('Ballesta_Astra_Vanilla_SE_v20')/'addons/Atalaya/AstraAsedio_Atalaya.esp')))
        self.assertEqual({k for k in before if k>>24==4},{k for k in self.records if k>>24==4})
    def test_no_scene_or_navigation_edits(self):
        self.assertFalse(any(r[:4] in (b'NAVM',b'QUST',b'PACK',b'ACHR') for r in self.records.values()))
        self.assertEqual({k for k in self.records if k>>24<4},{0x3c,0x963d,0xa63d,0xe4396,0xe4397})
        self.assertEqual(self.records[0xa63d][:4], b'LAND')
        for fid in (0xe4396, 0xe4397):
            self.assertTrue(struct.unpack_from('<I', self.records[fid], 8)[0] & 0x800)
    def test_site_and_cell_match(self):
        p=Plugin(str(ROOT/'addons/Atalaya/AstraAsedio_Atalaya.esp'));stack=[];count=0
        for typ,o,n,d in p.recorrer():
            if typ=='GRUP':stack[d:]=[struct.unpack_from('<Ii',p.d,o+8)];continue
            if typ!='REFR':continue
            f=dict(p.subrecords(p.datos(o)));x,y,z,*rot=struct.unpack('<6f',f['DATA'])
            self.assertTrue(4096<=x<8192 and -16384<=y<-12288)
            self.assertEqual(next(v for v,t in reversed(stack[:d]) if t==6),0x963d);count+=1
        self.assertEqual(count,17)
        x,y,z,*r=struct.unpack('<6f',subs(self.records[0x04000A01])['DATA'])
        self.assertAlmostEqual(x,4665.54,places=2);self.assertAlmostEqual(y,-14922.81,places=2);self.assertAlmostEqual(z,-5217.81,places=2)
        self.assertAlmostEqual(math.degrees(r[-1])%360,187.63,places=2)
        gx,gy,gz,*gr=struct.unpack('<6f',subs(self.records[0x04000A00])['DATA'])
        self.assertAlmostEqual(gx,x,places=2);self.assertAlmostEqual(gy,y,places=2)
        self.assertAlmostEqual(gz-z,151.55,places=2)
        self.assertAlmostEqual(math.degrees(gr[-1])%360,187.63,places=2)
        self.assertEqual(subs(self.records[0x04000A50])['MODL'].rstrip(b'\0'), b'AstraAsedio\\torre_atalaya_v20.nif')
    def test_whiterun_stations_and_floors_enabled(self):
        r=P.record_map(Plugin(str(ROOT/'addons/WhiterunTorres/AstraAsedio_WhiterunTorres.esp')))
        for fid in (0x04000B70,0x04000B80,0x04000B74,0x04000B84):
            self.assertEqual(r[fid][:4],b'REFR');self.assertFalse(struct.unpack_from('<I',r[fid],8)[0]&(0x20|0x800))
        for n in ('voladizo_este.nif','voladizo_oeste.nif'):
            self.assertTrue((ROOT/'addons/WhiterunTorres/meshes/AstraAsedio'/n).is_file())
    def test_fitted_mesh_matches_recorded_verification(self):
        report=json.loads((ROOT/'reports/atalaya_verified_v20.json').read_text())
        self.assertTrue(report['success'])
        self.assertEqual(report['static_aim_poses'],1512);self.assertEqual(report['walk_samples'],244)
        nif=ROOT/'addons/Atalaya/meshes/AstraAsedio/torre_atalaya_v20.nif'
        self.assertEqual(sha(nif), report['inputs_sha256']['addons/Atalaya/meshes/AstraAsedio/torre_atalaya_v20.nif'])
        for n,h in report['inputs_sha256'].items():
            if n=='config.json':continue
            self.assertEqual(sha(ROOT/n),h,n)
    def test_stair_entrance_is_a_step_and_rubble_stays_disabled(self):
        import clear_stair_entrance_v21 as C
        import nivelar_terreno as T
        esp=ROOT/'addons/Atalaya/AstraAsedio_Atalaya.esp'
        before=esp.read_bytes()
        C.apply(esp)
        self.assertEqual(esp.read_bytes(), before)
        parent=P.record_map(Plugin(str(ROOT.with_name('Ballesta_Astra_Vanilla_SE_v20')/'addons/Atalaya/AstraAsedio_Atalaya.esp')))
        for fid, raw in parent.items():
            self.assertEqual(self.records[fid], raw)
        _header, body = C.find_record(esp, C.LAND_ID, 'LAND')
        _off, grid = T.decodificar_vhgt(dict(Plugin.subrecords(body))['VHGT'])
        lips=C.foot_clearance(grid)
        self.assertTrue(all(4 <= lip <= 20 for lip in lips), lips)
        _uheader, ubody = C.find_record(C.runtime()/'Update.esm', C.LAND_ID, 'LAND')
        _uoff, vanilla = T.decodificar_vhgt(dict(Plugin.subrecords(ubody))['VHGT'])
        for row in range(33):
            for col in range(33):
                if (row, col) not in C.HEIGHTS:
                    self.assertEqual(grid[row][col], vanilla[row][col])
                else:
                    self.assertGreaterEqual(grid[row][col], vanilla[row][col])
    def test_regression_exposes_old_navigation_obstruction(self):
        j=json.loads((ROOT/'reports/nav_regression_v20.json').read_text());self.assertGreater(j['obstructions'],0)

if __name__=='__main__':unittest.main()
