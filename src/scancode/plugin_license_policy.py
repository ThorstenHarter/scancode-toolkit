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
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from os.path import abspath
from os.path import dirname
from os.path import exists
from os.path import isdir
from os.path import join

from commoncode import saneyaml
from plugincode.post_scan import PostScanPlugin
from plugincode.post_scan import post_scan_impl
from scancode import CommandLineOption
from scancode import POST_SCAN_GROUP


@post_scan_impl
class LicensePolicy(PostScanPlugin):
    """
    Add the "license_policy" attribute to a resouce if it contains a 
    detected license key that is found in the license_policy.yml file
    """
    sort_order = 9

    options = [
        CommandLineOption(('--license-policy',),
            # TODO: Not sure what the minimum set of defaults is here
            multiple=False,
            metavar='<license_policy>',
            help='Load License Policy file and apply it to the codebase.',
            help_group=POST_SCAN_GROUP
        )
    ]

    def is_enabled(self, license_policy, **kwargs):
        return license_policy

    def process_codebase(self, codebase, license_policy, **kwargs):
        """
        """
        if not self.is_enabled(license_policy):
            # TODO: fail here, or print a message
            return

        license_policy = load_license_policy(license_policy)
        
        # TODO: iterate thru and apply the policy


def load_license_policy(license_policy):
    """
    Return a license policy loaded from the license policy file.
    """
    if not license_policy or not exists(license_policy):
        return {}
    elif isdir(license_policy):
        return {}
    with open(license_policy, 'r') as conf:
        conf_content = conf.read()
    return saneyaml.load(conf_content)
