# ChessPath - Chess Opening Trainer

**ChessPath** allows users to manage opening databases, explore and train openings, replay mistakes from your `Chess.com` games, and simulate common moves from the `Lichess` database based on ELO and time controls.

---

## Manage Opening Database

### Reset or Initialize the Database

To reset or initialize the opening database, run:

```bash
python main.py db op reset
```

### Create an Opening

To create a new opening, use the following command:

```bash
python main.py db op commit create <name> <color>
```

- **`<name>`**: The name of the opening.  
- **`<color>`**: The color you play the opening with (`w` for white, `b` for black).

### Delete an Opening

To delete an existing opening, run:

```bash
python main.py db op commit delete <name> <color>
```

---

## Chess Game

### Display a Standard Chessboard

To display a chessboard, run:

```bash
python main.py board
```

---

## Edit Openings

### Modify an Existing Opening

To edit an opening, use:

```bash
python main.py editor <openingName> <color>
```

- **`<openingName>`**: The name of the opening to edit.  
- **`<color>`**: The color you play this opening with (`w` or `b`).

---

## Explore Openings

### View Opening Moves

To explore a specific opening, run:

```bash
python main.py player <openingName> <color>
```

---

## Train Openings

### Practice Opening Moves

To train an opening, use:

```bash
python main.py train <openingName> <color>
```

- For black openings (`<color>=b`), press `<r>` to reset and start the line.

---

## Replay Opening Mistakes

You can replay opening mistakes made on chess.com with:

```bash
python main.py mistakes <user-name> <from-date> <time-control>
```

Where:
- **`<user-name>`**: Your chess.com username.  
- **`<from-date>`**: A date in the format `yyyy-mm-dd` from which you want to analyze your games.  
- **`<time-control>`**: The time control in seconds or in the format `seconds+increment`.

For example:

```bash
python main.py mistakes Bob 2024-08-01 600
```

This would fetch rapid games played from 2024-08-01 by Bob in 10-minute time control. To go to the next mistake, press `<M>`. To reset the board to the current mistake, press `<m>`. If you want the app to automatically switch to the next mistake once the correct move is input, run:

```bash
python main.py mistakes <user-name> <from-date> <time-control> --auto-next
```

---

## Train Against Lichess Openings Database

You can train against the most common moves played on Lichess for a given ELO range, position, and time control:

```bash
python main.py lichess-sim <color> <min_elo> <max_elo> <time_control> <number_of_moves>
```

Where:
- **`<color>`**: The color you will play as, either `w` or `b`.  
- **`<min_elo>`**: Minimum ELO of the players in the database.  
- **`<max_elo>`**: Maximum ELO of the players in the database.  
- **`<time_control>`**: Time control to filter by (`bullet`, `blitz`, `rapid`, `classical`).  
- **`<number_of_moves>`**: Number of the most common moves to consider.

To use this feature effectively:
1. Press `<t>` to toggle two-player mode.
2. Input a position of interest.
3. Press `<t>` again to toggle back.
4. Press `<a>` to set an anchor to that position.
5. Continue playing, and press `<A>` to return to the anchor.

---

## Keyboard Commands

### General Commands

- **`<r>`**: Reset the board.  
- **`<s>`**: Show the moves of the opening once.  
- **`<S>`**: Always show the moves of the opening.  
- **`<c>`**: Clear all drawings on the board.  
- **`<W>`**: Show all written annotations for the current position.  
- **`<t>`**: Toggle between the current mode and two-player mode.  
- **`<a>`**: Set an anchor at the current position.  
- **`<A>`**: Jump to the anchor.  
- **`<Left>`**: Undo the last move.  
- **`<Forward>`**: Play the next move automatically.  
- **`<Space>`**: Show a hint for the next move.

### Editor Mode Commands

- **`<w>`**: Write all drawings into the position annotation.  
- **`<Ctrl+s>`**: Save the current state of the opening.  
- **`<Delete>`**: Delete the last move in the editor.

### Mistake Mode Commands

- **`<M>`**: Go to the next mistake.  
- **`<m>`**: Reset the board to the current mistake.