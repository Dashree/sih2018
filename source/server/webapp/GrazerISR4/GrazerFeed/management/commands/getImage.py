from watchdog.obsevers import Observer
from watchdog.events import PatternMatchingEventHandler

from django.core.management.base import BaseCommand

from .videoProcessing import VideoProcessing
