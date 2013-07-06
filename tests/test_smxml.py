"""test of smxml Summon Monster XML methods and functions

smxml.py contains the methods and functions used to 
query xml data for Summon Monster Four One One (sm411).
"""



import os
import random
import sys
import unittest


from summonfouroneone import smxml


class summon_monster_four_one_one(unittest.TestCase):
    """ test smxml """

    def setUp(self):
        """ set up goes here """
        pass


    def test_find_all_id_attributes_for_monster_elements_on_sm1_sl(self):
        """given a 1, find all ID values for monster elements on SM1 spell list"""
        expect = ['100', '101', '102', '103', '104', '105', '106', '107'] 
        mx = smxml.smxml()
        result = mx.search_for_id_attributes(1)
        self.assertEqual(expect, result)


    def test_find_all_id_attributes_for_monster_elements_on_sm2_sl(self):
        """given a 2, find all ID values for monster elements on SM2 spell list"""
        expect = ['200', '201', '202', '203', '204', '205', '206', '207', '208', '209', 
                  '210', '211', '212', '213', '214']
        mx = smxml.smxml()
        result = mx.search_for_id_attributes(2)
        self.assertEqual(expect, result)


    def test_find_all_id_attributes_for_monster_elements_on_sm3_sl(self):
        """given a 3, find all ID values for monster elements on SM3 spell list"""
        expect = ['300', '301', '302', '303', '304', '305', '306', '307', '308', '309', 
                  '310', '311', '312', '313', '314', ]
        mx = smxml.smxml()
        result = mx.search_for_id_attributes(3)
        self.assertEqual(expect, result)


    def test_find_all_id_attributes_for_monster_elements_on_sm4_sl(self):
        """given a 4, find all ID values for monster elements on SM4 spell list"""
        expect = ['400', '401', '402', '403', '404', '405', '406', '407', '408', '409', 
                  '410', '411', '412', '413', '414', '415', '416', '417', '418', '419', 
                  '420', '421', '422', '423', '424', '425', '426', '427', ]
        mx = smxml.smxml()
        result = mx.search_for_id_attributes(4)
        self.assertEqual(expect, result)


    def test_find_all_id_attributes_for_all_monster_elements_on_all_sl(self):
        self.maxDiff = None
        """given a 0, find all ID values for all monster elements on all spell lists"""
        expect = ['100', '101', '102', '103', '104', '105', '106', '107', 
                  '200', '201', '202', '203', '204', '205', '206', '207', '208', '209', 
                  '210', '211', '212', '213', '214',
                  '300', '301', '302', '303', '304', '305', '306', '307', '308', '309', 
                  '310', '311', '312', '313', '314',
                  '400', '401', '402', '403', '404', '405', '406', '407', '408', '409', 
                  '410', '411', '412', '413', '414', '415', '416', '417', '418', '419', 
                  '420', '421', '422', '423', '424', '425', '426', '427',
                  '600']
        mx = smxml.smxml()
        result = mx.search_for_id_attributes(0)
        self.assertEqual(expect, result)


    def test_return_elements_for_id_600(self):
        """given monster element with attribute id=600, return child elements"""
        expect = [[{'name': 'succubus (demon)'}, {'prd': 'http://paizo.com/pathfinderRPG/prd/monsters/demon.html#demon-succubus'}, {'alignment': 'CE'}, {'size': 'M'}]]
        mx = smxml.smxml()
        result = mx.id_attributes_into_element_values(['600'])
        self.assertEqual(expect, result)


    def test_find_id_value_for_monster_name(self):
        """given the name Dolphin, find id 106 """
        expect = ['106'] 
        mx = smxml.smxml()
        result = mx.search_for_monster_name("Dolphin")
        self.assertEqual(expect, result)


    def test_ignore_case_when_id_value_for_monster_name(self):
        """given the name doLPHin, find id 106 """
        expect = ['106'] 
        mx = smxml.smxml()
        result = mx.search_for_monster_name("doLPHin")
        self.assertEqual(expect, result)


    def test_on_partial_name_find_a_match(self):
        """given partial input dolph, find id 106 """
        expect = ['106'] 
        mx = smxml.smxml()
        result = mx.search_for_monster_name("dolph")
        self.assertEqual(expect, result)


    def test_given_id_return_dict_keys_simple_eagle(self):
        """sorted id2dict keys on eagle id 101 """
        expect = ['alignment', 'name', 'prd', 'size']
        mx = smxml.smxml()
        result = sorted(mx.id_into_dict('301', ['name','prd','alignment','size']).keys())
        self.assertEqual(expect, result)


    def test_given_id_return_dict_keys_complicated_dretch(self):
        """sorted id2dict keys on dretch id 308 with subelements """
        expect = ['alignment', 'name', 'prd', 'size', 'special_qualities']
        mx = smxml.smxml()
        result = sorted(mx.id_into_dict('308', ['name','prd','alignment','size','special_qualities']).keys())
        self.assertEqual(expect, result)


    def test_given_id_return_dict_values_complicated_dretch(self):
        """sorted id2dict values on dretch id 308 subelements  'special_qualities' """
        expect = ['DR 5/cold iron or good', 'cause fear (DC11) 1/day', 'immune electricity', 
           'immune poison', 'resist acid 10', 'resist cold 10', 
           'resist fire 10', 'stinking cloud (DC13) 1/day']
        mx = smxml.smxml()
        result = sorted(mx.id_into_dict('308', ['name','prd','alignment','size','special_qualities'])['special_qualities'])
        self.assertEqual(expect, result)


    def test_given_id_and_key_not_in_element_pass(self):
        """pass on nonexistent  key 'foobar' on dretch id 308 with subelements """
        expect = ['alignment', 'name', 'prd', 'size', 'special_qualities']
        mx = smxml.smxml()
        result = sorted(mx.id_into_dict('308', ['name','prd','alignment','foobar', 'size','special_qualities']).keys())
        self.assertEqual(expect, result)


    def test_find_id_value_for_monster_sq_term(self):
        """given the sq_term blindsense, find id 307 """
        expect = ['307'] 
        mx = smxml.smxml()
        result = mx.search_for_monster_sq("blindsense")
        self.assertEqual(expect, result)


    def test_ignore_case_when_id_value_for_monster_sq_term(self):
        """given the sq_term bliNDSEnse, find id 307 """
        expect = ['307'] 
        mx = smxml.smxml()
        result = mx.search_for_monster_sq("bliNDSEnse")
        self.assertEqual(expect, result)


    def test_on_partial_sq_term_find_a_match(self):
        """given partial input blindsens, find id 307 """
        expect = ['307'] 
        mx = smxml.smxml()
        result = mx.search_for_monster_sq("blindsens")
        self.assertEqual(expect, result)




if __name__ == "__main__":
    unittest.main() 
        