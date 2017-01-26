#! /usr/bin/python3

from gi.repository import Gtk, GObject

import singletons
import status
from util import trackers

class NotificationWidget(Gtk.Frame):
    """
    Notification widget is a child of the InfoPanel - it is
    only shown if we've received intercepted a non-transient
    notification that hasn't been sent from a media player.
    """
    __gsignals__ = {
        "notification": (GObject.SignalFlags.RUN_LAST, None, ()),
    }
    def __init__(self):
        super(NotificationWidget, self).__init__()
        self.set_shadow_type(Gtk.ShadowType.NONE)
        self.get_style_context().add_class("notificationwidget")

        self.set_size_request(50, -1)

        self.notification_count = 0

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.add(box)

        self.label = Gtk.Label.new("0")
        box.pack_start(self.label, False, False, 4)

        self.image = Gtk.Image.new_from_icon_name("screensaver-notification-symbolic", Gtk.IconSize.LARGE_TOOLBAR)
        box.pack_end(self.image, False, False, 4)

        box.show_all()

        self.notification_watcher = singletons.NotificationWatcher

        trackers.con_tracker_get().connect(self.notification_watcher,
                                           "notification-received",
                                           self.on_notification_received)

    def on_notification_received(self, proxy, sender, data=None):
        mp_watcher = singletons.MediaPlayerWatcher

        players = mp_watcher.get_all_player_names()

        if sender.lower() in players:
            return

        for ignored in ("network",):
            if ignored in sender.lower():
                return

        self.notification_count += 1

        self.update_label()

        self.emit("notification")

    def should_show(self):
        return self.notification_count > 0

    def update_label(self):
        self.label.set_text(str(self.notification_count))
