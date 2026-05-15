import os
import re
import mysql.connector
from dotenv import load_dotenv
from collections import defaultdict

# Cargar .env
load_dotenv()

cfg = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "bdtec"),
}

def q(cur, sql, params=None):
    cur.execute(sql, params or ())
    return cur.fetchall()

def safe_word(s: str, prefix="x_") -> str:
    """Convierte cualquier nombre a un identificador Mermaid válido (A-Za-z0-9_)."""
    if s is None:
        return "x"
    s2 = re.sub(r'\W+', '_', s)  # reemplaza no alfanum por _
    if re.match(r'^\d', s2 or ""):
        s2 = prefix + s2          # si empieza con dígito, prefijo
    if s2 == "":
        s2 = "x"
    return s2

# Conectar a MySQL
conn = mysql.connector.connect(**cfg)
cur = conn.cursor()

schema = cfg["database"]

# === Consultas a information_schema ===
cols_sql = """
SELECT TABLE_NAME, COLUMN_NAME, IS_NULLABLE, COLUMN_KEY
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = %s
ORDER BY TABLE_NAME, ORDINAL_POSITION;
"""

pk_sql = """
SELECT kcu.TABLE_NAME, kcu.COLUMN_NAME
FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc
JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE kcu
  ON tc.CONSTRAINT_NAME = kcu.CONSTRAINT_NAME
 AND tc.TABLE_SCHEMA = kcu.TABLE_SCHEMA
WHERE tc.TABLE_SCHEMA = %s
  AND tc.CONSTRAINT_TYPE = 'PRIMARY KEY'
ORDER BY kcu.TABLE_NAME, kcu.ORDINAL_POSITION;
"""

fk_sql = """
SELECT
  kcu.TABLE_NAME      AS FK_TABLE,
  kcu.COLUMN_NAME     AS FK_COLUMN,
  kcu.REFERENCED_TABLE_NAME AS PK_TABLE,
  kcu.REFERENCED_COLUMN_NAME AS PK_COLUMN
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE kcu
JOIN INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc
  ON tc.CONSTRAINT_NAME = kcu.CONSTRAINT_NAME
 AND tc.TABLE_SCHEMA = kcu.TABLE_SCHEMA
WHERE kcu.TABLE_SCHEMA = %s
  AND tc.CONSTRAINT_TYPE = 'FOREIGN KEY'
ORDER BY kcu.TABLE_NAME, kcu.POSITION_IN_UNIQUE_CONSTRAINT;
"""

cols = q(cur, cols_sql, (schema,))
pks  = q(cur, pk_sql,  (schema,))
fks  = q(cur, fk_sql,  (schema,))

cur.close()
conn.close()

# Estructuras
table_cols   = defaultdict(list)   # {tabla: [(col, isnull, key), ...]}
table_pkcols = defaultdict(set)    # {tabla: {colpk,...}}
relations    = []                  # [(fk_table, pk_table, fk_col, pk_col), ...]

tables_set = set()

for t, c, isnull, colkey in cols:
    table_cols[t].append((c, isnull, colkey))
    tables_set.add(t)

for t, c in pks:
    table_pkcols[t].add(c)
    tables_set.add(t)

for fk_table, fk_col, pk_table, pk_col in fks:
    relations.append((fk_table, pk_table, fk_col, pk_col))
    tables_set.update([fk_table, pk_table])

# Mapa de nombres saneados para Mermaid
safe_table = {t: safe_word(t, prefix="t_") for t in tables_set}

# === Generar Mermaid ===
lines = []
lines.append("# ERD bdtec (Mermaid)\n")
lines.append("```mermaid")
lines.append("erDiagram")

# Tablas (usar tipo genérico 'col' y solo marcar PK)
for t in sorted(table_cols.keys()):
    st = safe_table[t]
    lines.append(f"  {st} {{")
    for c, isnull, colkey in table_cols[t]:
        sc = safe_word(c, prefix="c_")
        flag = " PK" if c in table_pkcols[t] else ""
        lines.append(f"    col {sc}{flag}")
    lines.append("  }")
    lines.append("")  # separador para que el parser no pegue bloques

# Separador antes de relaciones
lines.append("")

# Relaciones Muchos (FK) a Uno (PK)
for fk_table, pk_table, fk_col, pk_col in relations:
    sfk = safe_table[fk_table]
    spk = safe_table[pk_table]
    label = f"{fk_col}→{pk_table}.{pk_col}"  # etiqueta legible con nombres originales
    lines.append(f'  {sfk} }}o--|| {spk} : "{label}"')

lines.append("```")

# Escribir archivo
with open("erd.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("✅ ERD generado en erd.md (Mermaid). Abre el archivo y usa Ctrl+Shift+V para previsualizar.")
