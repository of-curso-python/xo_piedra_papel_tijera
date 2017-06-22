import random
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# importar modulo que contiene clase base de actividad.
from sugar3.activity import activity

from sugar3.graphics.toolbarbox import ToolbarBox

# boton para toolbar
from sugar3.activity.widgets import (
    ActivityToolbarButton,
    StopButton
)

from sugar3.graphics import style
from ppt_utils import OPCIONES


class PiedraPapelTijeras(activity.Activity):

    def __init__(self, handle):
        activity.Activity.__init__(self, handle)
        self.max_participants = 1
        self.contador_usuario = 0
        self.contador_pc = 0
        self.mensaje = '<b>Victorias de {0}: {1}</b>'
        self.agregar_toolbar()
        self.agregar_canvas()

    def agregar_toolbar(self):
        # crear una instancia de ToolbarBox.
        # en este momento es un menu vacio
        toolbar_box = ToolbarBox()

        # Crear instancia de boton de actividad
        activity_toolbar_button = ActivityToolbarButton(self)

        # Crear instancia de boton para cerrar actividad.
        activity_stop_button = StopButton(self)

        # Insertar boton al toolbar en la posicion 0
        toolbar_box.toolbar.insert(activity_toolbar_button, 0)
        # Mostrar boton
        activity_toolbar_button.show()

        # Insertar boton cerrar al toolbar en la posicion -1
        toolbar_box.toolbar.insert(activity_stop_button, -1)
        # Mostrar boton
        activity_stop_button.show()

        # Asignar/establecer el toolbar box para esta actividad
        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()

    def agregar_canvas(self):
        self.canvas = Gtk.VBox()

        self.agregar_contadores()
        self.agregar_visualizador_manos()
        self.agregar_opciones()

        self.canvas.show_all()

    def agregar_contadores(self):
        self.contadores = Gtk.Grid()
        self.contadores.set_column_spacing(15)
        self.contadores.set_column_homogeneous(True)

        self.etiqueta_contador_usuario = Gtk.Label()
        self.etiqueta_contador_usuario.set_markup(
            self.mensaje.format('Usuario', self.contador_usuario)
        )

        self.etiqueta_contador_pc = Gtk.Label()
        self.etiqueta_contador_pc.set_markup(
            self.mensaje.format('PC', self.contador_pc)
        )

        self.contadores.attach(self.etiqueta_contador_usuario, 0, 0, 1, 1)
        self.contadores.attach_next_to(
            self.etiqueta_contador_pc,
            self.etiqueta_contador_usuario,
            Gtk.PositionType.RIGHT,
            1,
            1
        )

        self.canvas.pack_start(self.contadores, False, False, 0)

    def agregar_visualizador_manos(self):
        self.visualizador_manos = Gtk.HBox()
        # TODO: Reemplazar estas imagenes
        self.usr_img = Gtk.Image()
        label_img = Gtk.Label()
        label_img.set_markup('<b> Vs </b>')
        self.pc_img = Gtk.Image()

        self.visualizador_manos.pack_start(self.usr_img, True, False, 0)
        self.visualizador_manos.pack_start(label_img, True, False, 0)
        self.visualizador_manos.pack_start(self.pc_img, True, False, 0)

        self.canvas.pack_start(self.visualizador_manos, True, True, 0)

    def agregar_opciones(self):
        self.opciones = Gtk.Grid()
        self.opciones.set_column_homogeneous(True)
        self.opciones.set_column_spacing(15)
        boton_piedra = Gtk.Button(label='Piedra')
        boton_piedra.connect('clicked', self.seleccion, 'piedra')
        boton_papel = Gtk.Button(label='Papel')
        boton_papel.connect('clicked', self.seleccion, 'papel')
        boton_tijeras = Gtk.Button(label='Tijeras')
        boton_tijeras.connect('clicked', self.seleccion, 'tijeras')

        self.opciones.attach(
            boton_piedra,  # el widget a agregar.
            # El Nro de celda de izquierda a derecha a la que se agregara el
            # elemento. Posicion horizontal.
            0,
            # El Nro de celda de arriba hacia abajo a la que se agregara el elemento.
            # posicion vertical
            3,
            1,  # Nro de columnas que ocupara horizontalmente el elemento.
            1   # Nro de columnas que ocupara verticalmente el elemento.
        )

        self.opciones.attach_next_to(boton_papel, boton_piedra, Gtk.PositionType.RIGHT, 1, 1)
        self.opciones.attach_next_to(boton_tijeras, boton_papel, Gtk.PositionType.RIGHT, 1, 1)

        self.canvas.pack_start(self.opciones, False, False, 0)

    def seleccion(self, boton, seleccion):
        seleccion_pc = random.choice(OPCIONES.keys())

        if seleccion == seleccion_pc:
            pass

        elif OPCIONES[seleccion]['resultados'][seleccion_pc]:
            self.contador_usuario += 1
        else:
            self.contador_pc += 1

        self.actualizar_contadores()
        self.actualizar_visualizador_manos(seleccion, seleccion_pc)

    def actualizar_contadores(self):
        self.etiqueta_contador_usuario.set_markup(
            self.mensaje.format('Usuario', self.contador_usuario)
        )
        self.etiqueta_contador_pc.set_markup(
            self.mensaje.format('PC', self.contador_pc)
        )

    def actualizar_visualizador_manos(self, seleccion, seleccion_pc):
        img_usr = OPCIONES[seleccion]['imagen']
        img_pc = OPCIONES[seleccion_pc]['imagen']
        self.usr_img.set_from_file(img_usr)
        self.pc_img.set_from_file(img_pc)
