from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from apps.articulos.models import Articulos
from apps.usuarios.models import CustomUser
from apps.notificaciones.models import Notification, NotificationCustomUser
from apps.compras.models import Detalle_compras
from apps.ventas.models import Detalle_ventas

def enviar_notificacion_stock(articulo):
    """ Verificar el stock y enviar notificaciones """
    content_type = ContentType.objects.get_for_model(Articulos)
    if articulo.stock > 0 and articulo.stock < articulo.stock_minimo:
        mensaje = f"El producto '{articulo.descripcion_articulo}' con código: {articulo.codigoarticulo} tiene un stock de {articulo.stock}, por debajo del mínimo permitido {articulo.stock_minimo}."
        notificacion_id = 1
    elif articulo.stock > articulo.stock_maximo:
        mensaje = f"El producto '{articulo.descripcion_articulo}' con código: {articulo.codigoarticulo} tiene un stock de {articulo.stock}, por encima del máximo permitido {articulo.stock_maximo}."
        notificacion_id = 2
    elif articulo.stock == 0:
        mensaje = f"El producto '{articulo.descripcion_articulo}' con código: {articulo.codigoarticulo} ha llegado a un stock de 0."
        notificacion_id = 3
    else:
        return
    
    # Crear notificación para cada usuario
    for user in CustomUser.objects.all():
        NotificationCustomUser.objects.create(
            idnotification=Notification.objects.get(idnotification=notificacion_id),
            user=user,
            message=mensaje,
            target_content_type=content_type,
            target_id=articulo.idarticulo,
            target_object=articulo
        )

@receiver(post_save, sender=Detalle_compras)
def verificar_stock_compra(sender, instance, **kwargs):
    """ Enviar notificación cuando se registra una compra """
    articulo = instance.codigoarticulo
    enviar_notificacion_stock(articulo)

@receiver(post_save, sender=Detalle_ventas)
def verificar_stock_compra(sender, instance, **kwargs):
    """ Enviar notificación cuando se registra una venta """
    articulo = instance.codigoarticulo
    enviar_notificacion_stock(articulo)