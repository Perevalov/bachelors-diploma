import ngram,os
from Analyzing import TextAnalyzer


def get_best_frame(question,frames):
    probas = []
    for f in frames:
        s = TextAnalyzer.prepare_text(str(f)).split()
        s=[' '.join(x) for x in list(zip(s,s[1:],s[2:]))]
        G = ngram.NGram(s)
        try:
            probas.append(G.search(question)[0][1])
        except Exception:
            probas.append(0)
    max_index = probas.index(max(probas))
    return frames[max_index]

def speak(text):
    os.system("echo "" " + text + " "" | RHVoice-test -p Irina")