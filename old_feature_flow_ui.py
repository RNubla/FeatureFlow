from sys import flags
import wx
import wx.adv
# from wx.core import DefaultSpan
import wx.lib.agw.pygauge as pb
import os
from feature_flow_interface import CheckResolution, Resolution720p, Resolution360p
import threading
from sequence_run import getInterpolationRange, getInterpolationIndex, getIteration
# from wx.lib.pubsub import Publisher


class MainWindow(wx.Frame):

    def __init__(self, parent, title):
        super(MainWindow, self).__init__(parent, title=title)


        self.InitUI()
        self.Centre()
        
        self.input_file_dir = ''
        self.input_file = ''
        self.output_path = ''
        self.pbar = None
        self.interpNum = 0

        # self.pbar = wx.Gauge(self, range=getInterpolationRange(), size = (100, 25), style =  wx.GA_HORIZONTAL)
        # sizer.Add(self.pbar,pos=(7,0), span=(1,6), flag=wx.EXPAND|wx.ALL, border=5)

    def OnQuit(self, e):
        self.Close()

    def OnAbout(self, e):
        description = ("""
                        A state-of-the-art Video Frame Interpolation Method using deep semantic flows blending. 
                        FeatureFlow: Robust Video Interpolation via Structure-to-texture Generation (IEEE 
                        Conference on Computer Vision and Pattern Recognition 2020)
                        Source Code: https://github.com/CM-BF/FeatureFlow.git
                        """)

        licence = """MIT License
        Copyright (c) 2019 Citrine, RNubla

        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files (the "Software"), to deal
        in the Software without restriction, including without limitation the rights
        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        copies of the Software, and to permit persons to whom the Software is
        furnished to do so, subject to the following conditions:

        The above copyright notice and this permission notice shall be included in all
        copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
        SOFTWARE."""

        info = wx.adv.AboutDialogInfo()

        info.SetName('Feature Flow App')
        info.SetVersion('v0.1.0')
        info.SetDescription(description)
        info.SetLicence(licence)
        info.AddDeveloper('Citrine BM-BF')
        info.AddDeveloper('RNubla')

        wx.adv.AboutBox(info)

    def getSelectedChoice(self, event):
        choice = self.interpolation_choice.GetStringSelection()
        if choice == '2x':
            self.interpNum = 2
            # print(choice)
        elif choice == '4x':
            self.interpNum = 4
            # print(choice)
        elif choice == '8x':
            self.interpNum = 8
            # print(choice)
        
        print('Interp Num: ',self.interpNum)

    def onSelectFile(self, event):
        wildcard = "MP4 source (*.mp4)|*.mp4|" \
        "All files (*.*)|*.*"
        dlg = wx.FileDialog(self, 
                            message='Select a video file',
                            defaultDir=os.getcwd(),
                            defaultFile="",
                            wildcard=wildcard,
                            style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPath()
            print('Choose the following file (s): ')
            # for path in paths:
            self.input_file_dir = os.path.splitext(paths)[0]
            print(paths)
            print(self.input_file_dir)
            self.input_dir_TextCtrl.write(paths)
            self.input_file = paths
            print(self.input_file)
            resolution = CheckResolution(self.input_file)
            print(self.input_file)
            print('Width: ',resolution.getWidth())
            print('Height: ',resolution.getHeight())
        dlg.Destroy()

    def onSelectOutDir(self, event):
        dlg = wx.DirDialog(self, 'Choose Output Directory',
                           style = wx.DD_DEFAULT_STYLE
                           )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            print('Output Path: ', path)
            self.output_path = path
            self.output_dir_TextCtrl.write(path)
        dlg.Destroy()

    def onRunInterp(self, event):
        resolution = CheckResolution(self.input_file)
        if resolution.getWidth() < int(1280) and resolution.getHeight() < int(720):  
            interp = Resolution360p(self.input_file, self.interpNum, self.output_path)
            # interp.removeDupFrames()
            interp.runFeatureFlow()
            self.completeDialog()
        else:
            interp720 = Resolution720p(self.input_file, self.interpNum, self.output_path)
            print(self.interpolation_num_TextCtrl.GetValue())
            interp720.splitVideoIntoSections()
            interp720.runFeatureFlow()
            interp720.stitchVideo()
            self.completeDialog()
    
    def thread_start(self, event):
        thread = threading.Thread(target=self.onRunInterp, args=(event,))
        thread.start()

    def completeDialog(self):
        wx.MessageBox('Feature Flow has finished interpolating your video. \n Check your output directory', 
                      'Interpolation Complete', wx.OK |wx.ICON_EXCLAMATION)

    def progressBar(self, index):
        self.pbar.SetValue(index)

    def InitUI(self):

        menubar = wx.MenuBar()

        fileMenu = wx.Menu()
        helpMenu = wx.Menu()

        menubar.Append(fileMenu, '&File')
        menubar.Append(helpMenu, '&Help')

        fileItemQuit = fileMenu.Append(wx.ID_EXIT, '&Quit', 'Quit Application')
        fileItemAbout = helpMenu.Append(wx.ID_ANY, '&About')
        

        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.OnQuit, fileItemQuit)
        self.Bind(wx.EVT_MENU, self.OnAbout, fileItemAbout)

        

        panel = wx.Panel(self)

        sizer = wx.GridBagSizer(6, 6)

        topDescription = wx.StaticText(panel, label="Support video resolution: 640x360, 1280x720")
        sizer.Add(topDescription, pos=(0, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM,
            border=10)

        line = wx.StaticLine(panel)
        sizer.Add(line, pos=(1, 0), span=(1, 5),
            flag=wx.EXPAND|wx.BOTTOM, border=10)

        interpolation_num_StaticText = wx.StaticText(panel, label="Interpolation Number [2,4,8,...,etc]")
        sizer.Add(interpolation_num_StaticText, pos=(2, 0), flag=wx.LEFT, border=10)

        self.interpolation_choices = ['2x', '4x', '8x']
        self.interpolation_choice = wx.Choice(panel, wx.ID_ANY, wx.Point(-1,-1), wx.Size(100,-1), self.interpolation_choices, 0)
        sizer.Add(self.interpolation_choice, pos=(2,1), span=(1,3), flag=wx.TOP|wx.EXPAND)
        self.interpolation_choice.Bind(wx.EVT_CHOICE, self.getSelectedChoice)

        input_dir_StaticText = wx.StaticText(panel, label="Input Directory")
        sizer.Add(input_dir_StaticText, pos=(3, 0), flag=wx.LEFT|wx.TOP, border=10)

        self.input_dir_TextCtrl = wx.TextCtrl(panel)
        # self.Bind(wx.EVT_TEXT, self.input_dir_TextCtrl, self.onSelectFile)
        sizer.Add(self.input_dir_TextCtrl, pos=(3, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND,
            border=5)
        # input_dir_TextCtrl.write(self.input_file_name)

        input_button_browse = wx.Button(panel, label="Browse...")
        sizer.Add(input_button_browse, pos=(3, 4), flag=wx.TOP|wx.RIGHT, border=5)
        input_button_browse.Bind(wx.EVT_BUTTON, self.onSelectFile)

        output_dir_StaticText = wx.StaticText(panel, label="Output Directory")
        sizer.Add(output_dir_StaticText, pos=(4, 0), flag=wx.TOP|wx.LEFT, border=10)

        self.output_dir_TextCtrl = wx.TextCtrl(panel)
        sizer.Add(self.output_dir_TextCtrl, pos=(4, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND,
            border=5)

        output_button_browse = wx.Button(panel, label="Browse...")
        sizer.Add(output_button_browse, pos=(4, 4), flag=wx.TOP|wx.RIGHT, border=5)
        output_button_browse.Bind(wx.EVT_BUTTON, self.onSelectOutDir)

        sb = wx.StaticBox(panel, label="Options (Future option sections)")

        boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)
        boxsizer.Add(wx.CheckBox(panel, label="Placeholder"),
            flag=wx.LEFT|wx.TOP, border=5)
        boxsizer.Add(wx.CheckBox(panel, label="Placeholder"),
            flag=wx.LEFT, border=5)
        boxsizer.Add(wx.CheckBox(panel, label="Placeholder"),
            flag=wx.LEFT|wx.BOTTOM, border=5)
        sizer.Add(boxsizer, pos=(5, 0), span=(1, 5),
            flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT , border=10)

        button3 = wx.Button(panel, label='Help')
        sizer.Add(button3, pos=(8, 0), flag=wx.LEFT, border=10)

        CancleButton = wx.Button(panel, label="Cancel")
        sizer.Add(CancleButton, pos=(8, 3))

        RunButton = wx.Button(panel, label="Run")
        sizer.Add(RunButton, pos=(8, 4), span=(1, 1),
            flag=wx.BOTTOM|wx.RIGHT, border=10)
        # RunButton.Bind(wx.EVT_BUTTON, self.onRunInterp)
        RunButton.Bind(wx.EVT_BUTTON, self.thread_start)

        print(getInterpolationIndex())
        print(getInterpolationRange())
        self.pbar = wx.Gauge(panel, range=getInterpolationRange(), size = (100, 25), style =  wx.GA_HORIZONTAL)
        sizer.Add(self.pbar,pos=(7,0), span=(1,6), flag=wx.EXPAND|wx.ALL, border=5)

        sizer.AddGrowableCol(2)

        panel.SetSizer(sizer)
        sizer.Fit(self)

def main():

    app = wx.App()
    ex = MainWindow(None, title="Feature Flow App")
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()