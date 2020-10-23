from django import forms


class SearchForm(forms.Form):
    disease_name = forms.CharField(required=True,
                                   widget=forms.TextInput(
                                       attrs={'class': 'form-control', 'placeholder': 'Disease name'}))
    location = forms.CharField(required=True,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control', 'placeholder': 'Location'}))

    # start_date = forms.DateTimeField(
    #     input_formats=['%d/%m/%Y %H:%M'],
    #     widget=forms.DateTimeInput(attrs={
    #         'class': 'form-control datetimepicker-input',
    #         'data-target': '#datetimepicker1'
    #         , 'placeholder': 'Start date'
    #     })
    # )
    # end_date = forms.DateTimeField(
    #     input_formats=['%d/%m/%Y %H:%M'],
    #     widget=forms.DateTimeInput(attrs={
    #         'class': 'form-control datetimepicker-input',
    #         'data-target': '#datetimepicker2', 'placeholder': 'End date'
    #     })
    # )
