#-*-coding:utf8-*-

'''创建一个窗体'''
import wx

# app = wx.App()
# frame = wx.Frame(None, -1, u"极客学院")
# frame.Show()
# app.MainLoop()

'''堆砌各个控件，基于坐标位置的控件绝对布局'''
class Example2(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=-1, title=u'极客学院', size=(600, 600))
        panel = wx.Panel(self, -1)
        self.Centre()

        button = wx.Button(panel, label=u'我是按钮', pos=(20, 0), size=(100, 100))
        statictext = wx.StaticText(panel, -1, u'我是不能编辑的文本框', pos=(20, 100))
        text = wx.TextCtrl(panel, -1, u'请在这里输入内容', pos=(200, 210))
        password = wx.TextCtrl(panel, -1, u'请在这里输入内容', style=wx.TE_PASSWORD, pos=(200, 250))
        mutiText = wx.TextCtrl(panel, -1, u'我是多行\n文本框', style=wx.TE_MULTILINE, pos=(100, 300))
        checkBox1 = wx.CheckBox(panel, -1, u"我是复选框1", pos=(150, 20))
        checkBox2 = wx.CheckBox(panel, -1, u"我是复选框2", pos=(150, 40))

        radio1 = wx.RadioButton(panel, -1, u"我是单选按钮1", pos=(150, 60), style=wx.RB_GROUP)
        radio2 = wx.RadioButton(panel, -1, u"我是单选按钮2", pos=(150, 80))
        radio3 = wx.RadioButton(panel, -1, u"我是单选按钮3", pos=(150, 100))

        radioList = [u'一组单选按钮之1', u'一组单选按钮之2', u'一组单选按钮之3']
        wx.RadioBox(panel, -1, u"一组单选按钮", (10, 120), wx.DefaultSize, radioList, 2, wx.RA_SPECIFY_ROWS)

        jikexueyuan = [u'极', u'客', u'学', u'院', '1', '2', '3', '4', '5', '6']
        listBox = wx.ListBox(panel, -1, pos=(300, 20), size=(100, 100), choices=jikexueyuan, style=wx.LB_MULTIPLE)

        img = wx.Image(r'logo.jpg', wx.BITMAP_TYPE_ANY).Scale(200, 200)
        sb1 = wx.StaticBitmap(panel, -1, wx.BitmapFromImage(img), pos=(300, 300))

if __name__ == "__main__":
    app = wx.App()
    frame = Example2()
    frame.Show()
    app.MainLoop()