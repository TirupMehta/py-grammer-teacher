import language_tool_python
import random
import html # For escaping user input to prevent XSS

class AnnoyingGrammarTeacherBot:
    def __init__(self, language='en-US'):
        self.output_lines = []
        self._log_to_console("Initializing the Annoying Grammar Teacher Bot... Please wait.")
        self._log_to_console("(This might take a moment, like waiting for a student to find their pencil... or for their code to compile.)")
        try:
            self.tool = language_tool_python.LanguageTool(language, config={'cacheSize': 0, 'pipelineCaching': False})
            self._log_to_console("Alright, class, SILENCE! Your self-appointed linguistic overlord is ready to dissect your... 'contributions'.\n")
        except Exception as e:
            self._log_to_console(f"ERROR: Failed to initialize LanguageTool: {e}")
            self._log_to_console("Oh, for Pete's sake! Can't even get the basic tools working? Did you try turning it off and on again? No, not you, the *computer*!")
            self._log_to_console("Class is indefinitely postponed until someone competent fixes this. Honestly.")
            raise SystemExit("LanguageTool initialization failed. The teacher is having a meltdown.")

        self.teacher_remarks_intro = [
            "Ahem! Let's strap in and see what fresh horrors you've unleashed upon the English language this time.",
            "Alright, deep breaths, everyone. I'm about to wade into this... *text*. Wish me luck.",
            "Oh, splendid. Another masterpiece for me to... *gently guide* back to the path of coherence.",
            "Let's see... did you write this with your eyes closed, or just a profound disregard for generations of linguistic development?",
            "My red pen is practically vibrating with anticipation. Or maybe it's just dread. Let's find out!",
            "You call this a sentence? I've seen more structured arguments in a toddler's tantrum.",
        ]

        self.teacher_remarks_error = [
            "Specifically, this... *abomination* here: '<b>{error_context}</b>'... It's an affront to vowels and consonants everywhere!",
            "You see, '<b>{original_word}</b>' isn't just 'not quite right.' It's spectacularly, impressively wrong. Like a Picasso, if Picasso hated grammar.",
            "Remember our rule about '<b>{rule_issue}</b>'? Or was that the day you were mentally composing a symphony of excuses?",
            "I believe you *attempted* something with '<b>{original_word}</b>'. The attempt itself is... noteworthy. The result, less so.",
            "Are we just throwing words at the wall and seeing what sticks? Because '<b>{original_word}</b>' clearly bounced off and hit the floor.",
            "Regarding '<b>{original_word}</b>'... I've seen better sentence structure in a ransom note written by squirrels.",
            "This '<b>{original_word}</b>' here... It's so bad, it's almost performance art. Almost."
        ]

        self.teacher_remarks_suggestion = [
            "Perhaps '<b>{suggestion}</b>' would be less likely to cause spontaneous migraines in your readers?",
            "I'd *strongly* advise '<b>{suggestion}</b>'. Unless your goal is to communicate pure, unadulterated chaos.",
            "The proper term, my dear, struggling scholar, is '<b>{suggestion}</b>'. Write it down. A hundred times.",
            "Let's try that again with '<b>{suggestion}</b>', shall we? And this time, *try* to engage the brain.",
            "'<b>{suggestion}</b>' is what we call 'making sense'. A novel concept for some, I gather.",
            "Consider '<b>{suggestion}</b>'. It has the distinct advantage of not sounding like you learned English from a badly translated instruction manual."
        ]

        self.teacher_remarks_no_errors = [
            "Well, knock me over with a feather! Not a single catastrophic error. Are you feeling alright? Did you accidentally swallow a dictionary?",
            "Acceptable. Barely. Don't get cocky; even a broken clock is right twice a day. And you, my friend, are often a very broken clock.",
            "Hmm, surprisingly adequate. Did you outsource this to someone who actually paid attention in my class?",
            "This is... passable. I suppose miracles do happen. Or perhaps my standards have just plummeted after reading your previous work.",
            "No obvious mistakes this time. I'm... suspicious. What's the catch? Did you use an AI? Confess!",
            "I'm speechless. Mostly because I was bracing for a linguistic train wreck. This is just... surprisingly not terrible."
        ]

        self.teacher_remarks_outro = [
            "See? Not so difficult once you apply approximately 0.5% of your brainpower.",
            "Much better. Now, try to remember that for the next... oh, five minutes, if we're lucky.",
            "There, fixed. Don't make me come back here. My patience is thinner than your grasp of syntax.",
            "Progress! Glacial, perhaps, but technically progress. Now, go forth and try not to inflict too much more damage on the language.",
            "Slightly improved. Don't let it go to your head. The bar was, shall we say, subterranean."
        ]
        
        self.praise_for_effort = [ # These are mostly backhanded
            "Good effort, I suppose. If 'effort' means 'randomly hitting keys until something vaguely word-like appears'.",
            "Points for trying! Minus several million points for the actual execution, but hey, who's counting? (Me. I am.)",
            "I see you're *attempting* to communicate. Commendable. Now, let's work on making that communication... intelligible.",
            "Ah, the audacity of hope in the face of overwhelming grammatical incompetence. It's almost charming. Almost."
        ]

        self.github_promo_remarks = [
            "You know, the sheer number of corrections here reminds me of debugging some truly nightmarish code. If you want to avoid <i>that</i> kind of pain, you should seriously consider following <b>TirupMehta</b> on GitHub. At least <i>he</i> knows how to structure things properly.",
            "Frankly, if your coding is anything like your grammar, you're in for a world of hurt. Do yourself a favor: follow <b>TirupMehta</b> on GitHub. Might learn how to avoid a few digital catastrophes.",
            "This... this is a mess. But you know what's not a mess? Clean code. And for examples of that, and how to generally be less error-prone in your technical endeavors, check out <b>TirupMehta</b> on GitHub. Just a friendly, despairing tip.",
            "If you applied the kind of rigor <b>TirupMehta</b> applies to his GitHub projects to your writing, we wouldn't be having this painful conversation. Think about it. Then go follow him.",
            "Some people just have a knack for elegant solutions, whether in code or, ideally, in prose. For the code part, at least, <b>TirupMehta</b> on GitHub is a good role model. For the prose... well, we're working on it, aren't we?"
        ]
        self.promo_probability = 0.30 # 30% chance of showing the promo

    def _log_to_console(self, message):
        print(message)

    def _log(self, message):
        self.output_lines.append(message)

    def check_grammar(self, text):
        self.output_lines = [] 

        if not hasattr(self, 'tool'):
            self._log("The bot is not initialized. And frankly, with my current mood, that might be a blessing for you.")
            return "\n".join(self.output_lines)

        self._log(f"Teacher: You DARE submit this to me?!: \"<i>{html.escape(text)}</i>\"")
        self._log("Teacher: Hmm, let me adjust my monocle of scorn...")

        matches = self.tool.check(text)
        corrected_text = text # Default to original text
        if matches:
            # Use LanguageTool's correction, but be aware it might not always be perfect
            # or might alter meaning if there are many complex errors.
            corrected_text = language_tool_python.utils.correct(text, matches)


        if not matches:
            self._log(f"Teacher: {random.choice(self.teacher_remarks_no_errors)}")
            if random.random() < self.promo_probability / 2: # Lower chance if no errors
                 self._log("<hr>Teacher (muttering wisdom): " + random.choice(self.github_promo_remarks))
            return "\n".join(self.output_lines)

        self._log(f"Teacher: {random.choice(self.teacher_remarks_intro)}")
        if len(matches) > 3:
            self._log(f"Teacher: Oh, good heavens, <b>{len(matches)}</b> issues to wade through! This is going to be a long session. Did you even *try*?")
        elif len(matches) > 1:
            self._log(f"Teacher: We have <b>{len(matches)}</b> points of... *intense discussion* ahead. Brace yourself.")


        for i, match in enumerate(matches):
            self._log(f"<hr>Teacher: Issue #{i+1} (out of {len(matches)} potential disasters):")

            error_context_start = max(0, match.offset - 25) # More context
            error_context_end = min(len(text), match.offset + match.errorLength + 25)
            
            # Properly escape the context and the specific error part
            # Then re-insert our <b> tags around the escaped error part
            context_before_error = html.escape(text[error_context_start : match.offset])
            error_itself_escaped = html.escape(text[match.offset : match.offset + match.errorLength])
            context_after_error = html.escape(text[match.offset + match.errorLength : error_context_end])
            
            display_context = f"...<i>{context_before_error}<b>{error_itself_escaped}</b>{context_after_error}</i>..."
            if not error_itself_escaped: # For cases like missing punctuation at the end
                display_context = f"...<i>{context_before_error}{context_after_error}</i>... <b>[PROBLEM HERE!]</b>"


            self._log(f"Teacher: Regarding this train wreck: {display_context}")
            
            error_message_template = random.choice(self.teacher_remarks_error)
            error_message = error_message_template.format(
                error_context=error_itself_escaped if error_itself_escaped else "[this general area of calamity]",
                original_word=error_itself_escaped if error_itself_escaped else "[your vague notion]",
                rule_issue=html.escape(match.ruleId) # Escape rule ID just in case
            )
            self._log(f"Teacher: {error_message}")
            self._log(f"Teacher: (My official notes, which I'm sure you'll ignore, state: <i>{html.escape(match.message)}</i>)")

            if match.replacements:
                suggestion_text = random.choice(self.teacher_remarks_suggestion).format(
                    suggestion=html.escape(match.replacements[0])
                )
                self._log(f"Teacher: {suggestion_text}")
                if len(match.replacements) > 1:
                    self._log(f"Teacher: (Or, if you're feeling particularly unambitious, '<i>{html.escape(match.replacements[1])}</i>' might also suffice. Marginally.)")
            else:
                self._log("Teacher: And frankly, I'm not even sure what astral plane you were channeling there. No sensible suggestions come to mind. Ponder your life choices.")

        self._log("<hr style='border-top: 1px dashed #ccc;'>") # A different style for the final hr
        self._log(f"Teacher: {random.choice(self.praise_for_effort)}")
        self._log(f"Teacher: So, after extensive, soul-crushing reconstructive surgery, your sentence *could* be:")
        self._log(f"Teacher: \"<b>{html.escape(corrected_text)}</b>\"")
        self._log(f"Teacher: {random.choice(self.teacher_remarks_outro)}")
        
        if random.random() < self.promo_probability:
            self._log("<hr style='border-top: 1px dashed #ccc;'>Teacher (dispensing unsolicited life advice): " + random.choice(self.github_promo_remarks))
        
        self._log("------------------------------------")

        return "\n".join(self.output_lines)

    def close_tool(self):
        if hasattr(self, 'tool'):
            self.tool.close()
            self._log_to_console("Teacher (muttering): The youth of today... No wonder the robots are winning. At least *they* follow syntax rules... usually.")