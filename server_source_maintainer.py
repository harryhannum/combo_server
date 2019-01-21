from combo_core.source_maintainer import *
from git_tags_locator import *


class ServerSourceMaintainer(JsonSourceMaintainer):
    def __init__(self, json_path):
        super(ServerSourceMaintainer, self).__init__(json_path)
        self._supported_src_suppliers['git_tags'] = GitTagsSourceSupplier
