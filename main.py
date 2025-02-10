from unicode import join_jamos

def convert_mistyped_korean(text):
    """
    잘못 입력된 영문자열(두벌식 자판 기준)을 받아 올바른 한글 음절로 변환한다.
    대문자는 쌍자음(ㄲ,ㄸ,ㅃ,ㅆ,ㅉ)에 대응한다.
    """
    # 1. 영문자 → 한글 자모 매핑 (소문자 + 쌍자음용 대문자)
    mapping = {
        'r': 'ㄱ',  's': 'ㄴ',  'e': 'ㄷ',  'f': 'ㄹ',  'a': 'ㅁ',
        'q': 'ㅂ',  't': 'ㅅ',  'd': 'ㅇ',  'w': 'ㅈ',  'c': 'ㅊ',
        'z': 'ㅋ',  'x': 'ㅌ',  'v': 'ㅍ',  'g': 'ㅎ',
        'k': 'ㅏ',  'o': 'ㅐ',  'i': 'ㅑ',  'j': 'ㅓ',  'p': 'ㅔ', 'P': 'ㅖ',
        'u': 'ㅕ',  'h': 'ㅗ',  'y': 'ㅛ',  'n': 'ㅜ',  'b': 'ㅠ',
        'm': 'ㅡ',  'l': 'ㅣ'
    }
    # 대문자 -> 쌍자음 매핑 (두벌식 기준)
    mapping.update({
        'R': 'ㄲ',
        'E': 'ㄸ',
        'Q': 'ㅃ',
        'W': 'ㅉ',
        'T': 'ㅆ'
    })
    
    # 2. 모음 집합
    vowels = set([
        'ㅏ','ㅐ','ㅑ','ㅒ','ㅓ','ㅔ','ㅕ','ㅖ',
        'ㅗ','ㅘ','ㅙ','ㅚ','ㅛ','ㅜ','ㅝ','ㅞ','ㅟ',
        'ㅠ','ㅡ','ㅢ','ㅣ'
    ])
    
    # 3. 복합 중성 결합 규칙: (기존 중성, 새 모음) → 복합중성
    compound_vowels = {
       ('ㅗ', 'ㅏ'): 'ㅘ',
       ('ㅗ', 'ㅐ'): 'ㅙ',
       ('ㅗ', 'ㅣ'): 'ㅚ',
       ('ㅜ', 'ㅓ'): 'ㅝ',
       ('ㅜ', 'ㅔ'): 'ㅞ',
       ('ㅜ', 'ㅣ'): 'ㅟ',
       ('ㅡ', 'ㅣ'): 'ㅢ'
    }
    
    # 4. 복합 종성 결합 규칙: (기존 종성, 새 자음) → 복합종성
    compound_finals = {
       ('ㄱ', 'ㅅ'): 'ㄳ',
       ('ㄴ', 'ㅈ'): 'ㄵ',
       ('ㄴ', 'ㅎ'): 'ㄶ',
       ('ㄹ', 'ㄱ'): 'ㄺ',
       ('ㄹ', 'ㅁ'): 'ㄻ',
       ('ㄹ', 'ㅂ'): 'ㄼ',
       ('ㄹ', 'ㅅ'): 'ㄽ',
       ('ㄹ', 'ㅌ'): 'ㄾ',
       ('ㄹ', 'ㅍ'): 'ㄿ',
       ('ㄹ', 'ㅎ'): 'ㅀ',
       ('ㅂ', 'ㅅ'): 'ㅄ'
    }
    # 복합 종성 분리 규칙 (분리 시 사용)
    compound_final_split = {
       'ㄳ': ('ㄱ', 'ㅅ'),
       'ㄵ': ('ㄴ', 'ㅈ'),
       'ㄶ': ('ㄴ', 'ㅎ'),
       'ㄺ': ('ㄹ', 'ㄱ'),
       'ㄻ': ('ㄹ', 'ㅁ'),
       'ㄼ': ('ㄹ', 'ㅂ'),
       'ㄽ': ('ㄹ', 'ㅅ'),
       'ㄾ': ('ㄹ', 'ㅌ'),
       'ㄿ': ('ㄹ', 'ㅍ'),
       'ㅀ': ('ㄹ', 'ㅎ'),
       'ㅄ': ('ㅂ', 'ㅅ')
    }
    
    result = ""
    current_chosung = None   # 초성
    current_jungsung = None  # 중성
    current_jongsung = None  # 종성

    def flush_syllable():
        """현재 음절을 완성하여 결과 문자열에 추가하고 상태를 초기화한다."""
        nonlocal result, current_chosung, current_jungsung, current_jongsung
        if current_chosung is None:
            return
        # 음절 구성에 따라 결합: 이미 종성이 있는 경우 그대로, 없으면 초성+중성만.
        if current_jungsung is None:
            result += current_chosung
        else:
            if current_jongsung:
                syllable = join_jamos(current_chosung + current_jungsung + current_jongsung)
            else:
                syllable = join_jamos(current_chosung + current_jungsung)
            result += syllable
        current_chosung = None
        current_jungsung = None
        current_jongsung = None

    # 문자열 전체를 인덱스로 순회(lookahead를 위해)
    i = 0
    length = len(text)
    while i < length:
        char = text[i]
        if char in mapping:
            jamo = mapping[char]
        else:
            flush_syllable()
            result += char
            i += 1
            continue

        # 모음 입력 처리
        if jamo in vowels:
            # 만약 아직 초성이 없다면 기본 초성 'ㅇ' 할당
            if current_chosung is None:
                current_chosung = 'ㅇ'
            # 아직 중성이 없다면 바로 설정
            if current_jungsung is None:
                current_jungsung = jamo
            else:
                # 이미 중성이 있는데 새 모음이 들어온 경우
                # 먼저 복합 중성 결합을 시도
                compound = compound_vowels.get((current_jungsung, jamo))
                if compound:
                    current_jungsung = compound
                else:
                    # 모음 입력 시 현재 음절에 종성이 있다면
                    if current_jongsung is not None:
                        # 복합 종성인 경우: 종성을 분리하여 새 음절 초성으로 사용
                        if current_jongsung in compound_final_split:
                            first, second = compound_final_split[current_jongsung]
                            syllable = join_jamos(current_chosung + current_jungsung + first)
                            result += syllable
                            current_chosung = second
                            current_jungsung = jamo
                            current_jongsung = None
                        else:
                            # 단일 종성인 경우: flush할 때 종성은 분리(이전 음절은 초성+중성만)
                            temp = current_jongsung
                            syllable = join_jamos(current_chosung + current_jungsung)
                            result += syllable
                            current_chosung = temp
                            current_jungsung = jamo
                            current_jongsung = None
                    else:
                        # 중성만 있는데 결합할 수 없으면 기존 음절 flush 후 새 음절 시작
                        flush_syllable()
                        current_chosung = 'ㅇ'
                        current_jungsung = jamo
            i += 1
            continue

        # 자음 입력 처리
        else:
            if current_chosung is None:
                current_chosung = jamo
            elif current_jungsung is None:
                # 초성만 있는데 자음 입력이 들어오면 기존 자음을 flush하고 새 음절 초성으로 사용
                flush_syllable()
                current_chosung = jamo
            else:
                # 이미 초성과 중성이 존재하는 경우
                # lookahead: 다음 입력이 존재하며 모음이면 현재 음절을 flush하고 이번 자음을 새 음절 초성으로 사용
                if (i + 1 < length) and (text[i + 1] in mapping) and (mapping[text[i + 1]] in vowels):
                    # flush 시 현재 음절은 초성+중성(+종성이 있다면 그대로)
                    if current_jongsung is None:
                        syllable = join_jamos(current_chosung + current_jungsung)
                    else:
                        syllable = join_jamos(current_chosung + current_jungsung + current_jongsung)
                    result += syllable
                    current_chosung = jamo
                    current_jungsung = None
                    current_jongsung = None
                else:
                    # 다음 입력이 없거나 자음이면 종성으로 추가
                    if current_jongsung is None:
                        current_jongsung = jamo
                    else:
                        compound = compound_finals.get((current_jongsung, jamo))
                        if compound:
                            current_jongsung = compound
                        else:
                            flush_syllable()
                            current_chosung = jamo
            i += 1
            continue

    flush_syllable()
    return result

# 예시 실행
if __name__ == "__main__":
    while(1):
        test_input = input("입력 : ")
        print("출력 : ", convert_mistyped_korean(test_input))