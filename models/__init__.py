#!/usr/bin/python3
"""Initializing module-wide global variables Pattern"""
from models.engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()
