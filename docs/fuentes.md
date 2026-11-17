# Fuentes del catálogo de permisos

El catálogo tiene dos capas (columna `curated`):

| Capa | Archivo | Qué cubre |
|---|---|---|
| Automática (`curated = false`) | `seeds/01-catalogo-aosp.sql` | Los 1059 permisos de AOSP (androguard 4.1.4, API 4 a 36, gana el nivel más nuevo). Texto genérico en español según el `protectionLevel`. |
| Curada (`curated = true`) | `seeds/02-catalogo-curado.sql` | 52 permisos con explicación propia y peso propio. **Sobrescribe** a la automática. |

Regla de la capa automática (severidad y peso salen del `protectionLevel` oficial):

| protectionLevel | Severidad | Peso |
|---|---|---|
| contiene `dangerous` | atención | 4 |
| empieza con `normal` | normal | 1 |
| cualquier otro (`signature`, `internal`...) | atención | 2 |

Un permiso que no está en AOSP (por ejemplo los de Google Play Services o de fabricantes) sigue saliendo como "no está en nuestro catálogo".

La capa curada guarda en la columna `source` las claves de esta tabla.

## Qué es dato y qué es criterio propio
| Columna | Origen |
|---|---|
| `android_name`, `protection_level` | Datos oficiales de AOSP (API 4 a 36), tomados de los recursos de androguard 4.1.4. Se verificó que cada permiso curado exista. |
| `friendly_title`, `explanation` | Capa curada: redacción propia en español sencillo. Capa automática: texto genérico por nivel de protección. |
| `severity`, `weight` | **Ponderación propia del proyecto**, apoyada en las fuentes de abajo. No es un estándar de la industria y se puede ajustar. |

## Claves de fuentes
| Clave | Fuente | Qué respalda |
|---|---|---|
| `AOSP` | Android Open Source Project, datos de permisos incluidos en androguard | Existencia del permiso y su `protectionLevel` |
| `PLAY-SMS` | Google Play, política de permisos de SMS y registro de llamadas: https://support.google.com/googleplay/android-developer/answer/9047303 | Estos permisos están restringidos a apps con función central de SMS o teléfono |
| `PLAY-STORAGE` | Google Play, política de permisos sensibles: https://support.google.com/googleplay/android-developer/answer/9888170 | `MANAGE_EXTERNAL_STORAGE` es de acceso restringido |
| `PLAY-PKG` | Google Play, `QUERY_ALL_PACKAGES`: https://support.google.com/googleplay/android-developer/answer/10158779 | Visibilidad amplia de apps instaladas está restringida |
| `PLAY-INSTALL` | Google Play, `REQUEST_INSTALL_PACKAGES`: https://support.google.com/googleplay/android-developer/answer/13986130 | Solo para apps cuyo propósito central es instalar paquetes |
| `PLAY-LOC` | Google Play, política de permisos sensibles (ubicación en segundo plano): https://support.google.com/googleplay/android-developer/answer/9888170 | Solo si es parte de la función central |
| `PLAY-FSI` | Google Play, política de permisos (pantalla completa): https://support.google.com/googleplay/android-developer/answer/13986130 | `USE_FULL_SCREEN_INTENT` pasa a acceso especial desde Android 14 |
| `PLAY-MEDIA` | Google Play, política de permisos: https://support.google.com/googleplay/android-developer/answer/16909972 | Acceso amplio a fotos y videos solo si los selectores del sistema no bastan |
| `MITRE-T1517` | MITRE ATT&CK T1517, Access Notifications: https://attack.mitre.org/techniques/T1517/ | Lectura de notificaciones (incluye códigos 2FA) mediante `BIND_NOTIFICATION_LISTENER_SERVICE` |
| `SRLABS-FLUBOT` | SRLabs, FluBot abusa de accesibilidad: https://srlabs.de/blog/flubot-abuses-accessibility-features-to-steal-data | Troyano bancario que pide accesibilidad y acceso a notificaciones |
| `CLEAFY-TRICKMO` | Cleafy, TrickMo: https://cleafy.com/cleafy-labs/a-new-trickmo-saga-from-banking-trojan-to-victims-data-leak | Abuso de accesibilidad en un troyano bancario |
| `GROUPIB-REMCONTROL` | Group-IB, RemControl: https://www.group-ib.com/blog/remcontrol-android-banking-trojan/ | Pide accesibilidad al instalarse y la usa para control remoto y superposiciones |
| `ZIMPERIUM-OVERLAY` | Zimperium vía TechRepublic (abril 2026): https://techrepublic.com/article/news-android-malware-stealing-pin-overlay-attack | Campañas que combinan superposiciones y accesibilidad para robar PIN |
| `CYBLE-DRINIK` | Cyble vía BleepingComputer, Drinik: https://www.bleepingcomputer.com/news/security/drinik-android-malware-now-targets-users-of-18-indian-banks/amp/ | Pide leer, recibir y enviar SMS, y leer o escribir almacenamiento |
| `KEYSIGHT-PROMISC` | Keysight ATI, Promiscuous Permissions: https://medium.com/keysight-ati/promiscuous-permissions-catching-your-android-apps-in-the-act-1a8faa450be3 | Administrador de dispositivo entre los permisos explotados por malware |

## Límites que conviene decir en la defensa
- Un permiso peligroso no vuelve maliciosa a una app: muchas apps legítimas piden varios. El puntaje es un indicador, no un veredicto.
- Los permisos `signature` como accesibilidad o administrador de dispositivo no se "conceden" en la instalación: el usuario los activa a mano en Ajustes. Declararlos en el manifiesto ya es una señal.
- Las fuentes de malware describen familias concretas; no prueban que toda app con ese permiso sea maliciosa.
