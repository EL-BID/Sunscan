import pandas as pd
import numpy as np
import datetime
import time
from astral import LocationInfo
from astral import sun
import pytz


def sunlight_hours(lat,lon,start,end,excel_out):
  #date example=2019-01-01
  data = {}
  data['sunrise'] = []
  data['sunset'] = []
  data['noon'] = []
  delta = end - start

  for day in range(delta.days + 1):
      t_start = time.time()
      this_date = str((start+datetime.timedelta(days=day)).date())
      #print(this_date)
      params = {'lat':lat,'lng':lon,'date':this_date}
      #tz = pytz.timezone('Asia/Kolkata')
      l = LocationInfo()
      l.name = 'name'
      l.region = 'region'
      l.latitude = lat
      l.longitude = lon
      #print(l.observer)
      s = sun.sun(l.observer, date=start+datetime.timedelta(days=day)#,tzinfo=tz
                  )
      data['sunrise'].append(s["sunrise"].time().strftime('%H:%M:%S'))
      data['sunset'].append(s["sunset"].time().strftime('%H:%M:%S'))
      data['noon'].append(s["noon"].time().strftime('%H:%M:%S'))
  
  df=pd.DataFrame(data)
  df['noon'] = pd.to_datetime(df['noon'], format='%H:%M:%S').dt.time
  df['sunrise'] = pd.to_datetime(df['sunrise'], format='%H:%M:%S').dt.time
  df['sunset'] = pd.to_datetime(df['sunset'], format='%H:%M:%S').dt.time

  df['dif_sec'] = (pd.to_timedelta(df['noon'].astype(str)) -
                                  pd.to_timedelta(df['sunrise'].astype(str))).dt.total_seconds()
  df['sunlight_hours'] = (df['dif_sec']/60)/60
  sunlight_hours_sum= np.sum((df['dif_sec']/60)/60)
  df.to_excel(excel_out)
  return sunlight_hours_sum
