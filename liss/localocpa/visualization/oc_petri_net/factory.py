from liss.localocpa.visualization.oc_petri_net.versions import control_flow, annotated_with_opera
from pm4py.visualization.common import gview
from pm4py.visualization.common import save as gsave


CONTROL_FLOW = "control_flow"
ANNOTATED_WITH_OPERA = "annotated_with_opera"

VERSIONS = {
    CONTROL_FLOW: control_flow.apply,
    ANNOTATED_WITH_OPERA: annotated_with_opera.apply}


def apply(obj, variant=CONTROL_FLOW, **kwargs):
    return VERSIONS[variant](obj, **kwargs)


def save(gviz, output_file_path):
    """
    Save the diagram

    Parameters
    -----------
    gviz
        GraphViz diagram
    output_file_path
        Path where the GraphViz output should be saved
    """
    gsave.save(gviz, output_file_path)


def view(gviz):
    """
    View the diagram

    Parameters
    -----------
    gviz
        GraphViz diagram
    """
    return gview.view(gviz)
