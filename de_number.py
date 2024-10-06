import os
current_dir = os.path.dirname(__file__)
final_path = os.path.join(current_dir, 'multi.txt')
def number_to_german(n):

    units = ["null", "eins", "zwei", "drei", "vier", "fünf",
             "sechs", "sieben", "acht", "neun"]
    teens = ["zehn", "elf", "zwölf", "dreizehn", "vierzehn",
             "fünfzehn", "sechzehn", "siebzehn", "achtzehn", "neunzehn"]
    tens = ["", "", "zwanzig", "dreißig", "vierzig", "fünfzig",
            "sechzig", "siebzig", "achtzig", "neunzig"]

    if n < 0 or n > 1_000_000_000_000:
        return "Zahl außerhalb des unterstützten Bereichs."

    if n == 0:
        return units[0]

    result = []
    chunks = []
    while n > 0:
        chunks.append(n % 1000)
        n = n // 1000

    for i in range(len(chunks)-1, -1, -1):
        chunk = chunks[i]
        if chunk == 0:
            continue
        if i == 1:  # Tausender
            if chunk == 1:
                result.append("tausend")
            else:
                result.append(number_to_chunk(chunk) + "tausend")
        elif i == 2:  # Millionen
            if chunk == 1:
                result.append("eine Million")
            else:
                result.append(number_to_chunk(chunk) + " Millionen")
        elif i == 3:  # Milliarden
            if chunk == 1:
                result.append("eine Milliarde")
            else:
                result.append(number_to_chunk(chunk) + " Milliarden")
        elif i == 4:  # Billionen
            if chunk == 1:
                result.append("eine Billion")
            else:
                result.append(number_to_chunk(chunk) + " Billionen")
        else:
            result.append(number_to_chunk(chunk))

    return ' '.join(result)

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

def phone_number_to_german(number):

    def read_pairs(nums):
        pairs = []
        i = 0
        # 两两分组，最后可能剩下一个
        while i < len(nums) - 1:
            pairs.append(nums[i:i+2])
            i += 2
        if i < len(nums):  # 如果还有剩下的一个数字
            pairs.append(nums[i])
        return pairs
    read_pairs_result = read_pairs(number)
    results = []
    for pair in read_pairs_result:
        pa = number_to_chunk(int(pair))
        results.append(pa)

    return ' '.join(results)
    
def date_to_german(date_str):
    """
    优化处理日期。假设输入格式为 DD.MM.YYYY
    """
    parts = date_str.split('.')
    if len(parts) !=3:
        return "日期格式错误，应为DD.MM.YYYY"

    day, month, year = parts
    day = int(day)
    month = int(month)
    year = int(year)

    # 将1-31转换为德文
    day_german = number_to_german(day)
    # 月份
    months = ["Januar", "Februar", "März", "April", "Mai", "Juni",
              "Juli", "August", "September", "Oktober", "November", "Dezember"]
    if 1 <= month <=12:
        month_german = months[month-1]
    else:
        month_german = "Ungültiger Monat"

    # 年份，可以分为两部分
    year_german = number_to_german(year)

    return f"{day_german}. {month_german} {year_german}"

def other_long_number_to_german(number, type_desc=""):
    """
    处理其他类型的长串数字，如邮政编码、身份证号等。
    默认按每两个数字一组读。
    """
    def read_pairs(nums):
        pairs = [nums[i:i+2] for i in range(0, len(nums), 2)]
        return ' '.join([number_to_german(int(pair)) for pair in pairs])

    def read_digits(nums):
        units = ["null", "eins", "zwei", "drei", "vier", "fünf",
                 "sechs", "sieben", "acht", "neun"]
        return ' '.join([units[int(d)] for d in nums])

    # 这里可以根据type_desc进行不同的处理
    # 目前默认每两个数字一组
    return read_pairs(number)

'''def main():

    print("Bitte wählen Sie den Typ der Zahl, die verarbeitet werden soll:")
    print("1. Normale Zahl")
    print("2. Telefonnummer")
    print("3. Datum")
    print("4. Andere lange Zahlen (z.B. Postleitzahl, Personalausweisnummer)")

    choice = input("Geben Sie die Nummer des Typs ein (1/2/3/4): ")

    if choice == '1':
        number = input("Bitte geben Sie die Zahl ein (0 bis 1.000.000.000): ")
        if not number.isdigit():
            print("Ungültige Eingabe. Bitte geben Sie nur Ziffern ein.")
            return
        num = int(number)
        german_number = number_to_german(num)
        print(f"Die deutsche Zahl ist: {german_number}")

    elif choice == '2':
        number = input("Bitte geben Sie die Telefonnummer ein (nur Ziffern): ")
        if not number.isdigit():
            print("Ungültige Eingabe. Bitte geben Sie nur Ziffern ein.")
            return
        german_phone = phone_number_to_german(number)
        print(f"Die Telefonnummer auf Deutsch: {german_phone}")

    elif choice == '3':
        date_str = input("Bitte geben Sie das Datum ein (TT.MM.JJJJ): ")
        german_date = date_to_german(date_str)
        print(f"Das Datum auf Deutsch: {german_date}")

    elif choice == '4':
        number = input("Bitte geben Sie die lange Zahl ein (nur Ziffern): ")
        if not number.isdigit():
            print("Ungültige Eingabe. Bitte geben Sie nur Ziffern ein.")
            return
        type_desc = input("Bitte geben Sie eine Beschreibung des Zahlentyps ein (optional): ")
        german_other = other_long_number_to_german(number, type_desc)
        print(f"Die Zahl auf Deutsch: {german_other}")

    else:
        print("Ungültige Auswahl. Bitte starten Sie das Programm erneut und wählen Sie eine gültige Option.")

if __name__ == "__main__":
    main()
'''
def real_main():
    with open(final_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            ein_line = []
            line = line.split()
            for i in line:
                ein_line.append(number_to_german(int(i)))
            print(', '.join(str(num) for num in ein_line))
real_main()