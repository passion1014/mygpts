@app.get("/finstate_summary")
def finstate_summary(code: str):
    # Read encparam
    url = 'https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd=005930'
    html_text = requests.get(url).text

    if not re.search("encparam: '(.*?)'", html_text):
        print('encparam not found') # Return None if encparam is not found
        return None
    encparam = re.findall ("encparam: '(.*?)'", html_text)[0]

    url = f'https://navercomp.wisereport.co.kr/v2/company/ajax/cF1001.aspx?cmp_cd={code}&fin_typ={fin_type}&freq_typ={freq}&encparam={encparam}'
    r = requests.get(url, headers={'Referer': url})
    df_list = pd.read_html(io.StringIO(r.text), encoding='euc-kr')
    df = df_list[1]
    df.columns = [col[1] for col in df.columns]
    df.set_index('주요재무정보', inplace=True)
    df.columns = [re.sub('[^\\.\\d]', '', col) for col in df.columns]
    df.columns = [pd.to_datetime(col, format='%Y%m', errors='coerce') for col in df.columns]
    df = df.transpose()
    df.index.name = '날짜'
    return {df.to_csv()} ## Return CSV strin
