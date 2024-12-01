# ChessPath - Chess Opening Trainer

ChessPath is a tool designed to help users learn and master chess openings.

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
- **`<W>`** : Shows all writen anotation for the current position
- **`<t>`**: Toggle between current mode and two players mode
- **`<a>`**: Set an anchor at the current position.  
- **`<A>`**: Jump to the anchor. 
- **`<Left>`**: Undo the last move.
- **`<Forward>`**: Play the next move automatically.  
- **`<Space>`**: Show a hint for the next move.

### Editor Mode Commands

- **`<w>`** : Write all drawing into the position annotation
- **`<Ctrl+s>`**: Save the current state of the opening.  
- **`<Delete>`**: Delete the last move in the editor.