# tax_logic_s.py（所得税計算関数）

import streamlit as st
import math
from datetime import datetime, timedelta

"""
変数の定義
関数の引数、関数内の作業で使用する変数
            数値 val_1  から val_99
            文字 val_x1 から val_x99
結果変数
            数値 res_1  から res_99
            文字 res_x1  から res_x99
"""

def nenreikeisan1(x1, x2, ret):
    #
    # 誕生日<<前日>>に加齢する法律に基づく年齢計算--------------------
    #

    # x1=年齢計算する生年月日（西暦）
    # x2=年齢を判定したい年月日（西暦）（この日で何歳かをしる特定日）
    # ret　リターンする値  ret=1 年齢のみ,   ret=2 年齢＊１００+月数

    # 日本の法律では、誕生日前日の24時00分に歳をとることになっている。
    # ゆえに、年齢計算は以下通りに行う
    # 1. 生年月日（誕生年月日）から前日を作成する（加齢月日）。
    # 2．特定日の年と1の加齢月日から、特定年における加齢年月日を作成する。（法律上の加齢年月日）
    # 3．年齢　＝　特定年　ー　1の年
    # 4. 特定年月日　＜　 2の年月日（加齢年月日の前）　3の年齢 － 1歳
    #    特定年月日　＞＝ 2の年月日（加齢年月日がきた）3の年齢 － 0歳


    # ２月29日にうまれた場合
    # うるう年、うるう年でない年、すべての年において加齢月日は２月２８日となる
  
    if x1 == " " or int(x1) == 0: return 0
    date_birthday  = datetime.strptime( str( x1 ), "%Y%m%d")
    date_tokuteibi = datetime.strptime( str( x2 ), "%Y%m%d")
        #print(f"年齢計算する生年月日 x1:{date_birthday}")
        #print(f"年齢計算する特定日 x2:{date_tokuteibi}")

    #誕生日の前日を求める
    date_zenjitu = date_birthday - timedelta(days=1)

    #特定日の年における加齢年月日を作成する。
    try:
        date_kareibi = date_zenjitu.replace(year=date_tokuteibi.year )
    except ValueError:
        #うるう年の場合
        date_kareibi = date_zenjitu.replace(year=date_tokuteibi.year, month=2, day=28 )

    #特定年における年齢。ただし特定日が加齢日以前の時はー1歳
    date_val1 = date_tokuteibi.year - date_zenjitu.year
    if date_tokuteibi < date_kareibi:
        date_val1 = date_val1 - 1

    #トータル月数による計算
    date_val2 = ( ( date_tokuteibi.year * 12 + date_tokuteibi.month )  - 
        ( date_zenjitu.year * 12 + date_zenjitu.month )  )
    
    #  // は商（割り算の整数部分）
    date_val2_1 = date_val2 // 12
    #  % は余りを求める
    date_val2_2 = date_val2 % 12

 
        #print(f"関数パラ１ x1:{x1}")
        #print(f"関数パラ２ x2:{x2}")
        #print(f"年齢計算する生年月日 date_birthday:{date_birthday}")
        #print(f"年齢計算する特定日   date_tokuteibi:{date_tokuteibi}")
        #print(f"誕生日の前日 date_zenjitu:{date_zenjitu}")
        #print(f"特定年の加齢年月日 date_kareibi:{date_kareibi}")
        #print(f"年齢 date_val1:{date_val1}")
        #print(f"トータル月数計算 特定日ー前日 date_val2:{date_val2}")
        #print(f"トータル月数計算 年齢 date_val2_1:{date_val2_1}")
        #print(f"トータル月数計算 月数 date_val2_2:{date_val2_2}")

    if ret == 1:  return date_val1
    else: return (date_val2_1*100  +  date_val2_2 )


def nenreikeisan2(x1, x2, ret):
    #
    # 誕生日<<当日>>に加齢する年齢計算-------------------------
    #

    # x1=年齢計算する生年月日（西暦）
    # x2=年齢を判定したい年月日（西暦）（この日で何歳かをしる特定日）
    # ret　リターンする値  ret=1 年齢のみ,   ret=2 年齢＊１００+月数

    # 年齢計算は以下通りに行う
    # 1. 特定年における誕生年月日を作成する。
    # 2．年齢　＝　特定年　ー　生年月日の年
    # 2. 特定年月日　＜　 特定年における誕生年月日（誕生日の前）　2の年齢 － 1歳
    #    特定年月日　＞＝ 特定年における誕生年月日（誕生日がきた）2の年齢 － 0歳


    # ２月29日にうまれた場合
    # うるう年、うるう年でない年、すべての年において誕生月日は２月２８日となる
  
    if x1 == " " or int(x1) == 0: return 0
    date_birthday  = datetime.strptime( str( x1 ), "%Y%m%d")
    date_tokuteibi = datetime.strptime( str( x2 ), "%Y%m%d")
    #print(f"年齢計算する生年月日 x1:{date_birthday}")
    #print(f"年齢計算する特定日 x2:{date_tokuteibi}")

    #特定日の年における誕生年月日を作成する。
    try:
        date_kareibi = date_birthday.replace(year=date_tokuteibi.year )
    except ValueError:
        #うるう年の場合
        date_kareibi = date_birthday.replace(year=date_tokuteibi.year, month=2, day=28 )

    #特定年における年齢。ただし特定日が加齢日以前の時はー1歳
    date_val1 = date_tokuteibi.year - date_birthday.year
    if date_tokuteibi < date_kareibi:
        date_val1 = date_val1 - 1

    #トータル月数による計算
    date_val2 = ( ( date_tokuteibi.year * 12 + date_tokuteibi.month )  - 
        ( date_birthday.year * 12 + date_birthday.month )  )
    
    #  // は商（割り算の整数部分）
    date_val2_1 = date_val2 // 12
    #  % は余りを求める
    date_val2_2 = date_val2 % 12

 
    #print(f"nenreikeisan2 関数パラ１ x1:{x1}")
    #print(f"nenreikeisan2 関数パラ２ x2:{x2}")
    #print(f"nenreikeisan2 年齢計算する生年月日 date_birthday:{date_birthday}")
    #print(f"nenreikeisan2 年齢計算する特定日   date_tokuteibi:{date_tokuteibi}")
    #print(f"nenreikeisan2 特定年の加齢年月日 date_kareibi:{date_kareibi}")
    #print(f"nenreikeisan2 年齢 date_val1:{date_val1}")
    #print(f"nenreikeisan2 トータル月数計算 特定日ー前日 date_val2:{date_val2}")
    #print(f"nenreikeisan2 トータル月数計算 年齢 date_val2_1:{date_val2_1}")
    #print(f"nenreikeisan2 トータル月数計算 月数 date_val2_2:{date_val2_2}")

    if ret == 1:  return date_val1
    else: return (date_val2_1*100  +  date_val2_2 )
  

def syotokukingaku1():
#
#収入金額から所得金額を計算する関数
#
    #print("サブプロ syotokukingaku1")

    #事業所得-----------( res_1 )
    res_1 = ( int(st.session_state["a_jigyo"]) - int(st.session_state["a_jigyo_cost"]) )
    #print(f"事業所得 res_1=:{res_1}")

#給与所得-----------( res_2 )
    val_1 = int(st.session_state["a_kyuyo"]) 

    match val_1:
        case n if n <= 650999:  
            res_2 = 0
        case n if n <= 1899999: 
            res_2 = val_1 - 650000
        case n if n <= 3599999: 
            res_2 = int(val_1/4000)*1000 * 2.8 - 80000 
        case n if n <= 6599999: 
            res_2 = int(val_1/4000)*1000 * 3.2 - 440000
        case n if n <= 8499999: 
            res_2 = val_1 * 0.9 - 1100000 
        case _:                 
            res_2 = val_1 - 1950000

    res_2 = int( res_2 )        
    #print(f"給与所得 res_2=:{res_2}")

#年金所得-----------( res_3 )
    val_1 = int(st.session_state["a_nenkin"])
    val_2 = int(st.session_state["b_honnin_age"])
    match val_2:
        case n if n <65:
            match val_1:
                case n if n <= 1299999:   res_3 = val_1 - 600000
                case n if n <= 4099999:   res_3 = val_1 * 0.75 - 275000
                case n if n <= 7699999:   res_3 = val_1 * 0.85 - 685000
                case n if n <= 9999999:   res_3 = val_1 * 0.95 - 1455000
                case _:                   res_3 = val_1 - 1955000
        case n if n >= 65:
            match val_1:
                case n if n <= 3299999:   res_3 = val_1 - 1100000
                case n if n <= 4099999:   res_3 = val_1 * 0.75 - 275000
                case n if n <= 7699999:   res_3 = val_1 * 0.85 - 685000
                case n if n <= 9999999:   res_3 = val_1 * 0.95 - 1455000
                case _:                   res_3 = val_1 - 1955000
        case _:                           res_3 = 0


    if res_3 < 0:  res_3 = 0
    res_3 = int( res_3 )
    #print(f"年金所得 res_3=:{res_3}")

#所得金額調整控除の計算-----------( res_4 )
    if int(st.session_state["a_kyuyo"]) >0 and int(st.session_state["a_nenkin"]) >0:
        if ( res_2 + res_3 ) > 100000:
            val_1 = min( res_2 , 100000)
            val_2 = min( res_3 , 100000)
            res_4 = ( val_1 + val_2 - 100000 )
        else:
            res_4 = 0
    else:      
        res_4 = 0
    #print(f"所得金額調整控除 res_4=:{res_4}")

#源泉徴収額-----------( res_5 )
    res_5 = (
        int(st.session_state["a_kyuyo_gen"]) + int(st.session_state["a_nenkin_gen"]) )
    #print(f"源泉徴収額　所得税 res_5=:{res_5}")


    #計算結果の保存
    st.session_state["b_syotoku1"] = res_1
    st.session_state["b_syotoku6"] = res_2
    st.session_state["b_syotoku7"] = res_3
    st.session_state["b_syotoku6_tyosei"] = res_4
    st.session_state["g_gensentax"] = res_5
    st.session_state["gd_gensentax"] = 0

    return 'return syotokukingaku1'


def syotokukingaku2():
#
#金融所得金額を計算する関数
#
    #print("サブプロ syotokukingaku2")

#譲渡所得-----------( res_1, res_2, res_3 )
    res_1 = 0
    res_2 = 0
    res_3 = 0

    for i in range(3):
        #print(f"譲渡所得 i =:{i}")
        if st.session_state[f"a_jyotoselect_{i}"] == "申告分離課税":
            res_1 = res_1 + int(st.session_state[f"a_jyoto_{i}"])
            res_2 = res_2 + int(st.session_state[f"a_jyotostax_{i}"])
            res_3 = res_3 + int(st.session_state[f"a_jyotottax_{i}"])
    #print(f"譲渡所得 所得額 res_1=:{res_1}")
    #print(f"譲渡所得 所得税 res_2=:{res_2}")
    #print(f"譲渡所得 地方税 res_3=:{res_3}")

            
#特定上場株式等の配当等
#   申告分離課税-----------( res_4, res_5, res_6 )
    res_4 = 0
    res_5 = 0
    res_6 = 0

    for i in range(3):
        if st.session_state[f"a_haitou9select_{i}"] == "申告分離課税":
            res_4  = ( res_4  + 
                int(st.session_state[f"a_haitou4_{i}"]) +
                int(st.session_state[f"a_haitou5_{i}"]) +
                int(st.session_state[f"a_haitou6_{i}"]) +
                int(st.session_state[f"a_haitou7_{i}"]) +
                int(st.session_state[f"a_haitou8_{i}"]) 
            )
            res_5 = res_5 + int(st.session_state[f"a_haitou9stax_{i}"])
            res_6 = res_6 + int(st.session_state[f"a_haitou9ttax_{i}"])
    #print(f"特定上場配当 分離課税 所得額 res_4=:{res_4}")
    #print(f"特定上場配当 分離課税 所得税 res_5=:{res_5}")
    #print(f"特定上場配当 分離課税 地方税 res_6=:{res_6}")

#   総合課税-----------( res_7, res_8, res_9, res_10, res_11 )
    res_7 = 0
    res_8 = 0
    res_9 = 0
    res_10 = 0
    res_11 = 0

    for i in range(3):
        if st.session_state[f"a_haitou9select_{i}"] == "総合課税":
            res_7  = ( res_7  + 
                int(st.session_state[f"a_haitou4_{i}"]) +
                int(st.session_state[f"a_haitou5_{i}"])
            )
            res_8  = ( res_8 + 
                int(st.session_state[f"a_haitou6_{i}"]) +
                int(st.session_state[f"a_haitou7_{i}"])
            )
            res_9  = res_9  + int(st.session_state[f"a_haitou8_{i}"])
            res_10 = res_10 + int(st.session_state[f"a_haitou9stax_{i}"])
            res_11 = res_11 + int(st.session_state[f"a_haitou9ttax_{i}"])
    #print(f"特定上場配当 総合課税10% 所得額 res_7=:{res_7}")
    #print(f"特定上場配当 総合課税05% 所得額 res_8=:{res_8}")
    #print(f"特定上場配当 総合課税02.5% 所得額 res_9=:{res_9}")
    #print(f"特定上場配当 総合課税 所得税 res_10=:{res_10}")
    #print(f"特定上場配当 総合課税 地方税 res_11=:{res_11}")        

#特定上場以外の配当等
#   申告分離課税-----------( res_12, res_13, res_14 )
    res_12 = 0
    res_13 = 0
    res_14 = 0

    for i in range(3):            
        if st.session_state[f"a_haitou15select_{i}"] == "申告分離課税":
            res_12  = ( res_12  + 
                int(st.session_state[f"a_haitou10_{i}"]) +
                int(st.session_state[f"a_haitou11_{i}"]) +
                int(st.session_state[f"a_haitou12_{i}"]) +
                int(st.session_state[f"a_haitou13_{i}"]) +
                int(st.session_state[f"a_haitou14_{i}"])
            )
            res_13  = res_13  + int(st.session_state[f"a_haitou15stax_{i}"])
            res_14  = res_14  + int(st.session_state[f"a_haitou15ttax_{i}"])
    #print(f"特定上場以外配当 分離課税 所得額 res_12=:{res_12}")
    #print(f"特定上場以外配当 分離課税 所得税 res_13=:{res_13}")
    #print(f"特定上場以外配当 分離課税 地方税 res_14=:{res_14}")
    

#計算結果の保存
    st.session_state["b_syotoku73"] = res_1 
    st.session_state["b_syotoku74"] = ( res_4 + res_12 )
    st.session_state["b_syotoku5"]  = ( res_7 + res_8 + res_9 )
    st.session_state["g_gensentax"] += ( res_2 + res_5 + res_10 + res_13 )
    st.session_state["gd_gensentax"] += ( res_3 + res_6 + res_11 + res_14 )
    st.session_state["b_haitokojyo_1"] = res_7
    st.session_state["b_haitokojyo_2"] = res_8
    st.session_state["b_haitokojyo_3"] = res_9

    return 'return syotokukingaku2'


def syotokugoukei():
#総合課税所得
    st.session_state["g_sogosyotoku"] = (
        st.session_state["b_syotoku1"] +
        st.session_state["b_syotoku5"] +
        st.session_state["b_syotoku6"] -
        st.session_state["b_syotoku6_tyosei"] +
        st.session_state["b_syotoku7"]
    )
#分離課税所得
    st.session_state["g_bunrisyotoku"] = (
        st.session_state["b_syotoku73"] + 
        st.session_state["b_syotoku74"]
    )    
#合計所得金額
    st.session_state["g_gokeisyotoku"] = ( 
        st.session_state["g_sogosyotoku"] + st.session_state["g_bunrisyotoku"] )

    #print(f"総合課税所得 g_sogosyotoku=:{st.session_state["g_sogosyotoku"]}") 
    #print(f"分離課税所得 g_bunrisyotoku=:{st.session_state["g_bunrisyotoku"]}") 
    #print(f"合計所得金額 g_gokeisyotoku=:{st.session_state["g_gokeisyotoku"]}")   
    return 'return syotokugoukei'
    

def syotokukojyo():

#社会保険料控除-----------(res_1)
    val_1 = int(st.session_state["a_hoken13"])
    
    res_1 = val_1
    #print(f"社会保険料控除 res_1=:{res_1}")
    
#生命保険料控除-----------(res_2)
#   一般の生命保険料控除
    val_1 = int(st.session_state["a_hoken15_1"])
    val_2 = int(st.session_state["a_hoken15_2"])

    val_1 = min ( keisansiki1(val_1), 40000)
    val_2 = min ( keisansiki2(val_2), 50000)
    val_3 = min ( val_1 + val_2 , 40000 )
    val_4 = max ( val_2 , val_3 )
    #print(f"一般の生命保険料控除 val_4=:{val_4}")
    
#   個人年金保険料控除
    val_1 = int(st.session_state["a_hoken15_3"])
    val_2 = int(st.session_state["a_hoken15_4"])
 
    val_1 = min ( keisansiki1(val_1), 40000)
    val_2 = min ( keisansiki2(val_2), 50000)
    val_3 = min ( val_1 + val_2 , 40000 )
    val_5 = max ( val_2 , val_3 )
    #print(f"個人年金保険料控除 val_5=:{val_5}")

#   介護保険料控除
    val_1 = int(st.session_state["a_hoken15_5"])

    val_6 = min ( keisansiki1(val_1), 40000)
    #print(f"介護保険料控除 val_6=:{val_6}")

    res_2 = min ( ( val_4 + val_5 + val_6 ) , 120000)
    #print(f"生命保険料控除 res_2=:{res_2}")


#地震保険料控除-----------(res_3)
#   地震保険料
    val_1 = int(st.session_state["a_hoken16_1"])

    val_1 = min ( val_1, 50000)
    #print(f"地震保険料 val_1=:{val_1}")

#   長期損害保険料
    val_2 = int(st.session_state["a_hoken16_2"])

    if val_2 > 10000:
        val_2 = min ( math.ceil(val_2 * 0.5 + 5000) , 15000)
    #print(f"長期損害保険料 val_2=:{val_2}")

    res_3 = min ( ( val_1 + val_2 ) , 50000 )
    #print(f"地震保険料控除- res_3=:{res_3}")
 

#寡婦控除-----------(res_4)
    if st.session_state["a_honnin_sex"] == "女" and st.session_state["a_honnin_kafu"] == "あり": 
        res_4 = 270000
    else: res_4 = 0
    #print(f"寡婦控除- res_4=:{res_4}")
 

#障害者控除-----------(res_5)
#   本人
    if st.session_state["a_honnin_syogai"] == "障害者": val_1 = 270000
    elif st.session_state["a_honnin_syogai"] == "特別障害者": val_1 = 400000
    else: val_1 = 0
    #print(f"障害者控除 本人- val_1=:{val_1}")
#   配偶者
    if st.session_state["a_haigu_syogai"] == "障害者": val_2 = 270000
    elif st.session_state["a_haigu_syogai"] == "特別障害者": val_2 = 400000
    elif st.session_state["a_haigu_syogai"] == "同居特別障害者": val_2 = 750000
    else: val_2 = 0
    #print(f"障害者控除 配偶者- val_2=:{val_2}")

    res_5 = val_1 + val_2
    #print(f"障害者控除 res_5=:{res_5}")
    
 

#基礎控除-----------( res_6 )

    val_1 = st.session_state["g_gokeisyotoku"] 

#   基礎控除額
    match val_1:
        case n if n <=1320000:   res_6 = 950000 
        case n if n <=3360000:   res_6 = 880000 
        case n if n <=4890000:   res_6 = 680000 
        case n if n <=6550000:   res_6 = 630000 
        case n if n <=23500000:  res_6 = 580000 
        case n if n <=24000000:  res_6 = 480000 
        case n if n <=24500000:  res_6 = 320000 
        case n if n <=25000000:  res_6 = 160000 
        case _:             res_6 = 0 
    #print(f"基礎控除額 res_6=:{res_6}")


#配偶者控除、配偶者特別控除-----------(res_7, res_x1, res_x2, res_x3 )
    if (st.session_state["a_honnin_haigu"]) == "あり":
#   区分Ⅰ判定(1)-----------(res_x1 )
        match val_1:
            case n if n <=9000000:   res_x1 = "A"
            case n if n <=9500000:   res_x1 = "B"
            case n if n <=10000000:  res_x1 = "C"
            case _: res_x1=" "            
    

#   区分Ⅱ判定(1,2=配偶者控除に該当 )(3，4=配偶者特別控除に該当 ）
        val_1 = int(st.session_state["a_haigu_syotoku"])
        val_2 = int(st.session_state["b_haigu_age"])
        match val_1:
            case n if n <=580000:
                res_x3="配偶者控除"   
                if val_2 >= 70: 
                    res_x2 = "1"   
                else: res_x2 = "2"
            case n if n <=950000:
                res_x3="配偶者特別控除" 
                res_x2 = "3" 
            case n if n <=1330000:
                res_x3="配偶者特別控除"
                res_x2 = "4" 
            case _: 
                res_x2 = " "    
                res_x3 = " "


        match res_x2:
            case "1":
                match res_x1:
                    case "A":       res_7 = 480000
                    case "B":       res_7 = 320000
                    case "C":       res_7 = 160000
                    case _:         res_7 = 0
            case "2":  
                match res_x1:
                    case "A":       res_7 = 380000
                    case "B":       res_7 = 260000
                    case "C":       res_7 = 130000
                    case _:         res_7 = 0
            case "3":  
                match res_x1:
                    case "A":       res_7 = 380000
                    case "B":       res_7 = 260000
                    case "C":       res_7 = 130000
                    case _:         res_7 = 0
            case "4":  
                match val_1:
                    case n if n <= 1000000:
                        match res_x1:
                            case "A":  res_7 = 360000
                            case "B":  res_7 = 240000
                            case "C":  res_7 = 120000
                            case _:    res_7 = 0  
                    case n if n <= 1050000: 
                        match res_x1:
                            case "A":  res_7 = 310000
                            case "B":  res_7 = 210000
                            case "C":  res_7 = 110000
                            case _:    res_7 = 0  
                    case n if n <= 1100000:
                        match res_x1:
                            case "A":  res_7 = 260000
                            case "B":  res_7 = 180000
                            case "C":  res_7 = 90000
                            case _:    res_7 = 0  
                    case n if n <= 1150000:
                        match res_x1:
                            case "A":  res_7 = 210000
                            case "B":  res_7 = 140000
                            case "C":  res_7 = 70000
                            case _:    res_7 = 0
                    case n if n <= 1200000:
                        match res_x1:
                            case "A":  res_7 = 160000
                            case "B":  res_7 = 110000
                            case "C":  res_7 = 60000
                            case _:    res_7 = 0
                    case n if n <= 1250000:
                        match res_x1:
                            case "A":  res_7 = 110000
                            case "B":  res_7 = 80000
                            case "C":  res_7 = 40000
                            case _:    res_7 = 0
                    case n if n <= 1300000:
                        match res_x1:
                            case "A":  res_7 = 60000
                            case "B":  res_7 = 40000
                            case "C":  res_7 = 20000
                            case _:    res_7 = 0
                    case n if n <= 1330000:
                        match res_x1:
                            case "A":  res_7 = 30000
                            case "B":  res_7 = 20000
                            case "C":  res_7 = 10000
                            case _:    res_7 = 0
                    case _: res_7 = 0
    else:
        res_x1 = " "
        res_x2 = " "
        res_7  = 0
        res_x3 = " "
    #print(f"区分Ⅰ判定 res_x1=:{res_x1}")
    #print(f"区分Ⅱ判定 res_x1=:{res_x2}")
    #print(f"配偶者控除、配偶者特別控除 res_7=:{res_7}")
    #print(f"配偶者控除、配偶者特別控除区分 res_x3=:{res_x3}")
    


#医療費控除---------( res_8, res_x4 )
#   医療費控除とならない額
    val_1 = ( st.session_state["g_gokeisyotoku"] * 0.05 )
    if val_1 < 0:  val_1 = 0
    val_2 = min ( val_1, 100000)
#   医療費控除額
    val_3 = (int(st.session_state["a_skojyo28_1"]) - 
        int(st.session_state["a_skojyo28_2"]) - val_2 )
    if val_3 < 0:         val_3 = 0
    if val_3 > 2000000:   val_3 = 2000000
    #print(f"医療費控除額 val_3=:{val_3}")

#   セルフメディ控除額
    val_4 = (int(st.session_state["a_skojyo28_3"]) - 
        int(st.session_state["a_skojyo28_4"]) - 12000 )
    if val_4 < 0:       val_4 = 0
    if val_4 > 88000:   val_4=88000
    #print(f"セルフメディ控除額 val_4=:{val_4}")


    if val_3 == 0 and val_4 == 0: 
        res_8 = 0
        res_x4 = " "
    else:
        if val_3 >= val_4: 
            res_8 = val_3
            res_x4 = "医療費控除"
        else:
            res_8 = val_4
            res_x4 = "セルフメディケーション控除"
    #print(f"医療費控除 res_8=:{res_8}")
    #print(f"医療費控除区分 res_x4=:{res_x4}")

 
 
#寄付金控除-----------( res_9 )
    val_1 = int(st.session_state["a_skojyo29"])
    val_2 = ( st.session_state["g_gokeisyotoku"] * 0.4 )
    #print(f"寄付金額 val_1=:{val_1}")
    #print(f"寄付金上限額 val_2=:{val_2}")
 
    if val_2 < 0:  val_2=0
    val_3 = min ( val_1, val_2 )
     
    res_9 = (val_3 - 2000 ) 
    if res_9 < 0:  res_9 = 0
    #print(f"寄付金控除 res_9=:{res_9}")
 
    
#計算結果の保存
    st.session_state["b_skojyo13"] = res_1  
    st.session_state["b_skojyo15"] = res_2
    st.session_state["b_skojyo16"] = res_3
    st.session_state["b_skojyo17"] = res_4
    st.session_state["b_skojyo19"] = res_5

    st.session_state["b_skojyo21_kubun"] = res_x3
    st.session_state["b_skojyo21"] = res_7
    st.session_state["b_skojyo25"] = res_6
    st.session_state["b_skojyo28_kubun"] = res_x4
    st.session_state["b_skojyo28"] = res_8
    st.session_state["b_skojyo29"] = res_9

    st.session_state["b_kubun1"] = res_x1
    st.session_state["b_kubun2"] = res_x2

#
    st.session_state["g_syotokukojyo"] = ( 
        res_1 + res_2 + res_3 + res_4 + res_5 + res_6 + res_7 + res_8 + res_9 )
    #print(f"所得控除合計 g_syotokukojyo=:{st.session_state["g_syotokukojyo"]}")
    return 'return syotokukojyo'



def kazeisyotoku():
#
#課税所得計算
#
    #
    #総合所得、分離所得から所得控除を差し引く
    #-------- 所得控除残（val_1）----------

    val_1 = st.session_state["g_syotokukojyo"]

    #課税所得計算 総合課税------( res_1 )
    if st.session_state["g_sogosyotoku"] >= val_1:
        res_1 = st.session_state["g_sogosyotoku"] - val_1
        val_1 = 0
    else:
        res_1 = 0
        val_1 = val_1 - st.session_state["g_sogosyotoku"] 

    #課税所得額 分離課税（上場株式の譲渡）------( res_2 )
    if st.session_state["b_syotoku73"] >= val_1:
        res_2 = st.session_state["b_syotoku73"] - val_1
        val_1 = 0
    else:
        res_2 = 0
        val_1 = val_1 - st.session_state["b_syotoku73"] 

    #課税所得額 分離課税（上場株式の配当）------( res_3 )        
    if st.session_state["b_syotoku74"] >= val_1:
        res_3 = st.session_state["b_syotoku74"] - val_1
        val_1 = 0
    else:
        res_3 = 0
        val_1 = val_1 - st.session_state["b_syotoku74"] 

    #計算結果の保存
    res_1 = int( res_1 / 1000 ) * 1000
    res_2 = int( res_2 / 1000 ) * 1000
    res_3 = int( res_3 / 1000 ) * 1000
    st.session_state["b_kazei78"] = res_1  
    st.session_state["b_kazei81"] = res_2
    st.session_state["b_kazei82"] = res_3  
    #print(f"課税所得 総合課税 res_1=:{res_1}")
    #print(f"課税所得 分離課税（上場株式の譲渡) res_2=:{res_2}")
    #print(f"課税所得 分離課税（上場株式の配当） res_3=:{res_3}")
    return 'return kazeisyotoku'
    

def szeikeisan():
#
#所得税計算
#
    #所得税計算 総合課税------( res_1 )
    val_1 = st.session_state["b_kazei78"]

    match val_1:
        case n if n <1000:        res_1 = 0
        case n if n <=1949000:    res_1 = val_1 * 0.05 
        case n if n <=3299000:    res_1 = val_1 * 0.1  - 97500
        case n if n <=6949000:    res_1 = val_1 * 0.2  - 427500
        case n if n <=8999000:    res_1 = val_1 * 0.23 - 636000
        case n if n <=17999000:   res_1 = val_1 * 0.33 - 1536000
        case n if n <=39999000:   res_1 = val_1 * 0.4  - 2796000
        case _:                   res_1 = val_1 * 0.45 - 4796000

    #所得税計算 分離課税（上場株式の譲渡）------( res_2 )
    res_2 = st.session_state["b_kazei81"] * 0.15 

    #所得税計算 分離課税（上場株式の配当）------( res_3 )
    res_3 = st.session_state["b_kazei82"] * 0.15

    #所得税合計------( res_4 ) 
    res_4 = res_1 + res_2 + res_3

    #計算結果の保存
    st.session_state["b_szei86"] = int( res_1 )  
    st.session_state["b_szei89"] = int( res_2 )
    st.session_state["b_szei90"] = int( res_3 )
    st.session_state["g_szei"] = int( res_4 )
    #print(f"所得税 総合課税 res_1=:{res_1}")
    #print(f"所得税 分離課税（上場株式の譲渡) res_2=:{res_2}")
    #print(f"所得税 分離課税（上場株式の配当）res_3=:{res_3}")
    #print(f"所得税 合計 res_4=:{res_4}")
    return 'return szeikeisan'


def haitokojyo():
#
#配当控除計算 　計算変数 val_1 ～　val_nn
#（ nnは、特定証券投資信託に係る配当控除額の計算書の ①～⑱に対応 ）
#
    #所得税計算 総合課税------( res_1 )
    val_1 = ( st.session_state["b_kazei78"] + 
                st.session_state["b_kazei81"] + st.session_state["b_kazei82"] )
    val_2 = st.session_state["b_syotoku5"]
    val_3 = st.session_state["b_haitokojyo_1"]
    val_4 = st.session_state["b_haitokojyo_2"]
    val_5 = st.session_state["b_haitokojyo_3"]
    
    # ③に係る控除額の計算
    val_6 = val_1 - val_4 - val_5 - 10000000
    if val_6 < 0: val_6 = 0
    val_7 = val_3 - val_6
    if val_7 < 0: val_7 = 0 
    val_8 = math.ceil( val_7 * 0.1 )
    val_9 = math.ceil( ( val_3 - val_7 ) * 0.05 )

    # ④に係る控除額の計算
    val_10 = val_1 - val_5 - 10000000
    if val_10 < 0: val_10 = 0
    val_11 = val_4 - val_10
    if val_11 < 0: val_11 = 0 
    val_12 = math.ceil( val_11 * 0.05 )
    val_13 = math.ceil( ( val_4 - val_11 ) * 0.025 )

    # ⑤に係る控除額の計算
    val_14 = val_1 - 10000000
    if val_14 < 0: val_14 = 0
    val_15 = val_5 - val_14
    if val_15 < 0: val_15 = 0 
    val_16 = math.ceil( val_15 * 0.025 )
    val_17 = math.ceil( ( val_5 - val_15 ) * 0.0125 )
 
    #計算結果の保存
    res_1 = val_8 + val_9 + val_12 + val_13 + val_16 + val_17
    st.session_state["b_haitokojyo"] = res_1  
    #print(f"配当控除額 res_1=:{res_1}")
    return 'return haitokojyo'


def noufuszei():
#
#復興特別税、納付額（還付額）計算
#
    #差引所得税額(第一表44)　（税額-税額控除）1円以下切捨て
    res_1 = st.session_state["g_szei"] - st.session_state["b_haitokojyo"]
    if res_1 < 0 : res_1 = 0
    
    #復興特別所得税(第一表45)　(差引所得税額*2.1％)　1円以下切捨て
    res_2 =  int( res_1 * 0.021 ) 
    
    #所得税及び復興特別所得税の額(第一表46)　(44＋45)　1円以下切捨て
    res_3 = res_1 + res_2

    #申告納税額(第一表50)　(46-源泉徴収税額)
    res_4 = res_3 - int( st.session_state["g_gensentax"])

    #res_4  (-)還付   (+)納税　納税の場合100円以下切捨て
    if res_4 >= 0: res_4 = ( int ( res_4 / 100 ) ) * 100


    #計算結果の保存
    st.session_state["b_szei44"] = res_1  
    st.session_state["b_szei45"] = res_2
    st.session_state["g_kakuteitax"] = res_3
    st.session_state["g_noufutax"] = res_4
    #print(f"所得税 基準所得税額 res_1=:{res_1}")
    #print(f"所得税 復興特別所得税額 res_2=:{res_2}")
    #print(f"所得税 確定税額 res_3=:{res_3}")
    #print(f"所得税 申告納税額 res_4=:{res_4}")
    return 'return noufuszei'

    
#保険料控除　計算式1　(新保険料)
def keisansiki1(kval_1):
    kres_1 = 0

    match kval_1:
        case n if n <=20000:   kres_1 = kval_1
        case n if n <=40000:   kres_1 = math.ceil( kval_1 * 0.5 + 10000 )
        case n if n <=80000:   kres_1 = math.ceil( kval_1 * 0.25 + 20000 )
        case n if n >=80001:   kres_1 = 40000
    return kres_1

#保険料控除　計算式2　(旧保険料)
def keisansiki2(kval_1):
    kres_1 = 0

    match kval_1:
        case n if n <=25000:   kres_1 = kval_1
        case n if n <=50000:   kres_1 = math.ceil( kval_1 * 0.5 + 12500 )
        case n if n <=100000:  kres_1 = math.ceil( kval_1 * 0.25 + 25000 )
        case n if n >=100001:  kres_1 = 50000
    return kres_1

#
