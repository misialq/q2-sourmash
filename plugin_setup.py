# ----------------------------------------------------------------------------
# Copyright (c) 2016-2018, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------


import q2_sourmash
import tempfile

import qiime2.plugin
from qiime2.plugin import Plugin, Metadata, Str, List, Citations, SemanticType, SingleFileDirectoryFormat, TextFileFormat, ValidationError
from qiime2.plugin import model

plugin = Plugin(
    name='sourmash',
    version='0.0.0',
    website='http://sourmash.readthedocs.io/en/latest/',
    package='q2_sourmash',
    citations=Citations.load('citations.bib', package='q2_sourmash'),
    description=('This QIIME 2 plugin wraps sourmash and '
                 'supports the calculation and comparison of  '
                 'minhash signatures.'),
    short_description='Plugin for generation of minhash signatures.'
)

MinHashSig = SemanticType('MinHashSig')

plugin.register_semantic_types(MinHashSig)

load_signature_json()

class MinHashSigJson(TextFileFormat):
    def _validate_(self, level):
        pass

class MinHashSigJsonDirFormat(model.DirectoryFormat):
    signatures = model.FileCollection(
        r'.*\.sig', format=MinHashSigJson)

    @signature.set_path_maker
    def signature_path_maker(self, name):
        return(name + '.sig')

plugin.register_views(MinHashSigJson, MinHashSigJsonDirFormat)

plugin.register_semantic_type_to_format(
    MinHashSig,
    artifact_format=MinHashSigJsonDirFormat
)

plugin.methods.register_function(
    function=q2_sourmash.compute,
    inputs={'SequenceFile': SampleData[SequencesWithQuality |
                            PairedEndSequencesWithQuality]},
    parameters={'ksizes': qiime2.plugin.Int,
        'scaled': qiime2.plugin.Int
        'track_abundance': qiime2.plugin.Bool,
        'input_is_protein': qiime2.plugin.Bool},
    output=[('min_hash_signature', MinHashSig)]
)

plugin.methods.register_function(function=q2_sourmash.compare,
    inputs={'min_hash_signature':MinHashSig}
    parameters={'ksize': qiime2.plugin.Int,
    'ignore_abundance': qiime2.plugin.Bool},
    outputs=[('compare_output', DistanceMatrix)]
)
