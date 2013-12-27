"""Graphical windows."""

import wx

from runescape_price_watch import metadata

class MainFrame(wx.Frame):
    """The application's top-level frame."""
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title=metadata.project, size=(200,100))
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)

