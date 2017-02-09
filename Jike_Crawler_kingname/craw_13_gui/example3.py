#-*-coding:utf8-*-

import wx

'''基于Sizer的控件相对布局'''
class Example3(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=-1, title=u'极客学院', size=(600, 600))
        self.panel = wx.Panel(self, -1)
        self.Centre()

        #定义我们需要的各个控件

        commandStatic = wx.StaticText(self.panel, -1, u'输命令:')
        writePyStatic = wx.StaticText(self.panel, -1, u'写代码:')

        commandText = wx.TextCtrl(self.panel, -1, u'')
        writePyText = wx.TextCtrl(self.panel, -1, u'''#-*-coding:utf-8-*-\n#在这些Python代码''',
                                  style=wx.TE_MULTILINE, size=(300, 200))

        send = wx.Button(self.panel, label=u'发送命令')
        clear = wx.Button(self.panel, label=u'清空命令')
        screen = wx.Button(self.panel, label=u'查看屏幕')

        serverList = ['192.168.0.4', '10.19.2.1', '192.168.0.111', '172.26.123.5', '192.168.6.11', '192.99.8.8']
        server = wx.ListBox(self.panel, -1, size=(120, 100), choices=serverList, style=wx.LB_SINGLE)

        img = wx.Image(r'logo.jpg', wx.BITMAP_TYPE_ANY).Scale(200, 200)
        screenBox = wx.StaticBitmap(self.panel, -1, wx.BitmapFromImage(img))

        #基于BoxSizer布局
        # hBoxAll = wx.BoxSizer(wx.HORIZONTAL)
        # vBoxControl = wx.BoxSizer(wx.VERTICAL)
        # hBoxCommand = wx.BoxSizer(wx.HORIZONTAL)
        # vBoxWrite = wx.BoxSizer(wx.VERTICAL)
        # hBoxButton = wx.BoxSizer(wx.HORIZONTAL)
        #
        # hBoxCommand.Add(commandStatic, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        # hBoxCommand.Add(commandText, proportion=2, flag=wx.ALL | wx.EXPAND, border=5)
        #
        # vBoxWrite.Add(writePyStatic, proportion=0, flag=wx.ALL | wx.EXPAND, border=5)
        # vBoxWrite.Add(writePyText, proportion=0, flag=wx.ALL | wx.EXPAND, border=5)
        #
        # vBoxControl.Add(hBoxCommand, proportion=0, flag=wx.ALL, border=5)
        # vBoxControl.Add(vBoxWrite, proportion=0, flag=wx.ALL, border=5)
        #
        # hBoxButton.Add(send, proportion=0, flag=wx.ALL, border=5)
        # hBoxButton.Add(clear, proportion=0, flag=wx.ALL, border=5)
        # hBoxButton.Add(screen, proportion=0, flag=wx.ALL, border=5)
        #
        # vBoxControl.Add(hBoxButton, proportion=0, flag=wx.ALL, border=5)
        #
        # hBoxAll.Add(server, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        # hBoxAll.Add(vBoxControl, proportion=2, flag=wx.ALL | wx.EXPAND, border=5)
        # hBoxAll.Add(screenBox, proportion=3, flag=wx.ALL | wx.EXPAND, border=5)
        #
        # self.panel.SetSizer(hBoxAll)
        # hBoxAll.Fit(self)

        #基于GridSizer布局
        # gridSizerAll= wx.GridSizer(rows=3, cols=3, hgap=5, vgap=5)
        # gridSizerAll.AddMany([(server, 0, wx.EXPAND), (commandStatic, 0, wx.EXPAND), (commandText, 0, wx.EXPAND),
        #                      (writePyStatic, 0, wx.EXPAND), (send, 0, wx.EXPAND), (clear, 0, wx.EXPAND),
        #                      (writePyText, 0, wx.EXPAND), (screen, 0, wx.EXPAND), (screenBox, 0, wx.EXPAND)])
        # self.panel.SetSizer(gridSizerAll)
        # gridSizerAll.Fit(self)

        #基于FlexGridSizer布局
        # flexGridSizerAll= wx.FlexGridSizer(rows=3, cols=3, hgap=5, vgap=5)
        # flexGridSizerAll.AddMany([(server, 0, wx.EXPAND), (commandStatic, 0, wx.EXPAND), (commandText, 0, wx.EXPAND),
        #                      (writePyStatic, 0, wx.EXPAND), (send, 0, wx.EXPAND), (clear, 0, wx.EXPAND),
        #                      (writePyText, 0, wx.EXPAND), (screen, 0, wx.EXPAND), (screenBox, 0, wx.EXPAND)])
        # self.panel.SetSizer(flexGridSizerAll)
        #
        # # flexGridSizerAll.AddGrowableCol(2, 1)
        # # flexGridSizerAll.AddGrowableRow(2, 1)
        #
        # flexGridSizerAll.Fit(self)

        #基于GirdBagSizer布局
        gridBagSizerAll = wx.GridBagSizer(hgap=5, vgap=5)
        gridBagSizerAll.Add(server, pos=(0, 0),
                            flag=wx.ALL | wx.EXPAND,
                            span=(7, 2), border=5)

        gridBagSizerAll.Add(commandStatic, pos=(0, 2),
                            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                            border=5)
        gridBagSizerAll.Add(commandText, pos=(0, 3),
                            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                            span=(1, 2), border=5)

        gridBagSizerAll.Add(writePyStatic, pos=(1, 2),
                            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                            span=(1, 3), border=5)
        gridBagSizerAll.Add(writePyText, pos=(2, 2),
                            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                            span=(4, 3), border=5)
        gridBagSizerAll.Add(send, pos=(6, 2),
                            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                            span=(1, 1), border=5)
        gridBagSizerAll.Add(clear, pos=(6, 3),
                            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                            span=(1, 1), border=5)
        gridBagSizerAll.Add(screen, pos=(6, 4),
                            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                            span=(1, 1), border=5)

        gridBagSizerAll.Add(screenBox, pos=(0, 5),
                            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                            span=(7, 2), border=5)

        self.panel.SetSizer(gridBagSizerAll)

        self.SetSizeHints(250, 200, 700, 400) #设定窗口的最大最小值
        # gridBagSizerAll.AddGrowableCol(0, 1)
        # gridBagSizerAll.AddGrowableCol(1, 1)
        # gridBagSizerAll.AddGrowableCol(2, 1)
        # gridBagSizerAll.AddGrowableCol(3, 1)
        # gridBagSizerAll.AddGrowableCol(4, 1)
        # gridBagSizerAll.AddGrowableCol(5, 1)
        # gridBagSizerAll.AddGrowableCol(6, 1)
        #
        # gridBagSizerAll.AddGrowableRow(0, 1)
        # gridBagSizerAll.AddGrowableRow(1, 1)
        # gridBagSizerAll.AddGrowableRow(2, 1)
        # gridBagSizerAll.AddGrowableRow(3, 1)
        # gridBagSizerAll.AddGrowableRow(4, 1)
        # gridBagSizerAll.AddGrowableRow(5, 1)
        # gridBagSizerAll.AddGrowableRow(6, 1)
        gridBagSizerAll.Fit(self)



if __name__ == "__main__":
    app = wx.App()
    frame = Example3()
    frame.Show()
    app.MainLoop()