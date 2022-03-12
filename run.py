from bs4 import BeautifulSoup
import requests
from wordcloud import WordCloud

fontpath = 'font.otf'
title_data = ""

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}

print("디시 워드클라우드 생성기\nBased on https://github.com/pdjdev/dc_wordcloud")

id = input('갤러리 ID 입력:')
url = "https://gall.dcinside.com/"+id
print("갤러리 링크:", url)

keyword = input('검색어 입력:') or '*'
if keyword == '*':
    print("검색어 없음")
else:
    print(keyword, "검색")

start_page = int(input('조회 시작 페이지 입력(최소 1 이상):'))
end_page = int(input('조회 끝 페이지 입력(최소 1 이상):'))
print(start_page, "부터", end_page, "페이지까지 검색")

response = requests.get(url, headers=headers)
if response.status_code == 404:
    ("해당 갤러리가 존재하지 않습니다")
if response.status_code == 200:
    print("해당 갤러리로 리다이렉트 중")
    if "location.replace" in requests.get(response.url, headers=headers).text:
        url = response.url.replace('board/', 'mgallery/board/')
        print("리다이렉트 된 마이너 갤러리 주소:", url)
    else:
        url = response.url
        print("리다이렉트 된 갤러리 주소:", url)

    for i in range(start_page, end_page+1):
        print('페이지 읽는 중... [{}/{}]'.format(i-start_page +
                                           1, 1+end_page-start_page), end='\r')

        r = requests.get(url + '&page=' +
                         str(i), headers=headers)
        bs = BeautifulSoup(r.text, 'lxml')

        title_list = bs.find_all('td', class_='gall_tit ub-word')
        for title in title_list:
            if str(title).find('<b>') == -1 and ((keyword in title.find('a').text) or keyword == '*'):
                title_data += title.find('a').text + '\n'

    print("\n제목 워드클라우드 생성 중")
    wc_title = WordCloud(font_path=fontpath, width=1920, height=1080,
                         background_color='white').generate(title_data)

    print('이미지 저장 중...')
    wc_title.to_file('title.png')

    print('저장 완료')
else:
    print("Unexpected HTTP error")
