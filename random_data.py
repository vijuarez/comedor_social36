import numpy as np 
from random import randint
import json

def ask_normal(nombre):
    a = input(f'Cual es el promedio de {nombre}? ')
    b = input(f'Cual es la desviación estandard de {nombre}? ')
    return float(a), float(b)

auto = input('Deseas el modo automatico (yes) o dar las distribuciones de los datos manualmente (no)? ')

if auto == 'no':
    dias = int(input('Cuantos días serán optimizados? '))

    alimentos = int(input('Número de alimentos distintos a considerar? '))

    sueldo = int(input('Cual es el sueldo mensual del trabajador? '))

    entrada = int(input('Cual es el precio de admisión? '))

    volmax = int(input('Volumen máximo de la bodega? '))

    amin = int(input('El mínimo de alimentos que los cocineros puedan querer poner un día? '))
    amax = int(input('El máximo de alimentos que los cocineros puedan querer poner un día? '))

    vis_promedio, vis_desviacion = ask_normal('visitantes')
    cos_promedio, cos_desviacion = ask_normal('el costo de los alimentos')
    don_promedio, don_desviacion = ask_normal('las donaciones monetarias diarias')
    dal_promedio, dal_desviacion = ask_normal('las donaciones de un alimento diario')
    da_promedio, da_desviacion = ask_normal('la duracion de un alimento')
    vol_promedio, vol_desviacion = ask_normal('el volumen de los alimentos')
else:
    dias = 31

    alimentos = 50

    sueldo = 250000

    entrada = 200

    volmax = 500

    amin = 4
    amax = 7

    vis_promedio, vis_desviacion = 150, 25
    cos_promedio, cos_desviacion = 1000, 800
    don_promedio, don_desviacion = 15000, 6000
    dal_promedio, dal_desviacion = 8, 5
    da_promedio, da_desviacion = 15, 15
    vol_promedio, vol_desviacion = 1, 0

data = {}

data['dias'] = dias
data['alimentos'] = alimentos
data['sueldo_fijo'] = sueldo
data['vol_max'] = volmax
data['amax'] = [randint(amin, amax) for x in range(dias)]
data['donaciones_monetarias'] = [max(0, int(x)) for x in np.random.normal(don_promedio, don_desviacion, dias)]
data['visitas'] = [max(0, int(x)) for x in np.random.normal(vis_promedio, vis_desviacion, dias)]
data['cantidad_alimento'] = [[max(0, int(x)) for x in np.random.normal(dal_promedio, dal_desviacion, dias)] for a in range(alimentos)]
data['entrada'] = entrada
data['volumen_alimentos'] = [max(1, int(x)) for x in np.random.normal(vol_promedio, vol_desviacion, alimentos)]
data['duracion_alimentos'] = [max(10, int(x)) for x in np.random.normal(da_promedio, da_desviacion, alimentos)]
data['costo_alimento'] = [max(100, int(x)) for x in np.random.normal(cos_promedio, cos_desviacion, alimentos)]
data['verdura'] = [0] * alimentos
data['fruta'] = [0] * alimentos
data['proteina'] = [0] * alimentos
data['carbohidrato'] = [0] * alimentos

for i in range(alimentos):
    verdura = max(0, randint(-2, 1))
    fruta = 0 if verdura else randint(-1, 1)
    proteina = 0 if fruta else randint(0, 1)
    carbohidrato = 0 if proteina else 1
    data['verdura'][i] = verdura
    data['fruta'][i] = fruta
    data['proteina'][i] = proteina
    data['carbohidrato'][i] = carbohidrato

with open('data.json', 'w') as f:
    json.dump(data, f)
