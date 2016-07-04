# Copyright 2016 The Fabulous Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A series of functions that provide useful casts from strings into other common objects.

Mainly for usage with input_object in the above package.
"""

from os import path

def yes_no(value):
    """For a yes or no question, returns a boolean.
    """
    if value.lower() in ('yes','y'):
        return True
    if value.lower() in ('no','n'):
        return False
    raise ValueError, "value should be 'yes' or 'no'"


def file(value, **kwarg):
    """value should be a path to file in the filesystem.
    
    returns a file object
    """
    #a bit weird, but I don't want to hard code default values
    try:
        f = open(value, **kwarg)
    except IOError, e:
        raise ValueError, "unable to open %s : %s" % (path.abspath(value), e)
    return f
