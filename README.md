# Syneto Python Test
### A CLI for Google Translate

Google Translate is a fabulous tool, but we are hardcore hackers and resent the browser. As such, we’d like to use the command line for doing string translation. At the same time, we are polyglots and know multiple languages (RO, IT, EN, DE). What we want is a CLI tool that can translate between Romanian, Italian, German and English. The tool will read input data from a file and output the translation to the console. The output language is specified as a flag on the command line.

### CLI signature
```commandline
(localhost) $ gtranslate --help
gtanslate 1.0: command line utility for translating text
Usage: gtranslate -f <filename> -l <lang>
Parameters:
    -f <filename>: path to input filename to be translated
    -l <lang>: output language, can be one of "en", "it" or "de"
(localhost) $ 
```
**Input:** The input file has one or more lines to be translated, separated by newline. Each line can be in a different language, to be detected automatically by the script.

**Output:** The program will read the contents of <filename>, translate all the sentences and print them to back to the console, using <lang> as output language.

**Sample usage:**
```commandline
(localhost) $ QUERIES_PER_SEC=10 gtd
Translation daemon started, throttling at 10 queries/second.
(localhost) $ cat > input << EOF
> Buna dimineata
> Buona sera
> Gutten tag
> Arrivederci
> EOF
(localhost) $ gtranslate -f input -l en
Translating, please wait…
Good morning
Good evening
Good day
Goodbye
(localhost) $
```
