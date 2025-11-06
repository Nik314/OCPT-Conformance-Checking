# Datei: fast_hash.pyx
# Kompilieren mit: 707731


import hashlib
import numpy as np
cimport numpy as np
from libc.stdlib cimport malloc, free
from libc.string cimport memcpy

def compute_hash_map(np.ndarray[object, ndim=1] eids,
                     np.ndarray[object, ndim=1] oids):
    """
    Erwartet zwei Spalten:
      eids: Array der Event-IDs ("ocel:eid")
      oids: Array der Objekt-IDs ("ocel:oid")
    Gibt ein Dict {eid: hash_int} zurück.
    """
    cdef Py_ssize_t i
    cdef dict groups = {}
    cdef object eid, oid

    # Gruppierung nach Event-ID (schneller als pandas.groupby)
    for i in range(eids.shape[0]):
        eid = eids[i]
        oid = oids[i]
        if eid not in groups:
            groups[eid] = set()
        groups[eid].add(oid)

    # Jetzt Hashes berechnen
    cdef dict hash_map = {}
    cdef str sorted_repr
    cdef bytes encoded
    cdef object md5_hash

    for eid, oid_set in groups.items():
        sorted_repr = str(sorted(oid_set))
        encoded = sorted_repr.encode("utf_8")
        md5_hash = hashlib.md5(encoded).hexdigest()
        hash_map[eid] = int(md5_hash, 16)

    return hash_map
