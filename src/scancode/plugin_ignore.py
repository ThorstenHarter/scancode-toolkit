#
# Copyright (c) 2018 nexB Inc. and others. All rights reserved.
# http://nexb.com and https://github.com/nexB/scancode-toolkit/
# The ScanCode software is licensed under the Apache License version 2.0.
# Data generated with ScanCode require an acknowledgment.
# ScanCode is a trademark of nexB Inc.
#
# You may not use this software except in compliance with the License.
# You may obtain a copy of the License at: http://apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#
# When you publish or redistribute any data created with ScanCode or any ScanCode
# derivative work, you must accompany this data with the following acknowledgment:
#
#  Generated with ScanCode and provided on an "AS IS" BASIS, WITHOUT WARRANTIES
#  OR CONDITIONS OF ANY KIND, either express or implied. No content created from
#  ScanCode should be considered or used as legal advice. Consult an Attorney
#  for any legal advice.
#  ScanCode is a free software code scanning tool from nexB Inc. and others.
#  Visit https://github.com/nexB/scancode-toolkit/ for support and download.

from __future__ import absolute_import
from __future__ import unicode_literals

from functools import partial

from commoncode.fileset import match
from plugincode.pre_scan import PreScanPlugin
from plugincode.pre_scan import pre_scan_impl
from scancode import CommandLineOption
from scancode import PRE_SCAN_GROUP


@pre_scan_impl
class ProcessIgnore(PreScanPlugin):
    """
    Ignore files matching the supplied pattern.
    """

    options = [
        CommandLineOption(('--ignore',),
           multiple=True,
           metavar='<pattern>',
           help='Ignore files matching <pattern>.',
           help_group=PRE_SCAN_GROUP)
    ]

    def is_enabled(self):
        return self.is_command_option_enabled('ignore')

    def process_codebase(self, codebase):
        """
        Remove ignored Resources from the resource tree.
        """
        ignore_opt = self.get_command_option('ignore')
        ignores = ignore_opt and ignore_opt.value or  []
        if not ignores:
            return

        ignores = {
            pattern: 'User ignore: Supplied by --ignore' for pattern in ignores
        }

        ignorable = partial(is_ignored, ignores=ignores)
        resources_to_remove = []
        resources_to_remove_append = resources_to_remove.append

        # first walk top down the codebase and collect ignored resource ids
        for resource in codebase.walk(topdown=True):
            if ignorable(resource.get_path(absolute=False, posix=True)):
                resources_to_remove_append(resource)

        # then remove the collected ignored resource ids (that may remove whole
        # trees at once) in a second step
        removed_rids = set()
        removed_rids_update = removed_rids.update
        remove_resource = codebase.remove_resource

        for resource in resources_to_remove:
            if resource.rid in removed_rids:
                continue
            pruned_rids = remove_resource(resource)
            removed_rids_update(pruned_rids)


def is_ignored(location, ignores):
    """
    Return a tuple of (pattern , message) if a file at location is ignored or
    False otherwise. `ignores` is a mappings of patterns to a reason.
    """
    return match(location, includes=ignores, excludes={})
