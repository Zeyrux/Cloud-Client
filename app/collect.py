from threading import Thread
from json import load

from .models import Event

from watchdog.observers import Observer
from watchdog.events import (
    FileSystemEventHandler,
    FileModifiedEvent,
    FileMovedEvent,
    FileDeletedEvent,
    FileCreatedEvent,
)


class EventHandler(FileSystemEventHandler):
    def __init__(self, session) -> None:
        super().__init__()
        self.session = session

    def on_any_event(self, event):
        if type(event) in [
            FileModifiedEvent,
            FileMovedEvent,
            FileDeletedEvent,
            FileCreatedEvent,
        ]:
            self.session.add(
                Event(
                    self.session,
                    event.event_type,
                    event.src_path,
                    dest_path=event.dest_path
                    if type(event) == FileMovedEvent
                    else None,
                )
            )


class Collector:
    def __init__(self, session) -> None:
        self.paths = load(open("sync.json", "r"))
        self.observer = Observer()
        for path in self.paths:
            self.observer.schedule(EventHandler(session), path, recursive=True)

    def run(self) -> None:
        self.observer.start()
