import random
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
multi_path = os.path.join(current_dir, "multi.txt")
def number_to_chunk(num):
    """
    将小于1000的数字转换为德文数字词。
    """
    units = ["null", "ein", "zwei", "drei", "vier", "fünf",
             "sechs", "sieben", "acht", "neun"]
    teens = ["zehn", "elf", "zwölf", "dreizehn", "vierzehn",
             "fünfzehn", "sechzehn", "siebzehn", "achtzehn", "neunzehn"]
    tens = ["", "", "zwanzig", "dreißig", "vierzig", "fünfzig",
            "sechzig", "siebzig", "achtzig", "neunzig"]

    result = ""

    if num >= 100:
        if num // 100 == 1:
            result += "einhundert"
        else:
            result += units[num // 100] + "hundert"
        num = num % 100

    if num >= 20:
        if num % 10 != 0:
            if num % 10 == 1:
                result += "einund" + tens[num // 10]
            else:
                result += units[num % 10] + "und" + tens[num // 10]
        else:
            result += tens[num // 10]
    elif num >= 10:
        result += teens[num - 10]
    elif num == 1:
        result += "eins"
    elif num > 0:
        result += units[num]

    return result

def generate_random_times():
    times = []
    for _ in range(12):
        hour = random.randint(0, 224)
        minute = random.randint(0, 59)
        if hour == 0 and minute == 0:
            informal = "Mitternacht"
            formal = "null Uhr"
        elif hour == 12 and minute == 0:
            informal = "Mittag"
            formal = "zwölf Uhr"
        elif hour < 12 or hour == 24:
            if hour == 0 or hour == 24:
                informal = f"{number_to_chunk(minute)} Minuten nach Mitternacht"
                formal = f"null Uhr {number_to_chunk(minute)}"
            elif hour == 1 and minute == 0:
                informal = "ein Uhr morgens"
                formal = "ein Uhr"
            elif minute == 15:
                informal = f"Viertel nach {number_to_chunk(hour)} morgens"
                formal = f"{number_to_chunk(hour)} Uhr fünfzehn"
            elif minute == 30:
                informal = f"halb {number_to_chunk(hour + 1)} morgens"
                formal = f"{number_to_chunk(hour)} Uhr dreißig"
            elif minute == 45:
                informal = f"Viertel vor {number_to_chunk(hour + 1)} morgens"
                formal = f"{number_to_chunk(hour)} Uhr fünfundvierzig"
            else:
                if minute < 30:
                    informal = f"{number_to_chunk(minute)} Minuten nach {number_to_chunk(hour)} morgens"
                    formal = f"{number_to_chunk(hour)} Uhr {number_to_chunk(minute)}"
                elif minute > 30:
                    informal = f"{number_to_chunk(60 - minute)} Minuten vor {number_to_chunk(hour + 1)} abends"
                    formal = f"{number_to_chunk(hour)} Uhr {number_to_chunk(minute)}"
        elif 12 <= hour < 17:
            if minute == 0:
                informal = f"{number_to_chunk(hour % 12 if hour != 12 else 12)} Uhr mittags"
                formal = f"{number_to_chunk(hour)} Uhr"
            elif minute == 15:
                informal = f"Viertel nach {number_to_chunk(hour % 12 if hour != 12 else 12)} nachmittags"
                formal = f"{number_to_chunk(hour)} Uhr fünfzehn"
            elif minute == 30:
                informal = f"halb {number_to_chunk((hour % 12) + 1 if hour != 11 else 1)} nachmittags"
                formal = f"{number_to_chunk(hour)} Uhr dreißig"
            elif minute == 45:
                informal = f"Viertel vor {number_to_chunk((hour % 12) + 1 if hour != 11 else 1)} nachmittags"
                formal = f"{number_to_chunk(hour)} Uhr fünfundvierzig"
            else:
                if minute < 30:
                    informal = f"{number_to_chunk(minute)} Minuten nach {number_to_chunk(hour % 12 if hour != 12 else 12)} nachmittags"
                    formal = f"{number_to_chunk(hour)} Uhr {number_to_chunk(minute)}"
                elif minute > 30:
                    informal = f"{number_to_chunk(60 - minute)} Minuten vor {number_to_chunk((hour % 12) + 1 if hour != 11 else 1)} abends"
                    formal = f"{number_to_chunk(hour)} Uhr {number_to_chunk(minute)}"
        else:
            if minute == 0:
                informal = f"{number_to_chunk(hour % 12 if hour != 12 else 12)} Uhr abends"
                formal = f"{number_to_chunk(hour)} Uhr"
            elif minute == 15:
                informal = f"Viertel nach {number_to_chunk(hour % 12 if hour != 12 else 12)} abends"
                formal = f"{number_to_chunk(hour)} Uhr fünfzehn"
            elif minute == 30:
                informal = f"halb {number_to_chunk((hour % 12) + 1 if hour != 11 else 1)} abends"
                formal = f"{number_to_chunk(hour)} Uhr dreißig"
            elif minute == 45:
                informal = f"Viertel vor {number_to_chunk((hour % 12) + 1 if hour != 11 else 1)} abends"
                formal = f"{number_to_chunk(hour)} Uhr fünfundvierzig"
            else:
                if minute < 30:
                    informal = f"{number_to_chunk(minute)} Minuten nach {number_to_chunk(hour % 12 if hour != 12 else 12)} abends"
                    formal = f"{number_to_chunk(hour)} Uhr {number_to_chunk(minute)}"
                elif minute > 30:
                    informal = f"{number_to_chunk(60 - minute)} Minuten vor {number_to_chunk((hour % 12) + 1 if hour != 11 else 1)} morgens"
                    formal = f"{number_to_chunk(hour)} Uhr {number_to_chunk(minute)}"
        
        times.append(f"{informal}; {formal}")
    
    with open(multi_path, 'w',encoding= 'utf-8') as file:
        for i, time in enumerate(times, start=1):
            file.write(f"{random.randint(1, 6)} {time}\n")

def ask_user_for_time():
    random_time = random.choice(generate_random_times_for_quiz())
    print(f"Bitte geben Sie die richtige Zeit ein für: {random_time['description']} (in Worten)")
    user_input = input("Ihre Antwort: ")
    if user_input.lower().replace("uhr", "Uhr") == random_time['formal'].lower().replace("uhr", "Uhr") or user_input.lower().replace("uhr", "Uhr") == random_time['informal'].lower().replace("uhr", "Uhr"):
        print("Richtig!")
    else:
        print(f"Falsch. Die richtige Antwort ist: {random_time['formal']} oder {random_time['informal']}")

def generate_random_times_for_quiz():
    times = []
    for _ in range(12):
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        description = f"{hour:02d}:{minute:02d}"
        
        if hour < 12:
            if minute == 0:
                informal = f"{number_to_chunk(hour)} Uhr morgens"
                formal = f"{number_to_chunk(hour)} Uhr"
            elif minute == 15:
                informal = f"Viertel nach {number_to_chunk(hour)}"
                formal = f"{number_to_chunk(hour)} Uhr fünfzehn"
            elif minute == 30:
                informal = f"halb {number_to_chunk(hour + 1)}"
                formal = f"{number_to_chunk(hour)} Uhr dreißig"
            elif minute == 45:
                informal = f"Viertel vor {number_to_chunk(hour + 1)}"
                formal = f"{number_to_chunk(hour)} Uhr fünfundvierzig"
            else:
                informal = f"{number_to_chunk(minute)} Minuten nach {number_to_chunk(hour)}"
                formal = f"{number_to_chunk(hour)} Uhr {number_to_chunk(minute)}"
        else:
            if minute == 0:
                informal = f"{number_to_chunk(hour % 12 if hour != 12 else 12)} Uhr nachmittags"
                formal = f"{number_to_chunk(hour)} Uhr"
            elif minute == 15:
                informal = f"Viertel nach {number_to_chunk(hour % 12 if hour != 12 else 12)}"
                formal = f"{number_to_chunk(hour)} Uhr fünfzehn"
            elif minute == 30:
                informal = f"halb {number_to_chunk((hour % 12) + 1 if hour != 11 else 1)}"
                formal = f"{number_to_chunk(hour)} Uhr dreißig"
            elif minute == 45:
                informal = f"Viertel vor {number_to_chunk((hour % 12) + 1 if hour != 11 else 1)}"
                formal = f"{number_to_chunk(hour)} Uhr fünfundvierzig"
            else:
                informal = f"{number_to_chunk(minute)} Minuten nach {number_to_chunk(hour % 12 if hour != 12 else 12)}"
                formal = f"{number_to_chunk(hour)} Uhr {number_to_chunk(minute)}"
        
        times.append({
            'description': description,
            'informal': informal,
            'formal': formal
        })
    return times

# Example usage
generate_random_times()
#ask_user_for_time()
