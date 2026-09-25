import curses
import time
import random


# Sentences the player can type
SENTENCES = [
    "The future belongs to people who are willing to build it.",
    "Small progress every day can lead to something incredible.",
    "Learning to code is easier when you build real projects.",
    "Artificial intelligence will change the way we solve problems.",
    "The best way to learn programming is to actually write code.",
    "Every great project starts with a simple idea and a first step.",
]


def typing_test(stdscr):
    # Hide the blinking cursor
    curses.curs_set(0)

    # Enable colors
    curses.start_color()

    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    # Pick a random sentence
    sentence = random.choice(SENTENCES)

    typed = ""

    start_time = None
    finished = False

    while not finished:

        # Clear the screen
        stdscr.clear()

        # -------------------------
        # TITLE
        # -------------------------

        title = "⚡ PYTHON TYPING LAB ⚡"

        stdscr.addstr(
            1,
            max(0, (curses.COLS - len(title)) // 2),
            title,
            curses.color_pair(3) | curses.A_BOLD
        )

        stdscr.addstr(
            3,
            2,
            "Type the sentence below. Don't worry about mistakes — just keep going."
        )

        # -------------------------
        # TIMER
        # -------------------------

        if start_time is None:
            elapsed = 0
        else:
            elapsed = time.time() - start_time

        minutes = elapsed / 60

        if minutes > 0:
            words = len(typed.split())
            wpm = int(words / minutes)
        else:
            wpm = 0

        # -------------------------
        # STATS
        # -------------------------

        stdscr.addstr(
            5,
            2,
            f"TIME: {elapsed:05.1f}s    WPM: {wpm}"
        )

        # -------------------------
        # SENTENCE
        # -------------------------

        stdscr.addstr(8, 2, "TARGET:")

        for i, character in enumerate(sentence):

            if i >= len(typed):
                # Character has not been typed yet
                stdscr.addstr(
                    9,
                    2 + i,
                    character,
                    curses.A_DIM
                )

            elif typed[i] == character:
                # Correct character
                stdscr.addstr(
                    9,
                    2 + i,
                    character,
                    curses.color_pair(1)
                )

            else:
                # Wrong character
                stdscr.addstr(
                    9,
                    2 + i,
                    character,
                    curses.color_pair(2)
                )

        # -------------------------
        # TYPED TEXT
        # -------------------------

        stdscr.addstr(12, 2, "YOU:")

        stdscr.addstr(
            13,
            2,
            typed
        )

        # -------------------------
        # PROGRESS
        # -------------------------

        progress = len(typed)
        total = len(sentence)

        percentage = int((progress / total) * 100)

        stdscr.addstr(
            15,
            2,
            f"PROGRESS: {percentage}%"
        )

        # -------------------------
        # INSTRUCTIONS
        # -------------------------

        stdscr.addstr(
            curses.LINES - 2,
            2,
            "BACKSPACE = delete    ESC = quit",
            curses.color_pair(4)
        )

        stdscr.refresh()

        # Don't wait forever for input
        stdscr.timeout(100)

        key = stdscr.getch()

        # -------------------------
        # START TIMER
        # -------------------------

        if key != -1 and start_time is None:
            start_time = time.time()

        # -------------------------
        # ESCAPE
        # -------------------------

        if key == 27:
            break

        # -------------------------
        # BACKSPACE
        # -------------------------

        elif key in (curses.KEY_BACKSPACE, 127, 8):

            if typed:
                typed = typed[:-1]

        # -------------------------
        # NORMAL CHARACTER
        # -------------------------

        elif key != -1 and 32 <= key <= 126:

            if len(typed) < len(sentence):
                typed += chr(key)

        # -------------------------
        # CHECK COMPLETION
        # -------------------------

        if len(typed) == len(sentence):

            finished = True

    # -------------------------
    # RESULTS
    # -------------------------

    stdscr.clear()

    final_time = time.time() - start_time if start_time else 0

    correct = 0

    for i in range(min(len(typed), len(sentence))):
        if typed[i] == sentence[i]:
            correct += 1

    if len(typed) > 0:
        accuracy = (correct / len(typed)) * 100
    else:
        accuracy = 0

    words = len(sentence.split())

    if final_time > 0:
        final_wpm = int(words / (final_time / 60))
    else:
        final_wpm = 0

    # -------------------------
    # RESULT SCREEN
    # -------------------------

    stdscr.addstr(
        3,
        2,
        "🏁 TEST COMPLETE!",
        curses.color_pair(3) | curses.A_BOLD
    )

    stdscr.addstr(
        6,
        2,
        f"Time:     {final_time:.2f} seconds"
    )

    stdscr.addstr(
        7,
        2,
        f"WPM:      {final_wpm}"
    )

    stdscr.addstr(
        8,
        2,
        f"Accuracy: {accuracy:.1f}%"
    )

    stdscr.addstr(
        10,
        2,
        "Press any key to exit..."
    )

    stdscr.refresh()

    stdscr.getch()


# Run the program
curses.wrapper(typing_test)