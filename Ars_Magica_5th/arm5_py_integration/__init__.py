"""Module for providing the parts in the template.html file"""
from pathlib import Path

import markdown
from bs4 import BeautifulSoup as soup

from .helpers import (
    CHARACTERISTICS,
    FORMS,
    TECHNIQUES,
    enumerate_helper,
    repeat_template,
)
from .translations import translation_attrs, translation_attrs_setup


# Xp helper
def xp(
    name: str, *, suffix="_exp", adv_suffix="_advancementExp", tot_suffix="_totalExp"
) -> str:
    """
    Generate the HTML for the Xp parts of arts & abilities
    """
    return f"""[<input type="text" class="sheet-number_3" name="attr_{name}{suffix}" value="0"/>/<input type="text" class="sheet-number_3 advance" name="attr_{name}{adv_suffix}" value="0" readonly/>/<input type="text" class="sheet-number_3 total" name="attr_{name}{tot_suffix}" value="0" readonly/>]"""


def alert(title: str, text: str, *, level: str = "warning", ID: str = None):
    """
    Generate the HTML to display a banner that can be permanently hidden

    This is used to inform player of important changes in updates.

    Arguments:
        text: Main text of the banner
        title: Title of the banner
        type: On of "warning", "info". The aspect of the banner
        ID: optional string ID of this banner, if you need to check if it is
            open/closed somewhere. Do NOT use numbers
    """
    if not level in ("info", "warning"):
        raise ValueError("Level must be among 'info', 'warning'")
    if ID is None:
        numid = alert.numid
        alert.numid += 1
    else:
        numid = str(ID)
    return f"""<input type="hidden" class="sheet-alert-hidder" name="attr_alert-{numid}" value="0"/>
<div class="sheet-alert sheet-alert-{level}">
    <div>
        <h3> {level.title()} - {title}</h3>
        {text}
    </div>
    <label class="sheet-fakebutton">
        <input type="checkbox" name="attr_alert-{numid}" value="1" /> ×
    </label>
</div>"""


# python supports attributes on function
# we use that to store the internal global variable used by the function
alert.numid = 0

# Add new parts to this dictionary
# parts can be defined in other modules and imported here if the generating
# code is long
GLOBALS = {
    "markdown": markdown,  # makes the module available
    "xp": xp,  # makes the function available in the HTML
    "alert": alert,  # makes the function available in the HTML
    "translation_attrs": translation_attrs,
    "translation_attrs_setup": translation_attrs_setup,
    "header": "<!-- This file is automatically generated from a template. Any change will be overwritten -->",
}

# Personality traits
GLOBALS["personality_trait_rows"] = repeat_template(
    """<tr>
    <td><input type="text" class="sheet-heading_2" style="width:245px" name="attr_Personality_Trait%%"/></td>
    <td><input type="text" class="sheet-number_1" style="width:70px;" name="attr_Personality_Trait%%_score"/></td>
    <td><div class="sheet-flex-container">
        <button type="roll" class="sheet-button sheet-simple-roll" name="roll_personality%%_simple" value="&{template:generic} {{Banner=^{personality} ^{roll}}} {{Label=@{Personality_Trait%%}}} {{Result=[[@{simple-die} + [[@{Personality_Trait%%_Score}]] [@{Personality_Trait%%}] + (?{@{circumstantial_i18n}|0}) [@{circumstances_i18n}] ]]}} "></button>
        <button type="roll" class="sheet-button sheet-stress-roll" name="roll_personality%%_stress" value="&{template:generic} {{Banner=^{personality} ^{roll}}} {{Label=@{Personality_Trait%%}}} {{Result=[[@{stress-die} + [[@{Personality_Trait%%_Score}]] [@{Personality_Trait%%}] + (?{@{circumstantial_i18n}|0}) [@{circumstances_i18n}] ]]}} {{stress=1}} {{botch-button=[@{botch_i18n}!](~@{character_name}|botch)}} {{crit-button=[@{critical_i18n}!](~@{character_name}|critical)}}"></button>
    </div></td>
</tr>""",
    range(1, 7),
)


# Reputations
GLOBALS["reputation_rows"] = repeat_template(
    """<tr>
    <td><input type="text" class="sheet-heading_2" name="attr_Reputations%%"/></td>
    <td><input type="text" class="sheet-heading_2a" name="attr_Reputations%%_type"/></td>
    <td><input type="text" class="sheet-number_1" style="width:50px;" name="attr_Reputations%%_score"/></td>
    <td><div class="sheet-flex-container">
        <button type="roll" class="sheet-button sheet-simple-roll" name="roll_reputation%%_simple" value="&{template:generic} {{Banner=^{reputation} ^{roll}}} {{Label=@{Reputations%%}}} {{Result=[[@{simple-die} + [[@{Reputations%%_Score}]] [@{Reputations%%}] + (?{@{circumstantial_i18n}|0}) [@{circumstances_i18n}] ]] }}"></button>
        <button type="roll" class="sheet-button sheet-stress-roll" name="roll_reputation%%_stress" value="&{template:generic} {{Banner=^{reputation} ^{roll}}} {{Label=@{Reputations%%}}} {{Result=[[@{stress-die} + [[@{Reputations%%_Score}]] [@{Reputations%%}] + (?{@{circumstantial_i18n}|0}) [@{circumstances_i18n}]]] }} {{stress=1}} {{botch-button=[@{botch_i18n}!](~@{character_name}|botch)}} {{crit-button=[@{critical_i18n}!](~@{character_name}|critical)}}"></button>
    </div></td>
</tr>""",
    range(1, 7),
)


# Characteristics definitions
characteristic_roll = "(@{%(Char)s_Score}) [@{%(char)s_i18n}] + (@{wound_total}) [@{wounds_i18n}] + ([[floor(@{Fatigue})]]) [@{fatigue_i18n}] + (?{@{circumstantial_i18n}|0}) [@{circumstances_i18n}]"
GLOBALS["characteristic_rows"] = repeat_template(
    """<tr>
    <th data-i18n="%(char)s" >%(Char)s</th>
    <td><input type="text" class="sheet-heading_2" name="attr_%(Char)s_Description"/></td>
    <td><input type="text" class="sheet-number_1" name="attr_%(Char)s_Score" value="0"/></td>
    <td><input type="text" class="sheet-number_1" name="attr_%(Char)s_Aging" value="0"/></td>
    <td><div class="sheet-flex-container">
        <button type="roll" class="sheet-button sheet-simple-roll" name="roll_%(Char)s_simple" value="&{template:ability} {{name= @{character_name}}} {{label0=^{%(char)s}}} {{banner=@{%(Char)s_Description}}} {{label1=^{score}}} {{result1=@{%(Char)s_Score}}} {{label2=^{characteristic-m}}} {{label2=^{weakness-m}}} {{result2=[[[[floor(@{Fatigue})]][@{fatigue_i18n}] + @{wound_total}[@{wounds_i18n}]]]}} {{label3=^{circumstances-m}}} {{result3=[[(?{@{circumstantial_i18n}|0})]]}} {{result0=[[ @{simple-die} + $characteristic_roll$ ]]}}"></button>
        <button type="roll" class="sheet-button sheet-stress-roll" name="roll_%(Char)s_stress" value="&{template:ability} {{name= @{character_name}}} {{label0=^{%(char)s}}} {{banner=@{%(Char)s_Description}}} {{label1=^{score}}} {{result1=@{%(Char)s_Score}}} {{label2=^{characteristic-m}}} {{label2=^{weakness-m}}} {{result2=[[[[floor(@{Fatigue})]][@{fatigue_i18n}] + @{wound_total}[@{wounds_i18n}]]]}} {{label3=^{circumstances-m}}} {{result3=[[(?{@{circumstantial_i18n}|0})]]}} {{result0=[[ @{stress-die} + $characteristic_roll$ ]]}} {{stress=1}} {{botch-button=[@{botch_i18n}!](~@{character_name}|botch)}} {{crit-button=[@{critical_i18n}!](~@{character_name}|critical)}}"></button>
    </div></td>
</tr>""".replace(
        "$characteristic_roll$", characteristic_roll
    ),
    CHARACTERISTICS,
    str_key="char",
)

# Characteristic options
GLOBALS["characteristic_score_options"] = repeat_template(
    """<option value="@{%(Char)s_Score}" data-i18n="%(char)s" >%(Char)s</option>""",
    CHARACTERISTICS,
    str_key="char",
)
GLOBALS["characteristic_score_ask"] = (
    "?{@{characteristic_i18n}|"
    + "| ".join(
        "@{%(char)s_i18n}, @{%(Char)s_Score} [@{%(char)s_i18n}]"
        % {"char": char, "Char": char.capitalize()}
        for char in CHARACTERISTICS
    )
    + "}"
)
GLOBALS["characteristic_name_options"] = repeat_template(
    """<option value="%(Char)s" data-i18n="%(char)s" >%(Char)s</option>""",
    CHARACTERISTICS,
    str_key="char",
)
GLOBALS["characteristic_name_ask_attr"] = (
    "?{@{characteristic_i18n}|"
    + "| ".join(
        "@{%(char)s_i18n},@{%(char)s_Score} [@{%(char)s_i18n}]" % {"char": char}
        for char in CHARACTERISTICS
    )
    + "}"
)

# Abilities
ability_roll_template = "&{template:ability} {{name=@{character_name}}} {{label0=@{Ability_name}}} {{banner=@{Ability_Speciality}}} {{label1=^{rank}}} {{result1= [[ @{Ability_Score} + @{Ability_Puissant} ]]}} {{label2=@{Ability_CharacName}}} {{result2=[[@{sys_at}@{character_name}@{sys_pipe}@{Ability_CharacName}_Score@{sys_rbk}]]}} {{label3=^{weakness-m}}} {{result3=[[ ([[floor(@{Fatigue})]]) [@{fatigue_i18n}] + (@{wound_total}) [@{wounds_i18n}] ]]}} {{label4=^{circumstances-m}}} {{result4=[[(?{@{circumstantial_i18n}|0})]]}} {{result0=%(roll)s}} {{botch-button=[@{botch_i18n}!](~@{character_name}|botch)}} {{crit-button=[@{critical_i18n}!](~@{character_name}|critical)}}"
ability_roll = "[[ %(die)s + (@{Ability_Score} + @{Ability_Puissant}) [@{Ability_name}] + (@{sys_at}@{character_name}@{sys_pipe}@{Ability_CharacName}_Score@{sys_rbk}) [@{sys_at}@{character_name}@{sys_pipe}@{Ability_CharacName}_i18n@{sys_rbk}] + (@{wound_total}) [@{wounds_i18n}] + ([[floor(@{Fatigue})]]) [@{fatigue_i18n}] + (?{@{circumstantial_i18n}|0}) [@{circumstances_i18n}] ]]"
GLOBALS["ability_roll_simple"] = ability_roll_template % {
    "roll": ability_roll % {"die": "@{simple-die}"}
}
GLOBALS["ability_roll_stress"] = (
    ability_roll_template % {"roll": ability_roll % {"die": "@{stress-die}"}}
) + " {{stress=1}}"


# Technique definitions
GLOBALS["technique_definitions"] = repeat_template(
    """<tr>
    <td><input type="text" class="sheet-number_3" name="attr_%(Tech)s_Score" value="0"/></td>
    <td data-i18n="%(tech)s" >%(Tech)s</td>
    <td>"""
    + xp("%(Tech)s")
    + """</td>
    <td style="text-align: center"><input type="text" class="sheet-number_3 minor" name="attr_%(Tech)s_Puissant" value="0"/></td>
</tr>""",
    TECHNIQUES,
    str_key="tech",
)

# Technique options
GLOBALS["technique_score_options"] = repeat_template(
    """<option value="(@{%(Tech)s_Score} + @{%(Tech)s_Puissant}) [@{%(tech)s_i18n}]" data-i18n="%(tech)s" >%(Tech)s</option>""",
    TECHNIQUES,
    str_key="tech",
)
GLOBALS["technique_score_options_unlabeled"] = repeat_template(
    """<option value="@{%(Tech)s_Score} + @{%(Tech)s_Puissant}" data-i18n="%(tech)s" >%(Tech)s</option>""",
    TECHNIQUES,
    str_key="tech",
)
GLOBALS["technique_name_options"] = repeat_template(
    """<option value="%(Tech)s" data-i18n="%(tech)s" >%(Tech)s</option>""",
    TECHNIQUES,
    str_key="tech",
)

GLOBALS["technique_enumerated_options"] = repeat_template(
    """<option value="%(index)s" data-i18n="%(tech)s" >%(Tech)s</option>""",
    enumerate_helper(TECHNIQUES, [str.capitalize], start=1),
    tuple_keys=("index", "tech", "Tech"),
)

# Form definitions
form_template = (
    """<tr>
    <td><input type="text" class="sheet-number_3" name="attr_%(Form)s_Score" value="0"/></td>
    <td data-i18n="%(form)s" >%(Form)s</td>
    <td>"""
    + xp("%(Form)s")
    + """</td>
    <td style="text-align: center"><input type="text" class="sheet-number_3 minor" name="attr_%(Form)s_Puissant" value="0"/></td>
</tr>"""
)
GLOBALS["form_definitions_1"] = repeat_template(
    form_template, FORMS[:5], str_key="form"
)
GLOBALS["form_definitions_2"] = repeat_template(
    form_template, FORMS[5:], str_key="form"
)

# Form options
GLOBALS["form_score_options"] = repeat_template(
    """<option value="(@{%(Form)s_Score} + @{%(Form)s_Puissant}) [@{%(form)s_i18n}]" data-i18n="%(form)s" >%(Form)s</option>""",
    FORMS,
    str_key="form",
)
GLOBALS["form_score_options_unlabeled"] = repeat_template(
    """<option value="@{%(Form)s_Score} + @{%(Form)s_Puissant}" data-i18n="%(form)s" >%(Form)s</option>""",
    FORMS,
    str_key="form",
)
GLOBALS["form_name_options"] = repeat_template(
    """<option value="%(Form)s" data-i18n="%(form)s" >%(Form)s</option>""",
    FORMS,
    str_key="form",
)

GLOBALS["form_enumerated_options"] = repeat_template(
    """<option value="%(index)s" data-i18n="%(form)s" >%(Form)s</option>""",
    enumerate_helper(FORMS, [str.capitalize], start=1),
    tuple_keys=("index", "form", "Form"),
)


# Casting rolls
## Magic tab
spontaneous_roll_template = "&{template:arcane} {{label0=^{spontaneous} ^{casting}}} {{result0=%(roll)s}} {{label1=^{aura}}} {{result1=@{aura}}} {{label2=^{weakness-m}}} {{result2=[[ @{wound_total}[@{wounds_i18n}] + [[floor(@{fatigue})]][@{fatigue_i18n}] ]]}} {{label3=^{circumstances-m}}} {{result3=?{@{modifiers_i18n}|0}}} {{botch-button=[@{botch_i18n}!](~@{character_name}|botch)}} {{crit-button=[@{critical_i18n}!](~@{character_name}|critical-spontaneous)}}"
spontaneous_roll = "[[(%(die)s + @{Spontaneous1_Technique} + @{Spontaneous1_Form} + ([[@{Spontaneous1_Focus}]]) [@{focus_i18n}] + (@{gestures}) + (@{words}) + (@{Stamina_Score}) [@{stamina_i18n}] + (@{aura}) [@{aura_i18n}] + ([[floor(@{Fatigue})]]) [@{fatigue_i18n}] + (@{wound_total}) [@{wounds_i18n}] + (?{@{modifiers_i18n}|0}) [@{modifiers_i18n}] )/2 ]]"
GLOBALS["spontaneous_roll_simple"] = spontaneous_roll_template % {
    "roll": spontaneous_roll % {"die": "@{simple-die}"}
}
GLOBALS["spontaneous_roll_stress"] = (
    spontaneous_roll_template % {"roll": spontaneous_roll % {"die": "@{stress-die}"}}
) + " {{stress=1}}"

ceremonial_roll_template = "&{template:arcane} {{label0=^{ceremonial} ^{casting}}} {{result0= %(roll)s }} {{label1=^{aura}}} {{result1=@{aura}}} {{label2=^{weakness-m}}} {{result2=[[@{wound_total}[@{wounds_i18n}] + [[floor(@{fatigue})]][@{fatigue_i18n}] ]]}} {{label3=^{circumstances-m}}} {{result3=?{@{modifiers_i18n}|0}}} {{botch-button=[@{botch_i18n}!](~@{character_name}|botch)}} {{crit-button=[@{critical_i18n}!](~@{character_name}|critical-spontaneous)}}"
ceremonial_roll = "[[(%(die)s+ @{Ceremonial_Technique} + @{Ceremonial_Form} + ([[@{Ceremonial_Focus}]]) [@{focus_i18n}] + (@{gestures}) + (@{words}) + (@{Stamina_Score}) [@{stamina_i18n}] + (@{aura}) [@{aura_i18n}] + ([[floor(@{Fatigue})]]) [@{fatigue_i18n}] + (@{wound_total}) [@{wounds_i18n}] + (@{Ceremonial_Artes_Lib}) [@{artes_i18n}] + (@{Ceremonial_Philos}) [@{philos_i18n}] + (?{@{modifiers_i18n}|0}) [@{modifiers_i18n}] )/2  ]]"
GLOBALS["ceremonial_roll_simple"] = ceremonial_roll_template % {
    "roll": ceremonial_roll % {"die": "@{simple-die}"}
}
GLOBALS["ceremonial_roll_stress"] = (
    ceremonial_roll_template % {"roll": ceremonial_roll % {"die": "@{stress-die}"}}
) + " {{stress=1}}"

formulaic_roll_template = "&{template:arcane} {{label0=^{formulaic} ^{casting}}} {{result0= %(roll)s }} {{label1=^{aura}}} {{result1=@{aura}}} {{label2=^{weakness-m}}} {{result2=[[@{wound_total}[@{wounds_i18n}] + [[floor(@{fatigue})]][@{fatigue_i18n}] ]]}} {{label3=^{circumstances-m}}} {{result3=?{@{modifiers_i18n}|0}}} {{botch-button=[@{botch_i18n}!](~@{character_name}|botch)}} {{crit-button=[@{critical_i18n}!](~@{character_name}|critical)}}"
formulaic_roll = "[[%(die)s + @{Formulaic_Technique} + @{Formulaic_Form} + ([[@{Formulaic_Focus}]]) [@{focus_i18n}] + (@{gestures}) + (@{words}) + (@{Stamina_Score}) [@{stamina_i18n}] + (@{aura}) [@{aura_i18n}] + ([[floor(@{Fatigue})]]) [@{fatigue_i18n}] + (@{wound_total}) [@{wounds_i18n}] + (?{@{modifiers_i18n}|0}) [@{modifiers_i18n}] ]]"
GLOBALS["formulaic_roll_simple"] = formulaic_roll_template % {
    "roll": formulaic_roll % {"die": "@{simple-die}"}
}
GLOBALS["formulaic_roll_stress"] = (
    formulaic_roll_template % {"roll": formulaic_roll % {"die": "@{stress-die}"}}
) + " {{stress=1}}"

ritual_roll_template = "&{template:arcane} {{label0=^{ritual} ^{casting}}} {{result0= %(roll)s }} {{label1=^{aura}}} {{result1=@{aura}}} {{label2=^{weakness-m}}} {{result2=[[ @{wound_total}[@{wounds_i18n}] + [[floor(@{fatigue})]][@{fatigue_i18n}] ]]}} {{label3=^{circumstances-m}}} {{result3=?{@{modifiers_i18n}|0}}} {{botch-button=[@{botch_i18n}!](~@{character_name}|botch)}} {{crit-button=[@{critical_i18n}!](~@{character_name}|critical)}}"
ritual_roll = "[[%(die)s + @{Ritual_Technique} + @{Ritual_Form} + ([[@{Ritual_Focus}]]) [@{focus_i18n}] + (@{Stamina_Score}) [@{stamina_i18n}] + (@{aura}) [@{aura_i18n}] + (@{Ritual_Artes_Lib}) [@{artes_i18n}] + (@{Ritual_Philos}) [@{philos_i18n}] + (@{wound_total}) [@{wounds_i18n}] + ([[floor(@{fatigue})]]) [@{fatigue_i18n}] + (?{@{modifiers_i18n}|0}) [@{modifiers_i18n}] ]]"
GLOBALS["ritual_roll_simple"] = ritual_roll_template % {
    "roll": ritual_roll % {"die": "@{simple-die}"}
}
GLOBALS["ritual_roll_stress"] = (
    ritual_roll_template % {"roll": ritual_roll % {"die": "@{stress-die}"}}
) + " {{stress=1}}"

## Spells
# Deferred attribute access to get the spell's technique value
spell_tech_value = "(@{sys_at}@{character_name}@{sys_pipe}@{spell_tech_name}_Score@{sys_rbk} + @{sys_at}@{character_name}@{sys_pipe}@{spell_tech_name}_Puissant@{sys_rbk}) [@{sys_at}@{character_name}@{sys_pipe}@{spell_tech_name}_i18n@{sys_rbk}]"
spell_form_value = "(@{sys_at}@{character_name}@{sys_pipe}@{spell_form_name}_Score@{sys_rbk} + @{sys_at}@{character_name}@{sys_pipe}@{spell_form_name}_Puissant@{sys_rbk}) [@{sys_at}@{character_name}@{sys_pipe}@{spell_form_name}_i18n@{sys_rbk}]"
# Export the deferred attribute access for use in the HTML since the focus depends on them
GLOBALS["spell_tech_value"] = spell_tech_value
GLOBALS["spell_form_value"] = spell_form_value
spell_roll_template = "&{template:spell} {{spell= @{spell_name}}} {{character= @{character_name} }} {{sigil=@{sigil}}} {{roll= %(roll)s }} {{range= @{spell_range} }} {{duration= @{spell_duration} }} {{target= @{spell_target} }} {{effect= @{spell_note} }} {{mastery= @{spell_note-2} }} {{Technique= @{sys_at}@{character_name}@{sys_pipe}@{spell_tech_name}_i18n@{sys_rbk} }} {{Form= @{sys_at}@{character_name}@{sys_pipe}@{spell_form_name}_i18n@{sys_rbk} }} {{Level= @{spell_level} }} {{botch-button=[@{botch_i18n}!](~@{character_name}|botch)}} {{crit-button=[@{critical_i18n}!](~@{character_name}|critical)}}"
spell_roll = (
    "[[%(die)s + (@{Stamina_Score}) [@{stamina_i18n}] + "
    + spell_tech_value
    + " + "
    + spell_form_value
    + "+ ([[@{spell_Focus}]]) [@{focus_i18n}] + (@{spell_bonus}) [@{bonus_i18n}] + (@{gestures}) + (@{words}) + (@{aura}) [@{aura_i18n}] + ([[floor(@{Fatigue})]]) [@{fatigue_i18n}] + (@{wound_total}) [@{wounds_i18n}] + (?{@{modifiers_i18n}|0}) [@{modifiers_i18n}] ]]"
)
GLOBALS["spell_roll_simple"] = spell_roll_template % {
    "roll": spell_roll % {"die": "@{simple-die}"}
}
GLOBALS["spell_roll_stress"] = (
    spell_roll_template % {"roll": spell_roll % {"die": "@{stress-die}"}}
) + " {{stress=1}}"


# Botch formula
GLOBALS["botch_separated"] = (
    "?{@{botch_num_i18n} | "
    + "|".join(
        f"{n} {'Die' if n==1 else 'Dice'}," + " ".join(["[[1d10cf10cs0]]"] * n)
        for n in range(1, 13)
    )
    + "}"
)

# Fatigue
add_fatigue_lvl_num = 10
GLOBALS["fatigue_levels_options"] = repeat_template(
    """<option value="%%">%%</option>""", range(0, add_fatigue_lvl_num + 1)
)
GLOBALS["additional_fatigue_levels"] = repeat_template(
    """<tr class="sheet-addfatigue-%(num)s">
    <td><input type="radio" class="sheet-radio_1" name="attr_Fatigue" value="%(value)s"><span></span></td>
    <td style="text-align:center;">0</td>
    <td>2 min.</td>
    <td data-i18n="winded" >Winded</td>
</tr>""",
    [(str(i), str(i / 1000)) for i in range(1, add_fatigue_lvl_num + 1)],
    tuple_keys=("num", "value"),
)
GLOBALS["fatigue_level_css"] = "\n".join(
    (
        # IF the fatigue selector is not on a value for which the level is visible
        "".join(
            ':not(.sheet-fatigue-proxy[value="%s"])' % val
            for val in range(lvl, add_fatigue_lvl_num + 1)
        )
        # THEN hide the level
        + (" + table tr.sheet-addfatigue-%s" % lvl)
        + " {\n    display: none;\n}"
    )
    for lvl in range(1, add_fatigue_lvl_num + 1)
)


# Documentation
with open(Path(__file__).parents[1] / "documentation.md") as f:
    html = markdown.markdown("".join(f))
html = soup(html, "html.parser")
for i in range(1, 10):
    for tag in html.find_all(f"h{i}"):
        tag.attrs["class"] = tag.get("class", "") + " sheet-heading_label"
GLOBALS["documentation"] = html.prettify()
