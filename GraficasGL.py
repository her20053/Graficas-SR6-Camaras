# Modulo encargado de utilizar el la clase Render

import GraficasRender as libreriaRender
import GraficasTextura as libreriaTexturas

# Instanciando una variable render que sera declarada posteriormente:
render = None


def glCrearVentana(largo, alto):
    global render
    render = libreriaRender.Render(largo, alto)


def glInicializar(largoVentana, altoVentana):
    glCrearVentana(largo=largoVentana, alto=altoVentana)


def establecerColorLimpieza(r, g, b):
    render.establecerColorLimpieza(r, g, b)


def establecerColor(r, g, b):
    render.establecerColorActual(r, g, b)


def glViewPort(movimientoX, movimientoY, largoVP, altoVP):
    render.cargarMatrizViewPort(
        largoVP if largoVP < render.ancho else render.ancho - movimientoX - 1,
        altoVP if altoVP < render.alto else render.alto - movimientoY - 1
    )
    render.viewport_param = {
        "x": movimientoX,
        "y": movimientoY,
        "width": largoVP if largoVP < render.ancho else render.ancho - movimientoX - 1,
        "height": altoVP if altoVP < render.alto else render.alto - movimientoY - 1
    }


def glTextura(archivoTextura):
    render.textura = libreriaTexturas.Texture(archivoTextura)


def glMirarHacia(ojos, centro, arriba):
    render.mirarHacia(ojos, centro, arriba)


def glRenderizarObjeto(nombreArchivo, escala, transladar, rotar=(0, 0, 0)):
