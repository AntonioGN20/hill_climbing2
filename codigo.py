from flask import Flask, render_template, request, jsonify
import math
import random

app = Flask(__name__)

def distancia(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)

def evalua_ruta(ruta, coord):
    total = 0
    for i in range(len(ruta)):
        ciudad1 = ruta[i]
        ciudad2 = ruta[(i + 1) % len(ruta)]
        total += distancia(coord[ciudad1], coord[ciudad2])
    return total

def hill_climbing(coord):
    ruta = list(coord.keys())
    mejora = True
    while mejora:
        mejora = False
        dist_actual = evalua_ruta(ruta, coord)
        for i in range(len(ruta)):
            for j in range(len(ruta)):
                if i != j:
                    ruta_tmp = ruta[:]
                    ruta_tmp[i], ruta_tmp[j] = ruta_tmp[j], ruta_tmp[i]
                    dist = evalua_ruta(ruta_tmp, coord)
                    if dist < dist_actual:
                        mejora = True
                        ruta = ruta_tmp
                        dist_actual = dist
    return ruta

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcular_rutas', methods=['POST'])
def calcular_rutas():
    try:
        coord = {
            'JiloYork': (19.984146, -99.519127),
            'Toluca': (19.286167856525594, -99.65473296644892),
            'Atlacomulco': (19.796802401380955, -99.87643301629244),
            'Guadalajara': (20.655773344775373, -103.35773871581326),
            'Monterrey': (25.675859554333684, -100.31405053526082),
            'Cancún': (21.158135651777727, -86.85092947858692),
            'Morelia': (19.720961251258654, -101.15929186858635),
            'Aguascalientes': (21.88473831747085, -102.29198705069501),
            'Queretaro': (20.57005870003398, -100.45222862892079),
            'CDMX': (19.429550164848152, -99.13000959477478)
        }

        ruta_optima = hill_climbing(coord)
        distancia_total = evalua_ruta(ruta_optima, coord)

        return render_template('index.html', rutas=[ruta_optima], distancia_total=distancia_total)

    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)
