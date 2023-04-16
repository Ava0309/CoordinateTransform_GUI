# coding=<Big5>
import os, sys
import wx
from math import sin, cos, tan, radians
from twd2latlon import TMToLatLon
from math import degrees,radians


class MainWindow(wx.Frame):
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent=None, id=wx.ID_ANY, title="sel轉檔", size=(540,540),style = wx.DEFAULT_FRAME_STYLE & ~wx.MAXIMIZE_BOX ^ wx.RESIZE_BORDER)

		# 加入一個 Panel
		panel = wx.Panel(self, wx.ID_ANY)
		
		# 轉檔格式提示字
		wx.StaticText(parent=panel,label="點擊欲轉檔之格式", pos=(15,10),size=(200,20))


		# 轉檔格式按鈕
		self.btn1 = wx.Button(parent=panel,label=" csv ",pos=(460,40),size=(60,20))
		self.Bind(wx.EVT_BUTTON, self.OnBtn1, self.btn1)

		self.btn2 = wx.Button(parent=panel,label=" kml ",pos=(460,80),size=(60,20))
		self.Bind(wx.EVT_BUTTON, self.OnBtn2, self.btn2)

		#顯示框
		self.txtCtrl = wx.TextCtrl(panel, id=wx.ID_ANY, style=wx.TE_MULTILINE, pos=(10,300), size=(510,180))
		self.a = wx.TextCtrl(parent=panel,id=wx.ID_ANY, style=wx.TE_MULTILINE, pos=(10,110),size=(510,180))


	# csv button
	def OnBtn1(self, evt):
		defaultDir =' '
		defaultFile =' '
		dlg = wx.FileDialog(self, "Choose a file", defaultDir, defaultFile, "*.*", wx.FD_OPEN)
		if dlg.ShowModal() == wx.ID_OK:
			self.filename = dlg.GetFilename()
			self.dirname = dlg.GetDirectory()
			f = open(os.path.join(self.dirname, self.filename), 'r')

			self.a.WriteText("E,N,Lon,Lat\n")
			count=0
			c = TMToLatLon()
			for line in f:
				count = count + 1
				if count <= 2:
					continue
				e_97 = float(line[17:27])
				n_97 = float(line[28:39])
				Lat,Lon=c.convert(e_97,n_97)
				self.a.WriteText("{},{},{},{}\n".format(e_97, n_97, Lon, Lat))


			data=self.a.GetValue()
			fout = open('output.csv',mode='w')
			fout.write(data)
			fout.close()
			f.close()
		dlg.Destroy()



	# kml button
	def OnBtn2(self, evt):
		kml='''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
  <name>ex2out\ex2.kml</name>
  <Style id="DownArrow">
     <IconStyle><Icon><href>https://earth.google.com/images/kml-icons/track-directional/track-8.png</href>
                </Icon><scale>0.6</scale></IconStyle></Style>
  <Style id="UpArrow">
     <IconStyle><Icon><href>https://earth.google.com/images/kml-icons/track-directional/track-0.png</href>
                </Icon><scale>0.6</scale></IconStyle></Style>
   <Folder>
     <name>Placemarks</name>
     <description>ex2out\ex2.kml</description>
     {}
   </Folder>
  </Document>
</kml>
'''
		defaultDir =' '
		defaultFile =' '
		dlg = wx.FileDialog(self, "Choose a file", defaultDir, defaultFile, "*.*", wx.FD_OPEN)
		if dlg.ShowModal() == wx.ID_OK:
			self.filename = dlg.GetFilename()
			self.dirname = dlg.GetDirectory()
			f = open(os.path.join(self.dirname, self.filename), 'r')

			placemarks=""
			count=0
			c = TMToLatLon()

			for line in f:
				count = count + 1
				if count <= 2:
					continue

				name = line[:15]
				e_97 = float(line[17:27])
				n_97 = float(line[28:39])
				H=float(line[73:81])
				DP=int(line[124:126])
				Lat,Lon=c.convert(e_97,n_97)

				if DP==18:
					arrow="DownArrow"
				else:
					arrow="UpArrow"
				placemark='''<Placemark>
				<name>{}</name>
				<description>({},{},{})</description>
				<styleUrl>#{}</styleUrl>
				<Point><altitudeMode>absolute</altitudeMode>
				    <coordinates>{},{},{}</coordinates></Point>
				</Placemark>'''.format(name,e_97, n_97,H,arrow,Lon,Lat,H)
				placemarks+=placemark+"\n"
			self.txtCtrl.WriteText(kml.format(placemarks))
			data=self.txtCtrl.GetValue()
			fout = open('output.kml',mode='w')
			fout.write(data)
			fout.close()
			f.close()
		dlg.Destroy()

# Every wxWidgets application must have a class derived from wx.App
class MyApp(wx.App):

	# wxWindows calls this method to initialize the application
	def OnInit(self):

		# Create an instance of our customized Frame class
		frame = MainWindow(None, -1, "sel Transformation")
		frame.Show(True)

		# Tell wxWindows that this is our main window
		self.SetTopWindow(frame)

		# Return a success flag
		return True
		
#---------------------------------------------------------------------------
	
if __name__ == '__main__':
	app = MyApp(0)
	app.MainLoop()



