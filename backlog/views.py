# backlog/views.py
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy, reverse
from django.forms.models import inlineformset_factory

from backlog.charts import BurndownChart
from backlog.models import UserStory, TimeRecord, TrackHours, Sprint


"""
five UserStory views:
    1 - IndexView - displays a list of all user stories
    2 - DetailVeiw - displays all of the attributes of a UserStory object
                and a list of TimeRecords that have that UserStory as a 
                foreign key
    3 - UserStoryCreate - displays a form to create a new user story
                saves it to the database, and displays its DetailView on success
    4 - UserStoryUpdate - displays a form to modify an existing user story, 
                savies it to the database, and displays its DetailView on success
    5 - UserStoryDelete - displays a confirm form, deletes record from database
                and displays IndexView on success
"""
class IndexView(generic.ListView):
    model = UserStory
    template_name = 'backlog/index.html'
    context_object_name = 'backlog_list'

class DetailView(generic.DetailView):
    model = UserStory
    template_name = 'backlog/detail.html'
    
    def get_context_data(self, **kwargs):
        # call the base implementation
        context = super(DetailView, self).get_context_data(**kwargs)
        # add in a query set of time records
        #userstory = get_object_or_404(UserStory, title__iexact=self.args[0])
        userstory = context['object']
        context['time_records'] = TimeRecord.objects.filter(user_story=userstory)
        return context
    
class UserStoryCreate(CreateView):
    model = UserStory
    fields = ['title', 'description', 'validation', 'value', 'effort', 'assigned_to']
    
    def form_valid(self, form):
        form.instance.submitted_by = self.request.user
        return super(UserStoryCreate, self).form_valid(form)
    
class UserStoryUpdate(UpdateView):
    model = UserStory
    fields = ['title', 'description', 'validation', 'value', 'effort', 'assigned_to',
            'status', 'in_sprint']
    template_name_suffix = '_edit'

class UserStoryDelete(DeleteView):
    model = UserStory
    success_url = reverse_lazy('backlog:index')
    

"""
TIME RECORD VIEWS - there are 5 views
    1 - TimeRecordList - a list of all time records in database
    2 - TimeRecordVeiw - a detail view of one TimeRecord object
    3 - TimeRecordCreate - a form to submit, save a new TimeRecord
    4 - TimeRecordUpdate - a form to submit, save updates to existing TimeRecord
    5 - TimeRecordDelete - a form to delete an existing TimeRecord
"""
class TimeRecordList(generic.ListView):
    """ Shows a list of all time records """
    model = TimeRecord
    template_name = 'backlog/timerecords_list.html'
    context_object_name = 'time_records'

class TimeRecordView(generic.DetailView):
    """ shows a single time record """
    model = TimeRecord
    template_name = 'backlog/time_record.html'
    
class TimeRecordCreate(CreateView):
    model = TimeRecord
    fields = ['actual_time', 'estimated_time', 'user_story', 'day']
    
class TimeRecordUpdate(UpdateView):
    model = TimeRecord
    fields = ['actual_time', 'estimated_time', 'user_story', 'day']
    template_name = 'backlog/edit_time_record.html'

class TimeRecordDelete(DeleteView):
    model = TimeRecord
    success_url = reverse_lazy('backlog:hours_records')



#def submit(request, us_id):
#    us = get_object_or_404(UserStory, pk=us_id)

class SprintBacklogView(generic.ListView):
    """
    Shows a list of user stories that belong to the sprint
    """
    template_name = 'backlog/sprint_backlog.html'
    context_object_name = 'sprint_backlog'
    # queries user story objects that belong in the sprint
    queryset = UserStory.objects.filter(in_sprint=True)


def image_burndown_chart(request):
    """
    returns generated image of burndown chart
    """
    current_sprint = Sprint.objects.all()[0]
    
    current_sprint.update_time_sum()  #sum up hours

    chart = BurndownChart()
    image = chart.draw_chart(current_sprint.get_data(), 
                             current_sprint.sprint_days, 
                             current_sprint.productive_hours())
    image_data = image.asString('png')
    return HttpResponse(image_data, 'image/png')
    
    
"""
There are 5 views associated with the 
Sprint model:
    List - lists all sprint objects
    Detail - displays all of the attributes for a particular 
        sprint object
    Create - displays a form, submits data, creates new object
        saves a record in database, redirects to detail view upon 
        successful creation
    Update - displays a form, submits data, updates record in 
        database, redirects to detail view upon success
    Delete - displays confirm prompt, deletes record from database, 
        displays list view upon success.
"""
class SprintListView(generic.ListView):
    model = Sprint
    template_name = 'backlog/sprint_list.html'
    
class SprintDetailView(generic.DetailView):
    model = Sprint
    template_name = 'backlog/settings.html'
    
class SprintCreateView(CreateView):
    model = Sprint
    fields = ['sprint_days', 'start_date', 'num_dev']
    
class SprintUpdateView(UpdateView):
    model = Sprint
    fields = ['sprint_days', 'start_date', 'num_dev']
    template_name_suffix = '_edit'

class SprintDeleteView(DeleteView):
    model = Sprint
    success_url = reverse_lazy('backlog:settings')