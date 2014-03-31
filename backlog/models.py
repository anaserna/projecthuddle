# backlog/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from datetime import date, timedelta
from django.db import IntegrityError


class UserStory(models.Model):
    """
    UserStory Model class: User stories are objects that are
    saved in database.
    """
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500, default="As a <user/persona> \
        I want to <take this action> so that <I get this result>")
    validation = models.CharField(max_length=200, default="When I <take this action>, \
        <this happens>")
    
    SCORE_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (5, '5'),
        (8, '8'),
        (13, '13'),
        (21, '21'),
        (34, '34'),
        (55, '55'),
        (89, '89'), 
        (144, '144'),
    )
    
    value = models.IntegerField(choices=SCORE_CHOICES, default=0)
    effort = models.IntegerField(choices=SCORE_CHOICES, default=1)   
    
    STATUS_CHOICES = (
        ('B', 'Backlog'),        #In Backlog, not begun
        ('S', 'Sprint'),         #In sprint, not begun
        ('P', 'In Progress'),   
        ('I', 'Integrate'),      
        ('D', 'Document'),
        ('T', 'Test'),
        ('C', 'Complete'),
        ('A', 'Accepted'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='B')
    
    submitted_by = models.ForeignKey(User, related_name="submitter")
    assigned_to = models.ForeignKey(User, related_name="developer", null=True)
    
    in_sprint = models.BooleanField(default=False)
    
    def relative_priority(self):
        return self.value / self.effort
    
    # returns a srting that identifies the object
    def __str__(self):
        return self.title
    
    # returns the default url of object, detail view in this case
    def get_absolute_url(self):
        return reverse('backlog:detail', kwargs={'pk': self.pk})



class TimeRecord(models.Model):
    """
    TimeRecord model - TimeRecord objects are records in the database
    that have a user story as a foreign key. One user story may have 
    many TimeRecords. A time record only belongs to one user story.
    Provides a record of work acutal and estimated hours
    This data is used to create the burndown chart
    """
    actual_time = models.IntegerField(default=0, help_text="Time in hours") 
    estimated_time = models.IntegerField(default=0, help_text="Time in hours")
    user_story = models.ForeignKey(UserStory)
    day = models.DateField()
    
    #there should only be one record per user story per day
    class Meta:
        unique_together = (("user_story", "day"),)
    
    #string that identifies a time record (eg '2013-03-17 - User Story Title' )
    def __str__(self):
            return str(self.day) + " - " + self.user_story
    
    #default url for object, the detail view of the object
    def get_absolute_url(self):
            return reverse('backlog:time_record', kwargs={'pk': self.pk})
        
        
        
class TrackHours(models.Model):
    """ 
    total actual and estimated hours by day
    """
    day_of_sprint = models.IntegerField(default=1, primary_key=True)
    total_estimated_hours = models.IntegerField(default=0)
    total_actual_hours = models.IntegerField(default=0)
    
    def get_est_point(self):
        est_point = (self.day_of_sprint, self.total_estimated_hours)
        return est_point
    
    def get_act_point(self):
        act_point = (self.day_of_sprint, self.total_actual_hours)
        return act_point
        
        

class Sprint(models.Model):
    """ 
    Sprint Model Class: the application must have only one sprint object defined.
    In the future, support multiple (future and past) sprints.
    """
    CHOICES = (
        (7, '1 Week'),
        (14, '2 Weeks'),
        (21, '3 Weeks'),
        (28, '4 Weeks'),
    )
    
    #length in days of sprint.
    sprint_days = models.IntegerField(choices=CHOICES, default=14)
    start_date = models.DateField()
    #number of developers that work on project
    num_dev = models.IntegerField(default=1) 
    
    def productive_hours(self):
        productive_hours = self.num_dev * 35  #assuming 40 hour work week
                                                #change this to be custimizable
        return productive_hours
    
    
    def update_time_sum(self):
        """ 
        Creates a table in DB of record of daily sum of hours 
        does not return a value, updates database
        """
        #loop for each day in sprint
        for day in range(self.sprint_days):
            
            date = self.start_date + timedelta(days=day)
            #get all the time records for each day of sprint
            day_records = TimeRecord.objects.filter(user_story__in_sprint=True,day=str(date))
            
            tot_est = 0
            tot_act = 0
            #for all of the records for each day add up the totals
            for record in day_records:
                tot_est = tot_est + record.estimated_time
                tot_act = tot_act + record.actual_time
                
            #create a record for each day of sprint
            try:
               TrackHours.objects.create(day_of_sprint=day,
                        total_estimated_hours=tot_est, total_actual_hours=tot_act)
            #or if a record for each day already exists, update it
            except IntegrityError:
                item = TrackHours.objects.get(day_of_sprint=day)
                item.total_estimated_hours=tot_est
                item.total_actual_hours=tot_act
                item.save()


    def get_data(self):
        """
        sprint_object.get_data() - Sprint class method
        returns a list of tuples that hold data points for each line to plot
        ie data = [ (line data), (line data)]
        where line data = (x1, y1), (x2, y2), ... etc
        returns data for two lines: estimated and actual hours (date, hours)
        dets data from TrackHours database table
        """
        #get all TrackHours records, each record has data for both lines to plot
        daily_data = TrackHours.objects.all()
        
        line_est = []   #will hold a list of points for estimated work left
        line_act = []   #will hold a list of points for work actually done
        for points in daily_data:
            line_est.append(points.get_est_point())   #add a data point for each day
            line_act.append(points.get_act_point())   #add a data point for each day
        #make each line list into a tuple
        line_est = tuple(line_est)
        line_act = tuple(line_act)
        
        #pack up data to send to chart
        data = []
        data.append(line_est)
        data.append(line_act)
        
        return data
    
    #identifies each Sprint object, returns a string
    def __str__(self):
            return str(self.start_date)
    
    #maps object to a url, in this case the detail view of the object
    def get_absolute_url(self):
            return reverse('backlog:view_sprint', kwargs={'pk': self.pk})