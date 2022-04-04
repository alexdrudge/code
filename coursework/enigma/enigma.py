import re

class PlugLead:
    def __init__(self, mapping):
        validate_string(mapping, 2)
        # cannot map to itself
        if mapping[0] == mapping[1]:
            raise ValueError()
        else:
            self.mapping = mapping

    def encode(self, character):
        validate_string(character, 1)
        # swap character over mapping
        if self.mapping[0] == character:
            return self.mapping[1]
        elif self.mapping[1] == character:
            return self.mapping[0]
        else:
            return character
    
    def get_mapping(self):
        return self.mapping

class Plugboard:
    def __init__(self):
        self.plugleads = []
    
    def add(self, pluglead):
        # validate PlugLead
        if not isinstance(pluglead, PlugLead):
            raise ValueError()
        # check plug is not already in use
        for i in self.plugleads:
            if pluglead.get_mapping()[0] in i.get_mapping():
                raise ValueError()
            elif pluglead.get_mapping()[1] in i.get_mapping():
                raise ValueError()
        # maximum of 10 leads
        if len(self.plugleads) >= 10:
            raise ValueError()
        else:
            self.plugleads.append(pluglead)
    
    def encode(self, character):
        validate_string(character, 1)
        # pass the character though 'all' plugleads
        for pluglead in self.plugleads:
            if pluglead.encode(character) != character:
                return pluglead.encode(character)
        return character

class Rotor:
    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    def __init__(self, mapping, notch = "", position = "A", setting = "01"):
        validate_string(mapping, 26)
        validate_string(notch, reg = "^[A-Z]*$")
        # check its length 0 or 1
        if not (len(notch) == 0 or len(notch) == 1):
            raise ValueError()
        validate_string(position, 1)
        validate_string(setting, reg = "^[0-9]+$")
        # check its length 1 or 2
        if not (len(setting) == 1 or len(setting) == 2):
            raise ValueError()
        self.mapping = mapping
        self.notch = notch
        # convert both to integers representing letters
        self.position = Rotor.ALPHABET.find(position)
        self.setting = int(setting) - 1
        # check that the ring setting is in the range 0-25
        if not 0 <= self.setting <= 25:
            print(self.setting)
            raise ValueError()

    def encode_right_to_left(self, character):
        validate_string(character, 1)
        num = Rotor.ALPHABET.find(character)
        # adjust the letter going into the rotor
        character = Rotor.ALPHABET[(num + self.position - self.setting) % 26]
        for i in range(26):
            if character == Rotor.ALPHABET[i]:
                # adjust the letter coming out of the rotor
                num = Rotor.ALPHABET.find(self.mapping[i])
                return Rotor.ALPHABET[(num - self.position + self.setting) % 26]

    def encode_left_to_right(self, character):
        validate_string(character, 1)
        # adjust the letter going into the rotor
        num = Rotor.ALPHABET.find(character)
        character = Rotor.ALPHABET[(num + self.position - self.setting) % 26]
        for i in range(26):
            if character == self.mapping[i]:
                # adjust the letter coming out of the rotor
                return Rotor.ALPHABET[(i - self.position + self.setting) % 26]
    
    def rotate(self):
        self.position = (self.position + 1) % 26
    
    def on_notch(self):
        if Rotor.ALPHABET[self.position] == self.notch:
            return True
        return False
    
    def get_mapping(self):
        return self.mapping

class EnigmaMachine:
    def __init__(self, rotors, reflector, ring_settings, inital_positions, plugboard_pairs):
        # check that there are three or four rotors
        if not ((len(rotors) == 3 and len(ring_settings) == 3 and len(inital_positions) == 3) or (len(rotors) == 4 and len(ring_settings) == 4 and len(inital_positions) == 4)):
            raise ValueError()
        # check there are no duplicate rotors
        for i in range(len(rotors)):
            for j in range(len(rotors)):
                if rotors[i] == rotors[j] and i != j:
                    raise ValueError()
        # rotors from left to right
        self.rotors = []
        for i in range(3):
            self.rotors.append(rotor_from_name(rotors[i], inital_positions[i], ring_settings[i]))
        self.reflector = rotor_from_name(reflector)
        self.plugboard = Plugboard()
        for i in plugboard_pairs:
            self.plugboard.add(PlugLead(i))

    def encode(self, text):
        validate_string(text)
        result = ""
        for character in text:
            # first plugboard pass through
            character = self.plugboard.encode(character)
            # turnover and double step
            if self.rotors[-2].on_notch():
                self.rotors[-1].rotate()
                self.rotors[-2].rotate()
                self.rotors[-3].rotate()
            elif self.rotors[-1].on_notch():
                self.rotors[-1].rotate()
                self.rotors[-2].rotate()
            else:
                self.rotors[-1].rotate()
            # pass through rotors in reverse
            for i in self.rotors[::-1]:
                character = i.encode_right_to_left(character)
            # pass through reflector
            character = self.reflector.encode_right_to_left(character)
            # pass through rotors
            for i in self.rotors:
                character = i.encode_left_to_right(character)
            # second plugboard pass through
            character = self.plugboard.encode(character)
            result += character
        return result
    
    def set_reflector(self, reflector):
        if not isinstance(reflector, Rotor):
            raise ValueError()
        self.reflector = reflector

def validate_string(string, length = 0, reg = "^[A-Z]+$"):
    # defualt: length of 1 with only characters A-Z
    if not isinstance(string, str):
        raise ValueError()
    if length != 0:
        if not len(string) == length:
            raise ValueError()
    if not re.match(reg, string):
        raise ValueError()

def rotor_from_name(name, position = "A", setting = "01"):
    if name == "Beta":
        return Rotor("LEYJVCNIXWPBQMDRTAKZGFUHOS", "", position, setting)
    elif name == "Gamma":
        return Rotor("FSOKANUERHMBTIYCWLQPZXVGJD", "", position, setting)
    elif name == "I":
        return Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q", position, setting)
    elif name == "II":
        return Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E", position, setting)
    elif name == "III":
        return Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V", position, setting)
    elif name == "IV":
        return Rotor("ESOVPZJAYQUIRHXLNFTGKDCMWB", "J", position, setting)
    elif name == "V":
        return Rotor("VZBRGITYUPSDNHLXAWMJQOFECK", "Z", position, setting)
    elif name == "A":
        return Rotor("EJMZALYXVBWFCRQUONTSPIKHGD", "", position, setting)
    elif name == "B":
        return Rotor("YRUHQSLDPXNGOKMIEBFZCWVJAT", "", position, setting)
    elif name == "C":
        return Rotor("FVPJIAOYEDRZXWGCTKUQSBNMHL", "", position, setting)
    else:
        raise ValueError()

def create_enigma_machine(rotors, reflector, ring_settings, initial_positions, plugboard_pairs=[]):
    # check strings before spliting
    validate_string(rotors, reg = "^[A-Za-z ]+$")
    validate_string(initial_positions, reg = "^[A-Z ]+$")
    validate_string(ring_settings, reg = "^[0-9 ]+$")
    rotors_list = rotors.split()
    ring_settings_list = ring_settings.split()
    initial_positions_list = initial_positions.split()
    return EnigmaMachine(rotors_list, reflector, ring_settings_list, initial_positions_list, plugboard_pairs)

### TEST MATERIAL

def code_one():
    code = "DMEXBMKYCVPNQBEDHXVPZGKMTFFBJRPJTLHLCHOTKOYXGGHZ"
    crib = "SECRETS"
    solutions = []

    rotors = "Beta Gamma V"
    # reflector unknown
    ring_settings = "04 02 14"
    initial_positions = "M J M"
    plugboard_pairs = ["KI", "XN", "FL"]

    reflectors = ["A", "B", "C"]
    for reflector in reflectors:
        enigma = create_enigma_machine(rotors, reflector, ring_settings, initial_positions, plugboard_pairs)
        result = enigma.encode(code)
        if crib in result:
            solutions.append(result)
    return solutions

def code_two():
    code = "CMFSUPKNCBMUYEQVVDYKLRQZTPUFHSWWAKTUGXMPAMYAFITXIJKMH"
    crib = "UNIVERSITY"
    solutions = []

    rotors = "Beta I III"
    reflector = "B"
    ring_settings = "23 02 10"
    # initital positions unknown
    plugboard_pairs = ["VH", "PT", "ZG", "BJ", "EY", "FS"]

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in range(26):
        for j in range(26):
            for k in range(26):
                initial_positions = alphabet[i] + " " + alphabet[j] + " " + alphabet[k]
                enigma = create_enigma_machine(rotors, reflector, ring_settings, initial_positions, plugboard_pairs)
                result = enigma.encode(code)
                if crib in result:
                    solutions.append(result)
    return solutions

def code_three():
    code = "ABSKJAKKMRITTNYURBJFWQGRSGNNYJSDRYLAPQWIAGKJYEPCTAGDCTHLCDRZRFZHKNRSDLNPFPEBVESHPY"
    crib = "THOUSANDS"
    solutions = []

    # rotors unknown and restricted
    # reflector unknown
    # ring settings unknown and restricted
    initial_positions = "E M Y"
    plugboard_pairs = ["FH", "TS", "BE", "UQ", "KD", "AL"]

    rotor_list = ["II", "IV", "Beta", "Gamma"]
    reflectors = ["A", "B", "C"]
    for rotor1 in rotor_list:
        for rotor2 in rotor_list:
            for rotor3 in rotor_list:
                if rotor1 != rotor2 and rotor1 != rotor3 and rotor2 != rotor3:
                    rotors = rotor1 + " " + rotor2 + " " + rotor3
                    for reflector in reflectors:
                        for i in range(26):
                            for j in range(26):
                                for k in range(26):
                                    ring_settings = str(i+1) + " " + str(j+1) + " " + str(k+1)
                                    valid = True
                                    for l in ring_settings:
                                        if l in "13579":
                                            valid = False
                                    if valid:
                                        enigma = create_enigma_machine(rotors, reflector, ring_settings, initial_positions, plugboard_pairs)
                                        result = enigma.encode(code)
                                        if crib in result:
                                            solutions.append(result)
    return solutions

def code_four():
    code = "SDNTVTPHRBNWTLMZTQKZGADDQYPFNHBPNHCQGBGMZPZLUAVGDQVYRBFYYEIXQWVTHXGNW"
    crib = "TUTOR"
    solutions = []

    rotors = "V III IV"
    reflector = "A"
    ring_settings = "24 12 10"
    initial_positions = "S W U"
    plugboard = ["WP", "RJ", "VF", "HN", "CG", "BS"] # "A?", "I?"

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in range(26):
        for j in range(26):
            plugboard_pairs = plugboard[:]
            plugboard_pairs.append("A" + alphabet[i])
            plugboard_pairs.append("I" + alphabet[j])
            try:
                enigma = create_enigma_machine(rotors, reflector, ring_settings, initial_positions, plugboard_pairs)
                result = enigma.encode(code)
                if crib in result:
                    solutions.append(result)
            except:
                pass
    return solutions

def code_five():
    code = "HWREISXLGTTBYVXRCWWJAKZDTVZWKBDJPVQYNEQIOTIFX"
    # crib unknown but restricted
    solutions = []

    rotors = "V II IV"
    # reflector unknown and modified
    ring_settings = "06 18 07"
    initial_positions = "A J L"
    plugboard_pairs = ["UG", "IE", "PO", "NX", "WT"]

    cribs = ["TWITTER", "SNAPCHAT", "FACEBOOK", "INSTAGRAM", "TIKTOK", "WHATSAPP", "REDDIT"]
    reflectors = ["A", "B", "C"]
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for name in reflectors:
        for i in range(26):
            for j in range(26):
                for k in range(26):
                    for l in range(26):
                        # prevent answers with different letter orderings
                        if i < j  and k < l and i < k and j != k:
                            # get the positions of the letters within the mapping
                            mapping = rotor_from_name(name).get_mapping()
                            num1 = mapping.find(alphabet[i])
                            num2 = mapping.find(alphabet[j])
                            num3 = mapping.find(alphabet[k])
                            num4 = mapping.find(alphabet[l])
                            # prevent both wires from being the same
                            if i != num2 and k != num4:
                                # swap over the 8 letters
                                mapping = list(mapping)
                                mapping[i] = alphabet[num2]
                                mapping[j] = alphabet[num1]
                                mapping[k] = alphabet[num4]
                                mapping[l] = alphabet[num3]
                                mapping[num1] = alphabet[j]
                                mapping[num2] = alphabet[i]
                                mapping[num3] = alphabet[l]
                                mapping[num4] = alphabet[k]
                                mapping = "".join(mapping)
                                # create the new reflector
                                reflector = Rotor(mapping, "", "A", "01")
                                enigma = create_enigma_machine(rotors, name, ring_settings, initial_positions, plugboard_pairs)
                                enigma.set_reflector(reflector)
                                result = enigma.encode(code)
                                for crib in cribs:
                                    if crib in result:
                                        solutions.append(result)
    return solutions

if __name__ == "__main__":
    print(code_two())
    possible_messages = code_five()
    assert("YOUCANFOLLOWMYDOGONINSTAGRAMATTALESOFHOFFMANN" in possible_messages)
    #print(code_three())
    #print(code_five())