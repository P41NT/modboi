import re
import urllib.request
import time

length = len(open("memes.txt", "r").read().split("\n"))
url = f"https://old.reddit.com/r/Memes_Of_The_Dank/?count={length}"
i = 0
memes = []
f = open("memes.txt", "a")
while i < 20:
  reddit_page = urllib.request.urlopen(url)
  htmltext = reddit_page.read().decode('utf-8')
  content = htmltext
  these_regex = "data-url=\"(.+?)\""
  pattern = re.compile(these_regex)
  all_urls = re.findall(pattern,htmltext)
  next_button = "next-button.+?\"(.+?)\""
  pattern_next = re.compile(next_button)
  next_page = re.findall(pattern_next,htmltext)
  for meme in all_urls:
    memes.append(meme)
  url = next_page[0]
  i += 1
  time.sleep(5)

for meme in memes:
  f.write(meme + "\n")

f.close()