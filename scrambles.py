import random
from pyTwistyScrambler import squareOneScrambler

def gen(event, attempts):
    scrambles_list = []
    event = event.lower()

    for i in range(int(attempts)):
        if event == "333" or event == "oh":
            scramble = scr333()
        elif event == "222":
            scramble = scr222()
        elif event == "444":
            scramble = scr444()
        elif event == "555":
            scramble = scr555()
        elif event == "3bld":
            scramble = scr3BLD()
        elif event == "fmc":
            scramble = scrFMC()
        elif event == "clock":
            scramble = scrClock()
        elif event == "mega":
            scramble = scrMega()
        
        scrambles_list.append(scramble)

    return scrambles_list

def scr333():
    moves = ["R", "R'", "R2", "L", "L'", "L2", "U", "U'", "U2", "D", "D'", "D2", "F", "F'", "F2", "B", "B'", "B2"]
    no_r = [i for i in moves if 'R' not in i]
    no_l = [i for i in moves if 'L' not in i]
    no_u = [i for i in moves if 'U' not in i]
    no_d = [i for i in moves if 'D' not in i]
    no_f = [i for i in moves if 'F' not in i]
    no_b = [i for i in moves if 'B' not in i]
    no_rl = [i for i in moves if 'R' not in i and 'L' not in i]
    no_ud = [i for i in moves if 'U' not in i and 'D' not in i]
    no_fb = [i for i in moves if 'F' not in i and 'B' not in i]
    times = random.randint(19, 21)
    full_moves = []
    for i in range(times):
        move = random.choice(moves)
        full_moves.append(move)
        moves = no_r if 'R' in move else no_l if 'L' in move else no_u if 'U' in move else no_d if 'D' in move else no_f if 'F' in move else no_b
        if i > 1:
            if ('R' in full_moves[i-1] or 'L' in full_moves[i-1]) and ('R' in full_moves[i] or 'L' in full_moves[i]):
                moves = no_rl
            elif ('U' in full_moves[i-1] or 'D' in full_moves[i-1]) and ('U' in full_moves[i] or 'D' in full_moves[i]):
                moves = no_ud
            elif ('F' in full_moves[i-1] or 'B' in full_moves[i-1]) and ('F' in full_moves[i] or 'B' in full_moves[i]):
                moves = no_fb
    return ' '.join([i for i in full_moves])

def scr222():
    moves = ["R", "R'", "R2", "U", "U'", "U2", "F", "F'", "F2"]
    no_r = [i for i in moves if 'R' not in i]
    no_u = [i for i in moves if 'U' not in i]
    no_f = [i for i in moves if 'F' not in i]
    times = random.randint(9, 10)
    full_moves = []
    for i in range(times):
        move = random.choice(moves)
        full_moves.append(move)
        moves = no_r if 'R' in move else no_u if 'U' in move else no_f
    return ' '.join([i for i in moves])

def scr444():
    moves = ["R", "R'", "R2", "Rw", "Rw'", "Rw2", "L", "L'", "L2", "U", "U'", "U2", "Uw", "Uw'", "Uw2", "D", "D'", "D2", "F", "F'", "F2", "Fw", "Fw'", "Fw2", "B", "B'", "B2"]
    no_r = [i for i in moves if 'R' not in i]
    no_l = [i for i in moves if 'L' not in i]
    no_u = [i for i in moves if 'U' not in i]
    no_d = [i for i in moves if 'D' not in i]
    no_f = [i for i in moves if 'F' not in i]
    no_b = [i for i in moves if 'B' not in i]
    no_rl = [i for i in moves if 'R' not in i and 'L' not in i]
    no_ud = [i for i in moves if 'U' not in i and 'D' not in i]
    no_fb = [i for i in moves if 'F' not in i and 'B' not in i]
    times = random.randint(24, 26)
    full_moves = []
    for i in range(times):
        move = random.choice(moves)
        full_moves.append(move)
        moves = no_r if 'R' in move else no_l if 'L' in move else no_u if 'U' in move else no_d if 'D' in move else no_f if 'F' in move else no_b
        if i > 0:
            if ('R' in full_moves[i-1] or 'L' in full_moves[i-1]) and ('R' in full_moves[i] or 'L' in full_moves[i]):
                moves = no_rl
            elif ('U' in full_moves[i-1] or 'D' in full_moves[i-1]) and ('U' in full_moves[i] or 'D' in full_moves[i]):
                moves = no_ud
            elif ('F' in full_moves[i-1] or 'B' in full_moves[i-1]) and ('F' in full_moves[i] or 'B' in full_moves[i]):
                moves = no_fb
    return f"{scr333()} {' '.join([i for i in full_moves])}"

def scr555():
    moves = ["R", "R'", "R2", "Rw", "Rw'", "Rw2", "L", "L'", "L2", "Lw", "Lw'", "Lw2", "U", "U'", "U2", "Uw", "Uw'", "Uw2", "D", "D'", "D2", "Dw", "Dw'", "Dw2", "F", "F'", "F2", "Fw", "Fw'", "Fw2", "B", "B'", "B2", "Bw", "Bw'", "Bw2"]
    no_r = [i for i in moves if 'R' not in i]
    no_l = [i for i in moves if 'L' not in i]
    no_u = [i for i in moves if 'U' not in i]
    no_d = [i for i in moves if 'D' not in i]
    no_f = [i for i in moves if 'F' not in i]
    no_b = [i for i in moves if 'B' not in i]
    no_rl = [i for i in moves if 'R' not in i and 'L' not in i]
    no_ud = [i for i in moves if 'U' not in i and 'D' not in i]
    no_fb = [i for i in moves if 'F' not in i and 'B' not in i]
    times = 60
    full_moves = []
    for i in range(times):
        move = random.choice(moves)
        full_moves.append(move)
        moves = no_r if 'R' in move else no_l if 'L' in move else no_u if 'U' in move else no_d if 'D' in move else no_f if 'F' in move else no_b
        if i > 0:
            if ('R' in full_moves[i-1] or 'L' in full_moves[i-1]) and ('R' in full_moves[i] or 'L' in full_moves[i]):
                moves = no_rl
            elif ('U' in full_moves[i-1] or 'D' in full_moves[i-1]) and ('U' in full_moves[i] or 'D' in full_moves[i]):
                moves = no_ud
            elif ('F' in full_moves[i-1] or 'B' in full_moves[i-1]) and ('F' in full_moves[i] or 'B' in full_moves[i]):
                moves = no_fb
    return ' '.join([i for i in full_moves])

def scr666():
    moves = ["R", "R'", "R2", "Rw", "Rw'", "Rw2", "3Rw", "3Rw'", "3Rw2", "L", "L'", "L2", "Lw", "Lw'", "Lw2", "U", "U'", "U2", "Uw", "Uw'", "Uw2", "3Uw", "3Uw'", "3Uw2", "D", "D'", "D2", "Dw", "Dw'", "Dw2", "F", "F'", "F2", "Fw", "Fw'", "Fw2", "3Fw", "3Fw'", "3Fw2", "B", "B'", "B2", "Bw", "Bw'", "Bw2"]
    no_r = [i for i in moves if 'R' not in i]
    no_l = [i for i in moves if 'L' not in i]
    no_u = [i for i in moves if 'U' not in i]
    no_d = [i for i in moves if 'D' not in i]
    no_f = [i for i in moves if 'F' not in i]
    no_b = [i for i in moves if 'B' not in i]
    no_rl = [i for i in moves if 'R' not in i and 'L' not in i]
    no_ud = [i for i in moves if 'U' not in i and 'D' not in i]
    no_fb = [i for i in moves if 'F' not in i and 'B' not in i]
    times = 80
    full_moves = []
    for i in range(times):
        move = random.choice(moves)
        full_moves.append(move)
        moves = no_r if 'R' in move else no_l if 'L' in move else no_u if 'U' in move else no_d if 'D' in move else no_f if 'F' in move else no_b
        if i > 0:
            if ('R' in full_moves[i-1] or 'L' in full_moves[i-1]) and ('R' in full_moves[i] or 'L' in full_moves[i]):
                moves = no_rl
            elif ('U' in full_moves[i-1] or 'D' in full_moves[i-1]) and ('U' in full_moves[i] or 'D' in full_moves[i]):
                moves = no_ud
            elif ('F' in full_moves[i-1] or 'B' in full_moves[i-1]) and ('F' in full_moves[i] or 'B' in full_moves[i]):
                moves = no_fb
    return ' '.join([i for i in full_moves])

def scr777():
    moves = ["R", "R'", "R2", "Rw", "Rw'", "Rw2", "3Rw", "3Rw'", "3Rw2", "L", "L'", "L2", "Lw", "Lw'", "Lw2", "3Lw", "3Lw'", "3Lw2", "U", "U'", "U2", "Uw", "Uw'", "Uw2", "3Uw", "3Uw'", "3Uw2", "D", "D'", "D2", "Dw", "Dw'", "Dw2", "3Dw", "3Dw'", "3Dw2", "F", "F'", "F2", "Fw", "Fw'", "Fw2", "3Fw", "3Fw'", "3Fw2", "B", "B'", "B2", "Bw", "Bw'", "Bw2", "3Bw", "3Bw'", "3Bw2"]
    no_r = [i for i in moves if 'R' not in i]
    no_l = [i for i in moves if 'L' not in i]
    no_u = [i for i in moves if 'U' not in i]
    no_d = [i for i in moves if 'D' not in i]
    no_f = [i for i in moves if 'F' not in i]
    no_b = [i for i in moves if 'B' not in i]
    no_rl = [i for i in moves if 'R' not in i and 'L' not in i]
    no_ud = [i for i in moves if 'U' not in i and 'D' not in i]
    no_fb = [i for i in moves if 'F' not in i and 'B' not in i]
    times = 100
    full_moves = []
    for i in range(times):
        move = random.choice(moves)
        full_moves.append(move)
        moves = no_r if 'R' in move else no_l if 'L' in move else no_u if 'U' in move else no_d if 'D' in move else no_f if 'F' in move else no_b
        if i > 0:
            if ('R' in full_moves[i-1] or 'L' in full_moves[i-1]) and ('R' in full_moves[i] or 'L' in full_moves[i]):
                moves = no_rl
            elif ('U' in full_moves[i-1] or 'D' in full_moves[i-1]) and ('U' in full_moves[i] or 'D' in full_moves[i]):
                moves = no_ud
            elif ('F' in full_moves[i-1] or 'B' in full_moves[i-1]) and ('F' in full_moves[i] or 'B' in full_moves[i]):
                moves = no_fb
    return ' '.join([i for i in full_moves])

def scr3BLD():
    moves = ["Rw", "Rw'", "Rw2", "Uw", "Uw'", "Uw2", "Fw", "Fw'", "Fw2", ""]
    no_r = [i for i in moves if 'R' not in i]
    no_u = [i for i in moves if 'U' not in i]
    no_f = [i for i in moves if 'F' not in i]
    times = random.randint(1, 2)
    wide_moves = []
    for i in range(times):
        move = random.choice(moves)
        wide_moves.append(move)
        if i == 0:
            moves.remove('')
        moves = no_r if 'R' in move else no_u if 'U' in move else no_f
    return f"{scr333()} {' '.join([i for i in wide_moves])}"

def scrFMC():
    moves = ["R", "R'", "R2", "L", "L'", "L2", "U", "U'", "U2", "D", "D'", "D2", "F", "F'", "F2", "B", "B'", "B2"]
    no_r = [i for i in moves if 'R' not in i]
    no_l = [i for i in moves if 'L' not in i]
    no_u = [i for i in moves if 'U' not in i]
    no_d = [i for i in moves if 'D' not in i]
    no_f = [i for i in moves if 'F' not in i]
    no_b = [i for i in moves if 'B' not in i]
    no_rl = [i for i in moves if 'R' not in i and 'L' not in i]
    no_ud = [i for i in moves if 'U' not in i and 'D' not in i]
    no_fb = [i for i in moves if 'F' not in i and 'B' not in i]
    moves = no_f
    times = random.randint(13, 15)
    full_moves = []
    for i in range(times):
        move = random.choice(moves)
        full_moves.append(move)
        moves = no_r if 'R' in move else no_l if 'L' in move else no_u if 'U' in move else no_d if 'D' in move else no_f if 'F' in move else no_b
        if i > 1:
            if ('R' in full_moves[i-1] or 'L' in full_moves[i-1]) and ('R' in full_moves[i] or 'L' in full_moves[i]):
                moves = no_rl
            elif ('U' in full_moves[i-1] or 'D' in full_moves[i-1]) and ('U' in full_moves[i] or 'D' in full_moves[i]):
                moves = no_ud
            elif ('F' in full_moves[i-1] or 'B' in full_moves[i-1]) and ('F' in full_moves[i] or 'B' in full_moves[i]):
                moves = no_fb
        if i == times - 2 and moves != no_r and moves != no_rl: moves = no_r 
    return f"R' U' F {' '.join([i for i in full_moves])} R' U' F"

# OH is the same as 333

def scrClock():
    pins = [['UR', ''], ['DR', ''], ['DL', ''], ['UL', '']]
    pos = ['UR', 'DR', 'DL', 'UL', 'U', 'R', 'D', 'L', 'ALL', 'y', 'U', 'R', 'D', 'L', 'ALL']
    times = 15
    pin_times = 4
    full_pins = []
    full_ticks = []
    for i in range(times):
        ticks = random.randint(0, 6)
        direction = random.choice(['+', '-'] if ticks != 0 or ticks != 6 else ['+'])
        full_ticks.append(f'{pos[i]}{ticks}{direction}')
    full_ticks[9] = 'y2'
    for i in range(pin_times):
        pin = random.choice(pins[i])
        full_pins.append(pin)
    return f"{' '.join([i for i in full_ticks])} {' '.join([i for i in full_pins if i != ''])}"

def scrMega():
    moves = [['R++', 'R--'], ['D++', 'D--'], ["U", "U'"]]
    lines = 7
    times = 11
    full_moves = []
    for i in range(lines):
        line_moves = []
        for j in range(times):
            move = random.choice(moves[j % 2]) if j != 10 else random.choice(moves[2])
            line_moves.append(move)
        full_moves.append(' '.join([k for k in line_moves]))
    return '\n'.join([l for l in full_moves])

def scrPyra():
    tips = [["l", "l'", ""], ["r", "r'", ""], ["b", "b'", ""], ["u", "u'", ""]]
    times = 4
    full_tips = []
    for i in range(times):
        tip = random.choice(tips[i])
        full_tips.append(tip)
    return f"{scrSkewb()} {' '.join([i for i in full_tips if i != ''])}"

def scrSkewb():
    moves = ["R", "R'", "L", "L'", "U", "U'", "B", "B'"]
    no_r = [i for i in moves if 'R' not in i]
    no_l = [i for i in moves if 'L' not in i]
    no_u = [i for i in moves if 'U' not in i]
    no_b = [i for i in moves if 'B' not in i]
    times = random.randint(8, 9)
    full_moves = []
    for i in range(times):
        move = random.choice(moves)
        full_moves.append(move)
        moves = no_r if 'R' in move else no_l if 'L' in move else no_u if 'U' in move else no_b
    return ' '.join([i for i in full_moves])

def scrSQ1():
    return squareOneScrambler.get_WCA_scramble()

def scr4BLD():
    rotates = [["x", "x'", "x2", "z", "z'", "z2", ""], ["y", "y'", "y2", ""]]
    times = 2
    full_rotates = []
    for i in range(times):
        rotate = random.choice(rotates[i % 2])
        full_rotates.append(rotate)
    return f"{scr444()} {' '.join([i for i in full_rotates if i != ''])}"

def scr5BLD():
    moves = [["3Rw", "3Rw'", "3Rw2", "3Fw", "3Fw'", "3Fw2", ""], ["3Uw", "3Uw'", "3Uw2", ""]]
    times = 2
    full_moves = []
    for i in range(times):
        move = random.choice(moves[i % 2])
        full_moves.append(move)
    return f"{scr555()} {' '.join([i for i in full_moves if i != ''])}"

# MBLD is the same as 3BLD but with multiple scrambles