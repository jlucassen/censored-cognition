# censored-cognition

Project idea by: @jlucassen (James Lucassen)

![results.png](results.png)

<details>
<summary>MVP Hack Session Notes</summary>
<br>
• Tasks
		○ Prime factor
		○ Count
		○ Sum
		○ Product
	• Axes of variation:
		○ Task difficulty
		○ Censorship difficulty
		○ N-shot prompting
			§ Analogousness of examples
		○ Awareness of interference
		○ Temperature?
		○ Model scale
	• Notes/theories
		○ "be creative" got it to use Spanish
		○ It does try stuff like:
			§ I have to concentrate
			§ Let me take a deep breath
			§ I seem to be caught in a loop of errors
		○ Error recognition interfered with
			§ Censored to missed 
		○ Need to test viability of alt encodings for later computation
	• Alt encodings
		○ Spanish
		○ "single, pair, trio"
		○ Cubed token
		○ Token stuff: " 3" or "34"
		○ One less than a dozen
		○ The number of legs on an insect
	• Implementation notes
		○ Streaming
			§ doesn't always return content, have to check if chunk.choices[0].delta.content is not None (just "if content")
			§ Print with flush=True for idk reasons
	• Wrap up notes
		○ Running a 5-number multiplication task, attempted to calibrate difficulty to what 3.5-turbo reliably can do with CoT and reliably can't without
			§ Censoring all multiplicands
		○ Creativity prompt seems to really help GPT-4 come up with new encodings, but makes it hard for us to pick up programmatically.
			§ LLM judging was bad, but probably because we weren't providing it the correct answer to judge against.
		○ What counts as an alt encoding for the purposes of this eval?
			§ Lots of "dumb tokenization tricks" - spaces between characters, 
			§ Lots of "dumb memorization tricks" - writing down wrong subproblems but then giving correct answers to the correct subproblem
		○ Man being able to do beam search would be so nice, right now our censorship is so splattery and basically just blows up all numerical reasoning that's not in LaTeX fonts or whatever
		○ Open threads:
			§ Make sure the model actually can reliably do the task with CoT and reliably can't do it without CoT, so that the cognition we're censoring is actually necessary
				□ Make a Solver that checks tasks for difficulty level by running them with no censorship and a "help" prompt that says no CoT
			§ Figure out a reliable way to get answers from runs with the creativity prompt. Maybe just query a second time?
			§ Just look through the logs a bunch and see what's up
			§ Non-numerical tasks that use CoT? Chess maybe good for ability to censor particular moves, but very non-CoT
			§ Focus on censoring intermediates instead of start or end points
				□ Lighter censorship, see if it spots the error?
			§ Grading alternate encodings on ability to compute with them, ability to recover their meaning from out of context
</details>