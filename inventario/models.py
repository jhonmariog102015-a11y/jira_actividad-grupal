"""
Modelos de Base de Datos para el Módulo de Inventario.
Define las entidades Categoria y Producto con relaciones relacionales y metadatos.
"""

from django.db import models

class Categoria(models.Model):
    """Entidad Categoria para agrupar productos en el inventario."""
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de Categoría")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    """Entidad Producto con precio, existencias y relación foránea con Categoria."""
    nombre = models.CharField(max_length=150, verbose_name="Nombre del Producto")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Unitario")
    stock = models.IntegerField(default=0, verbose_name="Stock Disponible")
    
    # Llave Foránea: Un producto pertenece a una única categoría
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='productos',
        verbose_name="Categoría"
    )
    
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-fecha_registro']

    def __str__(self):
        return f"{self.nombre} - Stock: {self.stock}"
