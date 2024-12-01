# ChessPath - Chess Opening Trainer

ChessPath is a tool designed to help users learn and master chess openings.

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

## Train Against Lichess Openings Database

You can train against the most common moves played on Lichess for a given ELO, position, and time control:

```bash
python main.py lichess-sim <color> <min_elo> <max_elo> <time_control> <number_of_move>
```

Where:
- **`<color>`**: The color you will play as, either `w` or `b`.  
- **`<min_elo>`**: Minimum ELO of the players in the database.  
- **`<max_elo>`**: Maximum ELO of the players in the database.  
- **`<time_control>`**: Time control to filter by (`bullet`, `blitz`, `rapid`, `classical`).  
- **`<number_of_move>`**: Number of the most common moves to consider.

A good way to use this feature is to first press `<t>` to toggle to two-player mode. Input a position of interest, then press`<t>` to toggle back and `<a>` to set an anchor to that position. Continue playing, and to return to the anchor, press `<A>`.

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