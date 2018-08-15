Fork of https://github.com/daemanos/pangloss

Adds support for linguex examples + makes it possible to have examples without glosses or translation


# pangloss

Provides support for interlinear glosses with Markdown example lists.

## Example

The following code snippet demonstrates the most important features of
pangloss:

```
As you can see in the following examples, pangloss is really easy to use:

(@) Jorge  llama             a  Maria.
    George calls-3s.PRES.IND to Maria
    'George calls Maria.'
(@) Aussi, vous pouvez          avoir    de multiples   exemples.
    also   you  can-2p.PRES.IND have.INF of multiple-PL example-PL
    'You can also have multiple examples.' {#ex:french}

You can even refer to examples, as in @ex:french.
```

Each example consists of three lines: an original, a word-by-word analysis, and
an overall translation. Placing `{#ex:...}` after the translation line
introduces a new label, which can then be referred to with the `@ex:...`
syntax as in [pandoc-crossref](https://github.com/lierdakil/pandoc-crossref).

In this modified version, you can have examples in the following format, too:

```
(@) Вчера    совет     Евразийского   банка      развития           (ЕАБР)   утвердил   
yesterday   council   Eurasian-GEN   bank-GEN   developmennt-GEN   abbr     confirm-PRET  {#ex:eabr}
```

Or even without a gloss:

```
(@) Maanantai oli mukava päivä. {#ex:eisubj}
```



## Installation

Install with:

```
pip install git+https://github.com/hrmJ/pangloss_linguex
```

## Usage


An example yaml block of your Rmd or md file:

```
latexBackend: linguex
exampleRefFormat: '{}'
output:
  pdf_document2: 
    latex_engine: xelatex
    pandoc_args:
      - --filter
      - pangloss
```

