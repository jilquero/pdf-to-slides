import typer
import tempfile
import spacy
from collections import Counter
from heapq import nlargest
import en_core_web_sm  # noqa: F401
import xx_sent_ud_sm
import pytextrank  # noqa: F401

from typing import Optional
from typing_extensions import Annotated
from .converters import pdf_to_markdown
from .converters import markdown_to_json

app = typer.Typer()


@app.callback()
def callback():
    """
    Pdf and markdown to slides converter
    """


@app.command()
def md(
    filename: Annotated[str, typer.Argument(help="PDF file to parse")],
    output: Annotated[str, typer.Argument(help="Output base folder path")] = "output",
    langs: Annotated[
        Optional[str], typer.Option(help="Languages to use for OCR, comma separated")
    ] = None,
    batch_multiplier: Annotated[
        int, typer.Option(help="How much to increase batch sizes")
    ] = 2,
    start_page: Annotated[
        Optional[int], typer.Option(help="Page to start processing at")
    ] = None,
    max_pages: Annotated[
        Optional[int], typer.Option(help="Maximum number of pages to parse")
    ] = None,
):
    """
    Convert pdf to markdown
    """
    langs = langs.split(",") if langs else None
    pdf_to_markdown(filename, output, langs, batch_multiplier, start_page, max_pages)


@app.command()
def json(filename: Annotated[str, typer.Argument(help="Markdown file to parse")]):
    """
    Convert markdown to json
    """
    markdown_to_json(filename)


@app.command()
def pdf_to_json(
    filename: Annotated[str, typer.Argument(help="Markdown file to parse")],
    langs: Annotated[
        Optional[str], typer.Option(help="Languages to use for OCR, comma separated")
    ] = None,
    batch_multiplier: Annotated[
        int, typer.Option(help="How much to increase batch sizes")
    ] = 2,
    start_page: Annotated[
        Optional[int], typer.Option(help="Page to start processing at")
    ] = None,
    max_pages: Annotated[
        Optional[int], typer.Option(help="Maximum number of pages to parse")
    ] = None,
):
    """
    Convert pdf to json
    """
    langs = langs.split(",") if langs else None
    with tempfile.TemporaryDirectory() as tempdir:
        path = pdf_to_markdown(filename, tempdir, langs, batch_multiplier, start_page, max_pages)
        markdown_to_json(f"{path}/{path.split("/")[-1]}.md")


@app.command()
def summarize():
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("textrank")

    example_text = ""

    print('Original Document Size: ', len(example_text))
    doc = nlp(example_text)

    for sent in doc._.textrank.summary():
        print("Summary: ", sent)
        print('Summary Length:', len(sent))


@app.command()
def streszczenie():
    # Wczytanie modelu językowego
    nlp = spacy.load('xx_sent_ud_sm')
    nlp_en = spacy.load('en_core_web_sm')

    # Odczytanie pliku Markdown
    with open('./output/list_motywacyjny_ŁukaszSendecki/list_motywacyjny_ŁukaszSendecki.md', 'r', encoding='utf-8') as file:
        markdown_content = file.read()

    example="""Adolf Hitler  (ur. 20 kwietnia 1889 w Braunau am Inn, zm. 30 kwietnia 1945 w Berlinie) – niemiecki polityk pochodzenia austriackiego, kanclerz Rzeszy od 30 stycznia 1933, Wódz i kanclerz Rzeszy (niem. Der Führer und Reichskanzler) od 2 sierpnia 1934 do śmierci; twórca i dyktator III Rzeszy, przywódca Narodowosocjalistycznej Niemieckiej Partii Robotników (NSDAP), ideolog narodowego socjalizmu; zbrodniarz wojenny, odpowiedzialny za zbrodnie przeciw ludzkości. Uznawany za osobiście odpowiedzialnego za politykę rasową III Rzeszy i śmierć milionów ludzi zabitych podczas jego rządów – w tym – za Holocaust i Porajmos.Urodził się na obszarze ówczesnych Austro-Węgier i wychował się w pobliżu Linzu. W 1913 przeniósł się do Niemiec. W czasie I wojny światowej walczył na froncie zachodnim. W 1919 wstąpił do Niemieckiej Partii Robotników (DAP). W 1923 usiłował przejąć władzę w wyniku nieudanego zamachu stanu w Monachium i został pozbawiony wolności na pięć lat. Tam stworzył pierwszy tom Mein Kampf (Moja walka). W 1924 z pomocą charyzmatycznych przemówień i nazistowskiej propagandy atakował traktat wersalski oraz promował pangermanizm, antysemityzm i antykomunizm. Dzięki temu zyskał powszechne poparcie.W listopadzie 1932 roku partia nazistowska miała najwięcej miejsc w niemieckim Reichstagu, ale nie miała większości. W rezultacie żadna partia nie była w stanie utworzyć większości parlamentarnej popierającej kandydata na kanclerza. Były kanclerz Franz von Papen i inni konserwatywni przywódcy przekonali prezydenta Paula von Hindenburga, by 30 stycznia 1933 mianował Hitlera na stanowisko kanclerza. Wkrótce potem rozpoczął się proces przekształcania Republiki Weimarskiej w III Rzeszę. Dążył do wyeliminowania Żydów z Niemiec i ustanowienia nowego ładu, aby przeciwdziałać temu, co uważał za niesprawiedliwość międzynarodowego porządku zdominowanego przez Wielką Brytanię i Francję po I wojnie światowej. Pierwsze sześć lat jego władzy zaowocowało szybkim ożywieniem gospodarczym po Wielkim kryzysie, zniesieniem ograniczeń nałożonych na Niemcy i aneksją terytoriów zamieszkanych przez miliony Niemców.Poszukiwał Lebensraum (dosł. „przestrzeni życiowej”) dla narodu niemieckiego w Europie Wschodniej. Był ściśle zaangażowany w operacje wojskowe podczas wojny. Prowadzona pod jego przywództwem agresywna polityka zagraniczna oraz atak na Polskę 1 września 1939 roku doprowadziły do rozpoczęcia przez Niemcy II wojny światowej, w wyniku której zginęło ok 50 milionów ludzi. W czerwcu 1941 roku zarządził inwazję na Związek Radziecki. Do końca 1941 roku siły niemieckie i państwa Osi zajęły większość Europy i Afryki Północnej. Po 1941 roku sytuacja ulegała odwróceniu, a w 1945 wojska alianckie pokonały wojska niemieckie. 29 kwietnia 1945 roku poślubił swoją wieloletnią kochankę Evę Braun w bunkrze Führera w Berlinie. Niecałe dwa dni później para popełniła samobójstwo, aby uniknąć schwytania przez sowiecką Armię Czerwoną. Ich zwłoki zostały spalone."""

    # Przetwarzanie tekstu za pomocą spaCy
    doc = nlp(markdown_content) #markdown_content

    # Tokenizacja i filtrowanie
    words = [token.text for token in doc if not token.is_stop and not token.is_punct]
    word_freq = Counter(words)

    # Ważność zdań
    sentence_scores = {}
    for sent in doc.sents:
        for word in sent:
            if word.text in word_freq:
                if sent not in sentence_scores:
                    sentence_scores[sent] = word_freq[word.text]
                else:
                    sentence_scores[sent] += word_freq[word.text]

    # Wybór najważniejszych zdań
    summary_length = 6 # Liczba zdań w streszczeniu
    summary_sentences = nlargest(summary_length, sentence_scores, key=sentence_scores.get)

    # Stworzenie streszczenia
    summary = ' '.join([sent.text for sent in summary_sentences])
    print(summary)
