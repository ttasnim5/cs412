from collections import Counter
from django.shortcuts import render
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView
from . models import Voter

import plotly
import plotly.graph_objs as go

class VotersListView(ListView):
    '''View to display voter results'''
    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 50

    def get_queryset(self):
        qs = super().get_queryset().order_by('voter_id')

        # Retrieve filter parameters from request
        first_name = self.request.GET.get('first_name', '').strip()
        last_name = self.request.GET.get('last_name', '').strip()
        min_dob = self.request.GET.get('min_dob', '').strip()
        max_dob = self.request.GET.get('max_dob', '').strip()
        party = self.request.GET.get('party', '')
        voterscore = self.request.GET.get('voterscore', '').strip()

        # Boolean fields for election participation
        v20state = self.request.GET.get('v20state')
        v21town = self.request.GET.get('v21town')
        v21primary = self.request.GET.get('v21primary')
        v22general = self.request.GET.get('v22general')
        v23town = self.request.GET.get('v23town')

        # Apply filters conditionally
        if first_name:
            qs = qs.filter(first_name__icontains=first_name)
        if last_name:
            qs = qs.filter(last_name__icontains=last_name)
        if min_dob:
            qs = qs.filter(date_of_birth__gte=min_dob)
        if max_dob:
            qs = qs.filter(date_of_birth__lte=max_dob)
        if party:
            qs = qs.filter(party=party)
        if voterscore:
            qs = qs.filter(voterscore=voterscore)

        # Apply boolean filters for election participation
        if v20state:
            qs = qs.filter(v20state=True)
        if v21town:
            qs = qs.filter(v21town=True)
        if v21primary:
            qs = qs.filter(v21primary=True)
        if v22general:
            qs = qs.filter(v22general=True)
        if v23town:
            qs = qs.filter(v23town=True)

        return qs

    
class VoterDetailView(DetailView):
    '''View to show detail page for one result.'''
    template_name = 'voter_analytics/voter.html'
    model = Voter
    context_object_name = 'v'

class VoterGraphsView(ListView):
    '''View to show detail page for one result.'''
    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = 'v'

    def get_context_data(self, **kwargs) :
        '''Provide context variables for use in template'''
        # start with superclass context
        context = super().get_context_data(**kwargs)
        v = context.get('v')
        qs = super().get_queryset()

        # pie chart of parties
        x= ['U', 'D', 'R', 'L']
        y = [len(qs.filter(party='U ')), len(qs.filter(party='D ')), len(qs.filter(party='R ')), len(qs.filter(party='L '))]
        
        fig = go.Figure(data=[go.Pie(labels=x, values=y)])
        fig.update_layout(title_text="Party Affiliations")

        # render
        parties_graph = plotly.offline.plot(fig, auto_open=False, output_type="div")
        context['parties_graph'] = parties_graph

        # bar chart of dobs
        birth_years = [voter.date_of_birth.year for voter in qs if voter.date_of_birth]
        birth_year_counts = Counter(birth_years)

        # separate the keys and values for the bar chart
        x = sorted(birth_year_counts.keys())  # sorted list of years
        y = [birth_year_counts[year] for year in x]  # counts for each year in sorted order

        fig = go.Figure(data=[go.Bar(x=x, y=y)])
        fig.update_layout(title_text="Distribution of Voter Birth Years", 
                          xaxis_title="Year of Birth", 
                          yaxis_title="Number of Voters")

        # render
        birth_year_distribution_graph = plotly.offline.plot(fig, auto_open=False, output_type="div")
        context['birth_year_distribution_graph'] = birth_year_distribution_graph

        # bar chart of election participation
        counts = {
            'State Election 2020': qs.filter(v20state=True).count(),
            'Town Election 2021': qs.filter(v21town=True).count(),
            'Primary 2021': qs.filter(v21primary=True).count(),
            'General Election 2022': qs.filter(v22general=True).count(),
            'Town Election 2023': qs.filter(v23town=True).count(),
        }

        fig = go.Figure(data=[go.Bar(x=list(counts.keys()), y=list(counts.values()))])
        fig.update_layout(title_text="Recent Election Participation", 
                          xaxis_title="Election", 
                          yaxis_title="Number of Voters")

        # render
        elections_graph = plotly.offline.plot(fig, auto_open=False, output_type="div")
        context['elections_graph'] = elections_graph

        return context
