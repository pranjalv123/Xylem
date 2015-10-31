"""
Xylem - Phylogenetic Pipelines with MPI

Pipeline.py contains routines for managing dependency graphs.
    
Copyright (C) 2015 Pranjal Vachaspati
pr@nj.al

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import Scheduler
import cPickle


class Pipeline:
    def __init__(self, scheduler):
        self.tasks = []
        self.scheduler = scheduler
    def add_task(self, task):
        self.tasks.append(task)
        task.pipeline = self
        return task
    def verify(self):
        return True
    def prune(self):
        pass
    def ready(self, cache=True, regen=False):
        for task in self.tasks:
            if task.status() == "ready":
                self.scheduler.schedule(task)

    
