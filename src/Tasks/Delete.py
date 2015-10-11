import Task
import DataSet
import cPickle
import numpy as np
import subprocess
import StringIO
import uuid

class DeleteTaxaUniform(Task):
    def __init__(self, ndelete, *args, **kwargs):
        super(DeleteTaxaUniform, self).__init__(*args, **kwargs)
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
    def __init__(self, ndelete, sigma=0, *args, **kwargs):
        super(DeleteTaxaRandom, self).__init__(*args, **kwargs)
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
