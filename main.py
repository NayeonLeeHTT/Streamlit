import streamlit as st
import numpy as np
import pandas as pd 
import cx_Oracle
import datetime
# import _auth_config as auth
username = 'matuser'
password = 'aF3HQaZp5I'
host = '202.31.33.153'
port = '1521'
servicename = 'DHQPPLM'

# # 오라클 DB 접속
pd.set_option('mode.chained_assignment',  None)
# if 'DBconnect_flag' not in st.session_state:
#     st.session_state.DBconnect_flag = 0
try:
    cx_Oracle.init_oracle_client(lib_dir='C:/Users/HANTA/Desktop/Program/instantclient-basic-windows.x64-21.13.0.0.0dbru/instantclient_21_13') # DPI-1047: cannot locate a 64-bit oracle client library
    # https://somjang.tistory.com/entry/Python-sqlalchemy-cxOracle-%ED%99%9C%EC%9A%A9%ED%95%98%EC%97%AC-Oracle-DB-%EC%97%B0%EA%B2%B0-%EC%8B%9C-%EB%B0%9C%EC%83%9D%ED%95%98%EB%8A%94-sqlalchemyexcDatabaseError-cxOracleDatabaseError-DPI-1047-Cannot-locate-a-64-bit-Oracle-Client-library-%ED%95%B4%EA%B2%B0-%EB%B0%A9%EB%B2%95
    credentials = f"{username}/{password}@{host}:{port}/{servicename}/"
    connection = cx_Oracle.connect(credentials, encoding="UTF-8", nencoding="UTF-8")
    table_name='LNY_TCR'
except:
    credentials = f"{username}/{password}@{host}:{port}/{servicename}/"
    connection = cx_Oracle.connect(credentials, encoding="UTF-8", nencoding="UTF-8")
    table_name='LNY_TCR'


st.title('TCR Ver3 Demo')

# if 'Series_input' not in st.session_state:
#     st.session_state.Series_input=pd.DataFrame(columns=[
#                 'USER_ID','YEAR','COMMODITY','OLD_NEW','COMMETS','ITEM','AREA','TCR_START_YYYYMM',
#                 'COMPOUND_NAME_AS_IS','REVISION_AS_IS','COMPOUND_NAME_TO_BE','REVISION_TO_BE',
#                 'PJT_NAME','PJT_MANAGER','APP_NO_OF_MTH_PLN','SCR_UNIT_PRICE_PLAN','QTY_PLAN',
#                 'SCR_GUBUN','SCR_GUBUN_VALUE','ACT_GUBUN','ACT_GUBUN_VALUE'])


tab1,tab2,tab3,tab4 = st.tabs(['-- 입력 --','-- View / 수정 --','-- 월별 업데이트 --','-- MASTER --'])

 
with tab1:
    st. subheader("신규 아이템 입력")
    st.code('''
    '입력' 페이지에서는 신규 아이템을 입력할 수 있습니다. 
    
    - 'SETTING_NO', 'ITEM_NO', 'TIMESTAMP', 'OLD_NEW'는 사용자가 입력하지 않고 자동 부여됩니다. 
    - 'APP_NO_OF_MTH_PLN'는 'TCR_START_YYYYMM'에 의해 자동계산됩니다.
    - 'YEAR_MONTH'는 'TCR_START_YYYYMM'부터 'APP_NO_OF_MTH_PLN'만큼 자동으로 생성됩니다.
    - 각 월별 'SCR_GUBUN_VALUE', 'ACT_GUBUN_VALUE'는 초기값 0으로 설정된 후, 
       추후 월별 업데이트 TAB과 MASTER TAB의 REFESH 기능을 통해 업데이트 됩니다.  
            
    <사용법>
    1. 데이터를 각 입력칸에 입력합니다.
    2. '입력 데이터 확인' 버튼을 눌러 입력한 값을 확인합니다.
    3. '제출' 버튼을 눌러 DB에 데이터를 제출합니다.
    4. 제출에 성공한 경우 제출 성공 메세지가 출력됩니다.
    ''')
    

    # 사용자 입력 값
    USER_ID=st.text_input('사번 (8글자)',max_chars=8)
    COMMODITY=st.selectbox('COMMODITY',['Compound','원료','구조'], key="COMMODITY_input")
    COMMETS=st.selectbox('구분',['Blue Tech',"Comp'd Simplification",'배합 Pool제','원가합리화 - Case','원가합리화 - Tread'], key="COMMETS_input")
    ITEM=st.text_input('ITEM명 입력')
    AREA=st.selectbox('공장지',['CP','DP','HP','IP','JP','KP','MP','TP'], key="AREA_input")
    TCR_START_YYYYMM=st.text_input('TCR 적용일자 (YYYYMM)',max_chars=6)
    COMPOUND_NAME_AS_IS=st.text_input('기존 Compound NAME',max_chars=9)
    REVISION_AS_IS=st.text_input('기존 Revision',max_chars=5)
    COMPOUND_NAME_TO_BE=st.text_input('변경 Compound NAME',max_chars=9)
    REVISION_TO_BE=st.text_input('변경 Revision',max_chars=5)
    PJT_NAME=st.selectbox('PJT명',['AS/Winter','Case','TB','CTC재료개발팀'], key="PJT_NAME_input")
    PJT_MANAGER=st.text_input('담당자')
    # APP_NO_OF_MTH_PLN=st.number_input('APP_NO_OF_MTH_PLN', 1, 12) # TCR_START_YYYYMM에 따라 자동 부여
    SCR_UNIT_PRICE_PLAN=st.number_input('예상 금액(월)')
    QTY_PLAN=st.number_input('예상 생산량(월)')
    SCR_GUBUN=st.selectbox('SCR 자동계산 적용 여부',['MES 자동계산 (0)','예상 금액 적용 (1)'], key="SCR_GUBUN_input")
    # SCR_GUBUN_VALUE=st.text_input('직접 입력을 선택한 경우 SCR을 입력해주세요.') # 월별 업데이트 TAB에서 데이터 입력, 기본값 = 0
    ACT_GUBUN=st.selectbox('QTY 자동계산 적용 여부',['MES 자동계산 (0)','예상 생산량 적용 (1)'], key="ACT_GUBUN_input")
    # ACT_GUBUN_VALUE=st.text_input('직접 입력을 선택한 경우 ACT를 입력해주세요.') # 월별 업데이트 TAB에서 데이터 입력, 기본값 = 0

    #사용자 입력 값 수정
    # SCR_GUBUN / ACT_GUBUN를 0,1로 변환
    # SCR_GUBUN_VALUE / ACT_GUBUN_VALUE는 GUBUN=0인 경우 None, GUBUN=1인 경우 PLAN값(SCR_UNIT_PRICE_PLAN,QTY_PLAN), GUBUN=2인 경우 입력값 그대로
    SCR_GUBUN = 0 if SCR_GUBUN == 'MES 자동계산 (0)' else 1 
    ACT_GUBUN= 0 if ACT_GUBUN == 'MES 자동계산 (0)' else 1
    SCR_GUBUN_VALUE, ACT_GUBUN_VALUE = 0.0, 0.0 # 기본값


    # 시스템 계산 값
    TIMESTAMP=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    today=datetime.datetime.now().date()
    OLD_NEW ='NEW' if today.strftime('%Y')==TCR_START_YYYYMM[:4] else 'OLD'
    # ITEM_NO 부여 쿼리
    cursor = connection.cursor()
    cursor.execute(f"SELECT MAX(ITEM_NO) FROM {table_name}")
    result = cursor.fetchone()
    max_value = result[0] if result[0] is not None else 0
    cursor.close()
    ITEM_NO=max_value+1
    # SETTING_NO : Oracle DB의 시퀀스 열로 자동 입력

    if st.button('입력 데이터 확인'):
        YEAR_MONTH = TCR_START_YYYYMM
        APP_NO_OF_MTH_PLN = (12 - int(TCR_START_YYYYMM[-2:]) + 1) if (OLD_NEW=='NEW') else (int(TCR_START_YYYYMM[-2:]) - 1)

        input_list=[USER_ID,ITEM_NO,YEAR_MONTH,TIMESTAMP,COMMODITY,OLD_NEW,COMMETS,ITEM,AREA,TCR_START_YYYYMM,
                COMPOUND_NAME_AS_IS,REVISION_AS_IS,COMPOUND_NAME_TO_BE,REVISION_TO_BE,
                PJT_NAME,PJT_MANAGER,APP_NO_OF_MTH_PLN,SCR_UNIT_PRICE_PLAN,QTY_PLAN,
                SCR_GUBUN,SCR_GUBUN_VALUE,ACT_GUBUN,ACT_GUBUN_VALUE]
        input_col=['USER_ID','ITEM_NO','YEAR_MONTH','TIMESTAMP','COMMODITY','OLD_NEW','COMMETS','ITEM','AREA','TCR_START_YYYYMM',
                'COMPOUND_NAME_AS_IS','REVISION_AS_IS','COMPOUND_NAME_TO_BE','REVISION_TO_BE',
                'PJT_NAME','PJT_MANAGER','APP_NO_OF_MTH_PLN','SCR_UNIT_PRICE_PLAN','QTY_PLAN',
                'SCR_GUBUN','SCR_GUBUN_VALUE','ACT_GUBUN','ACT_GUBUN_VALUE']
        # st.session_state.Series_input=pd.DataFrame([input_list],columns=input_col)
        st.session_state.Series_input=pd.Series(input_list, index=input_col)
        st.dataframe(st.session_state.Series_input)
        # st.table(st.session_state.Series_input)

    if st.button('제출'):
        cursor = connection.cursor()
        df_apply=st.session_state.Series_input.copy()

        # 데이터프레임을 SQL 데이터베이스에 삽입
        # cursor.execute("SELECT setting_no_seq.NEXTVAL FROM DUAL")
        # setting_no_seq_value = cursor.fetchone()[0]
            
        # DateFrame과 DB Table의 column명이 일치하는 경우
        for i in range(df_apply['APP_NO_OF_MTH_PLN']):
            if df_apply['OLD_NEW']=='NEW':
                cursor.execute(f"SELECT TO_CHAR(ADD_MONTHS(TO_DATE({st.session_state.Series_input['YEAR_MONTH']}, 'YYYYMM'), {i}), 'YYYYMM') FROM dual")
                YEAR_MONTH_NEW=cursor.fetchone()[0]
            elif df_apply['OLD_NEW']=='OLD':
                cursor.execute(f"SELECT TO_CHAR(ADD_MONTHS(TO_DATE({datetime.datetime.now().date().strftime('%Y')+'01'}, 'YYYYMM'), {i}), 'YYYYMM') FROM dual")
                YEAR_MONTH_NEW=cursor.fetchone()[0]
            i+=1

            cursor.execute("SELECT setting_no_seq.NEXTVAL FROM DUAL")
            setting_no_seq_value = cursor.fetchone()[0]
            cursor.execute(f"INSERT INTO {table_name}  \
                            (USER_ID,SETTING_NO,ITEM_NO,YEAR_MONTH,TIMESTAMP,COMMODITY,OLD_NEW,COMMETS,ITEM,AREA,TCR_START_YYYYMM, \
                                COMPOUND_NAME_AS_IS,REVISION_AS_IS,COMPOUND_NAME_TO_BE,REVISION_TO_BE, \
                                PJT_NAME,PJT_MANAGER,APP_NO_OF_MTH_PLN,SCR_UNIT_PRICE_PLAN,QTY_PLAN, \
                                SCR_GUBUN,SCR_GUBUN_VALUE,ACT_GUBUN,ACT_GUBUN_VALUE) \
                            VALUES (:1, :2, :3, :4, TO_TIMESTAMP(:5, 'YYYY-MM-DD HH24:MI:SS'), :6, :7, :8, :9, :10, :11, :12, :13, :14, :15, :16, :17, :18, :19, :20, :21, :22, :23, :24 )", \
                        (df_apply['USER_ID'], setting_no_seq_value, df_apply['ITEM_NO'], YEAR_MONTH_NEW, df_apply['TIMESTAMP'], \
                         df_apply['COMMODITY'], df_apply['OLD_NEW'], df_apply['COMMETS'], df_apply['ITEM'], df_apply['AREA'], df_apply['TCR_START_YYYYMM'], \
                         df_apply['COMPOUND_NAME_AS_IS'], df_apply['REVISION_AS_IS'], df_apply['COMPOUND_NAME_TO_BE'], df_apply['REVISION_TO_BE'], \
                         df_apply['PJT_NAME'], df_apply['PJT_MANAGER'], df_apply['APP_NO_OF_MTH_PLN'], df_apply['SCR_UNIT_PRICE_PLAN'], df_apply['QTY_PLAN'], \
                         df_apply['SCR_GUBUN'], df_apply['SCR_GUBUN_VALUE'], df_apply['ACT_GUBUN'], df_apply['ACT_GUBUN_VALUE'])) 
            

        connection.commit()
        cursor.close()
        st.success('성공적으로 제출되었습니다.')
        del st.session_state.Series_input


with tab2:
    st. subheader("데이터 조회")
    st.code('''
    본인의 사번을 입력하면 본인이 입력한 모든 데이터를 확인할 수 있습니다.
    ''')
    input_userId=st.text_input('데이터 조회를 위한 사번(8글자)을 입력하세요.',max_chars=8)
    if st.button('조회'):
        df_userId = pd.DataFrame()
        query = f"SELECT * \
                    FROM {table_name}\
                    WHERE USER_ID= {input_userId}"
        df_userId = pd.read_sql(query, connection)
        st.dataframe(df_userId)

    st.markdown("""---""")
    
    st. subheader("아이템 정보 수정")
    st.code('''
    기존에 입력한 아이템의 정보를 수정할 수 있습니다.
    'TIMESTAMP'도 현재 입력 시간으로 일괄 업데이트 됩니다.
    'USER_ID', 'SETTING_NO', 'ITEM_NO', 'SCR_GUBUN_VALUE', 'ACT_GUBUN_VALUE'를 제외한 데이터를 수정할 수 있습니다.
    'TCR_START_YYYYMM' ('YEAR_MONTH', 'OLD_NEW', 'APP_NO_OF_MTH_PLN') 를 수정하면 DB 데이터의 행 수 자체를 수정해야하기 때문에 해당 페이지에서 수정할 수 없습니다.
            
    <사용법>
    1. 정보를 수정하고 싶은 아이템의 ITEM_NO를 입력하고 '선택' 버튼을 누릅니다.
    2. 현재 저장되어 있는 데이터의 값을 원하는 값으로 수정한 후 '수정 완료' 버튼을 누릅니다.
    3. 수정에 성공한 경우 수정 성공 메세지가 출력됩니다.
    ''')

    key_number=st.text_input("수정할 아이템의 ITEM_NO를 입력해주세요.")

    if 'ITEMEdit_Flag' not in st.session_state:
        st.session_state.ITEMEdit_Flag=False

    if (st.button('선택')) | (st.session_state.ITEMEdit_Flag==True):
        df_keyNumber = pd.DataFrame()
        query = f"SELECT * \
                    FROM {table_name}\
                    WHERE ITEM_NO= {key_number}"
        df_keyNumber = pd.read_sql(query, connection)
        # st.dataframe(df_keyNumber)

        # 수정할 값 입력
        st.session_state.ITEMEdit_Flag=True
        # USER_ID=st.text_input('사번 (8글자)',max_chars=8)
        default_index = ['Compound', '원료', '구조'].index(df_keyNumber['COMMODITY'][0])
        COMMODITY=st.selectbox('COMMODITY',['Compound','원료','구조'],index=default_index, key="COMMODITY_edit")
        default_index=['Blue Tech',"Comp'd Simplification",'배합 Pool제','원가합리화 - Case','원가합리화 - Tread'].index(df_keyNumber['COMMETS'][0])
        COMMETS=st.selectbox('구분',['Blue Tech',"Comp'd Simplification",'배합 Pool제','원가합리화 - Case','원가합리화 - Tread'],index=default_index, key="COMMETS_edit")
        ITEM=st.text_input('ITEM명 입력',df_keyNumber['ITEM'][0])
        default_index=['CP','DP','HP','IP','JP','KP','MP','TP'].index(df_keyNumber['AREA'][0])
        AREA=st.selectbox('공장지',['CP','DP','HP','IP','JP','KP','MP','TP'],index=default_index, key="AREA_edit")
        # TCR_START_YYYYMM=st.text_input('TCR 적용일자 (YYYYMM)',df_keyNumber['TCR_START_YYYYMM'][0] ,max_chars=6)
        COMPOUND_NAME_AS_IS=st.text_input('기존 Compound NAME',df_keyNumber['COMPOUND_NAME_AS_IS'][0], max_chars=9)
        REVISION_AS_IS=st.text_input('기존 Revision',df_keyNumber['REVISION_AS_IS'][0],max_chars=5)
        COMPOUND_NAME_TO_BE=st.text_input('변경 Compound NAME',df_keyNumber['COMPOUND_NAME_TO_BE'][0], max_chars=9)
        REVISION_TO_BE=st.text_input('변경 Revision',df_keyNumber['REVISION_TO_BE'][0],max_chars=5)
        default_index=['AS/Winter','Case','TB','CTC재료개발팀'].index(df_keyNumber['PJT_NAME'][0])
        PJT_NAME=st.selectbox('PJT명',['AS/Winter','Case','TB','CTC재료개발팀'],index=default_index, key="PJT_NAME_edit")
        PJT_MANAGER=st.text_input('담당자',df_keyNumber['PJT_MANAGER'][0])
        # APP_NO_OF_MTH_PLN=st.number_input('APP_NO_OF_MTH_PLN', min_value=1, max_value=12, value=df_keyNumber['APP_NO_OF_MTH_PLN'][0])
        SCR_UNIT_PRICE_PLAN=st.number_input('예상 금액(월)',df_keyNumber['SCR_UNIT_PRICE_PLAN'][0])
        QTY_PLAN=st.number_input('예상 생산량(월)',df_keyNumber['QTY_PLAN'][0])
        default_index=int(df_keyNumber['SCR_GUBUN'][0])
        SCR_GUBUN=st.selectbox('SCR 자동계산 적용 여부',['MES 자동계산 (0)','예상 금액 적용 (1)','직접 입력(아래 칸을 입력해주세요.) (2)'],index=default_index, key="SCR_GUBUN_edit")
        # SCR_GUBUN_VALUE=st.text_input('직접 입력을 선택한 경우 SCR을 입력해주세요.',df_keyNumber['SCR_GUBUN_VALUE'][0])
        default_index=int(df_keyNumber['ACT_GUBUN'][0])
        ACT_GUBUN=st.selectbox('QTY 자동계산 적용 여부',['MES 자동계산 (0)','예상 생산량 적용 (1)','직접 입력(아래 칸을 입력해주세요.) (2)'],index=default_index, key="ACT_GUBUN_edit")
        # ACT_GUBUN_VALUE=st.text_input('직접 입력을 선택한 경우 ACT를 입력해주세요.',df_keyNumber['ACT_GUBUN_VALUE'][0])

    if st.button('수정 완료'):
        st.session_state.ITEMEdit_Flag=False
        SCR_GUBUN = 0 if SCR_GUBUN == 'MES 자동계산 (0)' else (1 if SCR_GUBUN == '예상 금액 적용 (1)' else 2)
        ACT_GUBUN = 0 if ACT_GUBUN == 'MES 자동계산 (0)' else (1 if ACT_GUBUN == '예상 생산량 적용 (1)' else 2)
        IMESTAMP=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor = connection.cursor()
        cursor.execute(f"UPDATE {table_name}  \
                        SET TIMESTAMP=TO_TIMESTAMP(:1, 'YYYY-MM-DD HH24:MI:SS'), COMMODITY=:2 ,COMMETS=:3 ,ITEM=:4 ,AREA=:5 , \
                            COMPOUND_NAME_AS_IS=:6 ,REVISION_AS_IS=:7 ,COMPOUND_NAME_TO_BE=:8 ,REVISION_TO_BE=:9, \
                            PJT_NAME=:10 ,PJT_MANAGER=:11 ,SCR_UNIT_PRICE_PLAN=:12 ,QTY_PLAN=:13 , \
                            SCR_GUBUN=:14 ,ACT_GUBUN=:15 \
                        WHERE ITEM_NO= {key_number}",    
                    (TIMESTAMP, COMMODITY ,COMMETS ,ITEM ,AREA , \
                            COMPOUND_NAME_AS_IS ,REVISION_AS_IS ,COMPOUND_NAME_TO_BE ,REVISION_TO_BE, \
                            PJT_NAME ,PJT_MANAGER ,SCR_UNIT_PRICE_PLAN ,QTY_PLAN , \
                            SCR_GUBUN ,ACT_GUBUN)) 
        connection.commit()
        cursor.close()
        # del st.session_state.df_keyNumber
        st.session_state.ITEMEdit_Flag=False
        # del st.session_state.MonthlyUpdate_Flag
        st.success("아이템 정보가 수정되었습니다.")


with tab3:

    if 'MonthlyUpdate_Flag' not in st.session_state:
        st.session_state.MonthlyUpdate_Flag=False
    
    st. subheader("ITEM NO. 조회")
    st.code('''
    사번을 입력하고 '조회' 버튼을 누르면 본인이 작성한 아이템의 ITEM_NO와 아이템 정보를 확인할 수 있습니다.
    각 아이템 별로 한 행씩만 출력됩니다. 
    'ITEM_NO' 확인을 위한 기능으로 'SETTING_NO','YEAR_MONTH','TIMESTAMP'는 확인할 수 없습니다.
    ''')
    # 본인의 사번을 입력하여 ITEM_NO 조회
    input_userId=st.text_input('ITEM_NO 확인을 위해 사번(8글자)을 입력하세요.',max_chars=8, key='MonthlyUpdate_UserId_Input')
    if st.button('조회', key='MonthlyUpdate_UserId_Button'):
        df_userId = pd.DataFrame()
        query = f"SELECT * \
                    FROM {table_name}\
                    WHERE USER_ID= {input_userId}"
        df_userId = pd.read_sql(query, connection)
        df_userId = df_userId.drop_duplicates(subset=['ITEM_NO'], keep='first')
        df_userId.drop(labels=['SETTING_NO','YEAR_MONTH','TIMESTAMP'], axis=1, inplace=True)
        st.dataframe(df_userId)

    st.markdown('---')
    st. subheader("월별 실적 업데이트")
    st.code('''
    각 월별 실제 실적 업데이트를 위한 기능입니다.
    입력한 'ITEM_NO', 'YEAR_MONTH'에 해당하는 'SCR_GUBUN', 'SCR_GUBUN_VALUE', 'ACT_GUBUN', 'ACT_GUBUN_VALUE', 'REVIEW'를 수정할 수 있습니다.
    'TIMESTAMP'도 현재 입력 시간으로 업데이트 됩니다.
    호부진사유('REVIEW')는 필수 입력란으로 입력하지 않으면 DB가 수정되지 않고 경고창이 뜹니다.
            
    <사용법>
    1. 위 'ITEM NO. 조회'에서 확인한 아이템의 번호와 실적을 입력할 월을 입력하고 '확인'버튼을 누릅니다.
    2. 현재 저장되어 있는 데이터의 값을 원하는 값으로 수정한 후 '실적 제출' 버튼을 누릅니다.
    3. 제출에 성공한 경우 실적 제출 성공 메세지가 출력됩니다.
    4. 호부진사유를 입력하지 않은 경우 경고 메세지가 출력됩니다. 호부진사유를 입력한 후 재제출합니다.
    ''')

    # 입력할 ITEM_NO와 YEAR_MONTH 선택
    update_item=st.number_input('실적을 입력할 아이템의 ITEM_NO를 입력해주세요.', step=1, format="%d")
    update_month=st.text_input('실적을 입력할 날짜를 YYYYMM 형식으로 입력해주세요.', max_chars=6)

    # 해당 ITEM_NO, YEAR_MONTH 실적 수정
    if (st.button('확인', key='MonthlyUpdate_Key_Button')) | (st.session_state.MonthlyUpdate_Flag==True):
        df_keyNumber = pd.DataFrame()
        query = f"SELECT * \
                    FROM {table_name}\
                    WHERE ITEM_NO= {update_item} AND YEAR_MONTH={update_month}"
        df_keyNumber = pd.read_sql(query, connection)
        st.session_state.df_keyNumber=df_keyNumber
 
        st.session_state.MonthlyUpdate_Flag=True
        default_index=int(st.session_state.df_keyNumber['SCR_GUBUN'][0])
        SCR_GUBUN=st.selectbox('SCR 자동계산 적용 여부(SCR_GUBUN)',['MES 자동계산 (0)','예상 금액 적용 (1)','직접 입력(아래 칸을 입력해주세요.) (2)'], index=default_index, key="SCR_GUBUN_update")
        SCR_GUBUN_VALUE=st.number_input('직접 입력을 선택한 경우 이번 달 실제 가격을 입력해주세요.',value=st.session_state.df_keyNumber['SCR_GUBUN_VALUE'][0] ) 
        default_index=int(st.session_state.df_keyNumber['ACT_GUBUN'][0])
        ACT_GUBUN=st.selectbox('QTY 자동계산 적용 여부(ACT_GUBUN)',['MES 자동계산 (0)','예상 생산량 적용 (1)','직접 입력(아래 칸을 입력해주세요.) (2)'], index=default_index, key="ACT_GUBUN_update")
        ACT_GUBUN_VALUE=st.number_input('직접 입력을 선택한 경우 이번 달 실제 생산량을 입력해주세요.', value=st.session_state.df_keyNumber['ACT_GUBUN_VALUE'][0] )
        default_index=st.session_state.df_keyNumber['REVIEW'][0]
        REVIEW=st.text_area('호부진사유 (필수 입력)', default_index, height=100)

    if st.button('실적 제출'):
        if REVIEW:
            st.session_state.MonthlyUpdate_Flag=False
            SCR_GUBUN = 0 if SCR_GUBUN == 'MES 자동계산 (0)' else (1 if SCR_GUBUN == '예상 금액 적용 (1)' else 2)
            SCR_GUBUN_VALUE=SCR_GUBUN_VALUE if SCR_GUBUN==2 else 0.0
            ACT_GUBUN = 0 if ACT_GUBUN == 'MES 자동계산 (0)' else (1 if ACT_GUBUN == '예상 생산량 적용 (1)' else 2)
            ACT_GUBUN_VALUE=ACT_GUBUN_VALUE if ACT_GUBUN==2 else 0.0
            IMESTAMP=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor = connection.cursor()
            cursor.execute(f"UPDATE {table_name}  \
                            SET SCR_GUBUN={SCR_GUBUN}, SCR_GUBUN_VALUE={SCR_GUBUN_VALUE}, ACT_GUBUN={ACT_GUBUN}, ACT_GUBUN_VALUE={ACT_GUBUN_VALUE}, REVIEW='{REVIEW}', TIMESTAMP=TO_TIMESTAMP('{TIMESTAMP}', 'YYYY-MM-DD HH24:MI:SS')  \
                            WHERE ITEM_NO= {update_item} AND YEAR_MONTH={update_month} " ) 
            connection.commit()
            cursor.close()
            del st.session_state.df_keyNumber
            st.session_state.MonthlyUpdate_Flag=False
            # del st.session_state.MonthlyUpdate_Flag
            st.success("실적이 제출되었습니다.")
        else:
            st.warning("호부진사유를 입력해주세요. 실적이 제출되지 않았습니다.")

        
with tab4:

    st.subheader('월별 DB 리프레쉬')
    if st.button('REFRESH'):
        st.markdown('##### 구현 예정입니다.')
        st.write('매월 담당자가 REFRESH 클릭')
        st.write('')
        st.write('- DB에 최종 월별 가격/생산량 컬럼 추가 예정 (SCR_FINAL / QTY_FINAL)')
        st.write('- SCR_GUBUN/ACT_GUBUN 이')
        st.write('--  0 인 경우 MES 데이터 추출하여 SCR_GUBUN_VALUE / ACT_GUBUN_VALUE 컬럼에 추가')
        st.write('--  1 인 경우 SCR_UNIT_PRICE_PLAN / QTY_PLAN 데이터 추출하여 SCR_GUBUN_VALUE / ACT_GUBUN_VALUE 컬럼에 추가')
        st.write("--  2 인 경우 '월별 업데이트' 탭에서 입력한 SCR_GUBUN_VALUE / ACT_GUBUN_VALUE 값을 사용")
        st.write('')
        st.write("- 적용 월이 끝난 데이터의 'OLD_NEW' 값을 OUT(가칭)으로 변경 ")
        st.write('')

    st.markdown("""---""")
        

    st.subheader('전체 DB 확인')
    st.code('''
    설정된 마스터키를 정확히 입력하고 '전체DB확인'버튼을 누르면 DB 전체 데이터를 확인할 수 있습니다.
    올바르지 않은 키 값을 입력할 경우 실패 메세지가 출력됩니다.
            
    현재 설정된 마스터키는 'MVP'입니다.
    ''')

    master_key=st.text_input('마스터키를 입력하세요.')
    if st.button('전체 DB 확인'):
        if master_key=='MVP':
            df_total = pd.DataFrame()
            query = f"SELECT * \
                        FROM {table_name}"
            df_total = pd.read_sql(query, connection)
            st.dataframe(df_total)
        else:
            st.error('올바르지 않은 마스터키입니다.')

