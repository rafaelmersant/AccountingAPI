# Histórico de registros

## Publicación

1. Publicar el backend y ejecutar `python manage.py migrate entries` antes de habilitarlo.
2. Publicar el frontend generado con `npm run build`.
3. Verificar en un registro existente: cambiar un monto y guardar; abrir Histórico desde el detalle.

El endpoint de consulta es `GET /api/v1/entries/{id}/history/`. No permite editar ni eliminar eventos. El historial conserva valores y nombres al momento del cambio, aun cuando se elimine el registro, usuario o concepto. Los eventos de un registro eliminado se conservan en la base; la pantalla de ese registro ya no estará disponible.

Se registran las modificaciones de cabecera, altas, cambios y bajas de detalles efectuados mediante los endpoints de registros. No se generan eventos al guardar valores idénticos. Las altas de conceptos también forman parte del historial. No se reconstruyen cambios anteriores a esta versión. Cambios directos por SQL o por otras herramientas que omitan estos endpoints no están cubiertos.

La fecha se genera en el servidor y se presenta en America/Santo_Domingo. Cada operación y su evento se guardan en la misma transacción. El guardado completo de cabecera y detalles conserva las solicitudes separadas del sistema actual.

## Identidad actual

El login existente guarda la identidad en localStorage y no crea una sesión/token de servidor. El frontend envía X-Entry-User y el backend comprueba que el usuario exista, pero esta identidad todavía no está autenticada criptográficamente. No se usa created_by como sustituto del editor. Clientes anteriores sin cabecera se identifican como Usuario no identificado (cliente anterior). Para garantizar autoría frente a suplantación se requiere migrar el login a sesiones o tokens verificados en servidor.

## Validación

`python manage.py test entries --noinput` cubre valores anteriores/nuevos, usuario, fecha, eliminación de asociaciones, altas/bajas, cambios de método/período/referencia, guardado sin cambios, aislamiento de historiales, consulta de solo lectura y reversión si falla la auditoría.
