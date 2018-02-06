#!/usr/bin/python

import re
import panflute as pf
from itertools import groupby

label_re = re.compile(r'\{#ex:(\w+)\}')

def smallcapify(s):
    """
    Convert words in a string that are in all caps to use small caps, via the
    LaTeX \\textsc{} command. Used to auto-convert glossing abbreviations given
    in all caps (like PERF for perfective) to small caps in glosses. Words that
    are merely capitalized (like Mary) will be left alone.
    """

    def repl(match):
        word = match.group()
        if all(64 < ord(c) < 91 for c in word):
            return "\\textsc{" + word.lower() + "}"
        else:
            return word

    return re.sub(r"[\w']+", repl, s)


def output_gb4e(lst):
    """
    Convert an example list into a series of gb4e-formatted interlinear
    glosses.

    Because example list references are replaced at parsing by Pandoc, the
    normal syntax of (@foo) cannot be used for labels; instead, a label syntax
    similar to that used for headers (and tables and figures with
    pandoc-crossref) is used, namely a {#ex:foo} inserted after the
    translation, which will be stripped and replaced with a LaTeX label on the
    relevant example.
    """

    latex = "\\begin{exe}\n"
    for li in lst.content:
        is_break = lambda x: isinstance(x, pf.SoftBreak)
        content = list(li.content[0].content)
        lines = [pf.Para(*list(g)) for k, g in groupby(content, is_break) if not k]

        if len(lines) == 3:
            latex += "\\ex"

            orig = pf.stringify(lines[0], newlines = False)
            gloss = smallcapify(pf.stringify(lines[1], newlines = False))

            trans = pf.stringify(lines[2], newlines = False)
            label_match = label_re.search(trans)
            if label_match:
                label = label_match.group(1)
                latex += "\\label{ex:" + label + "}\n"

                trans = trans[:label_match.start() - 1]
            else:
                latex += "\n"

            latex += "\\gll " + orig + "\\\\\n"
            latex += gloss + "\\\\\n"
            latex += "\\trans `" + trans + "'\n\n"

    latex += "\\end{exe}"
    return pf.RawBlock(latex, format='latex')


def output_leipzigjs(lst):
    """
    Convert an eample list into a series of div's suitable for use with
    leipzigjs.
    """

    pass # TODO


formats = {
        'latex': output_gb4e,
        'html': output_leipzigjs
        }


def gloss(elem, doc):
    if isinstance(elem, pf.OrderedList):
        if elem.style == 'Example':
            if doc.format in formats:
                return formats[doc.format](elem)
            else:
                return None

def gloss_refs(elem, doc):
    if isinstance(elem, pf.Cite):
        text = elem.content[0].text
        if text[:4] == '@ex:':
            if doc.format == 'latex':
                return pf.RawInline("(\\ref{ex:" + text[4:] + "})",
                        format = 'latex')
            elif doc.format == 'html':
                # TODO
                pass

def main(doc = None):
    return pf.run_filters([gloss, gloss_refs], doc = doc)

if __name__ == '__main__':
    main()