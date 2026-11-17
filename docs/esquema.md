# Esquema de la base de datos

Las tablas las crean las migraciones de este repo (`migrator/migrations/versions/`). Este documento es la referencia del diseño.

Estado: ya existen `analyses` (0001) y `permission_catalog` (0002). Las demás llegan en fases siguientes.

```mermaid
erDiagram
  users ||--o{ analyses : sube
  users ||--o{ refresh_tokens : tiene
  analyses ||--o{ analysis_permissions : detecta
  permission_catalog ||--o{ analysis_permissions : describe

  users {
    uuid id PK
    text email UK
    text password_hash
    boolean is_active
    timestamptz created_at
  }
  refresh_tokens {
    uuid id PK
    uuid user_id FK
    text token_hash UK
    timestamptz expires_at
    timestamptz revoked_at
  }
  analyses {
    uuid id PK
    uuid user_id FK
    bytea file_name_enc
    char sha256
    bigint file_size_bytes
    text status
    smallint risk_score
    text risk_level
    smallint vt_malicious
    smallint vt_total
    bytea report_enc
  }
  permission_catalog {
    int id PK
    text android_name UK
    text friendly_title
    text explanation
    text severity
    smallint weight
    text icon
  }
  analysis_permissions {
    uuid analysis_id PK
    text permission_name PK
    int catalog_id FK
  }
```

## Tablas

| Tabla | Para qué sirve |
|---|---|
| `users` | Cuentas. Solo se guarda el hash de la contraseña (nunca la contraseña). |
| `refresh_tokens` | Tokens de refresco del login. Se guarda su hash, no el token. |
| `analyses` | Un registro por APK analizado: estado, puntaje, resultado de VirusTotal y reporte. |
| `permission_catalog` | Permisos de Android que sabemos explicar: nombre, traducción a español, severidad y peso. |
| `analysis_permissions` | Qué permisos trae cada APK. `catalog_id` queda vacío si el permiso no está en el catálogo. |

## Reglas de diseño

- **Cifrado en reposo (AES-256-GCM):** `file_name_enc` y `report_enc` guardan `nonce + texto cifrado + etiqueta`. El cifrado y la llave viven en la API; la base de datos nunca ve el contenido ni la llave.
- **El hash SHA-256 va sin cifrar** para poder buscar y consultar VirusTotal. Un hash no revela el contenido del archivo.
- `status`: `pending`, `running`, `done` o `failed`.
- `severity` (del catálogo): `peligroso`, `atencion` o `normal`.
- `risk_score` va de 0 a 100. Niveles propuestos (ajustables): `bajo` 0-29, `medio` 30-59, `alto` 60-100.
- Los pesos del catálogo son una propuesta inicial; se calibran con APKs de prueba.