"""
Handles importing dependencies from multiple possible sources (git repository, zip file, server, etc...)
"""

from source_locator_server import *


class DependencyBase(object):
    def __init__(self, dependency_source):
        self.dep_src = dependency_source

    def assert_keywords(self, *keywords):
        for keyword in keywords:
            assert hasattr(self.dep_src, keyword), 'Invalid import source, missing attribute "{}"'.format(keyword)

    def clone(self, dst_path):
        raise NotImplementedError


class GitDependency(DependencyBase):
    REMOTE_URL_KEYWORD = 'remote_url'
    COMMIT_HASH_KEYWORD = 'commit_hash'

    def clone(self, dst_path):
        self.assert_keywords(self.REMOTE_URL_KEYWORD, self.COMMIT_HASH_KEYWORD)

        from temp import git_api

        # Clone the dependency
        repo = git_api.GitRepo(dst_path)
        repo.clone(getattr(self.dep_src, self.REMOTE_URL_KEYWORD), getattr(self.dep_src, self.COMMIT_HASH_KEYWORD))

        repo.close()


class LocalPathDependency(DependencyBase):
    PATH_KEYWORD = 'local_path'

    def clone(self, dst_path):
        self.assert_keywords(self.PATH_KEYWORD)

        src_path = getattr(self.dep_src, self.PATH_KEYWORD)
        copytree(src_path, dst_path)


class DependencyImporter:
    def __init__(self, user_sources=None):
        self._handlers = {
            'git': GitDependency,
            'local_path': LocalPathDependency
        }

        self._external_server = user_sources is None
        if not self._external_server:
            # TODO: Should be independent from the server (There will be mutual code). currently goes to the "server"
            self._sources = user_sources

    def clone(self, combo_dep, dst_path):
        if self._external_server:
            import_src = get_version_source(*combo_dep.as_tuple())
        else:
            import_src = get_version_source(*combo_dep.as_tuple(), self._sources)

        if import_src.src_type not in self._handlers:
            raise NotImplementedError('Can not import dependency with source type "{}"'.format(import_src.src_type))

        if os.path.exists(dst_path):
            # If already imported, import can be skipped
            return

        handler_type = self._handlers[import_src.src_type]
        import_handler = handler_type(import_src)
        import_handler.clone(dst_path)