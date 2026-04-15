# =========================
# CATALOGO DE AUTOMATIZACIÓN IT
# =========================

SCRIPTS = {
    # =========================
    # SISTEMA / PC
    # =========================
    "reiniciar_pc": {
        "descripcion": "Reinicia el equipo del usuario",
        "microservice_id": "66e1466f51dcb8b8d0f7a948",
        "flx_unique_id": "bf3c245bf5a2ce7ae67e1b12bc29a731ba4433f7da57211fa21c27c7f9a1808a"
    },

    "apagar_pc": {
        "descripcion": "Apaga el equipo",
        "microservice_id": "MICRO_ID_SHUTDOWN",
        "flx_unique_id": "FLX_ID_SHUTDOWN"
    },

    "bloquear_sesion": {
        "descripcion": "Bloquea la sesión del usuario",
        "microservice_id": "MICRO_ID_LOCK",
        "flx_unique_id": "FLX_ID_LOCK"
    },


    # =========================
    # LIMPIEZA / SISTEMA
    # =========================
    "limpiar_cache": {
        "descripcion": "Limpia cache del sistema",
        "microservice_id": "MICRO_ID_CACHE",
        "flx_unique_id": "FLX_ID_CACHE"
    },

    "vaciar_papelera": {
        "descripcion": "Vacía la papelera de reciclaje",
        "microservice_id": "MICRO_ID_TRASH",
        "flx_unique_id": "FLX_ID_TRASH"
    },

    "limpiar_temporales": {
        "descripcion": "Elimina archivos temporales",
        "microservice_id": "MICRO_ID_TEMP",
        "flx_unique_id": "FLX_ID_TEMP"
    },


    # =========================
    # SOFTWARE / APPS
    # =========================
    "instalar_chrome": {
        "descripcion": "Instala Google Chrome",
        "microservice_id": "MICRO_ID_CHROME",
        "flx_unique_id": "FLX_ID_CHROME"
    },

    "instalar_vscode": {
        "descripcion": "Instala Visual Studio Code",
        "microservice_id": "MICRO_ID_VSCODE",
        "flx_unique_id": "FLX_ID_VSCODE"
    },

    "desinstalar_app": {
        "descripcion": "Desinstala aplicación del equipo",
        "microservice_id": "MICRO_ID_UNINSTALL",
        "flx_unique_id": "FLX_ID_UNINSTALL"
    },


    # =========================
    # SISTEMA AVANZADO
    # =========================
    "reiniciar_servicio": {
        "descripcion": "Reinicia un servicio del sistema",
        "microservice_id": "MICRO_ID_SERVICE_RESTART",
        "flx_unique_id": "FLX_ID_SERVICE_RESTART"
    },

    "estado_sistema": {
        "descripcion": "Consulta estado del sistema",
        "microservice_id": "MICRO_ID_STATUS",
        "flx_unique_id": "FLX_ID_STATUS"
    }
}
