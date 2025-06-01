#!/usr/bin/env python3

import pytz

MENU_ICON = ":material/sunny:"
EXPANDER_ICON = ":sunny: "
TAB_ICON = ":sunflower:"

SUCCESS_ICON = "✅"
INFO_ICON = "ℹ️"
WARNING_ICON = "⚠️"
ERROR_ICON = "❌"

US_EASTERN = pytz.timezone('US/Eastern')
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S %Z"

DATA_FORMATS = ["csv", "txt", "xlsx", "parquet"]
SAVE_DATA_FORMATS = ["csv", "parquet"]

AGG_FUNCTIONS = ["nunique", "count", "sum", "min","median", "mean", 'max', "var", "std"]

# If the number of cells exceed the MAX_CELLS, don't display all records using st.dataframe
# It would have performance issue and the server/browser will hang.
# Instead, users select to display top/bottom/random N (up to 100) rows

# MAX_CELLS = 100 for testing
MAX_CELLS = 1000000 

PLOTLY_CONFIG = {
    'editable': True, 
    'edits' : {'titleText': False, 
                "axisTitleText": True,
                'annotationText' : True, 
                'annotationPosition' : True,
                "shapePosition": True,
                'legendPosition' : True,
                'legendText' : False},
    'modeBarButtonsToAdd':['drawline',
                            'drawopenpath',
                            'drawclosedpath',
                            'drawcircle',
                            'drawrect',
                            'eraseshape'],
    'toImageButtonOptions' : {'scale' : 2}
}   


