# display an animated GIF image file using wxPython
# tested with Python24 and wxPython26    vegaseat   22nov2005
import wx
import wx.animate     
import urllib
from weatheralerts import WeatherAlerts
import json
import os.path
import iso8601
import warnings
import imghdr
import tempfile
warnings.simplefilter('ignore')


##### Begin win32 API code for hiding taskbar
import ctypes
from ctypes import wintypes

taskBarVis=1


FindWindow = ctypes.windll.user32.FindWindowA
FindWindow.restype = wintypes.HWND
FindWindow.argtypes = [
    wintypes.LPCSTR, #lpClassName
    wintypes.LPCSTR, #lpWindowName
]

SetWindowPos = ctypes.windll.user32.SetWindowPos
SetWindowPos.restype = wintypes.BOOL
SetWindowPos.argtypes = [
    wintypes.HWND, #hWnd
    wintypes.HWND, #hWndInsertAfter
    ctypes.c_int,  #X
    ctypes.c_int,  #Y
    ctypes.c_int,  #cx
    ctypes.c_int,  #cy
    ctypes.c_uint, #uFlags
] 

FindWindowEx = ctypes.windll.user32.FindWindowExA
FindWindowEx.restype = wintypes.HWND
FindWindowEx.argtypes = [
   wintypes.HWND, # hwndParent
   wintypes.HWND, # hwndChildAfter
   wintypes.LPCSTR, # lpszClass
   wintypes.LPCSTR, # lpszWindow
]

start_atom = wintypes.LPCSTR(0xc017)
TOGGLE_HIDEWINDOW = 0x80
TOGGLE_UNHIDEWINDOW = 0x40


def hide_taskbar():
	global taskBarVis
	handleW1 = FindWindow(b"Shell_traywnd", b"")
	SetWindowPos(handleW1, 0, 0, 0, 0, 0, TOGGLE_HIDEWINDOW)
	hStart = FindWindowEx(None, None, start_atom, None)
	SetWindowPos(hStart, 0, 0, 0, 0, 0, TOGGLE_HIDEWINDOW)
	taskBarVis=0

def unhide_taskbar():
	global taskBarVis
	handleW1 = FindWindow(b"Shell_traywnd", b"")
	SetWindowPos(handleW1, 0, 0, 0, 0, 0, TOGGLE_UNHIDEWINDOW)
	hStart = FindWindowEx(None, None, start_atom, None)
	SetWindowPos(hStart, 0, 0, 0, 0, 0, TOGGLE_UNHIDEWINDOW)
	taskBarVis=1

def toggleTaskBar(event):
	if taskBarVis:
		hide_taskbar()
	else:
		unhide_taskbar()
		
	
##### End win32 API code for hiding taskbar


##### Begin default parameters

# These will be overridden by the config file.  If one param isn't specified in config,
# these default values will ensure it still works and doesn't crash

radShiftX=0
radShiftY=0
radImgSizeX=320
radImgSizeY=240
refreshRadarTime=150000
refreshNWSTime=600000
SAMEcode="055133"
radarUrl="http://radar.weather.gov/Conus/Loop/NatLoop_Small.gif"
zipCode="53186"
alertBgColor="white"
alertFgColor="red"
alertFontSize=12
panelBgColor="black"
##### End default parameters

##### Begin config file loading
try:
	with open(os.environ['ProgramData'] + "\\radar_loop\config.json",'r') as fp:
		config=json.load(fp)
	radShiftX = config["radShiftX"]
	radShiftY=config["radShiftY"]
	radImgSizeX=config["radImgSizeX"]
	radImgSizeY=config["radImgSizeY"]
	refreshRadarTime=config["refreshRadarTime"]
	refreshNWSTime=config["refreshNWSTime"]
	SAMEcode=str(config["SAMEcode"])
	radarUrl=config["radarUrl"]
	zipCode=str(config["zipCode"])
	alertBgColor=config["alertBgColor"]
	alertFgColor=config["alertFgColor"]
	alertFontSize=config["alertFontSize"]
	panelBgColor=config["panelBgColor"]
except ValueError:
	print "Error parsing config file"
except Exception:
	pass
##### End config file loading

# Get path to the file we will use to save the radar loop
tempFileName = os.path.join(tempfile.gettempdir(), "lastradar.gif")

# Replace any parameters in the URL for any dynamically generated radar loops
radarUrl= radarUrl % {'radImgSizeX': radImgSizeX, 'radImgSizeY': radImgSizeY, 'zipCode': zipCode}

# Some example radar URLs that can work:
# "http://www.adiabatic.weather.net/cgi-bin/razradar.cgi?zipcode=53186&width=%d&height=%d"
# Regional Radar url: http://www.tephigram.weather.net/cgi-bin/razradar.cgi?zipcode=53186&width=720&height=486



##### Begin NWS updater code
def updateNWS(event):
	#try:
		nws=WeatherAlerts(samecodes=SAMEcode)
		stopAlert()
		if nws.alerts:
			startAlert()
			alertList = list()
			for alert in nws.alerts:
				#print "%s until %s" % (alert.event, iso8601.parse_date(alert.expiration).strftime("%I:%M %p on %m/%d"))
				alertList.append(alert.event + iso8601.parse_date(alert.expiration).strftime(" until %I:%M %p on %m/%d"))
			alertText.SetLabel("\r\n".join(alertList))	
			adjustLayout()
		else:
			#print "No Alerts for", SAMEcode
			stopAlert()
	#except Exception:
	#	pass
##### End NWS updater code

		
def adjustLayout():
	alertSize=alertText.GetClientSize().y
	frame.SetSizeWH(radImgSizeX+3,radImgSizeY+3+alertSize)
	panel.SetSizeWH(panel.GetClientSize().x,panel.GetClientSize().y+alertSize)
	frame.Move(((screenX-frame.GetClientSize().x), (screenY-frame.GetClientSize().y)))
	ag.Move((radShiftX,radShiftY+alertSize))
	alertText.SetSizeWH(frame.GetClientSize().x,alertText.GetClientSize().y)
	
def updateRadar(event):
	try:
		urllib.urlretrieve(radarUrl, tempFileName)
		if imghdr.what(tempFileName) == 'gif':
			ag.LoadFile(tempFileName,wx.animate.ANIMATION_TYPE_ANY)
			ag.Play()
	except IOError:
		pass

# startAlert() is called when the NWS update function finds an active alert
def startAlert():
	# Start radar update timer
	radtimer.Start(refreshRadarTime)
	updateRadar(None)
	# Show the radar window
	frame.Show(True)
	# Fix some buginess with screen refreshes
	frame.Iconize(True)
	frame.Iconize(False)
	hide_taskbar()

# stopAlert is called anytime the NWS update function doesn't find any active alerts
def stopAlert():
	# Stop radar update timer
	radtimer.Stop()
	frame.Show(False)

	
##### End functions and setup section
	

	
##### Begin main execution code
	
# Create the basic app/ui framework
app = wx.PySimpleApp()

# Get our screen resolution
screenX = wx.SystemSettings_GetMetric(wx.SYS_SCREEN_X)
screenY = wx.SystemSettings_GetMetric(wx.SYS_SCREEN_Y)

# create a window/frame, no parent, -1 is default ID
# Size it based on the config, add 3px for the framing border
frame = wx.Frame(None, -1, "Radar Loop", size = (radImgSizeX+3,radImgSizeY+3), style=wx.SYSTEM_MENU|wx.MINIMIZE_BOX|wx.MAXIMIZE_BOX|wx.CLOSE_BOX|wx.STAY_ON_TOP)

# Create a panel inside the frame
panel = wx.Panel(frame,-1)

# Color for any part of the panel that doesn't get covered.  Normally shouldn't see this but black can hide any minor
# sizing inaccuracies
panel.SetBackgroundColour(panelBgColor)

# Create the animation control object that will play the GIF
ag = wx.animate.AnimationCtrl(panel, -1)

# Create and set the parameters for the alert text box
alertText = wx.StaticText(panel, -1)
alertText.SetBackgroundColour(alertBgColor)
alertText.SetForegroundColour(alertFgColor)
alertText.SetFont(wx.Font(alertFontSize, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.FONTWEIGHT_BOLD))

# Redraw and adjust all our UI elements so they are positioned correctly
adjustLayout()

# Create radar update timer & register handler
# This updates the radar images when there is an active alert
radtimer = wx.Timer(panel, 100)
wx.EVT_TIMER(panel,100,updateRadar)

# Create NWS data update timer, register handler & start
# This is the timer that updates the actual alert data
nwstimer = wx.Timer(panel, 101)
wx.EVT_TIMER(panel,101,updateNWS)
nwstimer.Start(refreshNWSTime)

# Make sure we grab new data right away, otherwise we have to wait a full timer interval for the first check
updateNWS(None)

# Register global hotkey for hiding/showing the taskbar (ALT-T)
frame.RegisterHotKey(100,wx.MOD_ALT,84)
# Bind hotkey event handler
frame.Bind(wx.EVT_HOTKEY, toggleTaskBar, None, 100)


# start the event loop
app.MainLoop()

unhide_taskbar()