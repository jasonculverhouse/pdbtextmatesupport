from os.path import exists, realpath
from os import system


OSA_TEMEPLATE = """tell application "System Events"
    tell application "TextMate" to get url "%s"
    tell process "TextMate"
        keystroke tab using {command down}
    end tell
end tell"""

have_appscript = False
try:
    from appscript import app
    have_appscript = True
except:
    pass

def mate(self):
    frame, lineno = self.stack[self.curindex]
    filename = self.canonic(frame.f_code.co_filename)
    if exists(filename):
        filename = realpath(filename)
        tm_url = 'txmt://open?url=file://%s&line=%d&column=2' % (filename, lineno)
        if have_appscript:
            app("TextMate").get_url(tm_url)
        else:
            osa_cmd = OSA_TEMEPLATE % tm_url
            system('osascript -e \'%s\'' % osa_cmd)

def preloop(self):
    mate(self)

def precmd(self, line):
    mate(self)
    return line
