import re


def damage(spell):
    """
    Function calculating damage
    :param str spell: string with spell
    :rtype: int
    :return: points of damage
    """
    damage = 0
    # Get start of spell.
    start = spell.find('fe')
    # Return 0 if no 'fe' in spell.
    if start == -1:
        return damage
    # Invalid spell if 'fe' shows more than once.
    if spell.find('fe', start + 1) != -1:
        return damage

    # Get all valid spells and remove starting 'fe' and ending 'ai' from them.
    valid_spells = [spell[start + 2:match.start()] for match in
                    re.finditer(re.escape('ai'), spell) if
                    match.start() > start]

    # Possible spell damage combos. This order guarantees biggest damage.
    subspells = [('dai', 5), ('aine', 4), ('jee', 3), ('je', 2),
                 ('ain', 3), ('ai', 2), ('ne', 2)]

    # Calculate damage from all spells and find the best one.
    for valid_spell in valid_spells:
        # Omit start and end, which result in 3 starting damage.
        valid_spell_damage = 3

        # Check subspells in spell, starting from the most damaging ones.
        for i, j in subspells:
            if i in valid_spell:
                valid_spell_damage += j * valid_spell.count(i)
                # Replace subspells with a '!', to avoid creating subspells.
                valid_spell = valid_spell.replace(i, '!')
        # Reduce damage by count of left over letters.
        valid_spell_damage -= sum(x.isalpha() for x in valid_spell)
        # If it's the best spell, set damage to this spell's damage.
        if valid_spell_damage > damage:
            damage = valid_spell_damage

    return damage
