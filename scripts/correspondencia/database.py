import sqlite3

DATABASE_NAME = "correspondencia_sena.db"


def get_db():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
        yield conn
    finally:
        conn.close()


def seed_db(conn: sqlite3.Connection):
    cursor = conn.cursor()

    # Comprobar si ya existen remitentes registrados
    cursor.execute("SELECT COUNT(*) FROM remitentes;")
    count_remitentes = cursor.fetchone()[0]

    if count_remitentes == 0:
        # Datos predeterminados de Remitentes
        remitentes_data = [
            (
                "1017001001",
                "Carlos Alberto Mendoza",
                "carlos.mendoza@gmail.com",
                "3001234567",
                "Calle 50 # 45-10, Medellín",
            ),
            (
                "1017002002",
                "María Fernanda Gómez",
                "maria.gomez@hotmail.com",
                "3119876543",
                "Carrera 70 # 32-15, Medellín",
            ),
            (
                "900123456",
                "Empresa Servicios SENA S.A.S.",
                "contacto@serviciossena.com",
                "6044445566",
                "Avenida El Poblado # 10-20, Medellín",
            ),
        ]

        cursor.executemany(
            """
            INSERT INTO remitentes (numero_documento, nombre_completo, email, telefono, direccion)
            VALUES (?, ?, ?, ?, ?);
        """,
            remitentes_data,
        )

        # Datos predeterminados de Radicados
        radicados_data = [
            (
                "RAD-2026-001",
                "Solicitud de certificación académica",
                "Entrada",
                "En Tramite",
                1,
            ),
            (
                "RAD-2026-002",
                "Respuesta a petición de práctico ADSO",
                "Salida",
                "Finalizado",
                2,
            ),
            (
                "RAD-2026-003",
                "Envío de informes de correspondencia mensual",
                "Interno",
                "Pendiente",
                3,
            ),
        ]

        cursor.executemany(
            """
            INSERT INTO radicados (numero_radicado, asunto, tipo_radicado, estado, remitente_id)
            VALUES (?, ?, ?, ?, ?);
        """,
            radicados_data,
        )

        conn.commit()


def init_db():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Tabla Remitentes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS remitentes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_documento TEXT UNIQUE NOT NULL,
            nombre_completo TEXT NOT NULL,
            email TEXT NOT NULL,
            telefono TEXT,
            direccion TEXT
        );
    """)

    # Tabla Radicados
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS radicados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_radicado TEXT UNIQUE NOT NULL,
            asunto TEXT NOT NULL,
            tipo_radicado TEXT NOT NULL,
            estado TEXT NOT NULL DEFAULT 'Pendiente',
            fecha_radicacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            remitente_id INTEGER NOT NULL,
            FOREIGN KEY (remitente_id) REFERENCES remitentes (id) ON DELETE CASCADE
        );
    """)

    conn.commit()

    # Insertar datos predeterminados
    seed_db(conn)

    conn.close()