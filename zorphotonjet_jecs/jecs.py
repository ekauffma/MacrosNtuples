## Function to get prepare the correct JEC file based on year, era and Data/MC

def JECsInit(year, era, isData):

    period  = ''

    if year == 2022:
       JECversion = 'V2'
       if era in ['C','D']:
          JECtag     = '2022_Summer22'
          JECname    = 'Summer22_22Sep2023'
          period     = 'CD'
       else:
          JECtag     = "2022_Summer22EE"
          JECname    = "Summer22EE_22Sep2023"
          period     = era
    else:
       JECversion = 'V1'
       if era == 'C':
          JECtag     = '2023_Summer23'
          JECname    = 'Summer23Prompt23'
          period += 'v4'
       else:
          JECtag     = '2023_Summer23BPix'
          JECname    = 'Summer23BPixPrompt23'
       
    JECfile = f'JEC/{JECtag}/jet_jerc.json.gz'

    if isData:
       corrfile = f'{JECname}_Run{period}_{JECversion}_DATA_'
    else: 
       corrfile = f'{JECname}_{JECversion}_MC_'

    return JECfile, corrfile
