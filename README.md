# ChessPath - Chess Opening Trainer

This application helps users learn chess openings effectively.

## Manage Opening Database

To create or reset the opening database:

```bash
python main.py db op reset
```

You can then create an opening:

```bash
python main.py db op commit create name color
```

Where `name` is the name of the opening, and `color` is either `w` for white or `b` for black.

To delete an opening:

```bash
python main.py db op delete name color
```

## Chess Game

To display a standard chessboard:

```bash
python main.py board
```

## Edit Openings

You can edit an opening with:

```bash
python main.py editor openingName color
```

Where `openingName` is the name of the opening, and `color` is the color you play this opening with.

## Explore Openings

To explore openings:

```bash
python main.py player openingName color
```

## Train Openings

To train an opening:

```bash
python main.py train openingName color
```

If you are playing as black (`color=b`), press `<r>` (for reset) to start the line.

## Keyboard Commands

Here are some commands to help you navigate openings:

- `<r>` : Reset the board  
- `<s>` : Show the moves of the opening once  
- `<S>` : Always show the moves of the opening  
- `<c>` : Clear all drawings on the board  
- `<Left>` : Take back the last move  
- `<Forward>` : Automatically play the next move  
- `<Space>` : Provide a hint for the next opening move  

### Editor Mode Only:
- `<Control-s>` : Save the opening in the editor  
- `<Delete>` : Delete the last move in the editor  