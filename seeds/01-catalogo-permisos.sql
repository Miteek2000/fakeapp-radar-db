-- Catálogo inicial de permisos de Android (propuesta; los pesos se calibran con pruebas).
-- Se ejecuta DESPUÉS de que Alembic cree la tabla permission_catalog.
-- Se puede correr varias veces sin duplicar datos.

INSERT INTO permission_catalog (android_name, friendly_title, explanation, severity, weight, icon) VALUES
('android.permission.READ_SMS', 'Leer tus mensajes SMS', 'Puede copiar los códigos de verificación que te manda tu banco.', 'peligroso', 20, 'message-square'),
('android.permission.RECEIVE_SMS', 'Interceptar mensajes SMS nuevos', 'Puede ver cada mensaje en cuanto llega, incluidos los códigos de verificación.', 'peligroso', 20, 'message-square'),
('android.permission.SEND_SMS', 'Mandar mensajes SMS por ti', 'Puede enviar mensajes que te generen cargos o que se propaguen a tus contactos.', 'peligroso', 15, 'send'),
('android.permission.BIND_ACCESSIBILITY_SERVICE', 'Controlar lo que ves en pantalla', 'Puede leer lo que escribes y tocar botones por ti sin que lo notes.', 'peligroso', 25, 'eye'),
('android.permission.SYSTEM_ALERT_WINDOW', 'Dibujar encima de otras apps', 'Puede mostrar una pantalla falsa sobre tu app del banco para robar tu contraseña.', 'peligroso', 20, 'layers'),
('android.permission.REQUEST_INSTALL_PACKAGES', 'Instalar otras apps', 'Puede instalar más aplicaciones sin que lo notes.', 'peligroso', 15, 'package-plus'),
('android.permission.BIND_DEVICE_ADMIN', 'Volverse administrador del teléfono', 'Puede dificultar que la desinstales o bloquear tu dispositivo.', 'peligroso', 20, 'lock'),
('android.permission.READ_CONTACTS', 'Ver tus contactos', 'Podría mandar mensajes a tus conocidos para seguir propagándose.', 'atencion', 8, 'users'),
('android.permission.ACCESS_FINE_LOCATION', 'Saber dónde estás con exactitud', 'Una app bancaria no necesita tu ubicación exacta todo el tiempo.', 'atencion', 8, 'map-pin'),
('android.permission.ACCESS_COARSE_LOCATION', 'Saber más o menos dónde estás', 'Puede conocer en qué zona te encuentras.', 'atencion', 5, 'map-pin'),
('android.permission.RECORD_AUDIO', 'Grabar audio con el micrófono', 'Puede escuchar lo que ocurre a tu alrededor. Solo es normal en apps de llamadas o grabación.', 'atencion', 10, 'mic'),
('android.permission.READ_CALL_LOG', 'Ver tu historial de llamadas', 'Puede saber a quién llamas y quién te llama.', 'atencion', 10, 'phone'),
('android.permission.READ_PHONE_STATE', 'Ver datos de tu teléfono y llamadas', 'Puede identificar tu dispositivo y saber cuándo estás en una llamada.', 'atencion', 6, 'smartphone'),
('android.permission.RECEIVE_BOOT_COMPLETED', 'Iniciar sola al encender el teléfono', 'Se activa cada vez que prendes el teléfono, sin que la abras.', 'atencion', 3, 'power'),
('android.permission.CAMERA', 'Usar la cámara', 'Es normal si la app escanea documentos o códigos QR.', 'normal', 2, 'camera'),
('android.permission.INTERNET', 'Conectarse a internet', 'La mayoría de las apps lo necesitan para funcionar.', 'normal', 1, 'globe'),
('android.permission.POST_NOTIFICATIONS', 'Mostrarte notificaciones', 'Puede enviarte avisos en la pantalla.', 'normal', 1, 'bell')
ON CONFLICT (android_name) DO UPDATE SET
  friendly_title = EXCLUDED.friendly_title,
  explanation = EXCLUDED.explanation,
  severity = EXCLUDED.severity,
  weight = EXCLUDED.weight,
  icon = EXCLUDED.icon;