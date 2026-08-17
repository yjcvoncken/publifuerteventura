#!/usr/bin/env python3
import os, sys

if __name__ == "__main__":
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".vendor"))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fuerteguide.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
