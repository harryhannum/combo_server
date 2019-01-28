from combo_core.source_maintainer import *
from git_tags_locator import *


class GlobalSourceMaintainer(IndexerSourceMaintainer):
    def __init__(self, json_path):
        super(GlobalSourceMaintainer, self).__init__(json_path, clones_dir_name='server_clones')
        self._supported_src_suppliers['git_tags'] = GitTagsSourceSupplier
