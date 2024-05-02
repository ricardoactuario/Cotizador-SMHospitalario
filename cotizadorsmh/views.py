from django.shortcuts import render
from .forms import C_Intermediario2, form_CotizadorTAR, form_Conyuge
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime
import locale
import os
from .models import TR3
from decimal import Decimal
import base64
from django.core.mail import EmailMessage
from django.conf import settings
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from django.http import HttpResponse
# Create your views here.

def CotizadorSMH(request):
    if request.method == 'GET':
        return render(request, 'S_SMH.html', {
        'form_intermediario2': C_Intermediario2(),
        'form_CotizadorTAR': form_CotizadorTAR(),
        'form_Conyuge': form_Conyuge(),
        })
    else:
        buffer = BytesIO()
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        # Crear un objeto PDF
        pdf = canvas.Canvas(buffer)
        #Estilo de Letra
        pdf.setFont("Helvetica", 9)
        #Trabajo con Variables
        Nom = request.POST.get('Nombre', None)
        In = request.POST.get('Int', None)
        Te = request.POST.get('Tel', None)
        Cor = request.POST.get('Correo', None)
        Identificacion = request.POST.get('Id', None)
        Solicitante = request.POST.get('Sol', None)
        Nacimiento = request.POST.get('Nac', None)
        Suma = request.POST.get('Sum', 0)
        Gene = request.POST.get('Gen', None)
        Temporal = request.POST.get('Temp', None)
        Mails = request.POST.get('Mail', None)
        Cellphones = request.POST.get('Cellphone', None)
        hij = request.POST.get('hijos', None)
        Solic2 = request.POST.get('Sol2', None)
        Naci2 = request.POST.get('Nac2', None)

        fecha_actual = datetime.now().strftime("%d de %B de %Y")
        image_path = os.path.join('cotizadorsmh', 'static', 'atlanv.png')

        # Agregando contenido al PDF
        pdf.drawString(460, 805, fecha_actual)
            
        pdf.drawImage(image_path, x=50, y=750, width=100, height=40)
            
        pdf.setFont("Helvetica-Bold", 9)
            
        pdf.drawString(240, 765, "OFERTA DE SEGURO INDIVIDUAL DE GASTOS MÉDICOS")

        pdf.setFont("Helvetica", 9)

        if Gene == 'Hombre':
            Est = 'Estimado'
            Sñ = 'Señor'
        else:
            Est = 'Estimada'
            Sñ = 'Señorita'

        pdf.drawString(40, 730, str(Est) + " " + str(Sñ) + ": " + str(Solicitante))
        pdf.drawString(40, 717, "Sometemos a su consideración la cotización del Seguro de Gastos Médicos, de conformidad con el siguiente detalle:")
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(40, 691, 515, 16, fill=True, stroke=False)
        pdf.rect(40, 675, 58, 16, fill=True, stroke=False)
        pdf.rect(40, 659, 58, 16, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)

        pdf.setFont("Helvetica-Bold", 9)

        #PRIMER CUADRO DE DATOS        
        pdf.drawString(130, 694, "NOMBRE COMPLETO")
        pdf.setFont("Helvetica", 9)
        ancho_texto1 = pdf.stringWidth(Solicitante, "Helvetica", 9)
        x_centro1 = 98 + (155 - ancho_texto1)/2
        pdf.drawString(x_centro1, 678, Solicitante)
        pdf.rect(98, 677, 155, 16, fill=False, stroke=False)
        pdf.rect(98, 661, 155, 16, fill=False, stroke=False)
        ancho_txt1 = pdf.stringWidth(Solic2, "Helvetica", 9)
        x_center1 = 98 +(155 - ancho_txt1)/2
        if Solic2 == "" or Naci2 == "":
            pdf.drawString(x_center1, 662, "")
        else:
            pdf.drawString(x_center1, 662, Solic2)

        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(260, 694, "FECHA DE NACIMIENTO")
        pdf.setFont("Helvetica", 9)
        ancho_texto2 = pdf.stringWidth(Nacimiento, "Helvetica", 9)
        x_centro2 = 252 + (125 - ancho_texto2)/2
        pdf.drawString(x_centro2, 678, Nacimiento)
        pdf.rect(252, 677, 125, 16, fill=False, stroke=False)
        pdf.rect(252, 661, 125, 16, fill=False, stroke=False)
        if Solic2 == "" or Naci2 == "":
            pdf.drawString(x_centro2, 662, "")    
        else:
            pdf.drawString(x_centro2, 662, Naci2)

        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(390, 694, "EDAD")
        
        fecha_nacimiento = datetime.strptime(Nacimiento, "%Y/%m/%d")
        fechaActual = datetime.now()
        edad = fechaActual.year - fecha_nacimiento.year - ((fechaActual.month, fechaActual.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
        pdf.setFont("Helvetica", 9)
        ancho_texto3 = pdf.stringWidth(str(edad), "Helvetica", 9)
        x_centro3 = 376 + (55 - ancho_texto3)/2
        pdf.drawString(x_centro3, 678, str(edad))
        pdf.rect(376, 677, 55, 16, fill=False, stroke=False)
        pdf.rect(376, 661, 55, 16, fill=False, stroke=False)

        if Naci2 == "" or Solic2 == "":
            pdf.drawString(x_centro3, 662, "")
            edad2 = 0
        else:
            fecha_nacimiento = datetime.strptime(Naci2, "%Y/%m/%d")
            fechaActual = datetime.now()
            edad2 = fechaActual.year - fecha_nacimiento.year - ((fechaActual.month, fechaActual.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
            pdf.drawString(x_centro3, 662, str(edad2))

        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(450, 694, "SEXO")
        ancho_texto4 = pdf.stringWidth(Gene, "Helvetica", 9)
        x_centro4 = 430 + (63 - ancho_texto4)/2
        pdf.setFont("Helvetica", 9)
        pdf.drawString(x_centro4, 678, Gene)
        pdf.rect(430, 677, 63, 16, fill=False, stroke=False)
        pdf.rect(430, 661, 63, 16, fill=False, stroke=False)
        if Solic2 == "" or Naci2 == "":
            Gene2 = ""
        elif Gene == "Hombre":
            Gene2 = "Mujer"
        elif Gene == "Mujer": 
            Gene2 = "Hombre"
        else:
            Gene2 = ""
        ancho_txt4 = pdf.stringWidth(Gene2, "Helvetica", 9)
        x_center4 = 430 + (63 -ancho_txt4)/2 
        pdf.drawString(x_center4, 662, Gene2)

        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(505, 694, "N° HIJOS")
        ancho_texto5 = pdf.stringWidth(hij, "Helvetica", 9)
        x_centro5 = 492 + (63 - ancho_texto5)/2
        pdf.setFont("Helvetica", 9)
        pdf.drawString(x_centro5, 678, hij)
        pdf.rect(492, 677, 63, 16, fill=False, stroke=False)
        pdf.rect(492, 661, 63, 16, fill=False, stroke=False)
        pdf.drawString(45, 677, "TITULAR:")
        pdf.drawString(45, 664, "CÓNYUGE:")

        #SEGUNDO. CUADRO DE BENEFICIOS

        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(40, 640, 515, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(240, 642, "CUADRO DE BENEFICIOS")
        pdf.setFont("Helvetica", 9)

        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(40, 627, 515, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(45, 630, "BENEFICIOS")

        #PLANES
        if Suma == "$50,000":
            SumaP = 50000
        elif Suma == "$100,000":
            SumaP = 100000
        elif Suma == "$250,000":
            SumaP = 250000
        elif Suma == "$500,000":
            SumaP = 500000
        elif Suma == "$1,000,000":
            SumaP = 1000000

        if SumaP < 250000:
            Plan1 = ""
            Plan2 = "PLAN A"
            Plan3 = "PLAN B"
        else:
            Plan1 = "PLAN A"
            Plan2 = "PLAN B"
            Plan3 = "PLAN C"
        
        pdf.drawString(320, 630, Plan1)
        pdf.drawString(405, 630, Plan2)
        pdf.drawString(490, 630, Plan3)
        #BENEFICIOS-TEXTOS
        pdf.setFont("Helvetica", 9)
        pdf.drawString(45, 617, "Máximo Vitalicio")
        if SumaP < 250000:
            Max1 = ""
            Max2 = "$50,000.00"
            Max3 = "$100,000.00"
        else:
            Max1 = "$250,000.00"
            Max2 = "$500,000.00"
            Max3 = "$1,000,000.00"
        
        pdf.rect(297, 614, 80, 12, fill=False, stroke=False)
        pdf.rect(382, 614, 80, 12, fill=False, stroke=False)
        pdf.rect(467, 614, 80, 12, fill=False, stroke=False)
        ancho_texto6 = pdf.stringWidth(Max1, "Helvetica", 9)
        x_centro6 = 297 + (80 - ancho_texto6)/2
        pdf.drawString(x_centro6, 616, Max1)
        ancho_texto7 = pdf.stringWidth(Max2, "Helvetica", 9)
        x_centro7 = 382 + (80 - ancho_texto7)/2
        pdf.drawString(x_centro7, 616, Max2)
        ancho_texto8 = pdf.stringWidth(Max3, "Helvetica", 9)
        x_centro8 = 467 + (80 - ancho_texto8)/2
        pdf.drawString(x_centro8, 616, Max3)
        
        pdf.drawString(45, 604, "Ámbito de la cobertura")

        if SumaP < 250000:
            Amb1 = ""
            Amb2 = "CA"
            Amb3 = "CA"
        else:
            Amb1 = "MUNDIAL"
            Amb2 = "MUNDIAL"
            Amb3 = "MUNDIAL"
        
        pdf.rect(297, 601, 80, 12, fill=False, stroke=False)
        pdf.rect(382, 601, 80, 12, fill=False, stroke=False)
        pdf.rect(467, 601, 80, 12, fill=False, stroke=False)
        ancho_texto9 = pdf.stringWidth(Amb1, "Helvetica", 9)
        x_centro9 = 297 + (80 - ancho_texto9)/2
        pdf.drawString(x_centro9, 603, Amb1)
        ancho_texto10 = pdf.stringWidth(Amb2, "Helvetica", 9)
        x_centro10 = 382 + (80 - ancho_texto10)/2
        pdf.drawString(x_centro10, 603, Amb2)
        ancho_texto11 = pdf.stringWidth(Amb3, "Helvetica", 9)
        x_centro11 = 467 + (80 - ancho_texto11)/2
        pdf.drawString(x_centro11, 603, Amb3)

        pdf.drawString(45, 591, "Deducible en C.A. (Año póliza)")

        if SumaP < 250000:
            DedC1 = ""
            DedC2 = "$100.00"
            DedC3 = "$100.00"
        else:
            DedC1 = "$125.00"
            DedC2 = "$150.00"
            DedC3 = "$150.00"
        
        pdf.rect(297, 585, 80, 12, fill=False, stroke=False)
        pdf.rect(382, 585, 80, 12, fill=False, stroke=False)
        pdf.rect(467, 585, 80, 12, fill=False, stroke=False)
        ancho_texto12 = pdf.stringWidth(DedC1, "Helvetica", 9)
        x_centro12 = 297 + (80 - ancho_texto12)/2
        pdf.drawString(x_centro12, 587, DedC1)
        ancho_texto13 = pdf.stringWidth(DedC2, "Helvetica", 9)
        x_centro13 = 382 + (80 - ancho_texto13)/2
        pdf.drawString(x_centro13, 587, DedC2)
        ancho_texto14 = pdf.stringWidth(DedC3, "Helvetica", 9)
        x_centro14 = 467 + (80 - ancho_texto14)/2
        pdf.drawString(x_centro14, 587, DedC3)

        pdf.setFont("Helvetica", 7)
        pdf.drawString(45, 583, "(Sin deducible al usar proveedor de Red)")

        pdf.setFont("Helvetica", 9)
        pdf.drawString(45, 573, "Deducible Familiar")
        if SumaP < 250000:
            DedF1 = ""
            DedF2 = "$300.00"
            DedF3 = "$300.00"
        else:
            DedF1 = "$375.00"
            DedF2 = "$450.00"
            DedF3 = "$450.00"
        
        pdf.rect(297, 570, 80, 12, fill=False, stroke=False)
        pdf.rect(382, 570, 80, 12, fill=False, stroke=False)
        pdf.rect(467, 570, 80, 12, fill=False, stroke=False)
        ancho_texto15 = pdf.stringWidth(DedF1, "Helvetica", 9)
        x_centro15 = 297 + (80 - ancho_texto15)/2
        pdf.drawString(x_centro15, 572, DedF1)
        ancho_texto16 = pdf.stringWidth(DedF2, "Helvetica", 9)
        x_centro16 = 382 + (80 - ancho_texto16)/2
        pdf.drawString(x_centro16, 572, DedF2)
        ancho_texto17 = pdf.stringWidth(DedF3, "Helvetica", 9)
        x_centro17 = 467 + (80 - ancho_texto17)/2
        pdf.drawString(x_centro17, 572, DedF3)
        
        pdf.drawString(45, 560, "Reembolso en C.A.")
        if SumaP < 250000:
            Reem1 = ""
            Reem2 = "80%"
            Reem3 = "80%"
        else:
            Reem1 = "80%"
            Reem2 = "80%"
            Reem3 = "80%"
        
        pdf.rect(297, 558, 80, 12, fill=False, stroke=False)
        pdf.rect(382, 558, 80, 12, fill=False, stroke=False)
        pdf.rect(467, 558, 80, 12, fill=False, stroke=False)
        ancho_texto18 = pdf.stringWidth(Reem1, "Helvetica", 9)
        x_centro18 = 297 + (80 - ancho_texto18)/2
        pdf.drawString(x_centro18, 560, Reem1)
        ancho_texto19 = pdf.stringWidth(Reem2, "Helvetica", 9)
        x_centro19 = 382 + (80 - ancho_texto19)/2
        pdf.drawString(x_centro19, 560, Reem2)
        ancho_texto20 = pdf.stringWidth(Reem3, "Helvetica", 9)
        x_centro20 = 467 + (80 - ancho_texto20)/2
        pdf.drawString(x_centro20, 560, Reem3)
        pdf.drawString(45, 547, "Límite de coaseguro en C.A. (Año póliza)")
        if SumaP < 250000:
            Lim1 = ""
            Lim2 = "$3,000.00"
            Lim3 = "$3,000.00"
        else:
            Lim1 = "$3,000.00"
            Lim2 = "$3,000.00"
            Lim3 = "$3,000.00"
        
        pdf.rect(297, 545, 80, 12, fill=False, stroke=False)
        pdf.rect(382, 545, 80, 12, fill=False, stroke=False)
        pdf.rect(467, 545, 80, 12, fill=False, stroke=False)
        ancho_texto21 = pdf.stringWidth(Lim1, "Helvetica", 9)
        x_centro21 = 297 + (80 - ancho_texto21)/2
        pdf.drawString(x_centro21, 547, Lim1)
        ancho_texto22 = pdf.stringWidth(Lim2, "Helvetica", 9)
        x_centro22 = 382 + (80 - ancho_texto22)/2
        pdf.drawString(x_centro22, 547, Lim2)
        ancho_texto23 = pdf.stringWidth(Lim3, "Helvetica", 9)
        x_centro23 = 467 + (80 - ancho_texto23)/2
        pdf.drawString(x_centro23, 547, Lim3)
        pdf.drawString(45, 534, "Cuarto y alimento diario en C.A.")
        if SumaP < 250000:
            Cua1 = ""
            Cua2 = "$60.00"
            Cua3 = "$60.00"
        else:
            Cua1 = "$60.00"
            Cua2 = "$60.00"
            Cua3 = "$60.00"
        
        pdf.rect(297, 532, 80, 12, fill=False, stroke=False)
        pdf.rect(382, 532, 80, 12, fill=False, stroke=False)
        pdf.rect(467, 532, 80, 12, fill=False, stroke=False)
        ancho_texto24 = pdf.stringWidth(Cua1, "Helvetica", 9)
        x_centro24 = 297 + (80 - ancho_texto24)/2
        pdf.drawString(x_centro24, 534, Cua1)
        ancho_texto25 = pdf.stringWidth(Cua2, "Helvetica", 9)
        x_centro25 = 382 + (80 - ancho_texto25)/2
        pdf.drawString(x_centro25, 534, Cua2)
        ancho_texto26 = pdf.stringWidth(Cua3, "Helvetica", 9)
        x_centro26 = 467 + (80 - ancho_texto26)/2
        pdf.drawString(x_centro26, 534, Cua3)
        pdf.drawString(45, 521, "Maternidad en C.A. (Período de espera 10 meses)")
        if SumaP < 250000:
            Ma1 = ""
            Ma2 = "CCOI"
            Ma3 = "CCOI"
        else:
            Ma1 = "CCOI"
            Ma2 = "CCOI"
            Ma3 = "CCOI"
        
        pdf.rect(297, 519, 80, 12, fill=False, stroke=False)
        pdf.rect(382, 519, 80, 12, fill=False, stroke=False)
        pdf.rect(467, 519, 80, 12, fill=False, stroke=False)
        ancho_texto27 = pdf.stringWidth(Ma1, "Helvetica", 9)
        x_centro27 = 297 + (80 - ancho_texto27)/2
        pdf.drawString(x_centro27, 521, Ma1)
        ancho_texto28 = pdf.stringWidth(Ma2, "Helvetica", 9)
        x_centro28 = 382 + (80 - ancho_texto28)/2
        pdf.drawString(x_centro28, 521, Ma2)
        ancho_texto29 = pdf.stringWidth(Ma3, "Helvetica", 9)
        x_centro29 = 467 + (80 - ancho_texto29)/2
        pdf.drawString(x_centro29, 521, Ma3)
        pdf.drawString(45, 508, "Niño sano y vacunación hasta los 10 años (Año póliza)")
        if SumaP < 250000:
            Ni1 = ""
            Ni2 = "$300.00"
            Ni3 = "$300.00"
        else:
            Ni1 = "$500.00"
            Ni2 = "$500.00"
            Ni3 = "$500.00"
        
        pdf.rect(297, 506, 80, 12, fill=False, stroke=False)
        pdf.rect(382, 506, 80, 12, fill=False, stroke=False)
        pdf.rect(467, 506, 80, 12, fill=False, stroke=False)
        ancho_texto30 = pdf.stringWidth(Ni1, "Helvetica", 9)
        x_centro30 = 297 + (80 - ancho_texto30)/2
        pdf.drawString(x_centro30, 508, Ni1)
        ancho_texto31 = pdf.stringWidth(Ni2, "Helvetica", 9)
        x_centro31 = 382 + (80 - ancho_texto31)/2
        pdf.drawString(x_centro31, 508, Ni2)
        ancho_texto32 = pdf.stringWidth(Ni3, "Helvetica", 9)
        x_centro32 = 467 + (80 - ancho_texto32)/2
        pdf.drawString(x_centro32, 508, Ni3)
        pdf.drawString(45, 494, "Deducible fuera de C.A. (Año póliza)")
        if SumaP < 250000:
            De1 = ""
            De2 = "N/A"
            De3 = "N/A"
        else:
            De1 = "$2,000.00"
            De2 = "$2,000.00"
            De3 = "$2,000.00"
        
        pdf.rect(297, 490, 80, 12, fill=False, stroke=False)
        pdf.rect(382, 490, 80, 12, fill=False, stroke=False)
        pdf.rect(467, 490, 80, 12, fill=False, stroke=False)
        ancho_texto33 = pdf.stringWidth(De1, "Helvetica", 9)
        x_centro33 = 297 + (80 - ancho_texto33)/2
        pdf.drawString(x_centro33, 492, De1)
        ancho_texto34 = pdf.stringWidth(De2, "Helvetica", 9)
        x_centro34 = 382 + (80 - ancho_texto34)/2
        pdf.drawString(x_centro34, 492, De2)
        ancho_texto35 = pdf.stringWidth(De3, "Helvetica", 9)
        x_centro35 = 467 + (80 - ancho_texto35)/2
        pdf.drawString(x_centro35, 492, De3)
        pdf.drawString(45, 481, "Deducible familiar")
        if SumaP < 250000:
            DeF1 = ""
            DeF2 = "N/A"
            DeF3 = "N/A"
        else:
            DeF1 = "$6,000.00"
            DeF2 = "$6,000.00"
            DeF3 = "$6,000.00"
        
        pdf.rect(297, 477, 80, 12, fill=False, stroke=False)
        pdf.rect(382, 477, 80, 12, fill=False, stroke=False)
        pdf.rect(467, 477, 80, 12, fill=False, stroke=False)
        ancho_texto36 = pdf.stringWidth(DeF1, "Helvetica", 9)
        x_centro36 = 297 + (80 - ancho_texto36)/2
        pdf.drawString(x_centro33, 479, DeF1)
        ancho_texto37 = pdf.stringWidth(DeF2, "Helvetica", 9)
        x_centro37 = 382 + (80 - ancho_texto37)/2
        pdf.drawString(x_centro37, 479, DeF2)
        ancho_texto38 = pdf.stringWidth(DeF3, "Helvetica", 9)
        x_centro38 = 467 + (80 - ancho_texto38)/2
        pdf.drawString(x_centro38, 479, DeF3)
        pdf.drawString(45, 468, "Reembolso fuera de C.A. (Dentro de red)")
        if SumaP < 250000:
            Reemb1 = ""
            Reemb2 = "N/A"
            Reemb3 = "N/A"
        else:
            Reemb1 = "75%"
            Reemb2 = "75%"
            Reemb3 = "75%"
        
        pdf.rect(297, 464, 80, 12, fill=False, stroke=False)
        pdf.rect(382, 464, 80, 12, fill=False, stroke=False)
        pdf.rect(467, 464, 80, 12, fill=False, stroke=False)
        ancho_texto39 = pdf.stringWidth(Reemb1, "Helvetica", 9)
        x_centro39 = 297 + (80 - ancho_texto39)/2
        pdf.drawString(x_centro39, 466, Reemb1)
        ancho_texto40 = pdf.stringWidth(Reemb2, "Helvetica", 9)
        x_centro40 = 382 + (80 - ancho_texto40)/2
        pdf.drawString(x_centro40, 466, Reemb2)
        ancho_texto41 = pdf.stringWidth(Reemb3, "Helvetica", 9)
        x_centro41 = 467 + (80 - ancho_texto41)/2
        pdf.drawString(x_centro41, 466, Reemb3)
        pdf.drawString(45, 455, "Reembolso fuera de C.A. (Fuera de red)")
        if SumaP < 250000:
            Reembo1 = ""
            Reembo2 = "N/A"
            Reembo3 = "N/A"
        else:
            Reembo1 = "65%"
            Reembo2 = "65%"
            Reembo3 = "65%"
        
        pdf.rect(297, 451, 80, 12, fill=False, stroke=False)
        pdf.rect(382, 451, 80, 12, fill=False, stroke=False)
        pdf.rect(467, 451, 80, 12, fill=False, stroke=False)
        ancho_texto39 = pdf.stringWidth(Reembo1, "Helvetica", 9)
        x_centro39 = 297 + (80 - ancho_texto39)/2
        pdf.drawString(x_centro39, 453, Reembo1)
        ancho_texto40 = pdf.stringWidth(Reembo2, "Helvetica", 9)
        x_centro40 = 382 + (80 - ancho_texto40)/2
        pdf.drawString(x_centro40, 453, Reembo2)
        ancho_text41 = pdf.stringWidth(Reembo3, "Helvetica", 9)
        x_centro41 = 467 + (80 - ancho_text41)/2
        pdf.drawString(x_centro41, 453, Reembo3)
        pdf.drawString(45, 442, "Límite de Coaseguro fuera de C.A. (Año póliza)")
        if SumaP < 250000:
            Co1 = ""
            Co2 = "N/A"
            Co3 = "N/A"
        else:
            Co1 = "$15,000.00"
            Co2 = "$15,000.00"
            Co3 = "$15,000.00"
        
        pdf.rect(297, 438, 80, 12, fill=False, stroke=False)
        pdf.rect(382, 438, 80, 12, fill=False, stroke=False)
        pdf.rect(467, 438, 80, 12, fill=False, stroke=False)
        ancho_texto42 = pdf.stringWidth(Co1, "Helvetica", 9)
        x_centro42 = 297 + (80 - ancho_texto42)/2
        pdf.drawString(x_centro42, 440, Co1)
        ancho_texto43 = pdf.stringWidth(Co2, "Helvetica", 9)
        x_centro43 = 382 + (80 - ancho_texto43)/2
        pdf.drawString(x_centro43, 440, Co2)
        ancho_text44 = pdf.stringWidth(Co3, "Helvetica", 9)
        x_centro44 = 467 + (80 - ancho_text44)/2
        pdf.drawString(x_centro44, 440, Co3)
        pdf.drawString(45, 429, "Cuarto y alimento diario fuera de C.A.")
        if SumaP < 250000:
            Al1 = ""
            Al2 = "N/A"
            Al3 = "N/A"
        else:
            Al1 = "$400.00"
            Al2 = "$400.00"
            Al3 = "$400.00"
        
        pdf.rect(297, 425, 80, 12, fill=False, stroke=False)
        pdf.rect(382, 425, 80, 12, fill=False, stroke=False)
        pdf.rect(467, 425, 80, 12, fill=False, stroke=False)
        ancho_texto45 = pdf.stringWidth(Al1, "Helvetica", 9)
        x_centro45 = 297 + (80 - ancho_texto45)/2
        pdf.drawString(x_centro45, 427, Al1)
        ancho_texto46 = pdf.stringWidth(Al2, "Helvetica", 9)
        x_centro46 = 382 + (80 - ancho_texto46)/2
        pdf.drawString(x_centro46, 427, Al2)
        ancho_text47 = pdf.stringWidth(Al3, "Helvetica", 9)
        x_centro47 = 467 + (80 - ancho_text47)/2
        pdf.drawString(x_centro47, 427, Al3)
        pdf.drawString(45, 416, "Maternidad fuera de C.A. (por evento, p.e. 10 meses)")
        if SumaP < 250000:
            Mater1 = ""
            Mater2 = "N/A"
            Mater3 = "N/A"
        else:
            Mater1 = "$3,000.00"
            Mater2 = "$3,000.00"
            Mater3 = "$3,000.00"
        
        pdf.rect(297, 412, 80, 12, fill=False, stroke=False)
        pdf.rect(382, 412, 80, 12, fill=False, stroke=False)
        pdf.rect(467, 412, 80, 12, fill=False, stroke=False)
        ancho_texto48 = pdf.stringWidth(Mater1, "Helvetica", 9)
        x_centro48 = 297 + (80 - ancho_texto48)/2
        pdf.drawString(x_centro48, 414, Mater1)
        ancho_texto49 = pdf.stringWidth(Mater2, "Helvetica", 9)
        x_centro49 = 382 + (80 - ancho_texto49)/2
        pdf.drawString(x_centro49, 414, Mater2)
        ancho_text50 = pdf.stringWidth(Mater3, "Helvetica", 9)
        x_centro50 = 467 + (80 - ancho_text50)/2
        pdf.drawString(x_centro50, 414, Mater3)
        #OTRAS COBERTURAS Y TEXTOS
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(40, 399, 515, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(260, 402, "OTRAS COBERTURAS")
        pdf.setFont("Helvetica", 9)
        pdf.drawString(45, 389, "Trasplante de órganos (máximo vitalicio)")
        if SumaP < 250000:
            Tras1 = ""
            Tras2 = "$25,000.00"
            Tras3 = "$50,000.00"
        else:
            Tras1 = "$100,000.00"
            Tras2 = "$200,000.00"
            Tras3 = "$250,000.00"
        
        pdf.rect(297, 387, 80, 12, fill=False, stroke=False)
        pdf.rect(382, 387, 80, 12, fill=False, stroke=False)
        pdf.rect(467, 387, 80, 12, fill=False, stroke=False)
        ancho_texto51 = pdf.stringWidth(Tras1, "Helvetica", 9)
        x_centro51 = 297 + (80 - ancho_texto51)/2
        pdf.drawString(x_centro51, 389, Tras1)
        ancho_texto52 = pdf.stringWidth(Tras2, "Helvetica", 9)
        x_centro52 = 382 + (80 - ancho_texto52)/2
        pdf.drawString(x_centro52, 389, Tras2)
        ancho_text53 = pdf.stringWidth(Tras3, "Helvetica", 9)
        x_centro53 = 467 + (80 - ancho_text53)/2
        pdf.drawString(x_centro53, 389, Tras3)
        pdf.drawString(45, 376, "SIDA (máximo vitalicio)")
        if SumaP < 250000:
            SI1 = ""
            SI2 = "$25,000.00"
            SI3 = "$25,000.00"
        else:
            SI1 = "$50,000.00"
            SI2 = "$50,000.00"
            SI3 = "$50,000.00"
        
        pdf.rect(297, 374, 80, 12, fill=False, stroke=False)
        pdf.rect(382, 374, 80, 12, fill=False, stroke=False)
        pdf.rect(467, 374, 80, 12, fill=False, stroke=False)
        ancho_texto54 = pdf.stringWidth(SI1, "Helvetica", 9)
        x_centro54 = 297 + (80 - ancho_texto54)/2
        pdf.drawString(x_centro54, 376, SI1)
        ancho_texto55 = pdf.stringWidth(SI2, "Helvetica", 9)
        x_centro55 = 382 + (80 - ancho_texto55)/2
        pdf.drawString(x_centro55, 376, SI2)
        ancho_text56 = pdf.stringWidth(SI3, "Helvetica", 9)
        x_centro56 = 467 + (80 - ancho_text56)/2
        pdf.drawString(x_centro56, 376, SI3)
        pdf.drawString(45, 363, "Ambulancia aérea (año póliza)")
        if SumaP < 250000:
            Ae1 = ""
            Ae2 = "N/A"
            Ae3 = "N/A"
        else:
            Ae1 = "$5,000.00"
            Ae2 = "$10,000.00"
            Ae3 = "$15,000.00"
        
        pdf.rect(297, 361, 80, 12, fill=False, stroke=False)
        pdf.rect(382, 361, 80, 12, fill=False, stroke=False)
        pdf.rect(467, 361, 80, 12, fill=False, stroke=False)
        ancho_texto57 = pdf.stringWidth(Ae1, "Helvetica", 9)
        x_centro57 = 297 + (80 - ancho_texto57)/2
        pdf.drawString(x_centro57, 363, Ae1)
        ancho_texto58 = pdf.stringWidth(Ae2, "Helvetica", 9)
        x_centro58 = 382 + (80 - ancho_texto58)/2
        pdf.drawString(x_centro58, 363, Ae2)
        ancho_text59 = pdf.stringWidth(Ae3, "Helvetica", 9)
        x_centro59 = 467 + (80 - ancho_text59)/2
        pdf.drawString(x_centro59, 363, Ae3)
        pdf.drawString(45, 350, "Atención al recién nacido (neonatologo, nurseria)")
        if SumaP < 250000:
            At1 = ""
            At2 = "$200.00"
            At3 = "$200.00"
        else:
            At1 = "$250.00"
            At2 = "$300.00"
            At3 = "$400.00"
        
        pdf.rect(297, 348, 80, 12, fill=False, stroke=False)
        pdf.rect(382, 348, 80, 12, fill=False, stroke=False)
        pdf.rect(467, 348, 80, 12, fill=False, stroke=False)
        ancho_texto60 = pdf.stringWidth(At1, "Helvetica", 9)
        x_centro60 = 297 + (80 - ancho_texto60)/2
        pdf.drawString(x_centro60, 350, At1)
        ancho_texto61 = pdf.stringWidth(At2, "Helvetica", 9)
        x_centro61 = 382 + (80 - ancho_texto61)/2
        pdf.drawString(x_centro61, 350, At2)
        ancho_text62 = pdf.stringWidth(At3, "Helvetica", 9)
        x_centro62 = 467 + (80 - ancho_text62)/2
        pdf.drawString(x_centro62, 350, At3)
        pdf.drawString(45, 337, "Complicaciones del recién nacido")
        if SumaP < 250000:
            Comp1 = ""
            Comp2 = "$10,000.00"
            Comp3 = "$10,000.00"
        else:
            Comp1 = "$10,000.00"
            Comp2 = "$15,000.00"
            Comp3 = "$15,000.00"
        
        pdf.rect(297, 335, 80, 12, fill=False, stroke=False)
        pdf.rect(382, 335, 80, 12, fill=False, stroke=False)
        pdf.rect(467, 335, 80, 12, fill=False, stroke=False)
        ancho_texto63 = pdf.stringWidth(Comp1, "Helvetica", 9)
        x_centro63 = 297 + (80 - ancho_texto63)/2
        pdf.drawString(x_centro63, 337, Comp1)
        ancho_texto64 = pdf.stringWidth(Comp2, "Helvetica", 9)
        x_centro64 = 382 + (80 - ancho_texto64)/2
        pdf.drawString(x_centro64, 337, Comp2)
        ancho_text65 = pdf.stringWidth(Comp3, "Helvetica", 9)
        x_centro65 = 467 + (80 - ancho_text65)/2
        pdf.drawString(x_centro65, 337, Comp3)
        pdf.drawString(45, 324, "Condiciones congénitas (máximo vitalicio)")
        if SumaP < 250000:
            Cond1 = ""
            Cond2 = "$10,000.00"
            Cond3 = "$10,000.00"
        else:
            Cond1 = "$10,000.00"
            Cond2 = "$15,000.00"
            Cond3 = "$15,000.00"
        
        pdf.rect(297, 322, 80, 12, fill=False, stroke=False)
        pdf.rect(382, 322, 80, 12, fill=False, stroke=False)
        pdf.rect(467, 322, 80, 12, fill=False, stroke=False)
        ancho_texto66 = pdf.stringWidth(Cond1, "Helvetica", 9)
        x_centro66 = 297 + (80 - ancho_texto66)/2
        pdf.drawString(x_centro66, 324, Cond1)
        ancho_texto67 = pdf.stringWidth(Cond2, "Helvetica", 9)
        x_centro67 = 382 + (80 - ancho_texto67)/2
        pdf.drawString(x_centro67, 324, Cond2)
        ancho_text68 = pdf.stringWidth(Cond3, "Helvetica", 9)
        x_centro68 = 467 + (80 - ancho_text68)/2
        pdf.drawString(x_centro68, 324, Cond3)
        pdf.drawString(45, 311, "Psiquiatría ambulatoria")
        if SumaP < 250000:
            Psiq1 = ""
            Psiq2 = "$500.00"
            Psiq3 = "$500.00"
        else:
            Psiq1 = "$500.00"
            Psiq2 = "$600.00"
            Psiq3 = "$600.00"
        
        pdf.rect(297, 309, 80, 12, fill=False, stroke=False)
        pdf.rect(382, 309, 80, 12, fill=False, stroke=False)
        pdf.rect(467, 309, 80, 12, fill=False, stroke=False)
        ancho_texto69 = pdf.stringWidth(Psiq1, "Helvetica", 9)
        x_centro69 = 297 + (80 - ancho_texto69)/2
        pdf.drawString(x_centro69, 311, Psiq1)
        ancho_texto70 = pdf.stringWidth(Psiq2, "Helvetica", 9)
        x_centro70 = 382 + (80 - ancho_texto70)/2
        pdf.drawString(x_centro70, 311, Psiq2)
        ancho_text71 = pdf.stringWidth(Psiq3, "Helvetica", 9)
        x_centro71 = 467 + (80 - ancho_text71)/2
        pdf.drawString(x_centro71, 311, Psiq3)
        #ULTIMA SECCIÓN
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(40, 292, 515, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("Helvetica-Bold", 9)
        if Temporal == "Mensual":
            pdf.drawString(45, 294, "PRIMERA CUOTA DE MES")
        elif Temporal == "Trimestral":
            pdf.drawString(45, 294, "PRIMA TOTAL TRIMESTRAL")
        elif Temporal == "Semestral":
            pdf.drawString(45, 294, "PRIMA TOTAL SEMESTRAL")
        else:
            pdf.drawString(45, 294, "PRIMA TOTAL ANUAL")

        if Gene == "Hombre":
            fs = 1
        else: 
            fs = 1.15

        if Naci2 == "" or Solic2 == "":
            fs2 = 0
        elif Gene2 == "Hombre":
            fs2 = 1
        elif Gene2 == "Mujer": 
            fs2 = 1.15

        if hij == "Ninguno":
            fs3 = 0
        elif hij == "1":
            fs3 = 1
        elif hij == "2":
            fs3 = 2
        elif hij == "3 o más":
            fs3 = 3
        
        edadP = int(edad)
        edadC = int(edad2)
        if SumaP < 250000:
            
            tr_value1 = TR3.objects.get(Age=edadP).P50
            tr_valuedep = TR3.objects.get(Age=18).P50
            tr_value2 = TR3.objects.get(Age=edadC).P50

            tr_value1a = TR3.objects.get(Age=edadP).P100
            tr_valuedepa = TR3.objects.get(Age=18).P100
            tr_value2a = TR3.objects.get(Age=edadC).P100

            Prim1 = 0
            PrimaP1 = "{:,.2f}".format(float(Prim1))
            Prim2 = (((int(50000) * Decimal(tr_value1)) * Decimal(fs))/(1 - Decimal(0.4))  + ((int(50000) * Decimal(tr_value2)) * Decimal(fs2))/(1 - Decimal(0.4)) + ((int(50000) * Decimal(tr_valuedep)) * fs3 * Decimal(0.95))/(1 - Decimal(0.4))) * Decimal(1.07) * Decimal(0.0837) * Decimal(1.35)
            PrimaP2 = "{:,.2f}".format(float(Prim2))
            Prim3 = (((int(100000) * Decimal(tr_value1a)) * Decimal(fs))/(1 - Decimal(0.4))  + ((int(100000) * Decimal(tr_value2a)) * Decimal(fs2))/(1 - Decimal(0.4)) + ((int(100000) * Decimal(tr_valuedepa)) * fs3 * Decimal(0.95))/(1 - Decimal(0.4))) * Decimal(1.07) * Decimal(0.0837) * Decimal(1.35)
            PrimaP3 = "{:,.2f}".format(float(Prim3))
        else:
            tr_value1b = TR3.objects.get(Age=edadP).P250
            tr_valuedepb = TR3.objects.get(Age=18).P250
            tr_value2b = TR3.objects.get(Age=edadC).P250

            tr_value1c = TR3.objects.get(Age=edadP).P500
            tr_valuedepc = TR3.objects.get(Age=18).P500
            tr_value2c = TR3.objects.get(Age=edadC).P500

            tr_value1d = TR3.objects.get(Age=edadP).P1000
            tr_valuedepd = TR3.objects.get(Age=18).P1000
            tr_value2d = TR3.objects.get(Age=edadC).P1000
            Prim1 = (((int(250000) * Decimal(tr_value1b)) * Decimal(fs))/(1 - Decimal(0.4))  + ((int(250000) * Decimal(tr_value2b)) * Decimal(fs2))/(1 - Decimal(0.4)) + ((int(250000) * Decimal(tr_valuedepb)) * fs3 * Decimal(0.95))/(1 - Decimal(0.4))) * Decimal(1.30) * Decimal(1.07) * Decimal(0.0837) * Decimal(1.05)
            PrimaP1 = "{:,.2f}".format(float(Prim1))
            
            Prim2 = (((int(500000) * Decimal(tr_value1c)) * Decimal(fs))/(1 - Decimal(0.4))  + ((int(500000) * Decimal(tr_value2c)) * Decimal(fs2))/(1 - Decimal(0.4)) + ((int(500000) * Decimal(tr_valuedepc)) * fs3 * Decimal(0.95))/(1 - Decimal(0.4))) * Decimal(1.30) * Decimal(1.07) * Decimal(0.0837) * Decimal(1.05)
            PrimaP2 = "{:,.2f}".format(float(Prim2))

            Prim3 = (((int(1000000) * Decimal(tr_value1d)) * Decimal(fs))/(1 - Decimal(0.4))  + ((int(1000000) * Decimal(tr_value2d)) * Decimal(fs2))/(1 - Decimal(0.4)) + ((int(1000000) * Decimal(tr_valuedepd)) * fs3 * Decimal(0.95))/(1 - Decimal(0.4))) * Decimal(1.30) * Decimal(1.07) * Decimal(0.0837) * Decimal(1.05)
            PrimaP3 = "{:,.2f}".format(float(Prim3))

        if Temporal == "Mensual":
            pdf.rect(297, 292, 80, 12, fill=False, stroke=False)
            pdf.rect(382, 292, 80, 12, fill=False, stroke=False)
            pdf.rect(467, 292, 80, 12, fill=False, stroke=False)
            ancho_texto72 = pdf.stringWidth("$" + str(PrimaP1), "Helvetica", 9)
            x_centro72 = 297 + (80 - ancho_texto72)/2
            pdf.drawString(x_centro72, 294, "$" + str(PrimaP1))
            ancho_texto73 = pdf.stringWidth("$" + str(PrimaP2), "Helvetica", 9)
            x_centro73 = 382 + (80 - ancho_texto73)/2
            pdf.drawString(x_centro73, 294, "$" + str(PrimaP2))
            ancho_text74 = pdf.stringWidth("$" + str(PrimaP3), "Helvetica", 9)
            x_centro74 = 467 + (80 - ancho_text74)/2
            pdf.drawString(x_centro74, 294, "$" + str(PrimaP3))


            pdf.setFillColorRGB(0.87, 0.87, 0.87)
            pdf.setStrokeColorRGB(0, 0, 0)
            pdf.rect(40, 278, 515, 14, fill=True, stroke=False)
            pdf.setFillColorRGB(0, 0, 0)
            pdf.setFont("Helvetica-Bold", 9)
            pdf.drawString(45, 281, "SIGUIENTES ONCE CUOTAS")

            Prima1 = (Prim1 / Decimal(0.0837) * Decimal(0.0833))
            PrimaPP1 = "{:,.2f}".format(float(Prima1))
            Prima2 = (Prim2 / Decimal(0.0837) * Decimal(0.0833))
            PrimaPP2 = "{:,.2f}".format(float(Prima2))
            Prima3 = (Prim3 / Decimal(0.0837) * Decimal(0.0833))
            PrimaPP3 = "{:,.2f}".format(float(Prima3))

            pdf.rect(297, 279, 80, 12, fill=False, stroke=False)
            pdf.rect(382, 279, 80, 12, fill=False, stroke=False)
            pdf.rect(467, 279, 80, 12, fill=False, stroke=False)
            ancho_texto75 = pdf.stringWidth("$" + str(PrimaPP1), "Helvetica", 9)
            x_centro75 = 297 + (80 - ancho_texto75)/2
            pdf.drawString(x_centro75, 281, "$" + str(PrimaPP1))
            ancho_texto76 = pdf.stringWidth("$" + str(PrimaPP2), "Helvetica", 9)
            x_centro76 = 382 + (80 - ancho_texto76)/2
            pdf.drawString(x_centro76, 281, "$" + str(PrimaPP2))
            ancho_text77 = pdf.stringWidth("$" + str(PrimaPP3), "Helvetica", 9)
            x_centro77 = 467 + (80 - ancho_text77)/2
            pdf.drawString(x_centro77, 281, "$" + str(PrimaPP3))
        elif Temporal == "Trimestral":
            pdf.rect(297, 292, 80, 12, fill=False, stroke=False)
            pdf.rect(382, 292, 80, 12, fill=False, stroke=False)
            pdf.rect(467, 292, 80, 12, fill=False, stroke=False)

            Prima1 = (((Prim1 / Decimal(0.0837))/Decimal(1.07)) * Decimal(1.06))/4
            PrimaPP1 = "{:,.2f}".format(float(Prima1))
            Prima2 = (((Prim2 / Decimal(0.0837))/Decimal(1.07)) * Decimal(1.06))/4
            PrimaPP2 = "{:,.2f}".format(float(Prima2))
            Prima3 = (((Prim3 / Decimal(0.0837))/Decimal(1.07)) * Decimal(1.06))/4
            PrimaPP3 = "{:,.2f}".format(float(Prima3))
            ancho_texto72 = pdf.stringWidth("$" + str(PrimaPP1), "Helvetica", 9)
            x_centro72 = 297 + (80 - ancho_texto72)/2
            pdf.drawString(x_centro72, 294, "$" + str(PrimaPP1))
            ancho_texto73 = pdf.stringWidth("$" + str(PrimaPP2), "Helvetica", 9)
            x_centro73 = 382 + (80 - ancho_texto73)/2
            pdf.drawString(x_centro73, 294, "$" + str(PrimaPP2))
            ancho_text74 = pdf.stringWidth(str(PrimaPP3), "Helvetica", 9)
            x_centro74 = 467 + (80 - ancho_text74)/2
            pdf.drawString(x_centro74, 294, "$" + str(PrimaPP3))


            pdf.setFillColorRGB(1, 1, 1)
            pdf.setStrokeColorRGB(0, 0, 0)
            pdf.rect(40, 278, 515, 14, fill=True, stroke=False)
            pdf.setFillColorRGB(0, 0, 0)
            pdf.setFont("Helvetica-Bold", 9)
            pdf.drawString(45, 281, "")


            Prima1 = ""
            Prima2 = ""
            Prima3 = ""


            pdf.rect(297, 279, 80, 12, fill=False, stroke=False)
            pdf.rect(382, 279, 80, 12, fill=False, stroke=False)
            pdf.rect(467, 279, 80, 12, fill=False, stroke=False)
            ancho_texto75 = pdf.stringWidth(str(Prima1), "Helvetica", 9)
            x_centro75 = 297 + (80 - ancho_texto75)/2
            pdf.drawString(x_centro75, 281, str(Prima1))
            ancho_texto76 = pdf.stringWidth(str(Prima2), "Helvetica", 9)
            x_centro76 = 382 + (80 - ancho_texto76)/2
            pdf.drawString(x_centro76, 281, str(Prima2))
            ancho_text77 = pdf.stringWidth(str(Prima3), "Helvetica", 9)
            x_centro77 = 467 + (80 - ancho_text77)/2
            pdf.drawString(x_centro77, 281, str(Prima3))

        elif Temporal == "Semestral":
            pdf.rect(297, 292, 80, 12, fill=False, stroke=False)
            pdf.rect(382, 292, 80, 12, fill=False, stroke=False)
            pdf.rect(467, 292, 80, 12, fill=False, stroke=False)

            Prima1 = (((Prim1 / Decimal(0.0837))/Decimal(1.07)) * Decimal(1.04))/2
            PrimaPP1 = "{:,.2f}".format(float(Prima1))
            Prima2 = (((Prim2 / Decimal(0.0837))/Decimal(1.07)) * Decimal(1.04))/2
            PrimaPP2 = "{:,.2f}".format(float(Prima2))
            Prima3 = (((Prim3 / Decimal(0.0837))/Decimal(1.07)) * Decimal(1.04))/2
            PrimaPP3 = "{:,.2f}".format(float(Prima3))
            ancho_texto72 = pdf.stringWidth("$" + str(PrimaPP1), "Helvetica", 9)
            x_centro72 = 297 + (80 - ancho_texto72)/2
            pdf.drawString(x_centro72, 294, "$" + str(PrimaPP1))
            ancho_texto73 = pdf.stringWidth("$" + str(PrimaPP2), "Helvetica", 9)
            x_centro73 = 382 + (80 - ancho_texto73)/2
            pdf.drawString(x_centro73, 294, "$" + str(PrimaPP2))
            ancho_text74 = pdf.stringWidth("$" + str(PrimaPP3), "Helvetica", 9)
            x_centro74 = 467 + (80 - ancho_text74)/2
            pdf.drawString(x_centro74, 294, "$" + str(PrimaPP3))


            pdf.setFillColorRGB(1, 1, 1)
            pdf.setStrokeColorRGB(0, 0, 0)
            pdf.rect(40, 278, 515, 14, fill=True, stroke=False)
            pdf.setFillColorRGB(0, 0, 0)
            pdf.setFont("Helvetica-Bold", 9)
            pdf.drawString(45, 281, "")


            Prima1 = ""
            Prima2 = ""
            Prima3 = ""


            pdf.rect(297, 279, 80, 12, fill=False, stroke=False)
            pdf.rect(382, 279, 80, 12, fill=False, stroke=False)
            pdf.rect(467, 279, 80, 12, fill=False, stroke=False)
            ancho_texto75 = pdf.stringWidth(str(Prima1), "Helvetica", 9)
            x_centro75 = 297 + (80 - ancho_texto75)/2
            pdf.drawString(x_centro75, 281, str(Prima1))
            ancho_texto76 = pdf.stringWidth(str(Prima2), "Helvetica", 9)
            x_centro76 = 382 + (80 - ancho_texto76)/2
            pdf.drawString(x_centro76, 281, str(Prima2))
            ancho_text77 = pdf.stringWidth(str(Prima3), "Helvetica", 9)
            x_centro77 = 467 + (80 - ancho_text77)/2
            pdf.drawString(x_centro77, 281, str(Prima3))
        
        elif Temporal == "Anual":
            pdf.rect(297, 292, 80, 12, fill=False, stroke=False)
            pdf.rect(382, 292, 80, 12, fill=False, stroke=False)
            pdf.rect(467, 292, 80, 12, fill=False, stroke=False)

            Prima1 = (((Prim1 / Decimal(0.0837))/Decimal(1.07)) * 1)/1
            PrimaPP1 = "{:,.2f}".format(float(Prima1))
            Prima2 = (((Prim2 / Decimal(0.0837))/Decimal(1.07)) * Decimal(1))/1
            PrimaPP2 = "{:,.2f}".format(float(Prima2))
            Prima3 = (((Prim3 / Decimal(0.0837))/Decimal(1.07)) * Decimal(1))/1
            PrimaPP3 = "{:,.2f}".format(float(Prima3))
            ancho_texto72 = pdf.stringWidth("$" + str(PrimaPP1), "Helvetica", 9)
            x_centro72 = 297 + (80 - ancho_texto72)/2
            pdf.drawString(x_centro72, 294, "$" + str(PrimaPP1))
            ancho_texto73 = pdf.stringWidth("$" + str(PrimaPP2), "Helvetica", 9)
            x_centro73 = 382 + (80 - ancho_texto73)/2
            pdf.drawString(x_centro73, 294, "$" + str(PrimaPP2))
            ancho_text74 = pdf.stringWidth("$" + str(PrimaPP3), "Helvetica", 9)
            x_centro74 = 467 + (80 - ancho_text74)/2
            pdf.drawString(x_centro74, 294, "$" + str(PrimaPP3))


            pdf.setFillColorRGB(1, 1, 1)
            pdf.setStrokeColorRGB(0, 0, 0)
            pdf.rect(40, 278, 515, 14, fill=True, stroke=False)
            pdf.setFillColorRGB(0, 0, 0)
            pdf.setFont("Helvetica-Bold", 9)
            pdf.drawString(45, 281, "")


            Prima1 = ""
            Prima2 = ""
            Prima3 = ""


            pdf.rect(297, 279, 80, 12, fill=False, stroke=False)
            pdf.rect(382, 279, 80, 12, fill=False, stroke=False)
            pdf.rect(467, 279, 80, 12, fill=False, stroke=False)
            ancho_texto75 = pdf.stringWidth(str(Prima1), "Helvetica", 9)
            x_centro75 = 297 + (80 - ancho_texto75)/2
            pdf.drawString(x_centro75, 281, str(Prima1))
            ancho_texto76 = pdf.stringWidth(str(Prima2), "Helvetica", 9)
            x_centro76 = 382 + (80 - ancho_texto76)/2
            pdf.drawString(x_centro76, 281, str(Prima2))
            ancho_text77 = pdf.stringWidth(str(Prima3), "Helvetica", 9)
            x_centro77 = 467 + (80 - ancho_text77)/2
            pdf.drawString(x_centro77, 281, str(Prima3))

        if SumaP < 250000:
            pdf.setStrokeColorRGB(0.87, 0.87, 0.87)
            pdf.setFillColorRGB(0.87, 0.87, 0.87)
            pdf.rect(297, 292, 80, 12, fill=True, stroke=False)
            pdf.rect(297, 279, 80, 12, fill=True, stroke=False)
        
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.drawString(45, 268, "Frecuencia de pago de prima")
        pdf.setFont("Helvetica-Bold", 9)
        if Temporal == "Anual":
            pdf.setStrokeColorRGB(1, 1, 1)
            pdf.setFillColorRGB(1, 1, 1)
            pdf.rect(297, 279, 80, 12, fill=True, stroke=True)
            Tmp = "ANUAL"
        elif Temporal == "Mensual":
            Tmp = "MENSUAL"
        elif Temporal == "Semestral":
            pdf.setStrokeColorRGB(1, 1, 1)
            pdf.setFillColorRGB(1, 1, 1)
            pdf.rect(297, 279, 80, 12, fill=True, stroke=True)
            Tmp = "SEMESTRAL"
        elif Temporal == "Trimestral":
            pdf.setStrokeColorRGB(1, 1, 1)
            pdf.setFillColorRGB(1, 1, 1)
            pdf.rect(297, 279, 80, 12, fill=True, stroke=True)
            Tmp = "TRIMESTRAL"
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.drawString(402, 268, Tmp)

        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(295, 252, 261, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        if SumaP < 250000:
            pdf.drawString(390, 256, "PLAN A")
            pdf.rect(433, 254, 25, 10, fill=False, stroke=True)
            pdf.drawString(476, 256, "PLAN B")
            pdf.rect(519, 254, 25, 10, fill=False, stroke=True)
        else:
            pdf.drawString(304, 256, "PLAN A")
            pdf.rect(345, 254, 25, 10, fill=False, stroke=True)
            pdf.drawString(390, 256, "PLAN B")
            pdf.rect(433, 254, 25, 10, fill=False, stroke=True)
            pdf.drawString(476, 256, "PLAN C")
            pdf.rect(519, 254, 25, 10, fill=False, stroke=True)
        pdf.setFont("Helvetica", 9)
        pdf.drawString(45, 255, "Marque el Plan Elegido:")

        pdf.setFont("Helvetica", 9)
        pdf.drawString(45, 232, "Si usted acepta la presente cotización, favor devolver los siguientes documentos completos y firmados:")
        pdf.drawString(45, 219, "1. Solicitud de seguro")
        pdf.drawString(45, 206, "2. Ficha Integral")
        pdf.drawString(45, 193, "3. Declaración Jurada")
        pdf.drawString(270, 219, "4. DUI y NIT de asegurado")

        pdf.drawString(45, 180, "Oferta válida 30 días a partir de la fecha de su emisión: ")
        pdf.drawString(268, 180, fecha_actual)
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(45, 167, "La prima cotizada puede cambiar si en la fecha de emisión de la póliza la edad del titular o dependiente(s)")
        pdf.drawString(45, 154, "para el seguro fuere otra. Prima sujeta a verificación de exámen médico y análisis de suscripción.")
        pdf.setFont("Helvetica", 9)
        pdf.drawString(50, 114, "______________________")
        pdf.drawString(49, 102, "Firma de aceptación cliente")
        pdf.drawString(235, 114, "______________________")
        pdf.drawString(250, 102, "Fecha de aceptación")
        pdf.drawString(400, 114, "______________________")
        pdf.drawString(413, 102, "Firma de intermediario")

        if Nom == "" and In == "":
            pdf.setFillColorRGB(0.87, 0.87, 0.87)
            pdf.setStrokeColorRGB(0, 0, 0)
            pdf.rect(50, 40, 497, 14, fill=True, stroke=False)
            pdf.setFillColorRGB(0, 0, 0)
            pdf.drawString(50, 42, "Intermediario, Empresa: Oficina Principal, Atlántida Vida S.A. Seguro de Personas")
            pdf.drawString(500, 42, "V.01.2024")

            pdf.setFillColorRGB(0.87, 0.87, 0.87)
            pdf.setStrokeColorRGB(0, 0, 0)
            pdf.rect(50, 27, 497, 14, fill=True, stroke=False)
            pdf.setFillColorRGB(0, 0, 0)
            pdf.drawString(50, 29, "Correo Electrónico: " + str(Cor))
            pdf.drawString(460, 29, "Teléfono: " + str(Te))
        else:
            pdf.setFillColorRGB(0.87, 0.87, 0.87)
            pdf.setStrokeColorRGB(0, 0, 0)
            pdf.rect(50, 40, 497, 14, fill=True, stroke=False)
            pdf.setFillColorRGB(0, 0, 0)
            pdf.drawString(50, 42, "Intermediario, Empresa: " + str(In) + ", " + str(Nom))
            pdf.drawString(500, 42, "V.01.2024")

            pdf.setFillColorRGB(0.87, 0.87, 0.87)
            pdf.setStrokeColorRGB(0, 0, 0)
            pdf.rect(50, 27, 497, 14, fill=True, stroke=False)
            pdf.setFillColorRGB(0, 0, 0)
            pdf.drawString(50, 29, "Correo Electrónico: " + str(Cor))
            pdf.drawString(460, 29, "Teléfono: " + str(Te))
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(50, 14, 497, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawString(50, 16, "Atención al cliente: (503)2283-0800")
        pdf.drawString(332, 16, "Correo electrónico: aseguradoatlantida@seatlan.sv")
        # Guardar el PDF en el buffer
        pdf.showPage()
        pdf.setTitle('OFERTA_DE_GASTOS_MÉDICOS.pdf')
        pdf.save()

        # Obtener el contenido del buffer y devolverlo como una respuesta HTTP
        #buffer.seek(0)

        pdf_bytes = buffer.getvalue()
        pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')

        #response = HttpResponse(content_type='application/pdf')
        #response['Content-Disposition'] = 'inline; filename="Oferta_TemporalRenovable.pdf"'
        #response.write(buffer.read())

        correos = [correo for correo in [Cor, Mails] if correo]  # Filtrar correos válidos

        # Si hay correos válidos, enviar el correo
        if correos:
            enviar_correo(correos, Solicitante, Cellphones, edad, pdf_bytes)

        return render(request, 'Oferta_SMH.html', 
            {'pdf_base64': pdf_base64,
             'Solicitante': Solicitante,
             })
        

def enviar_correo(correos, Solicitante, Cellphones, edad, pdf_bytes):
    # Configuración del servidor SMTP
    smtp_server = 'smtp.gmail.com'
    port = 587
    sender_email = 'henriquezricardo459@gmail.com'
    password = 'omou bfpf amij afcw'  # Recuerda almacenar la contraseña de manera segura
    
    # Crear el objeto del mensaje
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ', '.join(correos)
    msg['Subject'] = 'Oferta de Gastos Médicos Individual'

    cuerpo_mensaje = f"""Información del cliente:

- Nombre: {Solicitante}
- Edad: {edad}
- Teléfono: {Cellphones}
    
Es un placer saludarle. Adjuntamos la oferta del seguro de Gastos Médicos Individual así cómo los documentos adicionales necesarios en caso de que acepte nuestra cotización.

Cualquier consulta, no dude en responder a este correo o comunicarse con nosotros al 2283-0800. Quedamos a su disposición para cualquier consulta adicional.

Saludos cordiales

Atentamente,

Seguros Atlántida S.A., de C.V.
    """
    msg.attach(MIMEText(cuerpo_mensaje, 'plain'))
    # Adjuntar el PDF generado
    attachment = MIMEBase('application', 'octet-stream')
    attachment.set_payload(pdf_bytes)
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', 'attachment', filename='Oferta de Gastos Médicos Individual.pdf')
    msg.attach(attachment)

    # Adjuntar otros archivos PDF
    for documento in ['Declaracion_Jurada_Persona_Natural.pdf', 'Solicitud_GMI.pdf', 'Hoja_de_Vinculacion_Persona_Natural.pdf']:
        with open(os.path.join('cotizadorsmh/static', documento), 'rb') as f:
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(f.read())
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', 'attachment', filename=documento)
            msg.attach(attachment)

    # Iniciar la conexión SMTP y enviar el correo
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)

        
        