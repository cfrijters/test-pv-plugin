#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import datetime
import os
import sys

from baseclasses.helper.utilities import (
    create_archive,
    get_entry_id_from_file_name,
    get_reference,
    set_sample_reference,
)
from nomad.datamodel import EntryArchive
from nomad.datamodel.context import ServerContext
from nomad.datamodel.data import (
    EntryData,
)
from nomad.datamodel.metainfo.basesections import (
    Activity,
)
from nomad.metainfo import (
    Quantity,
)
from nomad.parsing import MatchingParser

from test_pv_plugin.schema_packages.TNO_package import (
    TNO_EQEmeasurement_ELN,
    TNO_JVmeasurement,
    TNO_Measurement_ELN,
    TNO_SimpleMPPTracking,
)

"""
This is a hello world style example for an example parser/converter.
"""


class RawFileTNO(EntryData):
    processed_archive = Quantity(
        type=Activity,
    )


class TNOParser(MatchingParser):
    def parse(self, mainfile: str, archive: EntryArchive, logger):
        mainfile_split = os.path.basename(mainfile).split('.')
        notes = ''
        if len(mainfile_split) > 2:
            notes = '.'.join(mainfile_split[1:-2])

        entry = TNO_EQEmeasurement_ELN()

        archive.metadata.entry_name = os.path.basename(mainfile)

        search_id = mainfile_split[0]
        if isinstance(archive.m_context, ServerContext):
            set_sample_reference(archive, entry, search_id)

        entry.name = f'{search_id} {notes}'
        entry.description = f'Notes from file name: {notes}'

        entry.data_file = os.path.basename(mainfile)
        entry.datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

        file_name = f'{os.path.basename(mainfile)}.archive.json'
        eid = get_entry_id_from_file_name(file_name, archive)
        archive.data = RawFileTNO(processed_archive=get_reference(archive.metadata.upload_id, eid))
        create_archive(entry, archive, file_name)
