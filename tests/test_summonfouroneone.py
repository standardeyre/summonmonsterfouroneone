"""test of summonfouroneone module methods 

summonfouroneone is a (bad) portmanteau of
  Summon Monster 411

The file summonfouroneone.py contains methods
  to help with directory assistance when summoning monsters
  in the PFRPG.
"""



import os
import random
import sys
import unittest


from summonfouroneone import smfoo
from summonfouroneone import smxml
from summonfouroneone import rpg_data_mangling

class summonmonsterfouroneone(unittest.TestCase):
    """ test smfoo methods """

    def setUp(self):
        """ set up goes here """
        pass


    def test_return_html_for_monobj_attr_full(self):
        """for a monster object attribute with a value, return html string """
        expect = '5'
        monobj = smfoo.monster_object()
        monobj.set_hit_points(5)
        result = monobj.get_html_string('hit_points')
        self.assertEqual(expect, result)


    def test_return_html_for_monobj_attr_empty(self):
        """for an empty monster object attribute (value is None), return html non-brk space """
        expect = '&nbsp;'
        monobj = smfoo.monster_object()
        result = monobj.get_html_string('senses')
        self.assertEqual(expect, result)


    def test_find_hd_of_eagle(self):
        """given an eagle, return the number of hit dice the eagle has"""
        expect = 1 
        mx = smxml.smxml()
        raw_hitdice = sorted(mx.id_into_dict('101', ['hit_dice']).values())[0]
        # raw_hitdice would contain something like (1d8+2) and we want only the 1
        result = rpg_data_mangling.parse_dice(raw_hitdice)[0]
        self.assertEqual(expect, result)


    def test_find_hp_of_eagle(self):
        """given an eagle, return the value for average hit points """
        expect = 5 
        mx = smxml.smxml()
        raw_hitpoints = sorted(mx.id_into_dict('101', ['hit_points']).values())[0]
        result = int(raw_hitpoints)
        self.assertEqual(expect, result)


    def test_find_hp_of_eagle_w_augs_feat(self):
        """given an eagle, apply augment summoning feat, show hit points """
        expect = 7 
        mx = smxml.smxml()
        raw_hitpoints = sorted(mx.id_into_dict('101', ['hit_points']).values())[0]
        raw_hitdice = sorted(mx.id_into_dict('101', ['hit_dice']).values())[0]
        hitdice = rpg_data_mangling.parse_dice(raw_hitdice)[0]
        hitpoints = smfoo.apply_augs_feat(hitdice, raw_hitpoints)
        result = int(hitpoints)
        self.assertEqual(expect, result)


    def test_call_monster_apply_augs_feat_get_hit_points(self):
        """use monster's apply_augs_feat() method to apply feat, show hit points """
        expect = 7 
        monobj = smfoo.monster_object()
        monobj.set_hit_points(5)
        monobj.set_hit_dice("1d8+1")
        monobj.apply_augs_feat()
        hitpoints = monobj.get_html_string('hit_points')
        result = int(hitpoints)
        self.assertEqual(expect, result)


    def test_find_sq_of_eagle(self):
        """find the special qualities of a eagle, no template """
        expect = '&nbsp;'
        monobj = smfoo.monster_object()
        result = monobj.get_html_string('sq')
        self.assertEqual(expect, result)


    def test_find_sq_of_eagle_celestial(self):
        """find the special qualities of a eagle with celestial template """
        expect = 'DR 5/evil'
        monobj = smfoo.monster_object()
        monobj.set_hit_dice("1d8+1")
        monobj.apply_celestial_template()
        result = monobj.get_html_string('sq')
        self.assertEqual(expect, result)


    def test_find_sq_of_eagle_infernal(self):
        """find the special qualities of a eagle with infernal template """
        expect = """['DR 5/good', 'resist fire 5']"""
        monobj = smfoo.monster_object()
        monobj.set_hit_dice("1d8+1")
        monobj.apply_infernal_template()
        result = monobj.get_html_string('sq')
        self.assertEqual(expect, result)


    def test_find_name_of_first_monobj_in_resultset(self):
        """build a results list, find the name of the first object in that list """
        expect = 'dog, riding'
        ro = smfoo.results_object()
        for term in ['dog, riding', 'eagle']:
            monobj = smfoo.monster_object()
            monobj.set_name(term)
            ro.set_results_list(monobj)
        ### assumption here is that with two items, the term we want
        ### is always the name of the first item
        result_object = ro.get_results_list()[0]
        result = result_object.get_name()
        self.assertEqual(expect, result)
            

    def test_find_name_of_second_monobj_in_resultset(self):
        """build a results list, find the name of the second object in that list """
        expect = 'eagle'
        ro = smfoo.results_object()
        for term in ['dog, riding', 'eagle']:
            monobj = smfoo.monster_object()
            monobj.set_name(term)
            ro.set_results_list(monobj)
        ### assumption here is that with two items, the term we want
        ### is always the name of the second item
        result_object = ro.get_results_list()[1]
        result = result_object.get_name()
        self.assertEqual(expect, result)


    def test_build_name_w_hyperlink(self):
        """return href with name as linktext and prd link as link target"""
        expect = """<a href="foobar">eagle</a>"""
        monobj = smfoo.monster_object()
        monobj.set_name('eagle')  # give object a name 
        monobj.set_prd('foobar')  # give object a link
        monobj.set_name_w_link()  # set the attribe w name and link
        result = monobj.get_name_w_link() # get attribute 
        self.assertEqual(expect, result)
            

    def test_display_help_text(self):
        """request for help displays help text"""
        expect = smfoo.help_text
        result = smfoo.display_help_text()
        self.assertEqual(expect, result)


if __name__ == "__main__":
    unittest.main() 
        