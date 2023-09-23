from BaselineSummariser import TextScrapper, TextProcessor

# text = """Peter and Elizabeth took a taxi to attend the night party in the city. While in the party, Elizabeth
# collapsed and was rushed to the hospital. Since she was diagnosed with a brain injury, the doctor told Peter to stay
# besides her until she gets well. Therefore, Peter stayed with her at the hospital for 3 days without leaving."""


ts = TextScrapper(url='https://en.wikipedia.org/wiki/20th_century')
ts.fetch_data()
text = ts.get_content()

tp = TextProcessor(ip_text=text)
tp.calc_freq_table()
tp.calc_sentence_score()
average_score = tp.get_average_score()
summary = tp.get_summary(threshold=average_score)

print('SUMMARY')
print(summary)
