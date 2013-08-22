#!/usr/bin/env python

import wx
from wx.lib.floatcanvas import NavCanvas, FloatCanvas  
class FigFrame(wx.Frame):
    """create a color frame, inherits from wx.Frame"""
    PhotoMaxSize=800
    NewW = 0
    NewH = 0
    def __init__(self, parent):
        # -1 is the default ID
        wx.Frame.__init__(self, parent, -1, "LeftClick set Min, RightClick set Max",
                         style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        self.parent = parent        
        self.__OpenFig()
        self.Center()

    def __OpenFig(self):
        filename = self.parent.txtctrlPath.GetValue()
        self.panel= wx.Panel(self,-1)
        self.panel.SetBackgroundColour(wx.BLUE)
        self.img = wx.Image(filename, wx.BITMAP_TYPE_ANY)
        W = self.img.GetWidth()
        H = self.img.GetHeight()
        if W > H:
            self.NewW = self.PhotoMaxSize
            self.NewH = self.PhotoMaxSize * H / W
        else:
            self.NewH = self.PhotoMaxSize
            self.NewW = self.PhotoMaxSize * W / H
        self.img = self.img.Scale(self.NewW,self.NewH)
        self.bmp = wx.StaticBitmap(self.panel,0,self.img.ConvertToBitmap())   
        self.bmp.SetCursor(wx.StockCursor(wx.CURSOR_CROSS))
        self.SetSize((self.NewW,self.NewH))
        self.panel.Refresh()
             
        # hook some mouse events
        self.bmp.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.bmp.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
    
        
    def OnLeftDown(self, event):
        """left mouse button is pressed"""
        pt = event.GetPosition()  # position tuple
        self.SetTitle('LeftMouse = ' + str(pt[0])+',' +str(self.NewH-pt[1]))
        if self.parent.rdbtmdata.GetValue()==True:
            print 'original coordinate: '+str(pt)
            self.SetTitle('LeftMouse. Read Data: ' + str(pt[0])+',' +str(self.NewH-pt[1]))
            xout,yout = self.calculate(pt[0],(self.NewH-pt[1]))
            self.parent.txtctrlPnt.write('['+str(xout)+','+str(yout)+'],\n')
        elif self.parent.rdbtmlim.GetValue()==True:
            print 'original coordinate: '+str(pt)
            self.SetTitle('LeftMouse. Set Lim: ' + str(pt[0])+',' +str(self.NewH-pt[1]))
            self.parent.labelgetxmin.SetValue(str(pt[0]))
            self.parent.labelgetymin.SetValue(str(self.NewH-pt[1]))           
            
    def OnRightDown(self, event):
        """right mouse button is pressed"""
        pt = event.GetPosition()
        if self.parent.rdbtmdata.GetValue()==True:
            print 'original coordinate: '+str(pt)
            self.SetTitle('RightMouse. Read Data: ' + str(pt[0])+',' +str(self.NewH-pt[1]))
            xout,yout = self.calculate(pt[0],(self.NewH-pt[1]))
            self.parent.txtctrlPnt.write('['+str(xout)+','+str(yout)+'],\n')
        elif self.parent.rdbtmlim.GetValue()==True:
            print 'original coordinate: '+str(pt)
            self.SetTitle('RightMouse. Set Lim: ' + str(pt[0])+',' +str(self.NewH-pt[1]))
            self.parent.labelgetxmax.SetValue(str(pt[0]))
            self.parent.labelgetymax.SetValue(str(self.NewH-pt[1])) 
    
    def calculate(self,x,y):
        xpmin = float(self.parent.labelgetxmin.GetValue())
        xpmax = float(self.parent.labelgetxmax.GetValue())
        ypmin = float(self.parent.labelgetymin.GetValue())
        ypmax = float(self.parent.labelgetymax.GetValue())
        
        xvmin = float(self.parent.txtctrlxmin.GetValue())
        xvmax = float(self.parent.txtctrlxmax.GetValue())
        yvmin = float(self.parent.txtctrlymin.GetValue())
        yvmax = float(self.parent.txtctrlymax.GetValue())
        
        xres = xvmin+1.0*(x-xpmin)/(xpmax-xpmin)*(xvmax-xvmin)
        yres = yvmin+1.0*(y-ypmin)/(ypmax-ypmin)*(yvmax-yvmin) 
        print '(xres, yres): ('+str(xres)+','+str(yres)+')\n' 
        return (xres,yres)

class MainFrame(wx.Frame):
    def __init__(self,*args, **kwds):
        """initialize and create widgets"""
        wx.Frame.__init__(self, None, size=(400,300), title='MainFrame')
        self.btnOpenFig = wx.Button(self,-1,'Open a Figure',size=(-1,-1))
        self.txtctrlPath = wx.TextCtrl(self, -1, size=(200,-1))
        
        self.labelaxis = wx.StaticText(self, -1, label='Axis Mapping')
        self.labelxmin = wx.StaticText(self, -1, label='X min: ')
        self.labelxmax = wx.StaticText(self, -1, label=' X max: ')
        self.labelymin = wx.StaticText(self, -1, label='Y min: ')
        self.labelymax = wx.StaticText(self, -1, label=' Y max: ')
        
        self.labelgetxmin = wx.TextCtrl(self, -1, style=wx.TE_READONLY)
        self.labelgetxmax = wx.TextCtrl(self, -1, style=wx.TE_READONLY)
        self.labelgetymin = wx.TextCtrl(self, -1, style=wx.TE_READONLY)
        self.labelgetymax = wx.TextCtrl(self, -1, style=wx.TE_READONLY)
        
        self.labelforxmin = wx.StaticText(self, -1, label=' for')
        self.labelforxmax = wx.StaticText(self, -1, label=' for')
        self.labelforymin = wx.StaticText(self, -1, label=' for')
        self.labelforymax = wx.StaticText(self, -1, label=' for')
        
        self.txtctrlxmin = wx.TextCtrl(self,-1)
        self.txtctrlxmax = wx.TextCtrl(self,-1)
        self.txtctrlymin = wx.TextCtrl(self,-1)
        self.txtctrlymax = wx.TextCtrl(self,-1)
        
        self.rdbtmlim = wx.RadioButton(self,-1,'Set Lims ')
        self.rdbtmdata = wx.RadioButton(self,-1,'Read Data')
        self.txtctrlPnt = wx.TextCtrl(self,-1, style = wx.TE_MULTILINE)
        
        # bind event
        self.Bind(wx.EVT_BUTTON, self.hdlOpenFig, self.btnOpenFig)
        
        self.__layout()
 
    def __layout(self):
         sizer0 = wx.BoxSizer(wx.VERTICAL)
         self.SetSizer(sizer0) 
         sizerOpenFig = wx.BoxSizer(wx.HORIZONTAL)
         
         sizerOpenFig.Add(self.txtctrlPath,1,wx.EXPAND)
         sizerOpenFig.Add(self.btnOpenFig, 0, wx.RIGHT)
         sizer0.Add(sizerOpenFig, 0, wx.EXPAND)
         
         sizerAxis = wx.BoxSizer(wx.VERTICAL)
         sizerAxis.Add(self.labelaxis, 0, wx.LEFT)
         sizerxmapping = wx.BoxSizer(wx.HORIZONTAL)
         sizerymapping = wx.BoxSizer(wx.HORIZONTAL)
         
         sizerxmapping.Add(self.labelxmin,0,wx.LEFT)
         sizerxmapping.Add(self.labelgetxmin,1,wx.EXPAND)
         sizerxmapping.Add(self.labelforxmin,0,wx.LEFT) 
         sizerxmapping.Add(self.txtctrlxmin,1,wx.EXPAND)
         sizerxmapping.Add(self.labelxmax,0,wx.LEFT)
         sizerxmapping.Add(self.labelgetxmax,1,wx.EXPAND)
         sizerxmapping.Add(self.labelforxmax,0,wx.LEFT) 
         sizerxmapping.Add(self.txtctrlxmax,1,wx.EXPAND)
          
         sizerymapping.Add(self.labelymin,0,wx.LEFT)
         sizerymapping.Add(self.labelgetymin,1,wx.EXPAND)
         sizerymapping.Add(self.labelforymin,0,wx.LEFT) 
         sizerymapping.Add(self.txtctrlymin,1,wx.EXPAND)
         sizerymapping.Add(self.labelymax,0,wx.LEFT)
         sizerymapping.Add(self.labelgetymax,1,wx.EXPAND)
         sizerymapping.Add(self.labelforymax,0,wx.LEFT) 
         sizerymapping.Add(self.txtctrlymax,1,wx.EXPAND)
         
         sizer0.Add(sizerAxis,0,wx.EXPAND)
         sizer0.Add(sizerxmapping,0,wx.EXPAND)
         sizer0.Add(sizerymapping,0,wx.EXPAND)
         
         sizerRadBtn = wx.BoxSizer(wx.HORIZONTAL)
         sizerRadBtn.Add(self.rdbtmlim)
         sizerRadBtn.Add(self.rdbtmdata)
         
         sizerPnt = wx.BoxSizer(wx.VERTICAL)
         sizerPnt.Add(sizerRadBtn, 0, wx.LEFT)
         sizerPnt.Add(self.txtctrlPnt,1,wx.EXPAND)
         sizer0.Add(sizerPnt,1,wx.EXPAND)
         

         
    def hdlOpenFig(self,event):
        """   Browse for file         """
        wildcard = "pictures (*.jpeg,*.png)|*.jpeg;*.png"
        dialog = wx.FileDialog(None, "Choose a file",
                               wildcard=wildcard,
                               style=wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.txtctrlPath.SetValue(dialog.GetPath())
            dialog.Destroy() 
            self.child = FigFrame(self)
            self.child.Show()
        else:
            pass
    
if __name__=='__main__':
    app = wx.PySimpleApp()
    frame = MainFrame()
    frame.Show(True)
    app.MainLoop()