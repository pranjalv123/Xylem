from Tasks import *
import Pipeline
import Scheduler
import dendropy

sched = Scheduler.Scheduler()

def gen_pipeline(sched, i):

    pl = Pipeline.Pipeline(sched)
    
    readgenes = pl.add_task(ReadPhylip('../test/data/some-genes-'+str(i) +'.phylip'))
    ft = pl.add_task(RunFastTree(cachefile='/tmp/fasttree-trees' + str(i))).require(readgenes)
    astrid = pl.add_task(RunASTRID(cachefile='/tmp/astrid-tree'+str(i))).require(ft)
    truest = pl.add_task(CastName("speciestree", "truespeciestree", dendropy.Tree)).require(pl.add_task(ReadSpeciesTree('../test/data/stree')))
    
    writest = pl.add_task(WriteSpeciesTree('/tmp/this-is-astridtree'+str(i))).require(pl.add_task(CastName("estimatedspeciestree", "speciestree", dendropy.Tree)).require(astrid))

    compare = pl.add_task(CompareTrees().require(astrid).require(truest))
    return pl


sched.add(lambda s: gen_pipeline(s, 1))
sched.add(lambda s: gen_pipeline(s, 2))

sched.run()