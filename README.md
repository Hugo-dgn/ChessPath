# ChessPath - Chess Opening Trainer

ChessPath is a tool designed to help users learn and master chess openings effectively.

---

## Manage Opening Database

### Reset or Initialize the Database

To reset or initialize the opening database:

```bash
python main.py db op reset
```

### Create an Opening

To create a new opening:

```bash
python main.py db op commit create <name> <color>
```

- **`<name>`**: The name of the opening.  
- **`<color>`**: The color you play the opening with (`w` for white, `b` for black).

### Delete an Opening

To delete an existing opening:

```bash
python main.py db op commit delete <name> <color>
```

---

## Chess Game

### Display a Standard Chessboard

To display a chessboard:

```bash
python main.py board
```

---

## Edit Openings

### Modify an Existing Opening

To edit an opening:

```bash
python main.py editor <openingName> <color>
```

- **`<openingName>`**: The name of the opening to edit.  
- **`<color>`**: The color you play this opening with (`w` or `b`).

---

## Explore Openings

### View Opening Moves

To explore a specific opening:

```bash
python main.py player <openingName> <color>
```

---

## Train Openings

### Practice Opening Moves

To train an opening:

```bash
python main.py train <openingName> <color>
```

For black openings (`<color>=b`), press `<r>` to reset and start the line.

---

## Keyboard Commands

### General Commands

- **`<r>`**: Reset the board.  
- **`<s>`**: Show the moves of the opening once.  
- **`<S>`**: Always show the moves of the opening.  
- **`<c>`**: Clear all drawings on the board.  
- **`<Left>`**: Undo the last move.  
- **`<Forward>`**: Play the next move automatically.  
- **`<Space>`**: Show a hint for the next move.

### Editor Mode Commands

- **`<t>`**: Toggle between training and exploring the opening.  
- **`<a>`**: Set an anchor at the current position.  
- **`<A>`**: Jump to the anchor.  
- **`<Ctrl+s>`**: Save the current state of the opening.  
- **`<Delete>`**: Delete the last move in the editor.

--- 

ChessPath makes it easy to practice and perfect your favorite chess openings.