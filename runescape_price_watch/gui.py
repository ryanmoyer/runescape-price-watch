"""Graphical windows."""

import wx

from runescape_price_watch import metadata

class MainFrame(wx.Frame):
    """The application's top-level frame."""
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title=metadata.project, size=(200,100))
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.CreateStatusBar() # Create a bar at bottom of window for status

        # Add menu.
        app_menu = wx.Menu()

        # Add menubar.
        menubar = wx.MenuBar()
        menubar.Append(app_menu, '&App')
        self.SetMenuBar(menubar)

        # Add the option to exit.
        menu_exit = app_menu.Append(wx.ID_EXIT, 'E&xit', ' Terminate the program')

        self.Bind(wx.EVT_MENU, self._on_exit, menu_exit)

    def _on_exit(self, event):
        self.Close()
