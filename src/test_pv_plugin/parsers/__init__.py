from nomad.config.models.plugins import ParserEntryPoint
from pydantic import Field


class NewParserEntryPoint(ParserEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from test_pv_plugin.parsers.parser import NewParser

        return NewParser(**self.model_dump())


class TNOExperimentParserEntryPoint(ParserEntryPoint):

    def load(self):
        from test_pv_plugin.parsers.TNO_batch_parser import TNOExperimentParser

        return TNOExperimentParser(**self.model_dump())


class TNOParserEntryPoint(ParserEntryPoint):

    def load(self):
        from test_pv_plugin.parsers.TNO_measurement_parser import TNOParser

        return TNOParser(**self.model_dump())


parser_entry_point = NewParserEntryPoint(
    name='NewParser',
    description='New parser entry point configuration.',
    mainfile_name_re=r'.*\.newmainfilename',
)


TNO_experiment_parser_entry_point = TNOExperimentParserEntryPoint(
    name='TNOExperimentParserEntryPoint',
    description='TNO experiment parser entry point configuration.',
    mainfile_name_re='^(.+\.xlsx)$',
    mainfile_mime_re='(application|text|image)/.*',
)


TNO_parser_entry_point = TNOParserEntryPoint(
    name='TNOParserEntryPoint',
    description='TNO parser entry point configuration.',
    mainfile_name_re='^.+\.?.+\.((eqe|jv|mppt)\..{1,4})$',
    mainfile_mime_re='(application|text|image)/.*',
)
