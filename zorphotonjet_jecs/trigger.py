import ROOT
import fnmatch
import re

## Function to initialize the list of triggers
def TriggerInit(df, channel):
    
    columns = []
    columnnames = df.GetColumnNames() # This will be class : cppyy.gbl.std.string
    for c in columnnames:
        columns.append(str(c))        # Transform it to string and put in list
 
    if channel == 'Photon':
       #triggers = fnmatch.filter(columns, 'HLT_Photon*EB_TightID_TightIso')              # Full list of triggers of interest
       #triggers = ['HLT_Photon30EB_TightID_TightIso', 'HLT_Photon110EB_TightID_TightIso']
       triggers = ['HLT_Photon110EB_TightID_TightIso']
       print('List of triggers to be used : ',triggers)  
  
    return triggers


## Function to construct the filter expression that checks whether at least on trigger has fired
def TriggerFired(triggers):

   trigger_fired = triggers[0]
   for t in triggers[1:]:
       trigger_fired += ' || ' + t

   return trigger_fired 


## Function to construct the filter expression that select events based on pt and trigger threshold
def TriggerSelect(triggers, channel = 'Photon'):
 
    # Create a list with all pt thresholds
    thresholds = [int(re.findall(r'\d+', t)[0]) for t in triggers if re.findall(r'\d+', t)]
    print('Trigger thresholds : ',thresholds)
    
    # We use a trigger considering 5 GeV to become efficient
    thresholds = list(map(lambda i: i + 5, thresholds))
    print('Trigger thresholds considering 5 GeV for efficiency: ',thresholds)

    expr = '('
    for i in range(len(thresholds)-1):
        expr += '(' + channel + '_pt>=' + str(thresholds[i]) + '&&' + channel + '_pt<' + str(thresholds[i+1]) + '&&' + triggers[i] + ')||'
    expr += '(' + channel + '_pt>=' + str(thresholds[-1]) + '&&' + triggers[-1] + '))'
    print('Expression for filtering events according to trigger information: ',expr)

    return expr
