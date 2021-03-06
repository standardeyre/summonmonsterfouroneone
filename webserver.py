""" webserver.py

copyright (c) 2015  by david sloboda

This file is part of summonmonsterfouroneone.

summonmonsterfouroneone is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

summonmonsterfouroneone is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with summonmonsterfouroneone in the file COPYING.
If not, see <http://www.gnu.org/licenses/>.





PURPOSE:
run a webserver that takes user input and returns useful output
   about summoned monsters.

minimalist web server provided by web.py module

"""

import re
import web
from web import form
# next import breaks out XML search routines into a separate file
#   for ease in unit testing.
from summonfouroneone import smxml


### routines to check user input for sanity (sane characters only)
from summonfouroneone import handle_form_input

### treat the monsters as objects with methods and attributes
from summonfouroneone import smfoo
RO = smfoo.ResultsObject()
render = web.template.render('templates/')
URLS = ('/', 'IndexSummonMonster')
APP = web.application(URLS, globals())
MYFORM = form.Form(
    form.Textbox("searchfield",
        form.notnull,
        description="input: help, 0 to 9, 'dire wolf', blindSENSE, +a, +good ",
        size="60",
        maxlength="100"
        ),
    form.Button("Submit a SumMon411 search!")
    )


def check_for_synonyms(search_term):
    """There will be a better way of doing this... one day...
    """
    result = ""
    terms = {}
    terms[0] = ["all"]
    terms[1] = ["sm1", "smi", "msi", "ms1",
                "summon monster i", "summon monster 1",
                "monster summoning i",
                "monster summoning 1", "one"]
    terms[2] = ["sm2", "smii", "msii", "ms2", "summon monster ii",
                "summon monster 2", "monster summoning ii",
                "monster summoning 2", "two"]
    terms[3] = ["sm3", "smiii", "msiii", "ms3", "summon monster iii",
                "summon monster 3", "monster summoning iii",
                 "monster summoning 3", "three"]
    terms[4] = ["sm4", "smiv", "msiv", "ms4", "summon monster iv",
                "summon monster 4", "monster summoning iv",
                "monster summoning 4", "four"]
    terms[5] = ["sm5", "smv", "msv", "ms5", "summon monster v",
                "summon monster 5", "monster summoning v",
                "monster summoning 5", "five"]
    for res in terms.keys():
        if search_term.lower() in terms.values()[res]:
            result = res
            break
        else:
            result = search_term
    return result


def check_if_modifier(input_value):
    """determine if input starts with a plus sign

    modifers like +good +celestial +augs start with plus sign
    and modify other terms.

    returns either (yes, modifier_without_plus_sign)
    or
    (no, input_value)
    """
    result = ()
    pattern = '^\+'
    prog = re.compile(pattern)
    match_result = prog.search(input_value)
    if match_result:
        return_value = re.sub(pattern, '', input_value)
        result = ("yes", return_value)
    else:
        result = ("no", input_value)
    return result


def handle_modifier(myinput):
    """handle any modifiers thrown into the search field.

    A modifier starts with a plus sign
    example:   +good
    example:   +infernal

    return the text associated with the myinput.
    """
    result = ""
    augment_summoning_terms = ["augs", "augment_summoning",
                               "augment summoning", "a"]
    celestial_terms = ["good", "celestial", "g", "gd"]
    infernal_terms = ["evil", "infernal", "e", "ev"]
    extended_display_terms = ["extended", "extend", "ext", "ex", "x"]
    list_display_terms = ["normal", "list", "n"]
    myinput = myinput.lower()
    if myinput in augment_summoning_terms:
        result = "The Augment Summoning feat gives +4 to STR and +4 to CON"
        result = result + " for each summoned creature. "
    # set [celestial or infernal] flag once only.  Use first flag set
    if ("celestial" not in RO.get_modifier_flags() and
        "infernal" not in RO.get_modifier_flags()):
        if myinput in celestial_terms:
            RO.zero_modifier_flags()
            RO.set_modifier_flags("celestial")
            result = "Summoned creatures with the Celestial template "
            result = result + " smite evil. "
        if myinput in infernal_terms:
            RO.zero_modifier_flags()
            RO.set_modifier_flags("infernal")
            result = "Summoned creatures with the Infernal template "
            result = result + " smite good."
    ##### set display flag once only.  Use standard unless flag set
    if myinput in extended_display_terms:
        result = "You chose the extended display. "
        RO.set_display_output("extended")
    if myinput in list_display_terms:
        result = "You chose the normal display. "
        RO.set_display_output("standard_list")
    return result


def input_is_integer(myinput):
    """Determine if myinput is integer

    If it is an integer, return an integer.
    If not, lower case the myinput
       and see if it is something else.
    """
    result = ""
    try:
        term = int(myinput)
        if term > -1:
            result = myinput
    except ValueError:
        myinput = myinput.lower()
        result = check_if_modifier(myinput)
    return result


class IndexSummonMonster:
    """ used for web.py base page"""
    def __init__(self):
        """ not used """
        pass

    def GET(self):
        """ webserver.py GET method """
        my_form = MYFORM()
        global RO
        return render.formresult(my_form, RO)


    def POST(self):
        """ webserver.py POST method """
        post_form = MYFORM()
        global RO
        #  remove any previous results from previous searches
        RO.zero_results_list()
        # remove any previous modifier flags.  Maybe we're no longer evil.
        RO.zero_modifier_flags()
        myextras = ""
        if not post_form.validates():
            return render.formresult(post_form, RO)
        else:
            xml_element_results = []
            xml_id_results = []
            weed_out_duplicates = []
            text = ""
            searchterm = post_form.d.searchfield
            ### first, for debugging, capture original form input.
            ### comment out the next two lines for production use
            text = "You submitted: [%s]\n" % searchterm
            RO.set_results_text(text)
            ### sanity check the data sent from the customer
            searchterm = handle_form_input.check_input_length(searchterm)
            searchterm = handle_form_input.scrub_form_input(searchterm)
            searchterm = searchterm.lower()  # lower case text for searching
            ### check if this is a True Cry For Help
            if handle_form_input.check_is_input_cry_for_help(searchterm):
                help_text = RO.get_results_text()
                help_text = help_text +  smfoo.display_help_text("html")
                RO.set_results_text(help_text)
                return render.formresult(post_form, RO)
            smx = smxml.Smxml()
            input_values = handle_form_input.split_input_keep_quotes(searchterm)
            #### look up synonyms before weeding out duplicates.
            #### put something in here to weed out duplicates
            #
            #### set standard list of keys for monster attributes
#            makeys = ['alignment', 'name', 'prd', 'size']
            for myinput in input_values:
                result = input_is_integer(myinput)
                if type(result) == tuple:
                    if result[0] == "yes":# we have a modifier, like +good
                        modifier_text = handle_modifier(str(result[1]))
                        myextras = RO.get_results_text() + modifier_text
                        RO.set_results_text(myextras)
                    else:
                        # we have other text input, like "dog, riding" or "all"
                        # check it for synonyms and normalize it
                        norm_st = check_for_synonyms(str(result[1]))
                        try:
                            norm_st = int(norm_st)
                            xml_id_results = smx.search_for_id_attributes(
                                             norm_st)
                        except ValueError:
                            xml_id_results = smx.search_for_monster_name(
                                             norm_st)
                        # If this list is empty,
                        #  no monster names like 'wolf' have been provided.
                        # Assume it is a special quality search
                        #  on a term like "blindsense'
                        if not xml_id_results:
                            xml_id_results = smx.search_for_monster_sq(norm_st)
                else:  # we have an integer
                    xml_id_results = smx.search_for_id_attributes(result)
                mon_att_keys = ['name', 'prd', 'hit_dice', 'hit_points',
                                'special_qualities', 'size', 'alignment']
                for monster_id in xml_id_results:
                    # create new monster object
                    monster_obj = smfoo.MonsterObject()
                    mon_dict = {}
                    mon_dict = smx.id_into_dict(monster_id, mon_att_keys)
                    # set the monster id from xml file into MonsterObject
                    monster_obj.set_id(monster_id)
                    # set a boolean flag if the monster takes a c_or_i template
                    monster_obj.set_takes_c_or_i_template(
                        smx.monster_takes_c_or_i_template([monster_id]))
                    for attribute in mon_att_keys:
                        try:
                            throwaway = getattr(monster_obj,
                                                "set_%s" %
                                                attribute)(mon_dict[attribute])
                        except KeyError:
                            throwaway = getattr(monster_obj,
                                                "set_%s" % attribute)("")
                        throwaway = monster_obj.set_name_w_link()
                    # Sometimes the input could be "eagle eagle eagle"
                    # Weed out duplicates
                    if monster_obj.get_name() not in weed_out_duplicates:
                        xml_element_results.append(monster_obj)
                        weed_out_duplicates.append(monster_obj.get_name())
                for returned_result in xml_element_results:
                    if returned_result not in RO.get_results_list():
                        RO.set_results_list(returned_result)
            ### set HTML list or HTML table.  Default is list
            if RO.get_display_output() == "extended":
                ### see if apply celestial or infernal template
                if  "Celestial" in RO.get_results_text():
                    newlist = []
                    for monster_obj in RO.get_results_list():
                        newlist.append(monster_obj)
                    RO.zero_results_list()
                    for mon_obj in newlist:
                        mon_obj.apply_template("celestial")
                        RO.set_results_list(mon_obj)
                elif "Infernal" in RO.get_results_text():
                    newlist = []
                    for monster_obj in RO.get_results_list():
                        newlist.append(monster_obj)
                    RO.zero_results_list()
                    for mon_obj in newlist:
                        mon_obj.apply_template("infernal")
                        RO.set_results_list(mon_obj)
                ### hack to get Augmented Summoning
                ###     to show up in extended display
                if "The Augment Summoning feat" in RO.get_results_text():
                    newlist = []
                    for monster_obj in RO.get_results_list():
                        newlist.append(monster_obj)
                    RO.zero_results_list()
                    for mon_obj in newlist:
                        mon_obj.apply_augs_feat()
                        RO.set_results_list(mon_obj)
                return render.formresultextended(post_form, RO)
            else:
                return render.formresult(post_form, RO)



if __name__ == "__main__":
    web.internalerror = web.debugerror
    APP.run()
