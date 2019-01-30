# shitty-regex
ultra-basic regex matching engine written in python

This is an experiment in writing a regex matching engine with no knowledge of how real regex matching engines work. I took an automata and formal languages class last year and I wanted to see whether the theory I learned in that class was enough to write a whole regex engine. It acheives its goal by turning a regex into a representative NFA and using that to accept or reject strings. If I were to make it faster, I would probably write an NFA-to-DFA function, and then a DFA-reduction function. But it's more of a proof of concept than actual usable tool, so I probably won't do that.

If for some weird reason you want to use this, for now it only accepts lowercase letters a-z, union (|), kleene star (*) and parentheses. If I ever work on this more, I'll add more symbols probably. Just run it, it'll prompt you for an input regex and then let you input strings to test until you input 'X'. Right now it also prints the AST it makes from your input regex, which is neat if you're into that sort of thing. It also has no error protection, so invalid regexes or inputs might throw errors and will give weird results.
