from Summariser import WebScrapper, TextProcessor, PDFScrapper
from Summariser import ChatGPTSummariser

# ABSTRACTIVE SUMMARISER
filename = 'trial'
ps = PDFScrapper(filename=filename)

pn, pm = 3, 7
ps.get_text_from_pages(pn, pm)

ps.filename = f'{filename}-{pn}_{pm}'
text = ps.clean_text()
ps.store_text(text)

chat_gpt_summariser = ChatGPTSummariser(prompt="Summarise the following text:",
                                        text=text)
response = chat_gpt_summariser.get_response()
print(response)


# EXTRACTIVE SUMMARISER
"""
ts = WebScrapper(url='https://en.wikipedia.org/wiki/20th_century')
ts.fetch_data()
text = ts.get_content()

tp = TextProcessor(ip_text=text)
tp.calc_freq_table()
tp.calc_sentence_score()
average_score = tp.get_average_score()
summary = tp.get_summary(threshold=average_score)

print(summary)
"""