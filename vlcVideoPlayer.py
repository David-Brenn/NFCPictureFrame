import vlc
import sys

_isMacOS   = sys.platform.startswith('darwin')
_isLinux   = sys.platform.startswith('linux')
_isWindows = sys.platform.startswith('win')

class VlcVideoPlayer:
    instance = None
    mediaPlayer = None
    currentVideo = None
    playingVideo = False

    def __init__(self,canvas = None):
        self.setupPlayer()
        if canvas != None:
            self.setCanvas(canvas)


    def setupPlayer(self):
        self.instance = vlc.Instance("--no-audio --no-subsdec-autodetect-utf8")
        self.mediaPlayer = self.instance.media_player_new()
        self.currentVideo = None
        self.playingVideo = False

    def setCanvas(self,canvas):
        if _isLinux:
            self.mediaPlayer.set_xwindow(canvas.winfo_id())
        else:
            self.mediaPlayer.set_hwnd(canvas.winfo_id())


    def playVideo(self,videoPath):
        if self.playingVideo:
            self.stopVideo()
        self.currentVideoPath = videoPath
        self.currentMedia = self.instance.media_new(self.currentVideoPath)
        self.mediaPlayer.set_media(self.currentMedia)
        self.mediaPlayer.play()
        self.playingVideo = True


    def stopVideo(self):
        self.mediaPlayer.stop()
        self.playingVideo = False

    