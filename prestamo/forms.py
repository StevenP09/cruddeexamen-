from django import forms
from core.models import *

class PrestamoForm(forms.ModelForm):

    empleado = forms.ModelChoiceField(
        queryset=Empleado.objects.all(),
        empty_label="Seleccione un empleado",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    tipo_prestamo = forms.ModelChoiceField(
        queryset=TipoPrestamo.objects.all(),
        empty_label="Seleccione un tipo de prestamo",
        widget=forms.Select(attrs={'class': 'form-control', 'onchange': 'get_tipo()'})
    )

    class Meta:
        model = Prestamo
        fields = '__all__' 
        widgets = {
            'fecha_prestamo': forms.DateInput(attrs={'class': 'form-control', 'rows': 3, 'type': 'date'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'oninput': 'get_values()',}),
            'interes': forms.NumberInput(attrs={'class': 'form-control', 'oninput': 'get_values()',}),
            'monto_pagar': forms.NumberInput(attrs={'class': 'form-control'}),
            'numero_cuotas': forms.NumberInput(attrs={'class': 'form-control'}),
            'cuota_mensual': forms.NumberInput(attrs={'class': 'form-control'}),
            'saldo': forms.NumberInput(attrs={'class': 'form-control'}),
        }