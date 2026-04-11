# runs language from https://esolangs.org/wiki/Pig
def run_pig(code: str) -> None:
    if type(code) is not str:
        raise ValueError('ERROR: Code must be a string.')
    if 'PIG' not in code:
        raise ValueError('ERROR: Code must contain "PIG".')
    file_name, file_text = code.split('PIG',1)
    file = open(f'{file_name}.txt', 'w')
    file.write(file_text)
    file.close()
