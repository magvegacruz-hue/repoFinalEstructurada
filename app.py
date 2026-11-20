# Aplicación Flask del sistema UAM Conecta.
# Conecta la lógica del programa con las páginas HTML.

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    Response
)

from datetime import datetime
import io
import csv

# Importa las funciones de lógica y estructuras de datos.
from logica.gestorDatos import inicializar_sistema
from logica.gestorDatos import (
    obtener_actividades,
    obtener_actividades_disponibles,
    buscar_actividad_por_id,
    buscar_solicitud_por_id,
    crear_actividad,
    editar_actividad,
    eliminar_actividad,
    registrar_solicitud,
    obtener_solicitudes_pendientes,
    cambiar_estado_solicitud,
    obtener_historial_estudiante,
    calcular_horas_convalidadas,
    calcular_creditos_convalidados,
    generar_reportes,
    generar_grafo
)

from logica.ordenamiento import ordenar_por_insercion

# Crea la aplicación web.
app = Flask(__name__)

# Clave necesaria para utilizar sesiones en Flask.
app.secret_key = "uam_conecta_2026"

# Credenciales únicas del administrador de Vida Estudiantil.
ADMIN_USUARIO = "vidaestudiantil"
ADMIN_CONTRASENA = "uam2026"

# Carga los datos iniciales desde los archivos JSON.
datos = inicializar_sistema()


# Verifica si el usuario actual es el administrador.
def administrador_autenticado():
    return session.get("rol") == "administrador"


# Calcula los indicadores principales para el panel de Vida Estudiantil.
def obtener_estadisticas():
    solicitudes = datos["solicitudes"]["solicitudes"]

    pendientes = 0
    convalidadas = 0
    rechazadas = 0

    # Recorre todas las solicitudes y cuenta cada estado.
    for solicitud in solicitudes:
        if solicitud["estado"] == "Pendiente":
            pendientes += 1

        if solicitud["estado"] == "Convalidado":
            convalidadas += 1

        if solicitud["estado"] == "Rechazado":
            rechazadas += 1

    return {
        "pendientes": pendientes,
        "convalidadas": convalidadas,
        "rechazadas": rechazadas,
        "total_actividades": len(datos["actividades"]["actividades"])
    }


# Página principal para los estudiantes.
@app.route("/")
def inicio():
    actividades = obtener_actividades_disponibles(datos)
    return render_template("index.html", actividades=actividades)


# Inicio de sesión exclusivo para Vida Estudiantil.
@app.route("/login_admin", methods=["GET", "POST"])
def login_admin():
    if request.method == "POST":
        usuario = request.form.get("usuario", "")
        contrasena = request.form.get("contrasena", "")

        # Valida las credenciales del administrador.
        if usuario == ADMIN_USUARIO and contrasena == ADMIN_CONTRASENA:
            session["rol"] = "administrador"
            flash("Inicio de sesión exitoso.", "exito")
            return redirect(url_for("panel_admin"))

        flash("Usuario o contraseña incorrectos.", "error")

    return render_template("login_admin.html")


# Cierra la sesión del administrador.
@app.route("/cerrar_sesion")
def cerrar_sesion():
    session.clear()
    flash("Sesión cerrada correctamente.", "exito")
    return redirect(url_for("inicio"))


# Panel principal de Vida Estudiantil.
@app.route("/panel_admin")
def panel_admin():
    if not administrador_autenticado():
        return redirect(url_for("login_admin"))

    actividades = obtener_actividades(datos)
    solicitudes = obtener_solicitudes_pendientes(datos)
    estadisticas = obtener_estadisticas()

    return render_template(
        "panel_admin.html",
        actividades=actividades,
        solicitudes_pendientes=solicitudes,
        estadisticas=estadisticas
    )


# Permite crear una nueva actividad.
@app.route("/crear_actividad", methods=["GET", "POST"])
def crear_actividad_ruta():
    if not administrador_autenticado():
        return redirect(url_for("login_admin"))

    if request.method == "POST":
        # request.form contiene los datos enviados desde el formulario HTML.
        resultado = crear_actividad(datos, request.form)

        if resultado["exito"]:
            flash(resultado["mensaje"], "exito")
            return redirect(url_for("panel_admin"))

        flash(resultado["mensaje"], "error")

    return render_template("crear_actividad.html")


# Permite editar una actividad existente.
@app.route("/editar_actividad/<id_actividad>", methods=["GET", "POST"])
def editar_actividad_ruta(id_actividad):
    if not administrador_autenticado():
        return redirect(url_for("login_admin"))

    actividad = buscar_actividad_por_id(datos, id_actividad)

    if actividad is None:
        flash("La actividad no existe.", "error")
        return redirect(url_for("panel_admin"))

    if request.method == "POST":
        resultado = editar_actividad(datos, id_actividad, request.form)

        if resultado["exito"]:
            flash(resultado["mensaje"], "exito")
            return redirect(url_for("panel_admin"))

        flash(resultado["mensaje"], "error")

    return render_template("editar_actividad.html", actividad=actividad)


# Elimina una actividad y actualiza sus solicitudes.
@app.route("/eliminar_actividad/<id_actividad>")
def eliminar_actividad_ruta(id_actividad):
    if not administrador_autenticado():
        return redirect(url_for("login_admin"))

    resultado = eliminar_actividad(datos, id_actividad)

    if resultado["exito"]:
        flash(resultado["mensaje"], "exito")
    else:
        flash(resultado["mensaje"], "error")

    return redirect(url_for("panel_admin"))


# Muestra las solicitudes pendientes ordenadas por inserción.
@app.route("/solicitudes_pendientes")
def solicitudes_pendientes_ruta():
    if not administrador_autenticado():
        return redirect(url_for("login_admin"))

    # Permite ordenar por fecha, horas o nombre del estudiante.
    criterio = request.args.get("criterio", "fecha_solicitud")
    solicitudes = obtener_solicitudes_pendientes(datos)

    solicitudes_ordenadas = ordenar_por_insercion(
        solicitudes,
        clave=lambda solicitud: solicitud.get(criterio, "")
    )

    return render_template(
        "solicitudes_pendientes.html",
        solicitudes=solicitudes_ordenadas,
        criterio=criterio
    )


# Marca una solicitud como convalidada.
@app.route("/convalidar_solicitud/<id_solicitud>")
def convalidar_solicitud_ruta(id_solicitud):
    if not administrador_autenticado():
        return redirect(url_for("login_admin"))

    resultado = cambiar_estado_solicitud(datos, id_solicitud, "Convalidado")

    if resultado["exito"]:
        flash(resultado["mensaje"], "exito")
    else:
        flash(resultado["mensaje"], "error")

    return redirect(url_for("solicitudes_pendientes_ruta"))


# Permite rechazar una solicitud indicando el motivo.
@app.route("/rechazar_solicitud/<id_solicitud>", methods=["GET", "POST"])
def rechazar_solicitud_ruta(id_solicitud):
    if not administrador_autenticado():
        return redirect(url_for("login_admin"))

    if request.method == "POST":
        observacion = request.form.get("observacion", "").strip()

        resultado = cambiar_estado_solicitud(
            datos,
            id_solicitud,
            "Rechazado",
            observacion
        )

        if resultado["exito"]:
            flash(resultado["mensaje"], "exito")
        else:
            flash(resultado["mensaje"], "error")

        return redirect(url_for("solicitudes_pendientes_ruta"))

    solicitud = buscar_solicitud_por_id(datos, id_solicitud)
    return render_template("rechazar_solicitud.html", solicitud=solicitud)


# Muestra los detalles de una actividad.
@app.route("/actividad/<id_actividad>")
def detalle_actividad_ruta(id_actividad):
    actividad = buscar_actividad_por_id(datos, id_actividad)

    if actividad is None:
        flash("La actividad no existe.", "error")
        return redirect(url_for("inicio"))

    return render_template("detalle_actividad.html", actividad=actividad)


# Permite al estudiante enviar una solicitud de convalidación.
@app.route("/registrar_solicitud/<id_actividad>", methods=["GET", "POST"])
def registrar_solicitud_ruta(id_actividad):
    actividad = buscar_actividad_por_id(datos, id_actividad)

    if actividad is None:
        flash("La actividad no existe.", "error")
        return redirect(url_for("inicio"))

    if request.method == "POST":
        resultado = registrar_solicitud(datos, id_actividad, request.form)

        if resultado["exito"]:
            flash(resultado["mensaje"], "exito")
            return redirect(
                url_for("historial_ruta", cif=request.form.get("cif", ""))
            )

        flash(resultado["mensaje"], "error")

    return render_template("registrar_solicitud.html", actividad=actividad)


# Muestra el historial del estudiante y permite filtrar solicitudes.
@app.route("/historial")
def historial_ruta():
    cif = request.args.get("cif", "").strip()
    estado = request.args.get("estado", "")
    beneficio = request.args.get("beneficio", "")

    solicitudes = obtener_historial_estudiante(datos, cif)

    # Filtra por estado si el usuario seleccionó una opción.
    if estado:
        solicitudes_filtradas = []

        for solicitud in solicitudes:
            if solicitud["estado"] == estado:
                solicitudes_filtradas.append(solicitud)

        solicitudes = solicitudes_filtradas

    # Filtra por tipo de beneficio.
    if beneficio:
        solicitudes_filtradas = []

        for solicitud in solicitudes:
            if solicitud["beneficio_solicitado"] == beneficio:
                solicitudes_filtradas.append(solicitud)

        solicitudes = solicitudes_filtradas

    horas = calcular_horas_convalidadas(datos, cif)
    creditos = calcular_creditos_convalidados(datos, cif)

    return render_template(
        "historial.html",
        cif=cif,
        solicitudes=solicitudes,
        horas_convalidadas=horas,
        creditos=creditos,
        estado=estado,
        beneficio=beneficio
    )


# Descarga el historial del estudiante en formato CSV.
@app.route("/descargar_historial/<cif>")
def descargar_historial_ruta(cif):
    solicitudes = obtener_historial_estudiante(datos, cif)

    # Crea el archivo CSV en memoria.
    salida = io.StringIO()
    escritor = csv.writer(salida)

    escritor.writerow([
        "ID Solicitud",
        "Actividad",
        "Beneficio",
        "Horas",
        "Fecha Solicitud",
        "Estado",
        "Observación"
    ])

    for solicitud in solicitudes:
        escritor.writerow([
            solicitud["id_solicitud"],
            solicitud["nombre_actividad"],
            solicitud["beneficio_solicitado"],
            solicitud["horas_solicitadas"],
            solicitud["fecha_solicitud"],
            solicitud["estado"],
            solicitud["observacion"]
        ])

    salida.seek(0)

    return Response(
        salida,
        mimetype="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=historial_{cif}.csv"
        }
    )


# Muestra los reportes generales del sistema.
@app.route("/reportes")
def reportes_ruta():
    if not administrador_autenticado():
        return redirect(url_for("login_admin"))

    reportes = generar_reportes(datos)
    return render_template("reportes.html", reportes=reportes)


# Muestra las relaciones entre estudiantes, actividades y beneficios.
@app.route("/grafo")
def grafo_ruta():
    if not administrador_autenticado():
        return redirect(url_for("login_admin"))

    grafo = generar_grafo(datos)
    return render_template("grafo.html", grafo=grafo)


# Ejecuta la aplicación si este archivo se corre directamente.
if __name__ == "__main__":
    app.run(debug=True)