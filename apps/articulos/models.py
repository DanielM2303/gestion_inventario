from django.db import models
from apps.categorias.models import Categoriaarticulos

# Clase Graba Iva
class Givas(models.Model):
    idgiva = models.AutoField(primary_key=True)
    descripcion_giva = models.CharField(max_length=30, verbose_name="Descripción")
    valoriva = models.IntegerField(verbose_name="Valor Iva")

    def __str__(self):
        return self.descripcion_giva

    class Meta:
        db_table="givas"
        verbose_name="Graba Iva"
        verbose_name_plural="Graba Ivas"

# Clase Tipo Articulos
class TipoArticulos(models.Model):
    idtipoarticulo = models.AutoField(primary_key=True)
    descripcion_tipo = models.CharField(max_length=50, verbose_name="Descripción")

    def __str__(self):
        return self.descripcion_tipo

    class Meta:
        db_table="tipos_articulos"
        verbose_name="Tipo Artículo"
        verbose_name_plural="Tipos Artículos"

# Clase Niveles de Grasa
class NivelesGrasa(models.Model):
    idnivelgrasa = models.AutoField(primary_key=True)
    descripcion_ngrasa = models.CharField(max_length=50, verbose_name="Descripción")
    valor_nivel = models.IntegerField(verbose_name="Valor")

    def __str__(self):
        return self.descripcion_ngrasa

    class Meta:
        db_table="niveles_grasa"
        verbose_name="Nivel de Grasa"
        verbose_name_plural="Niveles de Grasa"

# Clase Niveles de Azucar
class NivelesAzucar(models.Model):
    idnivelazucar = models.AutoField(primary_key=True)
    descripcion_nazucar = models.CharField(max_length=50, verbose_name="Descripción")
    valor_nivel = models.IntegerField(verbose_name="Valor")

    def __str__(self):
        return self.descripcion_nazucar

    class Meta:
        db_table="niveles_azucar"
        verbose_name="Nivel de Azúcar"
        verbose_name_plural="Niveles de Azúcar"

# Clase Niveles de Sal
class NivelesSal(models.Model):
    idnivelsal = models.AutoField(primary_key=True)
    descripcion_nsal = models.CharField(max_length=50, verbose_name="Descripción")
    valor_nivel = models.IntegerField(verbose_name="Valor")

    def __str__(self):
        return self.descripcion_nsal

    class Meta:
        db_table="niveles_sal"
        verbose_name="Nivel de Sal"
        verbose_name_plural="Niveles de Sal"

# Clase Articulos
class Articulos(models.Model):
    idarticulo = models.AutoField(primary_key=True)
    codigoarticulo = models.CharField(max_length=10, unique=True, verbose_name="Código de Producto")
    idcategoriaarticulo = models.ForeignKey(Categoriaarticulos, on_delete=models.PROTECT, verbose_name="Categoría")
    idgiva = models.ForeignKey(Givas, on_delete=models.PROTECT, verbose_name="Graba Iva")
    idtipoarticulo = models.ForeignKey(TipoArticulos, on_delete=models.PROTECT, verbose_name="Tipo Producto")
    idnivelgrasa = models.ForeignKey(NivelesGrasa, on_delete=models.PROTECT, verbose_name="Nivel de Grasa", null=True, blank=True)
    idnivelazucar = models.ForeignKey(NivelesAzucar, on_delete=models.PROTECT, verbose_name="Nivel de Azúcar", null=True, blank=True)
    idnivelsal = models.ForeignKey(NivelesSal, on_delete=models.PROTECT, verbose_name="Nivel de Sal", null=True, blank=True)
    imagen = models.ImageField(upload_to="imagenes/", null=True, blank=True, verbose_name="Imagen")
    descripcion_articulo = models.CharField(max_length=100, verbose_name="Descripción")
    tiene_semaforo = models.BooleanField(default=False, verbose_name="¿Tiene semáforo?")
    tiene_fecha_caduca = models.BooleanField(default=False, verbose_name="¿Tiene fecha de caducidad?")
    manejo_por_lotes = models.BooleanField(default=False, verbose_name="¿Se maneja por lotes?")
    stock = models.IntegerField(default=0, verbose_name="Stock")
    stock_minimo = models.IntegerField(default=0, verbose_name="Alerta Stock Mínimo")
    stock_maximo = models.IntegerField(default=1, verbose_name="Alerta Stock Máximo")
    costo = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Costo")
    utilidad = models.IntegerField(verbose_name="Utilidad")
    precioventa = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Precio Venta")
    estado_articulo = models.IntegerField(default=1, verbose_name="Estado")

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
    