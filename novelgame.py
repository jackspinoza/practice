import sys

def wait():
    input()

def run_block(block):
    i = 0
    while i < len(block):
        entry = block[i]

        # Handle commands (lists)
        if isinstance(entry, list):
            command = entry[0]

            if command == "TITLE":
                print(f"\n=== {entry[1]} ===\n")
                wait()

            elif command == "narrate":
                print(entry[1])
                wait()

            elif command == "dialogue":
                speaker = entry[1]
                text = entry[2]
                print(f"  {speaker}\n {text}")
                wait()

            elif command == "SHOW":
                print(f"[SHOW CHARACTER: {entry[1]}]")

            elif command == "SPRITE":
                print(f"[{entry[1].upper()} sprite -> {entry[2]}]\n")

            elif command == "CHOICE":
                choices = entry[1]
                print("\nChoose an option:")
                for idx, choice in enumerate(choices, 1):
                    print(f"{idx}. {choice}")

                while True:
                    try:
                        selection = int(input("> "))
                        if 1 <= selection <= len(choices):
                            chosen = choices[selection - 1]
                            return chosen  # return choice key
                    except:
                        pass
                    print("Invalid choice. Try again.")

        # Handle branching dictionary
        elif isinstance(entry, dict):
            # We should already have a choice result
            print("Error: Choice not made before branch.")
            sys.exit(1)

        i += 1

    return None


def run_game(game):
    i = 0
    last_choice = None

    while i < len(game):
        entry = game[i]

        # If we hit a choice, run it and jump to branch
        if isinstance(entry, list) and entry[0] == "CHOICE":
            last_choice = run_block([entry])

            # Next item must be the branch dict
            branch_dict = game[i + 1]

            if last_choice in branch_dict:
                run_block(branch_dict[last_choice])
            else:
                print(f"No branch found for choice: {last_choice}")

            i += 2  # skip the dict
            continue

        # Otherwise run normally
        run_block([entry])
        i += 1


# --- YOUR GAME DATA ---
game = [
  ['TITLE','March'],
  ['narrate',"It's a fairly sunny day in the park."],
  ['dialogue','You','Hmm... what to do...'],
  ['narrate','Suddenly, a guy approaches.'],
  ['SHOW','stranger'], ['SPRITE','stranger','happy'],
  ['dialogue','You','Oh, hello.'],
  ['dialogue','Stranger','Hello, how`s your day?'],
  ["CHOICE",["Good","Meh","Not too good."]],
  {
    "Good":[
      ['dialogue','Stranger','Glad to hear that!'],
    ],
    "Meh":[
      ["SPRITE","stranger","concerned"],
      ['dialogue','Stranger','Ah, is there anything that can make it better?'],
    ],
    "Not too good":[
      ["SPRITE","stranger","concerned"],
      ['dialogue','Stranger','Ouch, what happened?'],
    ]
  }
]


# --- RUN ---
if __name__ == "__main__":
    run_game(game)
