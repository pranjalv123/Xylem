"""
Xylem - Phylogenetic Pipelines with MPI

Delete.py contains tasks that delete taxa from datasets.
    
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

import Task
import DataSet
import cPickle
import numpy as np
import subprocess
import StringIO
import uuid

class DeleteTaxaUniform(Task):
    def setup(self, ndelete):
        self.ndelete = ndelete
    def inputs(self):
        return [("genetrees", dendropy.TreeList), ("alignments", (dendropy.DnaCharacterMatrix,)), ("speciestree", dendropy.Tree)]
    def outputs(self):
        return [("genetrees", dendropy.TreeList), ("alignments", (dendropy.DnaCharacterMatrix,)), ("speciestree", dendropy.Tree)]
    def run(self):
        dna = self.input_data["alignments"]
        gt = self.input_data["genetrees"]
        st = self.input_data["speciestree"]
        gt.migrate_taxon_namespace(dna[0].taxon_namespace)
        st.migrate_taxon_namespace(dna[0].taxon_namespace)
        deletion_list = np.random.choice(list(gt.taxon_namespace), size=ndelete, replace=False)
        for g in gt:
            g.prune_taxa(deletion_list)
        for seq in dna:
            seq.discard_sequences(deletion_list)
        st.prune_taxa(deletion_list)
        self.result = {"alignments":dna, "genetrees":gt, "speciestrees":st}
        return self.result
        
class DeleteTaxaRandom(Task):
    def setup(self, ndelete, sigma=0):
        self.ndelete = ndelete
        self.sigma = sigma
    def inputs(self):
        return [("genetrees", dendropy.TreeList), ("alignments", (dendropy.DnaCharacterMatrix,))]
    def outputs(self):
        return [("genetrees", dendropy.TreeList), ("alignments", (dendropy.DnaCharacterMatrix,))]
    def run(self):
        dna = self.input_data["alignments"]
        gt = self.input_data["genetrees"]
        gt.migrate_taxon_namespace(dna[0].taxon_namespace)
        for seq, g in zip(dna, gt):
            nd = min(ndelete + np.random.randn() * sigma,  len([1 for j in seq if len(seq[j])]))
            deletion_list = np.random.choice(list(gt.taxon_namespace), size=nd, replace=False)
            for g in gt:
                g.prune_taxa(deletion_list)
            for seq in dna:
                seq.discard_sequences(deletion_list)
        self.result = {"alignments":dna, "genetrees":gt}
        return self.result