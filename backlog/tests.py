from django.test import TestCase
from backlog.models import Sprint, TimeRecord
from datetime import date, timedelta
    
cur_sprint = Sprint.objects.all()[0]

for day in range(cur_sprint.sprint_days):
    date = cur_sprint.start_date + timedelta(days=day)
    day_records = TimeRecord.objects.filter(day=str(date))
    tot_est = 0
    tot_act = 0
    for record in day_records:
        tot_est = tot_est + record.estimated_time
        tot_act = tot_act + record.actual_time
    item = TrackHours.objects.get(day_of_sprint=day)
    item.total_estimated_hours=tot_est
    item.total_actual_hours=tot_act
    item.save