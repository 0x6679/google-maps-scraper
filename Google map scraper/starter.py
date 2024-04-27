from scraper.scraper import Backend

places = [
    "Budapest I. kerület", "Budapest II. kerület", "Budapest III. kerület", "Budapest IV. kerület",
    "Budapest V. kerület", "Budapest VI. kerület", "Budapest VII. kerület", "Budapest VIII. kerület",
    "Budapest IX. kerület", "Budapest X. kerület", "Budapest XI. kerület", "Budapest XII. kerület",
    "Budapest XIII. kerület", "Budapest XIV. kerület", "Budapest XV. kerület", "Budapest XVI. kerület",
    "Budapest XVII. kerület", "Budapest XVIII. kerület", "Budapest XIX. kerület", "Budapest XX. kerület",
    "Budapest XXI. kerület", "Budapest XXII. kerület", "Budapest XXIII.", "Gyál", "Nyergesújfalu",
    "Bácsalmás", "Ráckeve", "Tiszaföldvár", "Veresegyház", "Szentlőrinc", "Dunavarsány", "Berettyószentmárton",
    "Kál", "Dány", "Jánoshalma", "Nyárlőrinc", "Lipót", "Piliscsaba", "Rákospalota", "Hajdúszoboszló", "Polgár",
    "Nagymaros", "Hajdúhadház", "Újfehértó", "Békéscsaba Görbehalom", "Sándorfalva", "Kistelek", "Székkutas",
    "Battonya", "Devecser", "Zsámbék", "Tamási", "Dunaharaszti", "Isaszeg", "Mindszent", "Üllő", "Pilis", "Diósd",
    "Kerepes", "Sárbogárd", "Vámosgyörk", "Dunaszeg", "Gödörháza", "Csopak", "Zebegény", "Szob", "Kenderes",
    "Nagycenk", "Szegvár", "Dunabogdány", "Fülöpszállás", "Lajosmizse", "Hernádkak", "Hódmezővásárhely-Kishomok",
    "Maglód", "Kerekegyháza", "Jászszentandrás", "Ócsa", "Szada", "Szalkszentmárton", "Dunaszentgyörgy", "Újszilvás", 
    "Budapest", "Debrecen", "Szeged", "Miskolc", "Pécs", "Győr", "Nyíregyháza", "Kecskemét", "Székesfehérvár",
    "Szombathely", "Szolnok", "Tatabánya", "Kaposvár", "Érd", "Veszprém", "Békéscsaba", "Zalaegerszeg", "Sopron",
    "Eger", "Nagykanizsa", "Dunaújváros", "Hódmezővásárhely", "Salgótarján", "Cegléd", "Ózd", "Baja", "Vác",
    "Szekszárd", "Pápa", "Gyöngyös", "Kazincbarcika", "Gödöllő", "Gyula", "Hajdúböszörmény", "Kiskunfélegyháza",
    "Ajka", "Orosháza", "Szentes", "Dunakeszi", "Kiskunhalas", "Esztergom", "Jászberény", "Komló", "Nagyatád",
    "Mosonmagyaróvár", "Dombóvár", "Budaörs", "Paks", "Szigetszentmiklós", "Tata", "Sellye", "Siófok", "Törökszentmiklós",
    "Hatvan", "Karcag", "Gyomaendrőd", "Keszthely", "Várpalota", "Békés", "Heves", "Balassagyarmat", "Tiszaújváros",
    "Beled", "Szentendre", "Hévíz", "Szentgotthárd", "Pécsvárad", "Százhalombatta", "Füzesabony", "Mohács", "Mezőkövesd",
    "Kisvárda", "Göd", "Szarvas", "Sátoraljaújhely", "Pomáz", "Tokaj", "Balmazújváros", "Kisújszállás", "Oroszlány",
    "Komárom", "Mátészalka", "Kalocsa", "Kiskőrös", "Nyírbátor", "Tiszaalpár", "Berettyóújfalu", "Makó", "Sajószentpéter",
    "Encs", "Csorna", "Bonyhád", "Lenti", "Fehérgyarmat", "Pásztó", "Mezőtúr", "Csákvár", "Kunszentmárton", "Bátaszék",
    "Szerencs", "Csongrád", "Nagykőrös", "Vecsés", "Bicske", "Tiszafüred", "Szeghalom", "Abony", "Bátonyterenye",
    "Gönc", "Monor", "Albertirsa", "Géderlak", "Barcs", "Tiszakécske", "Jászapáti", "Mezőberény", "Balatonfüred",
    "Fót", "Tapolca", "Biatorbágy", "Tiszavasvári", "Kemecse", "Pilisvörösvár", "Tura", "Kőszeg"   
    
]

def run_scraper(search_query, output_format, headless_mode):
    """ Run the scraper for a single query. """
    def show_message(value=None, **kwargs):
        print("Message from scraper:", value)

    backend = Backend(
        searchquery=search_query,
        outputformat=output_format,
        messageshowingfunc=show_message,
        healdessmode=headless_mode
    )
    backend.mainscraping()

def main(query, output_format, headless_mode):
    queries = [str(query+' '+place) for place in places]

    for query in queries:
        print(f"Starting scrape for query: {query}")
        run_scraper(query, output_format, headless_mode)

    print("All queries processed successfully.")

if __name__ == "__main__":

    query = input('qurery keyword: ')
    
    output_format = 'csv'
    headless_mode = 1 

    main(query, output_format, headless_mode)