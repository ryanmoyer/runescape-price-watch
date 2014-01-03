"""Graphical windows."""

import platform
from multiprocessing.pool import ThreadPool

import wx

from runescape_price_watch import metadata
from fetcher import fetch_prices


class MainPanel(wx.Panel):
    """Container for the main user interface."""
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self._item_ids = []
        self._pool = ThreadPool()

        border_width = 3

        input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self._item_id_field = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        # Error in docs, needs to be wx.EVT_TEXT_ENTER not
        # wx.EVT_COMMAND_TEXT_ENTER
        self.Bind(wx.EVT_TEXT_ENTER, self._on_add, self._item_id_field)
        # Need to use the AddF() method to add using wx.SizerFlags. We would
        # reduce duplication by copying a common wx.SizerFlags instance, but
        # this is apparently impossible (calling chained methods mutates the
        # original instance).
        input_sizer.AddF(
            self._item_id_field, wx.SizerFlags(1).Expand().Center().Border(
                wx.TOP | wx.BOTTOM | wx.LEFT, border_width))

        self._add_button = wx.Button(self, label='Add')
        self.Bind(wx.EVT_BUTTON, self._on_add, self._add_button)
        input_sizer.AddF(self._add_button, wx.SizerFlags(0).Center().Border(
            wx.TOP | wx.BOTTOM | wx.LEFT, border_width))

        self._refresh_button = wx.Button(self, label='Refresh')
        self.Bind(wx.EVT_BUTTON, self._on_refresh, self._refresh_button)
        input_sizer.AddF(
            self._refresh_button,
            wx.SizerFlags(0).Center().Border(wx.ALL, border_width))

        self._output_display = wx.TextCtrl(
            self, style=wx.TE_MULTILINE | wx.TE_READONLY)

        # Layout sizer.
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(input_sizer, 0, wx.EXPAND)
        main_sizer.Add(self._output_display, 1, wx.EXPAND | wx.ALL, border=3)
        # Add other sizer for text field and buttons here.
        self.SetSizer(main_sizer)
        self.SetAutoLayout(True)

    def _on_add(self, event):
        new_item_id = int(self._item_id_field.GetValue())
        self._item_ids.append(new_item_id)
        self._refresh()

    def _refresh(self):
        self._output_display.Clear()
        self._pool.apply_async(
            fetch_prices, [self._item_ids], {}, self._call_in_main_thread)

    def _call_in_main_thread(self, name_and_price_tuples):
        wx.CallAfter(self._display_names_and_prices, name_and_price_tuples)

    def _display_names_and_prices(self, name_and_price_tuples):
        for name, price in name_and_price_tuples:
            self._output_display.AppendText('{0}: {1}\n'.format(name, price))

    def _on_refresh(self, event):
        self._refresh()



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
