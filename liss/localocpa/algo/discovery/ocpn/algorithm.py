from liss.localocpa.algo.discovery.ocpn.versions import inductive
from liss.localocpa.objects.log.ocel import OCEL
from liss.localocpa.objects.log.variants.obj import ObjectCentricEventLog
import liss.localocpa.objects.log.converter.factory as convert_factory

INDUCTIVE = "inductive"

VERSIONS = {INDUCTIVE: inductive.apply}


def apply(ocel, variant=INDUCTIVE, parameters=None):
    if type(ocel) == OCEL:
        return VERSIONS[variant](ocel.log.log, parameters=parameters)
    if type(ocel) == ObjectCentricEventLog:
        df, _ = convert_factory.apply(ocel, variant='json_to_mdl')
        return VERSIONS[variant](df, parameters=parameters)
    else:
        return VERSIONS[variant](ocel, parameters=parameters)
