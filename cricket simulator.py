"""
🏏 11-a-side Cricket Match Simulator (5 Overs per Innings) 🏏
--------------------------------------------------------------
Two teams of 11 players play a 5-over match. Every ball's outcome is
typed in by the user. Two batsmen are on the crease at all times,
strike rotates on odd runs and at the end of every over, wickets
bring in the next batsman, and a full scorecard is shown at the end
of each innings. After the result, you can start a brand new match.

Run it in VS Code with:  python cricket_match.py
"""

import sys

OVERS_PER_INNINGS = 5
TOTAL_PLAYERS = 11
VALID_RUN_INPUTS = {"0", "1", "2", "3", "4", "5", "6"}


class Player:
    def __init__(self, name):
        self.name = name
        self.runs = 0
        self.balls = 0
        self.out = False
        self.how_out = "not out"


def divider(char="=", n=54):
    print(char * n)


# ----------------------------------------------------------------------
# SETUP HELPERS
# ----------------------------------------------------------------------

def get_players(team_name):
    divider("-")
    print(f"🧢 Setting up squad for {team_name} ({TOTAL_PLAYERS} players)")
    choice = input(
        "  Type '1' to enter player names yourself, or '2' to auto-generate "
        "(Player 1..Player 11): "
    ).strip()

    if choice == "1":
        names = []
        for i in range(1, TOTAL_PLAYERS + 1):
            name = input(f"    Enter name of Player {i}: ").strip()
            names.append(name if name else f"Player {i}")
    else:
        names = [f"Player {i}" for i in range(1, TOTAL_PLAYERS + 1)]

    return [Player(n) for n in names]


def get_team_setup():
    divider()
    print("🏏  WELCOME TO THE 11-A-SIDE CRICKET MATCH  🏏")
    divider()

    team_a_name = input("Enter Team A name: ").strip() or "Team A"
    team_b_name = input("Enter Team B name: ").strip() or "Team B"

    team_a_players = get_players(team_a_name)
    team_b_players = get_players(team_b_name)

    return team_a_name, team_a_players, team_b_name, team_b_players


def do_toss(team_a, team_b):
    divider("-")
    print("🪙  TOSS TIME  🪙")
    while True:
        winner = input(f"Which team won the toss? ({team_a}/{team_b}): ").strip()
        if winner.lower() == team_a.lower():
            winner = team_a
            break
        elif winner.lower() == team_b.lower():
            winner = team_b
            break
        print("  ⚠️  Please type the exact team name.")

    while True:
        decision = input(f"{winner} won the toss! Choose to (BAT/BOWL): ").strip().upper()
        if decision in ("BAT", "BOWL"):
            break
        print("  ⚠️  Please enter BAT or BOWL.")

    other_team = team_b if winner == team_a else team_a
    batting_first = winner if decision == "BAT" else other_team
    bowling_first = other_team if batting_first == winner else winner

    print(f"\n📣  {winner} chose to {decision}. {batting_first} will bat first!")
    return batting_first, bowling_first


# ----------------------------------------------------------------------
# BALL-BY-BALL ENGINE
# ----------------------------------------------------------------------

def ask_ball_outcome(over_num, ball_in_over, striker):
    prompt = (
        f"\n🎾 Over {over_num}.{ball_in_over} | {striker.name} on strike "
        f"-> Enter outcome [0-6 = runs, W = wicket, WD = wide, NB = no ball]: "
    )
    while True:
        raw = input(prompt).strip().upper()
        if raw in VALID_RUN_INPUTS or raw in ("W", "WD", "NB"):
            return raw
        print("  ⚠️  Invalid input. Use one of: 0,1,2,3,4,5,6,W,WD,NB")


def print_mini_scoreboard(batting_team, striker, non_striker, runs, wickets,
                           balls_bowled, target=None):
    overs_display = f"{balls_bowled // 6}.{balls_bowled % 6}"
    print(f"  📊 {batting_team}: {runs}/{wickets}  (Overs: {overs_display})")
    print(f"     🏃 {striker.name}* {striker.runs}({striker.balls})   "
          f"🧍 {non_striker.name} {non_striker.runs}({non_striker.balls})")
    if target is not None:
        remaining_runs = target - runs
        remaining_balls = OVERS_PER_INNINGS * 6 - balls_bowled
        if remaining_runs > 0 and remaining_balls > 0:
            print(f"     🎯 Need {remaining_runs} run(s) from {remaining_balls} ball(s)")


def print_scorecard(team_name, players, runs, wickets, balls_bowled, extras):
    divider("-")
    print(f"📋 SCORECARD: {team_name} — {runs}/{wickets} "
          f"({balls_bowled // 6}.{balls_bowled % 6} overs, Extras: {extras})")
    divider("-")
    print(f"  {'Batsman':<15}{'Runs':<8}{'Balls':<8}{'Status'}")
    for p in players:
        if p.balls > 0 or p.out:
            status = p.how_out
            print(f"  {p.name:<15}{p.runs:<8}{p.balls:<8}{status}")
    divider("-")


def play_innings(batting_team, players, bowling_team, target=None):
    divider()
    if target is None:
        print(f"🏁 INNINGS 1: {batting_team} 🏏 batting | {bowling_team} 🎯 bowling")
    else:
        print(f"🏁 INNINGS 2: {batting_team} 🏏 batting | {bowling_team} 🎯 bowling")
        print(f"🔥 Target: {target} runs to win!")
    divider()

    runs = 0
    wickets = 0
    balls_bowled = 0
    extras = 0

    striker_idx = 0
    non_striker_idx = 1
    next_batsman_idx = 2

    striker = players[striker_idx]
    non_striker = players[non_striker_idx]

    match_over = False

    for over_num in range(1, OVERS_PER_INNINGS + 1):
        if wickets >= TOTAL_PLAYERS - 1 or (target is not None and runs >= target):
            break

        print(f"\n🎬 --- Over {over_num} --- 🎬")
        balls_in_this_over = 0

        while balls_in_this_over < 6:
            if wickets >= TOTAL_PLAYERS - 1:
                print(f"\n💔 ALL OUT! {batting_team} have lost all their wickets.")
                match_over = True
                break
            if target is not None and runs >= target:
                print(f"\n🎉 {batting_team} have reached the target!")
                match_over = True
                break

            outcome = ask_ball_outcome(over_num, balls_in_this_over + 1, striker)

            if outcome == "W":
                striker.out = True
                striker.how_out = "out"
                striker.balls += 1
                wickets += 1
                balls_bowled += 1
                balls_in_this_over += 1
                print(f"  ❌🎉 WICKET! {striker.name} is out!")

                if wickets < TOTAL_PLAYERS - 1 and next_batsman_idx < TOTAL_PLAYERS:
                    striker_idx = next_batsman_idx
                    striker = players[striker_idx]
                    next_batsman_idx += 1
                    print(f"  🚶 In comes {striker.name} to bat.")

            elif outcome == "WD":
                runs += 1
                extras += 1
                print("  🙅 Wide ball! +1 extra run. Ball to be re-bowled.")

            elif outcome == "NB":
                runs += 1
                extras += 1
                print("  🚫 No ball! +1 extra run. Ball to be re-bowled.")

            else:
                run_val = int(outcome)
                runs += run_val
                striker.runs += run_val
                striker.balls += 1
                balls_bowled += 1
                balls_in_this_over += 1

                if run_val == 6:
                    print("  💥🚀 SIX! What a hit!")
                elif run_val == 4:
                    print("  🔥 FOUR! Cracking shot!")
                elif run_val == 0:
                    print("  🛑 Dot ball.")
                else:
                    print(f"  🏃 {run_val} run(s) taken.")

                if run_val % 2 == 1:
                    striker, non_striker = non_striker, striker

            print_mini_scoreboard(batting_team, striker, non_striker, runs,
                                   wickets, balls_bowled, target)

            if wickets >= TOTAL_PLAYERS - 1:
                print(f"\n💔 ALL OUT! {batting_team} have lost all their wickets.")
                match_over = True
                break
            if target is not None and runs >= target:
                print(f"\n🎉 {batting_team} have reached the target!")
                match_over = True
                break

        if match_over:
            break

        # end of over: swap ends
        striker, non_striker = non_striker, striker
        print(f"  🔚 End of over {over_num}. {batting_team}: {runs}/{wickets}")

    print(f"\n✅ Innings complete: {batting_team} finished on {runs}/{wickets} "
          f"in {balls_bowled // 6}.{balls_bowled % 6} overs.")
    print_scorecard(batting_team, players, runs, wickets, balls_bowled, extras)

    return runs, wickets


# ----------------------------------------------------------------------
# RESULT
# ----------------------------------------------------------------------

def declare_result(team1, runs1, wkts1, team2, runs2, wkts2):
    divider()
    print("🏆  MATCH RESULT  🏆")
    divider()
    print(f"  {team1}: {runs1}/{wkts1}")
    print(f"  {team2}: {runs2}/{wkts2}")
    print()

    if runs1 > runs2:
        margin = runs1 - runs2
        print(f"  🎉🏆 {team1} WIN by {margin} run(s)! 🏆🎉")
    elif runs2 > runs1:
        wickets_in_hand = (TOTAL_PLAYERS - 1) - wkts2
        print(f"  🎉🏆 {team2} WIN by {wickets_in_hand} wicket(s)! 🏆🎉")
    else:
        print("  🤝 MATCH TIED! What a thriller! 🤝")


# ----------------------------------------------------------------------
# MAIN GAME LOOP
# ----------------------------------------------------------------------

def play_match():
    team_a, team_a_players, team_b, team_b_players = get_team_setup()
    batting_first, bowling_first = do_toss(team_a, team_b)

    if batting_first == team_a:
        first_batting_players, second_batting_players = team_a_players, team_b_players
    else:
        first_batting_players, second_batting_players = team_b_players, team_a_players

    runs1, wkts1 = play_innings(batting_first, first_batting_players, bowling_first)

    target = runs1 + 1
    runs2, wkts2 = play_innings(bowling_first, second_batting_players, batting_first,
                                 target=target)

    declare_result(batting_first, runs1, wkts1, bowling_first, runs2, wkts2)


def main():
    while True:
        play_match()
        divider()
        again = input("🔁 Do you want to play a new match? (yes/no): ").strip().lower()
        if again not in ("yes", "y"):
            print("\n👋 Thanks for playing! See you next time. 🏏")
            sys.exit()


if __name__ == "__main__":
    main()