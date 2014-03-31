# charts.py - uses report lab libraries to create a burndown chart
from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.lib import colors
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.graphics.charts.textlabels import Label
from reportlab.graphics.charts.legends import LineLegend

class BurndownChart(Drawing):
    
    def draw_chart(self, data, sprint_days, productive_hours):
        #set drawing properties
        self.width = 500
        self.height = 300
        #create a drawing
        drawing = Drawing(self.width,self.height)
        
        #create a line plot object
        lp = LinePlot()
        #add date to line plot
        lp.data = data
        #set line plot properties
        lp.x = 40
        lp.y = 40
        lp.height = self.height - 70
        lp.width = self.width - 70
        lp.joinedLines = True
        lp.lineLabelFormat = '%2.0f'
        lp.strokeColor = colors.black
        lp.lines[0].strokeColor = colors.red  #estimated hours
        lp.lines[0].symbol = makeMarker('FilledCircle')
        lp.lines[1].strokeColor = colors.blue  #actual hours
        lp.lines[1].symbol = makeMarker('FilledDiamond')
        # x range for chart 
        lp.xValueAxis.valueMin = 0
        lp.xValueAxis.valueMax = sprint_days
        lp.xValueAxis.valueStep = 1
        # y range for chart
        lp.yValueAxis.valueMin = 0
        lp.yValueAxis.valueMax = productive_hours
        lp.yValueAxis.valueStep = productive_hours / sprint_days
        # add line plot to drawings
        drawing.add(lp)
        
        # create a title label
        title = Label()
        # set the title properties
        title._text = 'Burndown Chart'
        title.fontSize = 20
        title.x = 270
        title.y = 290
        title.textAnchor = 'middle'
        # add title to chart
        drawing.add(title)
        
        # create a y axis label
        hours = Label()
        # set label properties
        hours._text = 'Hours'
        hours.fontSize = 16
        hours.x = 5
        hours.y = 150
        hours.textAnchor = 'middle'
        hours.angle = 90
        # add label to drawing
        drawing.add(hours)
        
        # create an x axis label
        days = Label()
        # set label properties
        days._text = 'Day of Sprint'
        days.fontSize = 16
        days.x = 260
        days.y = 10
        days.textAnchor = 'middle'
        #add label to drawing
        drawing.add(days)
        
        # create a lengend 
        legend = LineLegend()
        # set legend properties
        legend.x = 380
        legend.y = 260
        legend.colorNamePairs = [
            (colors.red, 'Estimated Hours'),
            (colors.blue, 'Actual Hours'),
        ]
        # add lengend to drawing
        drawing.add(legend)
        
        return drawing