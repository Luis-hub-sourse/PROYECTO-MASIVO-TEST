from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt5.QtCore import QDate
from servicios.servicio_inasistencia import ServicioInasistencia
from servicios.servicio_materia import ServicioMateria

class VentanaInasistencia(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi("xml/inasistencia_form.ui", self)
        
        # Inicializar la capa servicio
        self.servicio_inasistencia = ServicioInasistencia()
        self.servicio_materia = ServicioMateria()

        self.uso_fecha_finalizacion = False

        # Cargar materias en el combo box
        self.cargar_materias()

        # Conexión de botones
        self.btnEnviar.clicked.connect(self.reportar_inasistencia)
        self.chboxMasDias.stateChanged.connect(self.mostrar_fecha_finalizacion)

    def mostrar_fecha_finalizacion(self):
        if self.chboxMasDias.isChecked():
            self.deFechaFinalizacion.setEnabled(True)
            self.label_2.setEnabled(True)
            finalizacion_true = self.deFecha.date().addDays(1)  # Establecer fecha finalización al día siguiente por defecto
            self.deFechaFinalizacion.setDate(finalizacion_true)
            self.uso_fecha_finalizacion = True
        else:
            self.deFechaFinalizacion.setEnabled(False)
            self.label_2.setEnabled(False)
            self.deFechaFinalizacion.setDate(self.deFecha.date())
            self.uso_fecha_finalizacion = False

    def reportar_inasistencia(self):
        try:
            emisor = "Sistema Escolar <funciondeprueba@gmail.com>"
            id_materia = self.cbMateria.currentText()
            fecha_falta_qt = self.deFecha.date()
            if self.uso_fecha_finalizacion:
                fecha_finalizacion_qt = self.deFechaFinalizacion.date()
            else:               fecha_finalizacion_qt = None
            motivo = self.cbMotivo.currentText()
            detalle = self.cuadroTexto.toPlainText()
            exito, mensaje = self.servicio_inasistencia.registrar_inasistencia(emisor, id_materia, fecha_falta_qt, fecha_finalizacion_qt, motivo, detalle)
            exito_notificacion, mensaje_notificacion = self.servicio_inasistencia.enviar_notificacion(emisor, id_materia, fecha_falta_qt, fecha_finalizacion_qt, motivo, detalle)
            if exito:
                QMessageBox.information(self, "Éxito", mensaje)
                self.cuadroTexto.clear()
            if exito_notificacion:
                QMessageBox.information(self, "Notificación Enviada", mensaje_notificacion)
            else:
                QMessageBox.warning(self, "Error", mensaje)
                QMessageBox.warning(self, "Error Notificación", mensaje_notificacion)
        except Exception as ex:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {str(ex)}")

    def cargar_materias(self):
        try:
            materias = self.servicio_materia.buscar_materias()
            for materia in materias:
                self.cbMateria.addItem(materia[1])
        except Exception as ex:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar las materias: {str(ex)}")

class VentanaRegsitroInasistencia(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi("xml/registro_inasistencia.ui", self)
        
        # Inicializar la capa servicio
        self.servicio_inasistencia = ServicioInasistencia()
        self.servicio_materia = ServicioMateria()

        self.btnIrInforme.clicked.connect(self.abrir_ventana_informes)
        self.cBoxMateria.currentTextChanged.connect(self.filtrar_tabla_materia)
        self.dateFalta.dateChanged.connect(self.filtrar_tabla_dia_falta)
        self.cBoxMotivo.currentTextChanged.connect(self.filtrar_tabla_motivo)
        self.chBoxDetalle.stateChanged.connect(self.filtrar_tabla_detalle)
        self.btnActualizar.clicked.connect(self.cargar_inasistencias)

        # Cargar inasistencias en la tabla
        self.cargar_inasistencias()
        self.cargar_materias()

    def abrir_ventana_informes(self):
        ventana_informes = VentanaInasistencia(self)
        ventana_informes.exec_()

    def cargar_inasistencias(self):
        try:
            inasistencias = self.servicio_inasistencia.listar_inasistencias()
            self.tableInasistencias.setRowCount(0)  # Limpiar tabla antes de cargar
            if inasistencias:
                for inasistencia in inasistencias:
                    row_position = self.tableInasistencias.rowCount()
                    self.tableInasistencias.insertRow(row_position)
                    self.tableInasistencias.setItem(row_position, 0, QTableWidgetItem(inasistencia[0]))  # Emisor
                    self.tableInasistencias.setItem(row_position, 1, QTableWidgetItem(inasistencia[1]))  # Materia
                    self.tableInasistencias.setItem(row_position, 2, QTableWidgetItem(str(inasistencia[2])))  # Fecha
                    self.tableInasistencias.setItem(row_position, 3, QTableWidgetItem(inasistencia[3]))  # Motivo
                    self.tableInasistencias.setItem(row_position, 4, QTableWidgetItem(inasistencia[4]))  # Detalle
                    self.tableInasistencias.setItem(row_position, 5, QTableWidgetItem(str(inasistencia[5])))  # Fecha de registro
            else:
                QMessageBox.warning(self, "Error", inasistencias[1])
        except Exception as ex:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar las inasistencias: {str(ex)}")

    def cargar_materias(self):
        try:
            materias = self.servicio_materia.buscar_materias()
            for materia in materias:
                self.cBoxMateria.addItem(materia[1])
        except Exception as ex:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar las materias: {str(ex)}")

    def filtrar_tabla_materia(self):
        materia_seleccionada = self.cBoxMateria.currentText()
        self.tableInasistencias.setRowCount(0)
        todos_los_datos = self.servicio_inasistencia.listar_inasistencias()
        registros_filtrados = []
        for registro in todos_los_datos:
            correo, id_materia, periodo, motivo, detalle, fecha_reg = registro
            
            # Filtro por materia (si seleccionó algo)
            if materia_seleccionada and materia_seleccionada != "Todas":
                if str(id_materia) != materia_seleccionada:
                    continue

            registros_filtrados.append(registro)
        self.mostrar_registros_filtrados(registros_filtrados)

    def filtrar_tabla_dia_falta(self):
        fecha_seleccionada = self.dateFalta.date().toPyDate()
        self.tableInasistencias.setRowCount(0)
        todos_los_datos = self.servicio_inasistencia.listar_inasistencias()
        registros_filtrados = []
        for registro in todos_los_datos:
            correo, id_materia, periodo, motivo, detalle, fecha_reg = registro
            # Filtro por fecha (si seleccionó algo)
            if fecha_seleccionada:
                fecha_registro = QDate.fromString(str(registro[5]).split(' ')[0], 'yyyy/MM/dd')
                if fecha_registro != fecha_seleccionada:
                    continue

            registros_filtrados.append(registro)
        self.mostrar_registros_filtrados(registros_filtrados)

    def filtrar_tabla_motivo(self):
        motivo_seleccionado = self.cBoxMotivo.currentText()
        self.tableInasistencias.setRowCount(0)
        todos_los_datos = self.servicio_inasistencia.listar_inasistencias()
        registros_filtrados = []
        for registro in todos_los_datos:
            correo, id_materia, periodo, motivo, detalle, fecha_reg = registro

            # Filtro por motivo (si seleccionó algo)
            if motivo_seleccionado and motivo_seleccionado != "Todos":
                if str(motivo) != motivo_seleccionado:
                    continue
            
            registros_filtrados.append(registro)
        self.mostrar_registros_filtrados(registros_filtrados)

    def filtrar_tabla_detalle(self):
        sin_detalle = self.chBoxDetalle.isChecked()
        self.tableInasistencias.setRowCount(0)
        todos_los_datos = self.servicio_inasistencia.listar_inasistencias()

        registros_filtrados = []
        for registro in todos_los_datos:
            correo, id_materia, periodo, motivo, detalle, fecha_reg = registro

            # Filtro por detalle (si no se seleccionó mostrar detalles)
            if sin_detalle: 
                if detalle: 
                    continue
            else:  
                if not detalle:
                    continue

            registros_filtrados.append(registro)
        self.mostrar_registros_filtrados(registros_filtrados)
        
    def mostrar_registros_filtrados(self, registros_filtrados):
        # Mostrar solo registros filtrados
        for row_position, inasistencia in enumerate(registros_filtrados):
            self.tableInasistencias.insertRow(row_position)
            self.tableInasistencias.setItem(row_position, 0, QTableWidgetItem(str(inasistencia[0])))
            self.tableInasistencias.setItem(row_position, 1, QTableWidgetItem(str(inasistencia[1])))
            self.tableInasistencias.setItem(row_position, 2, QTableWidgetItem(str(inasistencia[2])))
            self.tableInasistencias.setItem(row_position, 3, QTableWidgetItem(str(inasistencia[3])))
            self.tableInasistencias.setItem(row_position, 4, QTableWidgetItem(str(inasistencia[4])))
            self.tableInasistencias.setItem(row_position, 5, QTableWidgetItem(str(inasistencia[5])))