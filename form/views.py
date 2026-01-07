from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from fpdf import FPDF
from .forms import IncidentFormForm
from .models import IncidentForm
# Import BASE_DIR from settings
from django.conf import settings
import os
from triatlon.commons import show_exc
from io import BytesIO
from django.http import FileResponse
from django.utils import translation, timezone
from django.utils.formats import date_format
from django.template.loader import render_to_string

LOG_FILEPATH = os.path.join(settings.BASE_DIR, "debug.log")

class PartePDF(FPDF):
    def __init__(self, data: IncidentForm):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.data = data
        self.set_auto_page_break(auto=True, margin=15)

        self.set_margins(left=15, top=15, right=15)

    def build(self):
        # Left logo and right logo
        try:
            translation.activate('es')
            # Translate date to Spanish format

            self.add_page()
            self.image(os.path.join(settings.BASE_DIR, "static", "img", "logo_left.png"), 10, 8, 33)
            self.image(os.path.join(settings.BASE_DIR, "static", "img", "logo_right.png"), 170, 8, 33)
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, "PARTE DE LESIONES", 0, 1, "C")
            self.ln(5)

            # Paragraph
            intro = """Federación Canaria de Triatlón asegurada con ASISA con el número de póliza 75233 para la cobertura del seguro deportivo, con efecto de las 00:00 horas del 1 de enero de 2026 hasta las 24:00 horas del 31 de diciembre de 2026."""
            self.set_font("Arial", "", 10)
            self.multi_cell(0, 5, intro)
            self.ln(5)

            # Subtitle: Datos del lesionado
            self.set_font("Arial", "B", 12)
            self.cell(0, 5, "Datos del lesionado", 0, 1, "L")
            self.ln(5)

            self.set_font("Arial", "", 10)
            self.set_fill_color(200, 220, 255)
            self.cell(95, 10, f"Nombre y apellidos: {self.data.first_name} {self.data.last_name}", 1, 0, "L", fill=True)
            data_birth = self.data.birth_date.strftime("%d/%m/%Y") if self.data.birth_date else ""
            self.cell(95, 10, f"DNI y fecha de nacimiento: {self.data.nif} {data_birth}", 1, 1, "L", fill=True)
            self.cell(190, 10, f"Domicilio, localidad y provincia: ", 1, 1, "L", fill=True)
            # Break line x 2
            self.ln(5)
            # subtitle: Datos del accidente
            self.set_font("Arial", "B", 12)
            self.cell(0, 5, "Datos del accidente", 0, 1 , "L")
            self.ln(5)
            # Date and time of the incident
            self.set_font("Arial", "", 10)
            self.cell(95, 10, f"Fecha y hora: {self.data.incident_date.strftime('%d/%m/%Y')} {self.data.incident_time.strftime('%H:%M')}", 1, 0, "L", fill=True)
            # Actividad deportiva, manual input
            self.cell(95, 10, f"Actividad deportiva: ", 1, 1, "L", fill=True)

            # subtitle: Descripción del accidente
            self.ln(5)
            self.set_font("Arial", "B", 12)
            self.cell(0, 5, "Descripción del accidente", 0, 1 , "L")
            self.ln(5)
            # description from data, multi cell
            self.set_font("Arial", "", 10)
            self.multi_cell(0, 5, self.data.incident_description)
            self.ln(5)
            self.multi_cell(0, 5, f"{self.data.injuries_sustained}")
            self.ln(5)

            # subtitle: Centro sanitario donde recibe la primera asistencia:
            self.set_font("Arial", "B", 12)
            self.cell(0, 5, "Centro sanitario donde recibe la primera asistencia:", 0, 1 , "L")
            # medical_center_visited from data, multi cell
            self.set_font("Arial", "", 10)
            self.multi_cell(0, 5, self.data.medical_center_visited)
            self.ln(5)
            # Two rectangles for signatures; the first one left with "Firma dle representante y sello del tomador" below, the second one right with "Firma del lesionado" below. Rectangles blues

            self.set_fill_color(200, 220, 255)
            # Left rectangle
            self.rect(15, self.get_y(), 80, 30, style="F")
            self.set_xy(15, self.get_y() + 32)
    


            # Load sello1..jpg in the left rectangle
            sello_path = os.path.join(settings.BASE_DIR, "static", "img", "sello.png")
            if os.path.exists(sello_path):
                self.image(sello_path, 55, self.get_y() - 32 + 2, 35)   
            self.set_font("Arial", "B", 10)
            self.cell(80, 10, "Firma del representante y sello del tomador", 0, 0, "C")
            
            # Right rectangle
            self.set_xy(110, self.get_y() - 32)
            self.rect(110, self.get_y(), 80, 30, style="F")
            self.set_xy(110, self.get_y() + 32)
            self.set_font("Arial", "B", 10)
            self.cell(80, 10, "Firma del lesionado", 0, 0, "C")
            self.ln(10)
            
            self.set_fill_color(200, 220, 255)
            self.rect(15, self.get_y(), 80, 15, style="F")  # horizontal line
            self.set_font("Arial", "", 10)
            self.cell(0, 10, "Nombre y apellidos:", 0, 1, "L", fill=False)
            self.ln(10)
            date_submitted = date_format(timezone.localtime(self.data.date_submitted), r"j \d\e F \d\e Y")
            
            pos_y= (0.85 * self.h - 25)
            self.set_y(pos_y)
            self.cell(0, 10, f"En                                         , a {date_submitted}", 0, 1, "L")
            self.ln(10)
            self.set_font("Arial", "", 8)
            footer_text_01 ="El firmante del presente documento se compromete a recabar el consentimiento expreso del deportista que haya sufrido las lesiones reflejadas en el presente parte, con el objeto de que sus datos se incorporen a un registro informatizado titularidad de la Federación Canaria de Triatlón e informarle que le asisten los derechos contenidos en el art. 5 de la LOPD, pudiendo ejercitarlos en cualquier momento remitiéndose al titular del fichero."

            footer_text_02 ="La presentación de este parte de lesiones es imprescindible para la correcta tramitación del expediente de accidente deportivo. La no presentación del mismo en dos días laborables podría suponer la no aceptación del mismo como tal y por lo tanto la no cobertura sanitaria por el concierto firmado entre la Federación Canaria de Triatlón y ASISA."

            self.multi_cell(0, 4, footer_text_01)
            self.ln(2)
            self.multi_cell(0, 4, footer_text_02)

            raw = self.output(dest="S")
            # fpdf2 suele devolver bytearray; otras versiones pueden devolver str
            if isinstance(raw, (bytes, bytearray)):
                return bytes(raw)

        except Exception as e:
            log2file(show_exc(e))
            raise None


    


def log2file(message, filename=LOG_FILEPATH):
    with open(filename, "a") as f:
        f.write(message + "\n")


# Create your views here.
def index(request):
    context= {}
    return render(request, "form/index.html", context=context)

def save_form(request):
    try:
        if request.method == "POST":
            data = request.POST
            form = IncidentFormForm(data)
            if form.is_valid():
                incident_form = form.save()
                if incident_form.parte_required:
                    parte_url = request.build_absolute_uri(reverse("form:download-pdf", args=[incident_form.uuid]))

                if incident_form.talon_required:
                    talon_url = request.build_absolute_uri(reverse("form:download-talon", args=[incident_form.uuid]))

                email_html = render_to_string("form/email-template.html", {
                    "data": incident_form,
                    "parte_url": parte_url if incident_form.parte_required else None,
                    "talon_url": talon_url if incident_form.talon_required else None,
                })
                # Send confirmation email
                from django.core.mail import EmailMultiAlternatives
                subject = "Confirmación de recepción de formulario de accidente."
                from_email = settings.EMAIL_FROM_DEFAULT
                to_email = [incident_form.email, 'web@dsegur.com']
                email = EmailMultiAlternatives(subject, "", from_email, to_email)
                email.attach_alternative(email_html, "text/html")
                email.send()
  
                return JsonResponse({"status": "success", "message": "Form saved successfully.", "id": incident_form.id})
            else:
                log2file(f"Form errors: {form.errors.as_json()}")
                html = form.errors.as_ul()
                return JsonResponse({"status": "error", "errors": form.errors, "html": html}, status=400)
        else:
            return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)
    except Exception as e:
        log2file(show_exc(e))
        return JsonResponse({"status": "error", "message": "An error occurred while saving the form."}, status=500)

def generate_pdf(request, uuid):
    try:
        if request.method == "GET":
            form_uuid = uuid
            incident_form = IncidentForm.objects.get(uuid=form_uuid)
            pdf_parte = PartePDF(incident_form)
            pdf_content = pdf_parte.build()
            response = HttpResponse(pdf_content, content_type="application/pdf")
            # Open in line in browser
            response["Content-Disposition"] = f'inline; filename="parte_incidente_{form_uuid}.pdf"'
            return response

            # bio = BytesIO(pdf_content)
            # bio.seek(0)
            # response = FileResponse(bio, as_attachment=True, filename=f"parte_incidente_{form_uuid}.pdf", content_type="application/pdf")
            # return response
        else:
            return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)
    except Exception as e:
        log2file(show_exc(e))
        return JsonResponse({"status": "error", "message": "An error occurred while generating the PDF."}, status=500)

def download_talon(request, uuid):
    try:
        if request.method == "GET":
            form_uuid = uuid
            incident_form = IncidentForm.objects.get(uuid=form_uuid)
            # For now, just return a placeholder response
            return JsonResponse({"status": "success", "message": "Talon download not implemented yet."})
        else:
            return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)
    except Exception as e:
        log2file(show_exc(e))
        return JsonResponse({"status": "error", "message": "An error occurred while downloading the talon."}, status=500)
