#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    plugins.probe.py

    Written by:               Josh.5 <jsunnex@gmail.com>
    Date:                     12 Aug 2021, (9:20 AM)

    Copyright:
           Copyright (C) Josh Sunnex - All Rights Reserved

           THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
           EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
           MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
           IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
           DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
           OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
           OR OTHER DEALINGS IN THE SOFTWARE.

"""
import mimetypes
import os
from logging import Logger

# TODO: Replace with direct call to FFProbe
#   Unmanic is losing reliance on FFmpeg
from unmanic.libs import unffmpeg


class Probe(object):
    """
    Probe
    """

    probe_info = {}

    def __init__(self, logger: Logger):
        self.logger = logger

    def file(self, file_path):
        """
        Sets the 'probe' dict by probing the given file path.
        Files that are not able to be probed will not set the 'probe' dict.

        :param file_path:
        :return:
        """
        self.probe_info = {}

        # Ensure file exists
        if not os.path.exists(file_path):
            self.logger.debug("File does not exist - '{}'".format(file_path))
            return

        # Only run this check against video/audio/image MIME types
        mimetypes.init()
        file_type = mimetypes.guess_type(file_path)[0]
        # If the file has no MIME type then it cannot be tested
        if file_type is None:
            self.logger.debug("Unable to fetch file MIME type - '{}'".format(file_path))
            return
        # Make sure the MIME type is either audio, video or image
        file_type_category = file_type.split('/')[0]
        if file_type_category not in ['audio', 'video', 'image']:
            self.logger.debug("File MIME type not in 'audio', 'video' or 'image' - '{}'".format(file_path))
            return

        try:
            # Get the file probe info
            self.probe_info = unffmpeg.Info().file_probe(file_path)
        except unffmpeg.exceptions.ffprobe.FFProbeError:
            # This will only happen if it was not a file that could be probed.
            self.logger.debug("File unable to be probed by FFProbe - '{}'".format(file_path))
            return
        except Exception as e:
            # The process failed for some unknown reason. Log it.
            self.logger.debug("Failed to set file probe - ".format(str(e)))
            return

    def get_probe(self):
        """Return the probe dictionary"""
        return self.probe_info

    def get(self, key, default=None):
        return self.probe_info.get(key, default)
