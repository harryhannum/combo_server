from combo_core.source_locator import *
from git_tags_locator import *


class ServerSourceLocator(SourceLocator):
    def __init__(self, json_path):
        super(ServerSourceLocator, self).__init__(json_path)
        self._supported_src_suppliers['git_tags'] = GitTagsSourceSupplier
