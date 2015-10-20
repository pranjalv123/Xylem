from Tasks import *
import Pipeline
import Scheduler
import dendropy

sched = Scheduler.Scheduler()

pl = Pipeline.Pipeline(sched)

readgenes = pl.add_task(ReadPhylip('../test/data/some-genes.phylip'))
ft = pl.add_task(RunFastTree(cachefile='/tmp/fasttree-trees')).require(readgenes)
astrid = pl.add_task(RunASTRID(cachefile='/tmp/astrid-tree')).require(ft)
truest = pl.add_task(CastName("speciestree", "truespeciestree", dendropy.Tree)).require(pl.add_task(ReadSpeciesTree('../test/data/stree', cachefile='/tmp/diff')))


compare = pl.add_task(CompareTrees().require(astrid).require(truest))
                         


pl.run()
