"""단단 증기압축 사이클 계산 (CoolProp).
사용: python3 vcc.py R1234yf --te 7.2 --tc 50 --sh 5 --sc 5 --eta-is 0.7 --eta-motor 0.92 --q 2.3
--q: 냉방능력 kW (주면 질량유량·소비전력 계산)
"""
import argparse
import CoolProp.CoolProp as CP

def cycle(fluid, te, tc, sh=5.0, sc=5.0, eta_is=0.7, eta_motor=1.0, q_kw=None):
    K = 273.15
    pe = CP.PropsSI('P', 'T', te + K, 'Q', 1, fluid)
    pc = CP.PropsSI('P', 'T', tc + K, 'Q', 0, fluid)
    t1 = te + sh + K
    h1 = CP.PropsSI('H', 'T', t1, 'P', pe, fluid)
    s1 = CP.PropsSI('S', 'T', t1, 'P', pe, fluid)
    d1 = CP.PropsSI('D', 'T', t1, 'P', pe, fluid)
    h2s = CP.PropsSI('H', 'P', pc, 'S', s1, fluid)
    h2 = h1 + (h2s - h1) / eta_is
    t2 = CP.PropsSI('T', 'P', pc, 'H', h2, fluid) - K
    h3 = CP.PropsSI('H', 'T', tc - sc + K, 'P', pc, fluid)
    qe, w = h1 - h3, h2 - h1
    r = {
        'fluid': fluid, 'Pe_bar': pe / 1e5, 'Pc_bar': pc / 1e5, 'PR': pc / pe,
        'T_discharge_C': t2, 'q_evap_kJkg': qe / 1e3, 'w_comp_kJkg': w / 1e3,
        'w_isen_kJkg': (h2s - h1) / 1e3, 'suction_density_kgm3': d1,
        'COP_cool_shaft': qe / w, 'COP_cool_elec': qe / w * eta_motor,
        'COP_heat_elec': (qe + w) / w * eta_motor,
        'COP_carnot_cool': (te + K) / (tc - te),
    }
    if q_kw:
        m = q_kw * 1e3 / qe
        r.update({'mdot_kgs': m, 'V_suction_Ls': m / d1 * 1e3,
                  'P_elec_kW': m * w / eta_motor / 1e3})
    return r

if __name__ == '__main__':
    a = argparse.ArgumentParser()
    a.add_argument('fluid'); a.add_argument('--te', type=float, required=True)
    a.add_argument('--tc', type=float, required=True)
    a.add_argument('--sh', type=float, default=5); a.add_argument('--sc', type=float, default=5)
    a.add_argument('--eta-is', type=float, default=0.7)
    a.add_argument('--eta-motor', type=float, default=1.0)
    a.add_argument('--q', type=float)
    p = a.parse_args()
    for k, v in cycle(p.fluid, p.te, p.tc, p.sh, p.sc, p.eta_is, p.eta_motor, p.q).items():
        print(f'{k:24s} {v:.4g}' if isinstance(v, float) else f'{k:24s} {v}')
