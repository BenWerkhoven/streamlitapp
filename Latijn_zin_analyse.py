import streamlit as st
import spacy
import pandas as pd
from cltk import NLP
import stanza

stanza.download('la')

cltk_nlp = NLP(language="lat")

st.set_page_config(page_title="My App",layout='wide')
st.title('Test app')

def maak_omschr(x):
    token = x
    if (str(token.pos) == 'adjective')|(str(token.pos) == 'noun')|(str(token.pos) == 'pronoun')|(str(token.pos) == 'determiner'):
        try:
            naamval = str(token.features["Case"])
            getal = str(token.features["Number"])
            geslacht = str(token.features["Gender"])
            omschr = naamval + ' ' + getal + ' ' + geslacht
            return omschr
        except:
            omschr = 'Afkorting'
    elif (str(token.pos) == 'verb')|(str(token.pos) == 'auxiliary'):
        if str(token.features["VerbForm"]) == '[finite]':
            # VOor een werkwoord in de normale vorm
            wijs = str(token.features["Mood"])
            persoon = str(token.features["Person"])
            getal = str(token.features["Number"])
            tijd = str(token.features["Tense"])
            voice = str(token.features["Voice"])
            
            vorm = str(token.features["VerbForm"])
            omschr = wijs + ' ' + tijd + ' ' + persoon + ' ' + 'persoon ' + getal + ' ' + voice + vorm
        elif str(token.features["VerbForm"]) == '[infinitive]':
            #Voor een infinitief
            aspect = str(token.features["Aspect"])
            tijd = str(token.features["Tense"])
            voice = str(token.features["Voice"])
            vorm = str(token.features["VerbForm"])
            omschr = aspect + ' ' + tijd + ' ' + vorm + ' ' + voice        
        elif (str(token.features["VerbForm"]) == '[gerundive]')|(str(token.features["VerbForm"]) == '[participle]'):
                vorm = str(token.features["VerbForm"])
                naamval = str(token.features["Case"])
                getal = str(token.features["Number"])
                geslacht = str(token.features["Gender"])
                omschr = vorm + ' ' + naamval + ' ' + getal + ' ' + geslacht
        elif (str(token.features["VerbForm"]) == '[gerund]'):
                vorm = str(token.features["VerbForm"])
                naamval = str(token.features["Case"])
                getal = str(token.features["Number"])
                #geslacht = str(token.features["Gender"])
                omschr = vorm + ' ' + naamval + ' ' + getal #+ ' ' + geslacht
        else:
            omschr = 'Niet gevonden: ' + str(token.features)
        return omschr

def governor(x):
    if x == -1:
        return ''
    else:
        return sent_to_analyse[x].string
    
# Normaal gesproken runs streamlit de hele code bij elke klik van de gebruiker.
# Een form maakt een kleine omgeving waar de gebruiker aanpassingen kan doen (input kan leveren) zonder dat de hele script loopt, tot dat op de knop gedrukt wordt. Dit is essentieel als de script lang duurt
form1 = st.sidebar.form(key = 'Opties')
form1.header('Zin om te analyseren')

text_input = form1.text_area('Plak hier je tekst:', 'Gallia est omnis divisa in partes tres.')
form1.form_submit_button('Klik hier!')

doc = cltk_nlp.analyze(text=text_input)
sent_to_analyse = doc.sentences[0]
woorden = [token for token in doc if str(token.pos) not in ['punctuation']]
df = pd.DataFrame([woord.string for woord in woorden])


#a_word_concurrunt = sent_to_analyse[0]

df['pos'] = [str(token.pos) for token in woorden]
df['Lemma'] = [token.lemma for token in woorden]
df['Omschrijving'] = [maak_omschr(token) for token in woorden]
df['Govern'] = [token.governor for token in woorden]
df['Hoort bij'] = df['Govern'].apply(governor)

#df['Definitie'] = [token.definition.split(':')[0] for token in doc]

#st.write(doc.sentences_tokens[0][0])
#st.write([str(sent_to_analyse[0].pos), sent_to_analyse[0].string])
df = df.rename(columns = {0:'Woord'})
st.write(text_input)
st.table(df[['Woord','Lemma','Omschrijving', 'pos','Hoort bij']].T)

