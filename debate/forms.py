from django import forms
from .models import Debate

class DebateForm(forms.ModelForm):
    class Meta:
        model = Debate
        fields = ['topic', 'debate_type', 'time_limit']
        widgets = {
            'topic': forms.TextInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition'}),
            'debate_type': forms.Select(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition'}),
            'time_limit': forms.NumberInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition', 'min': 30}),
        }
