#
# Gramps - a GTK+/GNOME based genealogy program
#
# Copyright (C) 2003-2006  Donald N. Allingham
#               2009       Gary Burton
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

#-------------------------------------------------------------------------
#
# internationalization
#
#-------------------------------------------------------------------------

#-------------------------------------------------------------------------
#
# gramps modules
#
#-------------------------------------------------------------------------
from gramps.gen.const import GRAMPS_LOCALE as glocale
_ = glocale.translation.sgettext
from ..views.treemodels import FamilyModel
from .baseselector import BaseSelector
from gramps.gui.display import display_help
from gramps.gen.const import URL_MANUAL_PAGE

#-------------------------------------------------------------------------
#
# Constants
#
#-------------------------------------------------------------------------
WIKI_HELP_PAGE = '%s_-_Categories' % URL_MANUAL_PAGE
WIKI_HELP_SEC = _('manual|Select_Family_selector')

FAMILY_DATE = None

#-------------------------------------------------------------------------
#
# SelectFamily
#
#-------------------------------------------------------------------------
class SelectFamily(BaseSelector):

    namespace = 'Family'

    def __init__(self, dbstate, uistate, track=[], title=None, filter=None,
                 skip=set(), show_search_bar=False, default=None):

        # SelectFamily may have a title passed to it which should be used
        # instead of the default defined for get_window_title()
        if title is not None:
            self.title = title

        history = uistate.get_history(self.namespace).mru
        active_handle = uistate.get_active(self.namespace)

        # see gui.plug._guioptions

        from gramps.gen.filters import GenericFilterFactory, rules

        # Baseselector?
        # Create a filter for the family selector.
        sfilter = GenericFilterFactory(self.namespace)()
        sfilter.set_logical_op('or')
        sfilter.add_rule(rules.family.IsBookmarked([]))

        # Add recent families.
        for handle in history:
            recent = dbstate.db.get_family_from_handle(handle)
            gid = recent.get_gramps_id()
            sfilter.add_rule(rules.family.HasIdOf([gid]))

        # Add bookmarked families.
        for handle in dbstate.db.get_family_bookmarks().get():
            marked = dbstate.db.get_family_from_handle(handle)
            gid = marked.get_gramps_id()
            sfilter.add_rule(rules.family.HasIdOf([gid]))

        BaseSelector.__init__(self, dbstate, uistate, track, sfilter,
                              skip, show_search_bar, active_handle)

    def _local_init(self):
        """
        Perform local initialisation for this class
        """
        self.setup_configs('interface.family-sel', 600, 450)
        SWITCH = self.switch.get_state()

    def get_window_title(self):
        return _("Select Family")

    def get_model_class(self):
        return FamilyModel

    def get_column_titles(self):
        return [
            (_('ID'),      75, BaseSelector.TEXT, 0),
            (_('Father'), 200, BaseSelector.TEXT, 1),
            (_('Mother'), 200, BaseSelector.TEXT, 2),
            #(_('Last Change'), 150, BaseSelector.TEXT, 7),
            ]

    def get_from_handle_func(self):
        return self.db.get_family_from_handle
