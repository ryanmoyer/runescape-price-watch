"""Graphical windows."""

import platform

import wx

from runescape_price_watch import metadata


class MainPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self._item_id_field = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        input_sizer.Add(self._item_id_field, 1, wx.ALIGN_CENTER)

        self._add_button = wx.Button(self, label='Add')
        input_sizer.Add(self._add_button, 0)

        self._refresh_button = wx.Button(self, label='Refresh')
        input_sizer.Add(self._refresh_button, 0)

        self._output_display = wx.TextCtrl(
            self, style=wx.TE_MULTILINE | wx.TE_READONLY)

        # Layout sizer.
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(input_sizer, 0, wx.EXPAND)
        main_sizer.Add(self._output_display, 1, wx.EXPAND)
        # Add other sizer for text field and buttons here.
        self.SetSizer(main_sizer)
        self.SetAutoLayout(True)


class MainFrame(wx.Frame):
    """The application's top-level frame."""
    def __init__(self, parent):
        wx.Frame.__init__(
            self, parent, title=metadata.project, size=(500, 600))
        # Create a bar at bottom of window for status.
        self.CreateStatusBar()

        # Add menu.
        app_menu = wx.Menu()

        # Add menubar.
        menubar = wx.MenuBar()
        if platform.system() != 'Darwin':
            menubar.Append(app_menu, '&App')
            # Add the option to exit.
            menu_exit = app_menu.Append(
                wx.ID_EXIT, 'E&xit', 'Terminate program')
            self.Bind(wx.EVT_MENU, self._on_exit, menu_exit)

        self.SetMenuBar(menubar)

        self._panel = MainPanel(self)

    def _on_exit(self, event):
        self.Close()
