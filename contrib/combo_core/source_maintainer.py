from .importer import *
from .manifest import *


class VersionAlreadyExists(ComboException):
    pass


class SourceMaintainer(SourceLocator):
    def get_source(self, project_name, version):
        raise NotImplementedError()

    def add_project(self, project_name, source_type=None):
        raise NotImplementedError()

    def add_version(self, version_details, **kwargs):
        raise NotImplementedError()


class IndexerSourceMaintainer(IndexerSourceLocator, SourceMaintainer):
    def __init__(self, json_path, importer):
        super(IndexerSourceMaintainer, self).__init__(json_path)
        self._importer = importer

    def add_project(self, project_name, source_type=None):
        if project_name in self._projects:
            requested_src_type = source_type or IndexerSourceHandler.DEFAULT_SRC_TYPE
            actual_src_type = self._get_src_type(self._projects[project_name])
            assert requested_src_type == actual_src_type, 'Project already exists with different source type'
            return

        # Project does not exist, we need to add its details

        project_details = dict()

        # If the source type is not the default, we need to manually specify it
        if source_type is not None and source_type != IndexerSourceHandler.DEFAULT_SRC_TYPE:
            project_details[IndexerSourceHandler.IDENTIFIER_TYPE_KEYWORD] = source_type

        self._projects[project_name] = project_details

    def _extract_details(self, version_details, **kwargs):
        if 'project_name' in kwargs and 'project_version' in kwargs:
            return kwargs['project_name'], kwargs['project_version']

        import_details = ProjectSource(version_details['type'], **version_details).as_dict()
        clone_dir = self._importer.clone(import_details)

        manifest = Manifest(clone_dir)
        return manifest.name, manifest.version

    def add_version(self, version_details, **kwargs):
        project_name, project_version = self._extract_details(version_details, **kwargs)

        if project_name not in self._projects:
            raise UndefinedProject('Project {} could not be found'.format(project_name))

        project_details = self._projects[project_name]

        # This function is only relevant for version dependency source types
        source_type = project_details.get(
            IndexerSourceHandler.IDENTIFIER_TYPE_KEYWORD, IndexerSourceHandler.DEFAULT_SRC_TYPE)
        assert source_type == 'version_dependent', 'Unsupported action'

        # If the requested version already exists this is an error
        if str(project_version) in project_details:
            raise VersionAlreadyExists('Version "{}" of project "{}" already exist in file "{}"'.format(
                project_version, project_name, self.get_json_file_path()))

        # Remove details which are not necessary due to defaults
        project_defaults = project_details.get(VersionDependentSourceSupplier.SOURCE_DEFAULTS_KEYWORD)
        if project_defaults is not None:
            version_details = VersionDependentSourceSupplier.filter_version_details(version_details, project_defaults)

        project_details[str(project_version)] = version_details

        # This update is necessary for the file update
        self._projects[project_name] = project_details

