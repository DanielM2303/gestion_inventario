from django.db import models
from apps.categorias.models import Categoriaarticulos

# Clase Graba Iva
class Givas(models.Model):
    # Atributos
    idgiva = models.AutoField(primary_key=True)
    descripcion_giva = models.CharField(max_length=30, verbose_name="Descripción")
    valoriva = models.IntegerField(verbose_name="Valor Iva")

    # Representación del objeto
    def __str__(self):
        return self.descripcion_giva

    # Opciones adicionales
    class Meta:
        db_table="givas"
        verbose_name="Graba Iva"
        verbose_name_plural="Graba Ivas"

# Clase Articulos
class Articulos(models.Model):
    # Atributos
    idarticulo = models.AutoField(primary_key=True)
    codigoarticulo = models.CharField(max_length=10, unique=True, verbose_name="Código de Producto")
    idcategoriaarticulo = models.ForeignKey(Categoriaarticulos, on_delete=models.PROTECT, verbose_name="Categoría")
    idgiva = models.ForeignKey(Givas, on_delete=models.PROTECT, verbose_name="Graba Iva")
    imagen = models.ImageField(upload_to="imagenes/", null=True, blank=True, verbose_name="Imagen")
    descripcion_articulo = models.CharField(max_length=100, verbose_name="Descripción")
    tiene_fecha_caduca = models.BooleanField(default=False, verbose_name="¿Tiene fecha de caducidad?")#nuevo
    manejo_por_lotes = models.BooleanField(default=False, verbose_name="¿Se maneja por lotes?")#nuevo
    stock = models.IntegerField(default=0, verbose_name="Stock")
    stock_minimo = models.IntegerField(default=0, verbose_name="Alerta Stock Mínimo")
    stock_maximo = models.IntegerField(default=1, verbose_name="Alerta Stock Máximo")
    costo = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Costo")
    utilidad = models.IntegerField(verbose_name="Utilidad")
    precioventa = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Precio Venta")
    estado_articulo = models.IntegerField(default=1, verbose_name="Estado")

    # Representación del objeto
    def __str__(self):
        return self.descripcion_articulo
    
    # Obtener el valor del IVA
    def get_valor_iva(self):
        return self.idgiva.valoriva

    # Eliminar las imagenes del directorio
    def delete(self, using=None, keep_parents=False):
        if self.imagen:
            self.imagen.storage.delete(self.imagen.name)
        return super().delete(using, keep_parents)
    
    # Opciones adicionales
    class Meta:
        ordering = ['-estado_articulo', 'descripcion_articulo']
        db_table="articulos"
        verbose_name="Artículo"
        verbose_name_plural="Artículos"
    