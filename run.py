import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests, lxml
from wordcloud import WordCloud

fontpath='C:/Windows/Fonts/NotoSansMonoCJKkr-Regular.otf'
tdata = ''

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}

name = input('갤러리 입력:')
keyword = input('검색어 입력(*=전체):')
page = int(input('조회 페이지 범위 입력(최소 1 이상):'))
dtype = input('수집 항목 [title:제목(기본값), nick:닉네임]:')

print('갤러리 검색중...')
r = requests.get('https://search.dcinside.com/gallery/q/' + name, headers = headers).text

if 'integrate_cont_list' in r:

    bs = BeautifulSoup(r, 'lxml')
    link = bs.find('ul', class_='integrate_cont_list').a['href']

    r = requests.get(link, headers = headers).text

    print('갤러리 형식:', end=' ')
    #마이너 갤러리일 경우
    if 'location.replace' in r:
        link = link.replace('board/','mgallery/board/')
        
        print('마이너')
    else:
        print('정식')

    print('값 읽어내는 중...')

    for i in range(1, page + 1):

        print(i,'번째 페이지 읽는 중...')
        r = requests.get(link + '&page=' + str(i), headers = headers).text
        
        bs = BeautifulSoup(r, 'lxml')

        if dtype == 'nick':
            tmp1 = bs.find_all('td', class_='gall_tit ub-word')
            tmp2 = bs.find_all("td", {"class", "gall_writer ub-writer"})

            post_data = zip(tmp1, tmp2)
            
            for s in post_data:
                 if str(s[0]).find('<b>')==-1 and s[1]['data-nick'].strip() != 'ㅇㅇ': tdata += s[1]['data-nick'].strip() + '\n'
        else:
            tmp1 = bs.find_all('td', class_='gall_tit ub-word')
            tmp2 = bs.find_all('td', class_='gall_num')

            post_data = zip(tmp1, tmp2)

            for s in post_data:
                if str(s[0]).find('<b>')==-1 and ((keyword in s[0].find('a').text) or keyword=='*'):
                    #print(s[1].text + '\t' + s[0].find('a').text)
                    tdata += s[0].find('a').text + '\n'

    #open('result.txt', 'w').write(tdata)
    print('워드클라우드 생성 중...')
    wordcloud = WordCloud(font_path=fontpath, width=1280, height=720, background_color='white').generate(tdata)

    plt.figure(figsize=(12,12))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
    
else:
    print('해당 명칭의 갤러리가 없습니다.')



