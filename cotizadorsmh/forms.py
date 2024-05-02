from django import forms

Opcion1 = [
    ('Hombre', 'Hombre'),
    ('Mujer', 'Mujer'),
]
Opcion2 = [
    ('$50,000', '$50,000'),
    ('$100,000', '$100,000'),
    ('$250,000', '$250,000'),
    ('$500,000', '$500,000'),
    ('$1,000,000', '$1,000,000'),
]
Opciones5 = [
    ('Mensual', 'Mensual'),
    ('Trimestral', 'Trimestral'),
    ('Semestral', 'Semestral'),
    ('Anual', 'Anual'),
]
Opciones6 = [
    ('Ninguno', 'Ninguno'),
    ('1', '1'),
    ('2', '2'),
    ('3 o más', '3 o más'),
]
class C_Intermediario2(forms.Form):
    Nombre = forms.CharField(label="Nombre de Empresa:", max_length=200, required=False)
    Int = forms.CharField(label="Intermediario:", max_length=200, required=False)
    Tel = forms.CharField(label="Teléfono:", max_length=200, required=False)
    Correo = forms.CharField(label="Correo electrónico:", max_length=200, required=False)
    Id = forms.CharField(label="IVD o CVD:", max_length=200, required=False) 
    
class form_CotizadorTAR(forms.Form):
    Sol = forms.CharField(label="Solicitante:", max_length=200)
    Mail = forms.CharField(label="Correo Electrónico:", max_length=200, required=False)
    Cellphone = forms.CharField(label="Celular:", max_length=200)
    Nac = forms.CharField(label="Fecha de Nacimiento (YYYY/MM/DD):", max_length=200)
    Gen = forms.ChoiceField(label="Género:", choices=Opcion1, widget=forms.Select(attrs={'id':'gen'}))
    Sum = forms.ChoiceField(label="Suma Asegurada:", choices=Opcion2 , widget=forms.Select(attrs={'id':'sum'}))
    Temp = forms.ChoiceField(label="Forma de Pago:", choices=Opciones5, widget=forms.Select(attrs={'id':'temp'}))
    hijos = forms.ChoiceField(label="Hijos dependientes:", choices=Opciones6, widget=forms.Select(attrs={'id':'hij'}))
class form_Conyuge(forms.Form):
    Sol2 = forms.CharField(label="Nombre:", max_length=200, required=False)
    Nac2 = forms.CharField(label="Fecha de Nacimiento (YYYY/MM/DD):", max_length=200, required=False)
    