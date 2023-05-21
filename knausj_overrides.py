from talon import Context, Module, app

from ..knausj_talon.core.keys import keys
from ..knausj_talon.core.text import text_and_dictation

mod = Module()

ctx = Context()

# Match more specific so talon loads this second, as an override.
ctx.matches = """
language: en
"""

# Alphabet replacement
mod.list("letter", desc="The spoken phonetic alphabet")

alphabet_list = keys.setup_default_alphabet()
alphabet_list.pop("bat")
alphabet_list["bite"] = "b"  # Could be Bloom
alphabet_list.pop("cap")
alphabet_list[
    "cast"
] = "c"  # Could be Charm, Crux, Cleave, Card, Carve, Cask, Cast, Coax

ctx.lists["user.letter"] = alphabet_list


@mod.capture(rule="{user.letter}")
def letter(m) -> str:
    "One letter key"
    return m.letter


# Symbols and punctuation
mod.list("addl_punctuation", "Additional punctuation (typing and cmd mode)")
addl_punctuation = {
    "splat": "*",
    "huh": "?",
    "squiggly": "~",
    "open paren": "(",
    "close paren": ")",
    "open bracket": "[",
    "close bracket": "]",
    "open brack": "[",
    "close brack": "]",
    "open brace": "{",
    "close brace": "}",
}
ctx.lists["user.addl_punctuation"] = addl_punctuation

mod.list("addl_symbol_key", "Additional symbols (cmd mode)")
addl_symbols = {
    "semi": ";",
    "ex": ":",  # Vim Ex mode; one syllable instead of "colon"
}
addl_symbols.update(addl_punctuation)
ctx.lists["user.addl_symbol_key"] = addl_symbols


@mod.capture(rule="{user.symbol_key} | {user.addl_symbol_key}")
def symbol_key(m) -> str:
    "One symbol key"
    theirs = getattr(m, "symbol_key", None)
    if theirs and theirs == "£":
        return "#"
    return str(m)


@mod.capture(
    rule="({user.vocabulary} | {user.punctuation} | {user.addl_punctuation} | {user.prose_snippets} | <phrase> | <user.prose_number> | <user.prose_modifier>)+"
)
def prose(m) -> str:
    return text_and_dictation.prose(m)


@mod.capture(
    rule="({user.vocabulary} | {user.punctuation} | {user.addl_punctuation} | {user.prose_snippets} | <phrase> | <user.prose_number>)+"
)
def raw_prose(m) -> str:
    return text_and_dictation.raw_prose(m)


# Modifier Keys

mod.list("addl_modifier_key", "Additional modifier keys")
if app.platform == "mac":
    ctx.lists["user.addl_modifier_key"] = {"rose": "cmd"}


@mod.capture(rule="({user.modifier_key} | {user.addl_modifier_key})+")
def modifiers(m) -> str:
    "One or more modifier keys"
    mods = [
        *getattr(m, "addl_modifier_key_list", []),
        *getattr(m, "modifier_key_list", []),
    ]
    print("MODS", mods)
    return "-".join(mods)


# @mod.capture(
#     rule="({user.modifier_key} | {user.addl_modifier_key})* <user.unmodified_key>"
# )
# def key(m) -> str:
#     "A single key with optional modifiers"
#     mods = [
#         *getattr(m, "addl_modifier_key_list", []),
#         *getattr(m, "modifier_key_list", []),
#     ]
#     return "-".join(mods + [m.unmodified_key])


# Special keys

mod.list("addl_special_key", "Additional special keys")
ctx.lists["user.addl_special_key"] = {"junk": "backspace", "esc": "escape"}


@mod.capture(rule="{user.special_key} | {user.addl_special_key}")
def special_key(m) -> str:
    return str(m)
