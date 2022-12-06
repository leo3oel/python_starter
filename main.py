from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent, PreferencesEvent, PreferencesUpdateEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.item.ExtensionSmallResultItem import ExtensionSmallResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

import subprocess as sub
from folder import *

path = "~"
terminal_name = "xfce4-terminal"
terminal_command = "--command="
filename = ".py"
command_to_execute = "python3"

class ZathuraExtension(Extension):

    def __init__(self):
        super().__init__() # Parent Constructor
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener()) # if Keywords get entered -> KeywordQueryEventListener
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())  # <-- add this line
        self.subscribe(PreferencesEvent, PreferencesEventListener())

def getList(path):
    global filename
    """
    Make Liste to Display
    """
    folders = getFolders(path)
    items = []
    for folder in folders:
        pathtofolder = f"00;{path}/{folder}" # next folder path
        items.append(ExtensionSmallResultItem(icon='images/folder.png',
                                            name=folder,
                                            on_enter=ExtensionCustomAction(pathtofolder, keep_app_open=True)))
    files = getFiles(path, filename)
    for file in files:
        pathtofile = f"01;{path}/{file}"
        items.append(ExtensionSmallResultItem(icon='images/file.png',
                                            name=file,
                                            on_enter=ExtensionCustomAction(pathtofile, keep_app_open=False)))
    return(items)

"""
Listeners
"""
class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        # return List
        return RenderResultListAction(getList(path))

class ItemEnterEventListener(EventListener):
    """
    Executes Code on Enter
    get_data starts with 2 digits and a ; to seperate Folder Actions from PDF Actions
    """

    def on_event(self, event, extension):
        global terminal_command, terminal_name, command_to_execute
        # event is instance of ItemEnterEvent
        data = event.get_data()
        if data[0:2] == "00":
            temppath = data[3:] # set new path

            #return new list
            return RenderResultListAction(getList(temppath))
        else:
            filename = data[3:] # extract filename
            # Open File in Zathura
            execcomand = "bash -c '" +command_to_execute+ " "+filename+ "; read'"
            sub.call([terminal_name, terminal_command, execcomand])

            return RenderResultListAction([])

class PreferencesEventListener(EventListener):
    """
    Listener for prefrences event.
    It is triggered on the extension start with the configured preferences
    """

    def on_event(self, event, extension):
        global path, terminal_name, terminal_command, filename, command_to_execute
        path = "~"
        if event.preferences["start_path"] != "":
            path = event.preferences["start_path"]
        if event.preferences["terminal_name"] != "":
            terminal_name = event.preferences["terminal_name"]
        if event.preferences["terminal_command"] != "":
            terminal_command = event.preferences["terminal_command"]
        if event.preferences["filename"] != "":
            filename = event.preferences["filename"]
        if event.preferences["command_to_execute"] != "":
            command_to_execute = event.preferences["command_to_execute"]



if __name__ == '__main__':
    ZathuraExtension().run()
