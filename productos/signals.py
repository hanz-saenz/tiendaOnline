from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Producto

@receiver([post_save, post_delete], sender=Producto)
def actualizar_cache_prouctos(sender, instance, **kwargs):

    total_producto = Producto.objects.filter(activo=True).count()
    produtos_por_pagina = 3

    total_paginas = (total_producto + produtos_por_pagina - 1) // (1 if total_producto % produtos_por_pagina else 0)

    if kwargs.get('created', False):
        total_paginas += 1
    
    for page in range(1, total_paginas + 1):
        cache_key = f"productos_{page}"
        cache.delete(cache_key)
        # cache.set('productos_{page}', total_producto, 60 * 1)
