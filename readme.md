Radar Loop
==========

# Overview
This small project is designed for use in digital signage displays.  When run, it sits silently in the background and queries the NWS CAP feeds for current alerts.  If an alert is active for the configured area, it makes itself visible and downloads & displays a configurable GIF animation.  Above the animation, the alert type and duration will be shown for all active alerts.

The intent of the image is for it to download a radar loop animated GIF from either the NWS or another provider.  If using another provider, be sure you are allowed to use the data in this way, especially for commercial purposes.  NWS data and images are released in the public domain and so are a safe bet.

# Requirements
The following extra modules are used in this project:

 - wxPython
 - WeatherAlerts (http://github.com/zebpalmer/WeatherAlerts)
 - iso8601

# Configuration
Configurable parameters are stored as JSON in a config.json file alongside the app.  See below for the list of options that should all pre present in the config file.

## Parameters	
<table>
	<tr>
		<th>Parameter</th> <th>Type</th> <th>Description</th>
	</tr>
	<tr>
		<td>radShiftX</td> <td>Int</td> <td>Shift the entire image horizontally.  Useful if the configured viewport size is smaller than the loaded image size</td>
	</tr>
	<tr>
		<td>radShiftY</td> <td>Int</td> <td>Shift the entire image vertically.  Useful if the configured viewport size is smaller than the loaded image size</td>
	</tr>
	<tr>
		<td>radImgSizeX</td> <td>Int</td> <td>The horizontal pixel size to use for the image viewport.  This will also be substituted into the URL as the first parameter if one exists.</td>
	</tr>
	<tr>
		<td>radImgSizeY</td> <td>Int</td> <td>The vertical pixel size to use for the image viewport.  This will also be substituted into the URL as the second parameter if one exists.</td>
	</tr>
	<tr>
		<td>refreshRadarTime</td> <td>Int</td> <td>Time in milliseconds to refresh the image when an alert is active.</td>
	</tr>
	<tr>
		<td>refreshNWSTime</td> <td>Int</td> <td>Time in milliseconds to refresh the NWS alert infomation.  Try not to hammer their servers too hard - 10 minutes between updates is likely sufficient</td>
	</tr>
	<tr>
		<td>SAMEcode</td> <td>String</td> <td>The SAME code(s) for the area(s) to check for alerts.  Note that this is string data.  For multiple SAME codes, format this as an array of strings.</td>
	</tr>
	<tr>
		<td>radarUrl</td> <td>String</td> <td>The URL to query for a radar image.  NWS has gif loops for regional radar at http://radar.weather.gov/lite/.  See http://www.srh.noaa.gov/jetstream/doppler/radarfaq.htm for more details.</td>
	</tr>
	<tr>
		<td>alertBgColor</td> <td>String</td> <td>Background color for the alert text area.</td>
	</tr>
	<tr>
		<td>alertFgColor</td> <td>String</td> <td>Text color for the alert text.</td>
	</tr>
	<tr>
		<td>alertFontSize</td> <td>Int</td> <td>Font size for the alert text.</td>
	</tr>
	<tr>
		<td>panelBgColor</td> <td>String</td> <td>Background color for the entire wxWidgets panel.  Normally this won't be seen at all, unless your image is smaller than the given viewport.</td>
	</tr>
</table>

`http://radar.weather.gov/Conus/Loop/NatLoop_Small.gif`
# License
##Zlib License
Copyright (c) 2013 Chris Burger

This software is provided 'as-is', without any express or implied
warranty. In no event will the authors be held liable for any damages
arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to the following restrictions:

   1. The origin of this software must not be misrepresented; you must not
   claim that you wrote the original software. If you use this software
   in a product, an acknowledgment in the product documentation would be
   appreciated but is not required.

   2. Altered source versions must be plainly marked as such, and must not be
   misrepresented as being the original software.

   3. This notice may not be removed or altered from any source
   distribution.