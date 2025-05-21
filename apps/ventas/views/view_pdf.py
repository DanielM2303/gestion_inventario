from django.contrib.auth.decorators import login_required, permission_required
from apps.ventas.models import Ventas, Detalle_ventas, Pagos
from apps.empresa.models import Empresas
from django.db.models import Sum
from django.http import HttpResponse
from weasyprint import HTML
from io import BytesIO
from django.template.loader import get_template
from django.views import View
from django.utils.decorators import method_decorator
import os
from django.conf import settings

# Vista Factura
@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('ventas.ver_ventas', raise_exception=True), name='dispatch')
class FacturaPDFView(View):
    def get(self, request, pk_id):
        # Obtener datos
        venta = Ventas.objects.get(idventa=pk_id)
        pago = Pagos.objects.get(idventa=pk_id)
        venta_detalles = Detalle_ventas.objects.filter(idventa=pk_id)
        total_cantidad = Detalle_ventas.objects.filter(idventa=pk_id).aggregate(total_cantidad=Sum('cantidad'))['total_cantidad']
        empresa = Empresas.objects.get(idempresa=100)
        logo_url = request.build_absolute_uri(empresa.logo.url) if empresa.logo else None # uso al no estar desplegado
        #logo_url = f"file://{os.path.join(settings.MEDIA_ROOT, empresa.logo.name)}" if empresa.logo else None # uso al estar desplegado

        # Renderizar la plantilla y generar el PDF
        template_path = 'pdf/factura_template.html'
        template = get_template(template_path)
        html = template.render({ 'empresa': empresa, 'venta': venta, 'venta_detalles': venta_detalles,
            'total_cantidad': total_cantidad, 'pago': pago, 'cambio': pago.monto-venta.total, 'logo_url': logo_url})
        
        # Crear el PDF
        result = BytesIO()
        HTML(string=html, base_url=request.build_absolute_uri('/')).write_pdf(result)
        
        # Retornar el PDF
        filename = f"factura_{pk_id}.pdf"
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'filename="{filename}"'
        return response
