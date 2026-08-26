import dustmaps.csfd
dustmaps.csfd.fetch() # 首次使用先下载csfd模型到本地，conda环境burst_advocate下已安装

# 获取ebv
from astropy import units as u
from astropy.coordinates import SkyCoord
from dustmaps.csfd import CSFDQuery
coords = SkyCoord('191.2582', '23.8536', unit=(u.deg,u.deg), frame='icrs') # 输入要查询的坐标
csfd = CSFDQuery()
ebv = csfd(coords)
# print('CSFD(2023) E(B-V) = {:.3f} mag'.format(ebv))

# 计算得到Av
Rv = 3.1 # 银河系参数固定为3.1
Av = Rv * ebv
# print('Av = {:.3f}'.format(Av))

# 使用P92模型得到各个光学波段的消光值
import numpy as np
import json
import astropy.units as u
from dust_extinction.shapes import P92
wl_list   = []   # 波长
v2a_list  = []   # Vega2AB
Ax_list   = []   # 消光值
with open('./filters.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
for band, params in data.items():
    wl = params['wavelength']      # wavelength
    v2a  = params['Vega2AB']       # Vega2AB
    desc = params['description']   # description
    ext_model = P92()
    Ax = Av * ext_model(wl* u.Angstrom)
    wl_list.append(wl)
    v2a_list.append(v2a)
    Ax_list.append(Ax)
    print(f"{band:>15}, {Ax:>1.3f}")
# 注意：此时输出的Ax是各个光学波段的银河系消光的星等值，直接用观测原始星等减去对应波段Ax就得到银河系消光改正后的星等值

