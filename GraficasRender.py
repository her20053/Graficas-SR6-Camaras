# Clase Render

import GraficasColor as libreriaColores
import GraficasMatriz as libreriaMatrices
import GraficasVector as libreriaVectores
import GraficasObjeto as libreriaObjeto
from math import *


class Render(object):

    def __init__(self, ancho, alto):

        self.ancho = ancho
        self.alto = alto

        self.colorActual = libreriaColores.NEGRO
        self.colorLimpieza = libreriaColores.BLANCO

        self.textura = None
        self.material = None
        self.Modelo = None

        self.vista = None
        self.proyeccion = None

        self.limpiar()

    def limpiar(self):
        self.framebuffer = [
            [self.colorLimpieza for x in range(self.ancho)]
            for y in range(self.alto)
        ]

        self.zBuffer = [
            [-9999999 for x in range(self.ancho)]
            for y in range(self.alto)
        ]

        self.zClear = [
            [self.colorLimpieza for x in range(self.ancho)]
            for y in range(self.alto)
        ]

    def clamping(self, valor):
        return int(max(min(valor, 255), 0))

    def establecerColorLimpieza(self, r, g, b):
        nuevoR = self.clamping(r*255)
        nuevoG = self.clamping(g*255)
        nuevoB = self.clamping(b*255)
        self.colorLimpieza = libreriaColores.color(nuevoR, nuevoG, nuevoB)

    def establecerColorActual(self, r, g, b):
        nuevoR = self.clamping(r*255)
        nuevoG = self.clamping(g*255)
        nuevoB = self.clamping(b*255)
        self.colorActual = libreriaColores.color(nuevoR, nuevoG, nuevoB)

    def cargarMatrizDelModelo(self, escala=(1, 1, 1), trasladar=(0, 0, 0), rotar=(0, 0, 0)):

        translate = libreriaVectores.V3(*trasladar)
        scale = libreriaVectores.V3(*escala)
        rotate = libreriaVectores.V3(*rotar)

        translation_matrix = libreriaMatrices.matriz([
            [1, 0, 0, translate.x],
            [0, 1, 0, translate.y],
            [0, 0, 1, translate.z],
            [0, 0, 0,           1]
        ])

        scale_matrix = libreriaMatrices.matriz([
            [scale.x, 0, 0, 0],
            [0, scale.y, 0, 0],
            [0, 0, scale.z, 0],
            [0, 0, 0, 1]
        ])

        a = rotate.x
        rotation_x = libreriaMatrices.matriz([
            [1,      0,       0, 0],
            [0, cos(a), -sin(a), 0],
            [0, sin(a),  cos(a), 0],
            [0,      0,       0, 1]
        ])

        a = rotate.y
        rotation_y = libreriaMatrices.matriz([
            [cos(a), 0, sin(a), 0],
            [0, 1,      0, 0],
            [-sin(a), 0, cos(a), 0],
            [0, 0,      0, 1]
        ])

        a = rotate.z
        rotation_z = libreriaMatrices.matriz([
            [cos(a), -sin(a), 0, 0],
            [sin(a), cos(a), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        rotation_matrix = rotation_x * rotation_y * rotation_z
        self.Modelo = translation_matrix * rotation_matrix * scale_matrix

    def cargarMatrizViewPort(self, largo, alto):

        x = 0
        y = 0
        w = largo if largo != 0 else self.ancho/2
        h = alto if alto != 0 else self.alto/2

        self.Viewport = libreriaMatrices.matriz([
            [w, 0,   0, x + w],
            [0, h,   0, y + h],
            [0, 0, 128,   128],
            [0, 0,   0,     1]
        ])

    def cargarMatrizVista(self, x, y, z, centro):
        Mi = libreriaMatrices.matriz([
            [x.x, x.y, x.z, 0],
            [y.x, y.y, y.z, 0],
            [z.x, z.y, z.z, 0],
            [0, 0, 0, 1],
        ])

        O = libreriaMatrices.matriz([
            [1, 0, 0, -centro.x],
            [0, 1, 0, -centro.y],
            [0, 0, 1, -centro.z],
            [0, 0, 0,         1]
        ])

        self.View = Mi * O

    def cargarProyeccionVistaMatriz(self, ojos, centro):
        coeff = -1/(ojos.length() - centro.length())
        self.Projection = libreriaMatrices.matriz([
            [1, 0,      0, 0],
            [0, 1,      0, 0],
            [0, 0,      1, 0],
            [0, 0, coeff, 1]
        ])

    def mirarHacia(self, ojos, centro, arriba):

        ojos = libreriaVectores.V3(*ojos)
        centro = libreriaVectores.V3(*centro)
        arriba = libreriaVectores.V3(*arriba)

        z = (ojos - centro).normalize()
        x = (arriba * z).normalize()
        y = (z * x).normalize()

        self.cargarMatrizVista(x, y, z, centro)
        self.cargarProyeccionVistaMatriz(ojos, centro)

    def generarObjeto(self, nombreArchivo, escala=(0, 0, 0), trasladar=(0, 0, 0), rotar=(0, 0, 0)):

        self.cargarMatrizDelModelo(escala, trasladar, rotar)
        cube = libreriaObjeto.Obj(nombreArchivo)

        for faceDict in cube.faces:

            face = faceDict['face']
            if len(face) == 4:

                v1 = self.transform_vertex(cube.vertices[face[0][0] - 1])
                v2 = self.transform_vertex(cube.vertices[face[1][0] - 1])
                v3 = self.transform_vertex(cube.vertices[face[2][0] - 1])
                v4 = self.transform_vertex(cube.vertices[face[3][0] - 1])

                if self.textura and len(cube.tvertices) != 0:
                    ft1 = face[0][1] - 1
                    ft2 = face[1][1] - 1
                    ft3 = face[2][1] - 1
                    ft4 = face[3][1] - 1

                    vt1 = libreriaVectores.V3(*cube.tvertices[ft1])
                    vt2 = libreriaVectores.V3(*cube.tvertices[ft2])
                    vt3 = libreriaVectores.V3(*cube.tvertices[ft3])
                    vt4 = libreriaVectores.V3(*cube.tvertices[ft4])

                    self.triangle((v1, v2, v3), (vt1, vt2, vt3),
                                  material=faceDict['material'])
                    self.triangle((v1, v3, v4), (vt1, vt3, vt4),
                                  material=faceDict['material'])
                else:
                    self.triangle((v1, v2, v3), material=faceDict['material'])
                    self.triangle((v1, v3, v4), material=faceDict['material'])

            if len(face) == 3:

                v1 = self.transform_vertex(cube.vertices[face[0][0] - 1])
                v2 = self.transform_vertex(cube.vertices[face[1][0] - 1])
                v3 = self.transform_vertex(cube.vertices[face[2][0] - 1])

                if self.textura and len(cube.tvertices) != 0:

                    ft1 = face[0][1] - 1
                    ft2 = face[1][1] - 1
                    ft3 = face[2][1] - 1

                    vt1 = libreriaVectores.V3(*cube.tvertices[ft1])
                    vt2 = libreriaVectores.V3(*cube.tvertices[ft2])
                    vt3 = libreriaVectores.V3(*cube.tvertices[ft3])

                    self.triangle((v1, v2, v3), (vt1, vt2, vt3),
                                  material=faceDict['material'])
                else:
                    self.triangle((v1, v2, v3), material=faceDict['material'])
