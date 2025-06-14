from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Count
from .models import Voter
from django import forms
from datetime import datetime
import plotly
import plotly.graph_objs as go

class VoterFilterForm(forms.Form):
    party_affiliation = forms.ChoiceField(choices=[('', 'Any')], required=False)
    min_dob = forms.ChoiceField(choices=[('', 'Any')] + [(str(y), str(y)) for y in range(1900, datetime.now().year + 1)], required=False)
    max_dob = forms.ChoiceField(choices=[('', 'Any')] + [(str(y), str(y)) for y in range(1900, datetime.now().year + 1)], required=False)
    voter_score = forms.ChoiceField(choices=[('', 'Any')] + [(str(i), str(i)) for i in range(6)], required=False)
    v20state = forms.BooleanField(required=False)
    v21town = forms.BooleanField(required=False)
    v21primary = forms.BooleanField(required=False)
    v22general = forms.BooleanField(required=False)
    v23town = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            parties = Voter.objects.values_list('party_affiliation', flat=True).distinct()
            self.fields['party_affiliation'].choices = [('', 'Any')] + [(p.strip(), p.strip()) for p in parties]
        except:
            pass

class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = VoterFilterForm(self.request.GET or None)
        
        birth_years = Voter.objects.dates('date_of_birth', 'year')
        years = sorted([date.year for date in birth_years])
        context['years'] = years
        
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = VoterFilterForm(self.request.GET or None)
        
        if form.is_valid():
            if form.cleaned_data.get('party_affiliation'):
                queryset = queryset.filter(party_affiliation=form.cleaned_data['party_affiliation'])
            if form.cleaned_data.get('min_dob'):
                queryset = queryset.filter(date_of_birth__year__gte=form.cleaned_data['min_dob'])
            if form.cleaned_data.get('max_dob'):
                queryset = queryset.filter(date_of_birth__year__lte=form.cleaned_data['max_dob'])
            if form.cleaned_data.get('voter_score'):
                queryset = queryset.filter(voter_score=form.cleaned_data['voter_score'])
            for field in ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']:
                if form.cleaned_data.get(field):
                    queryset = queryset.filter(**{field: True})
        
        return queryset
    
class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'

class GraphListView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_queryset(self):
        def parse_boolean(value):
            return value.lower() == 'true' if value else None
        
        queryset = super().get_queryset()
        party = self.request.GET.get('party')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')

        # Boolean fields for election participation
        v20state = parse_boolean(self.request.GET.get('v20state'))
        v21town = parse_boolean(self.request.GET.get('v21town'))
        v21primary = parse_boolean(self.request.GET.get('v21primary'))
        v22general = parse_boolean(self.request.GET.get('v22general'))
        v23town = parse_boolean(self.request.GET.get('v23town'))

        if party:
            queryset = queryset.filter(party_affiliation=party)
        if min_dob:
            queryset = queryset.filter(date_of_birth__gte=min_dob)
        if max_dob:
            queryset = queryset.filter(date_of_birth__lte=max_dob)
        if voter_score:
            queryset = queryset.filter(voter_score=voter_score)
        if v20state is not None:
            queryset = queryset.filter(v20state=v20state)
        if v21town is not None:
            queryset = queryset.filter(v21town=v21town)
        if v21primary is not None:
            queryset = queryset.filter(v21primary=v21primary)
        if v22general is not None:
            queryset = queryset.filter(v22general=v22general)
        if v23town is not None:
            queryset = queryset.filter(v23town=v23town)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Generate the Birth Year Distribution histogram
        birth_years = self.get_queryset().values_list('date_of_birth', flat=True)
        birth_year_counts = {}
        for birth_year in birth_years:
            year = birth_year.year
            if year not in birth_year_counts:
                birth_year_counts[year] = 0
            birth_year_counts[year] += 1

        birth_year_chart = go.Figure(
            data=[go.Bar(x=list(birth_year_counts.keys()), y=list(birth_year_counts.values()))]
        )
        birth_year_chart.update_layout(title='Birth Year Distribution')
        context['birth_year_chart'] = birth_year_chart.to_html(full_html=False)

        party_counts = self.get_queryset().values('party_affiliation').annotate(count=Count('party_affiliation'))
        party_labels = [entry['party_affiliation'] for entry in party_counts]
        party_values = [entry['count'] for entry in party_counts]

        party_chart = go.Figure(
            data=[go.Pie(labels=party_labels, values=party_values)]
        )
        party_chart.update_layout(title='Party Affiliation Distribution')
        context['party_chart'] = party_chart.to_html(full_html=False)

        election_counts = {
            '2020 State': self.get_queryset().filter(v20state=True).count(),
            '2021 Town': self.get_queryset().filter(v21town=True).count(),
            '2021 Primary': self.get_queryset().filter(v21primary=True).count(),
            '2022 General': self.get_queryset().filter(v22general=True).count(),
            '2023 Town': self.get_queryset().filter(v23town=True).count(),
        }

        election_chart = go.Figure(
            data=[go.Bar(x=list(election_counts.keys()), y=list(election_counts.values()))]
        )
        election_chart.update_layout(title='by Election')
        context['election_chart'] = election_chart.to_html(full_html=False)

        return context