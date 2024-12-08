from PIL import Image, ImageTk
import yaml

with open("config.yaml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

def load_chess_pieces():
    chess_pieces_path = config['chess_pieces'] + "/image.png"
    return Image.open(chess_pieces_path).convert('RGBA')

def load_chess_pieces_rect():
    chess_pieces_rect_path = config['chess_pieces'] + "/rect.yaml"
    with open(chess_pieces_rect_path, 'r') as stream:
        try:
            chess_pieces_rect = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return chess_pieces_rect

def extract_piece(image, rect, case_size):
    piece_image =  image.crop(rect)
    piece_image = piece_image.resize((case_size, case_size))
    piece_tk_image = ImageTk.PhotoImage(piece_image)
    return piece_tk_image