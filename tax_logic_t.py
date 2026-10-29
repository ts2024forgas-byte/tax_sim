# tax_logic_t.py（地方税計算関数）

import streamlit as st
import math
import tax_logic_s 

"""
変数の定義
関数の引数、関数内の作業で使用する変数
            数値 val_1  から val_99
            文字 val_x1 から val_x99
結果変数
            数値 res_1  から res_99
            文字 res_x1  から res_x99
"""



#-----------------------------------------------------------
#                          地方税
#-----------------------------------------------------------
#
def hikazeihantei():
#
#地方税（所得割、均等割、森林環境税の3つの税）の課税、非課税判定
#
#      所得割     st.session_state["d_hikazei1"]：  "課税" "非課税"
#      均等割     st.session_state["d_hikazei2"]：  "課税" "非課税"
#      森林環境税  st.session_state["d_hikazei3"]：  "課税" "非課税"
#

    val_1  = st.session_state["g_gokeisyotoku"]
    val_x1 = st.session_state["a_honnin_haigu"]
    val_x2 = st.session_state["b_kubun2"]
    if val_x1 == "あり":
        if (val_x2 == "1" or val_x2 == "2"):
            val_2 = 280000 * 2 + 100000 + 168000
            val_3 = 350000 * 2 + 100000 + 320000
        else:
            val_2 = 380000
            val_3 = 450000
    else: 
        val_2 = 380000
        val_3 = 450000

    st.session_state["d_hikazei1"] = "非課税"
    st.session_state["d_hikazei2"] = "非課税" 
    st.session_state["d_hikazei3"] = "非課税"    

    #非課税判定1(所得割、均等割、森林環境税非課税)
    if val_1 <= 13500000:
        if ( st.session_state["a_honnin_syogai"] == "障害者" or 
             st.session_state["a_honnin_syogai"] == "特別障害者" or 
             st.session_state["a_honnin_kafu"] == "あり" 
           ):
                #print(f"所得割、均等割、森林環境税非課税に該当")
                return 'return hikazeihantei_1'

    #非課税判定2(均等割、森林環境税非課税)
    if val_1 <= val_2: 
                st.session_state["d_hikazei1"] = "課税"
                #print(f"均等割、森林環境税非課税に該当")
                return 'return hikazeihantei_2'

    #非課税判定3（所得割非課税、非課税判定1、非課税判定2以外の人）
    if val_1 <= val_3: 
                st.session_state["d_hikazei2"] = "課税" 
                st.session_state["d_hikazei3"] = "課税"
                #print(f"所得割非課税に該当")
                return 'return hikazeihantei_3'

    st.session_state["d_hikazei1"] = "課税"
    st.session_state["d_hikazei2"] = "課税" 
    st.session_state["d_hikazei3"] = "課税"
    #print(f"所得割、均等割、森林環境税が課税に該当")

    return 'return hikazeihantei'


def syotokukojyo():
 
#社会保険料控除-----------(res_1)
    val_1 = int(st.session_state["a_hoken13"])
    
    res_1 = val_1
    #print(f"地方税＿社会社会保険料控除 res_1=:{res_1}")
    
#生命保険料控除-----------(res_2)
#   一般の生命保険料控除
    val_1 = int(st.session_state["a_hoken15_1"])
    val_2 = int(st.session_state["a_hoken15_2"])

    val_1 = min ( keisansiki1(val_1), 28000)
    val_2 = min ( keisansiki2(val_2), 35000)
    val_3 = min ( val_1 + val_2 , 28000 )
    val_4 = max ( val_2 , val_3 )
    #print(f"地方税 一般の生命保険料控除 val_4=:{val_4}")
    
#   個人年金保険料控除
    val_1 = int(st.session_state["a_hoken15_3"])
    val_2 = int(st.session_state["a_hoken15_4"])
 
    val_1 = min ( keisansiki1(val_1), 28000)
    val_2 = min ( keisansiki2(val_2), 35000)
    val_3 = min ( val_1 + val_2 , 28000 )
    val_5 = max ( val_2 , val_3 )
    #print(f"地方税 個人年金保険料控除 val_5=:{val_5}")

#   介護保険料控除
    val_1 = int(st.session_state["a_hoken15_5"])

    val_6 = min ( keisansiki1(val_1), 28000)
    #print(f"地方税 介護保険料控除 val_6=:{val_6}")

    res_2 = min ( ( val_4 + val_5 + val_6 ) , 70000)
    #print(f"地方税 生命保険料控除 res_2=:{res_2}")


#地震保険料控除-----------(res_3)
#   地震保険料(val_2)
    val_1 = int(st.session_state["a_hoken16_1"])

    if val_1 <= 50000: val_2 = math.ceil( val_1 * 0.5 )
    else: val_2 = 25000
    #print(f"地方税 地震保険料 val_2=:{val_2}")

#   長期損害保険料(val_4)
    val_3 = int(st.session_state["a_hoken16_2"])

    match val_3:
        case n if n <=5000:   val_4 = val_3
        case n if n <=15000:  val_4 = math.ceil( kval_3 * 0.5 + 2500 )
        case _:  val_4 = 10000
    #print(f"地方税 長期損害保険料 val_4=:{val_4}")

    res_3 = min ( ( val_2 + val_4 ) , 25000 )
    #print(f"地方税 地震保険料控除- res_3=:{res_3}")
 

#寡婦控除-----------(res_4)
    if st.session_state["a_honnin_sex"] == "女" and st.session_state["a_honnin_kafu"] == "あり": 
        res_4 = 260000
    else: res_4 = 0
    #print(f"地方税 寡婦控除- res_4=:{res_4}")
 

#障害者控除-----------(res_5)
#   本人
    if st.session_state["a_honnin_syogai"] == "障害者": val_1 = 260000
    elif st.session_state["a_honnin_syogai"] == "特別障害者": val_1 = 300000
    else: val_1 = 0
    #print(f"地方税 障害者控除 本人- val_1=:{val_1}")
#   配偶者
    if st.session_state["a_haigu_syogai"] == "障害者": val_2 = 260000
    elif st.session_state["a_haigu_syogai"] == "特別障害者": val_2 = 300000
    elif st.session_state["a_haigu_syogai"] == "同居特別障害者": val_2 = 530000
    else: val_2 = 0
    #print(f"地方税 障害者控除 配偶者- val_2=:{val_2}")

    res_5 = val_1 + val_2
    #print(f"地方税 障害者控除 res_5=:{res_5}")
    
 
#基礎控除-----------( res_6 )

    val_1 = st.session_state["g_gokeisyotoku"] 

#   基礎控除額
    match val_1:
        case n if n <=24000000:   res_6 = 430000 
        case n if n <=24500000:   res_6 = 290000 
        case n if n <=25000000:   res_6 = 150000 
        case _:               res_6 = 0 
    #print(f"地方税 基礎控除額 res_6=:{res_6}")


#配偶者控除、配偶者特別控除-----------( res_7 )
    if (st.session_state["a_honnin_haigu"]) == "あり":
        res_x1 = st.session_state["b_kubun1"]
        res_x2 = st.session_state["b_kubun2"]

        if res_x2 == "1" or res_x2 == "2":   res_x3="配偶者控除"
        else: res_x3="配偶者特別控除"
    
        match res_x2:
            case "1":
                match res_x1:
                    case "A":       res_7 = 380000
                    case "B":       res_7 = 260000
                    case "C":       res_7 = 130000
                    case _:         res_7 = 0
            case "2":  
                match res_x1:
                    case "A":       res_7 = 330000
                    case "B":       res_7 = 220000
                    case "C":       res_7 = 110000
                    case _:         res_7 = 0
            case "3":  
                match res_x1:
                    case "A":       res_7 = 330000
                    case "B":       res_7 = 222000
                    case "C":       res_7 = 110000
                    case _:         res_7 = 0
            case "4":  
                match val_1:
                    case n if n <= 1000000:
                        match res_x1:
                            case "A":  res_7 = 330000
                            case "B":  res_7 = 220000
                            case "C":  res_7 = 110000
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
    #print(f"地方税 区分Ⅰ判定 res_x1=:{res_x1}")
    #print(f"地方税 区分Ⅱ判定 res_x1=:{res_x2}")
    #print(f"地方税 配偶者控除、配偶者特別控除 res_7=:{res_7}")
    #print(f"地方税 配偶者控除、配偶者特別控除区分 res_x3=:{res_x3}")
    


#医療費控除---------( res_8, res_x4 )
#   医療費控除とならない額
    val_1 = ( st.session_state["g_gokeisyotoku"] * 0.05 )
    if val_1 < 0:  val_1=0
    val_2 = min ( val_1, 100000)
#   医療費控除額
    val_3 = (int(st.session_state["a_skojyo28_1"]) - 
        int(st.session_state["a_skojyo28_2"]) - val_2 )
    if val_3 < 0:         val_3 = 0
    if val_3 > 2000000:   val_3 = 2000000
    #print(f"地方税 医療費控除額 val_3=:{val_3}")

#   セルフメディ控除額
    val_4 = (int(st.session_state["a_skojyo28_3"]) - 
        int(st.session_state["a_skojyo28_4"]) - 12000 )
    if val_4 < 0:       val_4 = 0
    if val_4 > 88000:   val_4=88000
    #print(f"地方税 セルフメディ控除額 val_4=:{val_4}")

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
    #print(f"地方税 医療費控除 res_8=:{res_8}")
    #print(f"地方税 医療費控除区分 res_x4=:{res_x4}")
 
     
#計算結果の保存
    st.session_state["d_skojyo13"] = res_1  
    st.session_state["d_skojyo15"] = res_2
    st.session_state["d_skojyo16"] = res_3
    st.session_state["d_skojyo17"] = res_4
    st.session_state["d_skojyo19"] = res_5

    st.session_state["d_skojyo21_kubun"] = res_x3
    st.session_state["d_skojyo21"] = res_7
    st.session_state["d_skojyo25"] = res_6
    st.session_state["d_skojyo28_kubun"] = res_x4
    st.session_state["d_skojyo28"] = res_8

    st.session_state["gd_syotokukojyo"] = ( 
        res_1 + res_2 + res_3 + res_4 + res_5 + res_6 + res_7 + res_8 )
    #print(f"地方税 所得控除合計 gd_syotokukojyo=:{st.session_state["gd_syotokukojyo"]}")
    #print(f"地方税の所得控除合計には、人的控除差額による調整控除は含まず")
    
    return 'return syotokukojyo'



def kazeisyotoku():
#
#課税所得計算
#
    #
    #総合所得、分離所得から所得控除を差し引く
    #-------- 所得控除残（val_1）----------

    val_1 = st.session_state["gd_syotokukojyo"]

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

    st.session_state["d_kazei78"] = res_1  
    st.session_state["d_kazei81"] = res_2
    st.session_state["d_kazei82"] = res_3  
    #print(f"地方税 課税所得 総合課税 res_1=:{res_1}")
    #print(f"地方税 課税所得 分離課税（上場株式の譲渡) res_2=:{res_2}")
    #print(f"地方税 課税所得 分離課税（上場株式の配当） res_3=:{res_3}")

    return 'return kazeisyotoku'
    

def szeikeisan():
#
#所得割税計算
#
    #地方税 所得割額計算 総合課税------( res_1, res_2)
    val_1 = st.session_state["d_kazei78"]
    #市民税
    res_1 = val_1 * 0.06
    res_1 = int( res_1 / 10 ) * 10

    #県民税
    res_2 = val_1 * 0.04
    res_2 = int( res_2 / 10 ) * 10


    #地方税 所得割額計算 分離課税（上場株式の譲渡+上場株式の配当）------( res_3, res_4 )
    val_1 = st.session_state["d_kazei81"] + st.session_state["d_kazei82"]
    #市民税
    res_3 = val_1 * 0.03
    res_3 = int ( res_3 / 10 ) * 10
    #県民税
    res_4 = val_1 * 0.02
    res_4 = int ( res_4 / 10 ) * 10

    
    #計算結果の保存
    st.session_state["d_szei86_1"] = res_1  
    st.session_state["d_szei86_2"] = res_2  
    st.session_state["d_szei89&90_1"] = res_3
    st.session_state["d_szei89&90_2"] = res_4
    st.session_state["gd_szei_1"] = res_1 + res_3
    st.session_state["gd_szei_2"] = res_2 + res_4

    #print(f"地方税 総合課税市民税 res_1=:{res_1}")
    #print(f"地方税 総合課税県民税 res_2=:{res_2}")
    #print(f"地方税 分離課税市民税 res_3=:{res_3}")
    #print(f"地方税 分離課税県民税 res_4=:{res_4}")
    #print(f"地方税 総合課税 合計 :{res_1 + res_3}")
    #print(f"地方税 分離課税 合計 :{res_2 + res_4}")

    if st.session_state["d_hikazei1"] == "非課税":
        st.session_state["d_szei86_1"] = 0  
        st.session_state["d_szei86_2"] = 0  
        st.session_state["d_szei89&90_1"] = 0
        st.session_state["d_szei89&90_2"] = 0
        st.session_state["gd_szei_1"] = 0
        st.session_state["gd_szei_2"] = 0
        #print(f"地方税 所得割非課税者 ALL所得割額ゼロ処理")

    return 'return szeikeisan'


def tyoseikojyo():
#
#調整控除額計算
#
#人的控除差額-----------( res_1 )
    #基礎控除( val_1 )
    val_1 = 50000

    #本人障害( val_2 )
    if st.session_state["a_honnin_syogai"] == "障害者": val_2 = 10000
    elif st.session_state["a_honnin_syogai"] == "特別障害者": val_2 = 100000
    else: val_2 = 0

    #本人寡婦( val_3 )
    if st.session_state["a_honnin_sex"] == "女" and st.session_state["a_honnin_kafu"] == "あり": 
        val_3 = 10000
    else: val_3 = 0

    #配偶者障害( val_4 )
    if st.session_state["a_haigu_syogai"] == "障害者": val_4 = 10000
    elif st.session_state["a_haigu_syogai"] == "特別障害者": val_4 = 100000
    elif st.session_state["a_haigu_syogai"] == "同居特別障害者": val_4 = 220000
    else: val_4 = 0

    #配偶者控除( val_5 )
    val_x1 = st.session_state["b_kubun1"]
    val_x2 = st.session_state["b_kubun2"]
    match val_x2:
            case "1":
                match val_x1:
                    case "A":       val_5 = 100000
                    case "B":       val_5 = 60000
                    case "C":       val_5 = 30000
                    case _:         val_5 = 0
            case "2":  
                match val_x1:
                    case "A":       val_5 = 50000
                    case "B":       val_5 = 40000
                    case "C":       val_5 = 20000
                    case _:         val_5 = 0
            case _: val_5 = 0
    res_1 = val_1 + val_2 + val_3 + val_4 + val_5


    #調整控除( res_2_1, res_2_2 )
    val_1 = st.session_state["g_gokeisyotoku"]
    val_2 = ( st.session_state["d_kazei78"] + 
            st.session_state["d_kazei81"] + st.session_state["d_kazei82"] ) 

    if val_1 > 25000000 or st.session_state["d_kazei78"] == 0: 
        val_3 = 0
    else:
        match val_2:
            case n if n <= 2000000:
                val_3 = min ( val_2, res_1 )
                val_3 = val_3 * 0.05
            case _: 
                val_3 = ( res_1 - ( val_2 - 2000000 ) ) * 0.05

        if val_3 < 2500:   val_3 = 2500  
    
    res_2_1 = int( val_3 * 3 / 5 )
    res_2_2 = val_3 - res_2_1
    st.session_state["d_jinkjsagaku"] = res_1
    st.session_state["d_tyoseikojyo_1"] = res_2_1  
    st.session_state["d_tyoseikojyo_2"] = res_2_2  
    #print(f"地方税 人的控除差額 res_1=:{res_1}")
    #print(f"地方税 調整控除額市民税 res_2_1=:{res_2_1}")
    #print(f"地方税 調整控除額県民税 res_2_2=:{res_2_2}")


def zeigakukojyo():
#
#税額控除計算
#
#   配当控除計算 　計算変数 val_1 ～　val_nn
#（ nnは、特定証券投資信託に係る配当控除額の計算書の ①～⑱に対応 ）
#
    #所得税計算 総合課税------( res_1_1, res_1_2 )
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
    val_8_1 = math.ceil( val_7 * 0.016 )
    val_9_1 = math.ceil( ( val_3 - val_7 ) * 0.008 )
    val_8_2 = math.ceil( val_7 * 0.012 )
    val_9_2 = math.ceil( ( val_3 - val_7 ) * 0.006 )

    # ④に係る控除額の計算
    val_10 = val_1 - val_5 - 10000000
    if val_10 < 0: val_10 = 0
    val_11 = val_4 - val_10
    if val_11 < 0: val_11 = 0 
    val_12_1 = math.ceil( val_11 * 0.008 )
    val_13_1 = math.ceil( ( val_4 - val_11 ) * 0.004 )
    val_12_2 = math.ceil( val_11 * 0.006 )
    val_13_2 = math.ceil( ( val_4 - val_11 ) * 0.003 )

    # ⑤に係る控除額の計算
    val_14 = val_1 - 10000000
    if val_14 < 0: val_14 = 0
    val_15 = val_5 - val_14
    if val_15 < 0: val_15 = 0 
    val_16_1 = math.ceil( val_15 * 0.004 )
    val_17_1 = math.ceil( ( val_5 - val_15 ) * 0.002 )
    val_16_2 = math.ceil( val_15 * 0.003 )
    val_17_2 = math.ceil( ( val_5 - val_15 ) * 0.0015 )
 
 
    #計算結果の保存
    res_1_1 = val_8_1 + val_9_1 + val_12_1 + val_13_1 + val_16_1 + val_17_1
    res_1_2 = val_8_2 + val_9_2 + val_12_2 + val_13_2 + val_16_2 + val_17_2
    st.session_state["d_haitokojyo_1"] = res_1_1  
    st.session_state["d_haitokojyo_2"] = res_1_2  
    #print(f"地方税 配当控除額市民税 res_1_1=:{res_1_1}")
    #print(f"地方税 配当控除額県民税 res_1_2=:{res_1_2}")


    #寄付金税額控除-----------( res_2_1, res_2_2 )
    #第一段階
    val_1 = int(st.session_state["a_skojyo29"])
    val_2 = ( st.session_state["g_gokeisyotoku"] * 0.3 )
    #print(f"第一段階 寄付金額 val_1=:{val_1}")
    #print(f"第一段階 地方税 寄付金上限額 総所得金額の30％ val_2=:{val_2}")
 
    val_3 = min ( val_1, val_2 )
    val_3 = val_3 - 2000
    if val_3 < 0:  val_3 = 0
    res_2_1 = math.ceil( val_3 * 0.06 )
    res_2_2 = math.ceil( val_3 * 0.04 )
    #print(f"第一段階計算 寄付金控除 市民税 res_2_1=:{res_2_1}")
    #print(f"第一段階計算 寄付金控除 県民税 res_2_2=:{res_2_2}")


    #第二段階
    val_1 = int(st.session_state["a_skojyo29"])
    
    val_2 = val_1 - 2000
    if val_2 < 0:  val_2 = 0
    val_3 = ( st.session_state["d_kazei78"] + st.session_state["d_kazei81"] + 
        st.session_state["d_kazei82"] - st.session_state["d_jinkjsagaku"] ) 
    match val_3:
        case n if n <0:           val_4 = 0.9
        case n if n <=1950000:    val_4 = 0.84895
        case n if n <=3300000:    val_4 = 0.7979 
        case n if n <=6950000:    val_4 = 0.6958
        case n if n <=9000000:    val_4 = 0.66517
        case n if n <=18000000:   val_4 = 0.56307
        case n if n <=40000000:   val_4 = 0.4916
        case _:                   val_4 = 0.44055
    val_5 = math.ceil( val_2 * val_4 )
    val_5_1 = math.ceil( val_5 * 3 / 5 )
    val_5_2 = math.ceil( val_5 * 2 / 5 )

    #第二段階の上限は、所得割の20％
    if val_5_1 > st.session_state["gd_szei_1"] * 0.2:
        val_5_1 = math.ceil( st.session_state["gd_szei_1"] * 0.2 )
    if val_5_2 > st.session_state["gd_szei_2"] * 0.2:
        val_5_2 = math.ceil( st.session_state["gd_szei_2"] * 0.2 )
    #print(f"第二段階計算 寄付金控除 市民税 val_5_1=:{val_5_1}")
    #print(f"第二段階計算 寄付金控除 県民税 val_5_2=:{val_5_2}")

    res_2_1 = res_2_1 + val_5_1
    res_2_2 = res_2_2 + val_5_2
    #print(f"計算 寄付金控除 市民税 res_2_1 =:{res_2_1}")
    #print(f"計算 寄付金控除 県民税 res_2_2 =:{res_2_2}")


    ##print(f"地方税 寄付金上限額 所得割の20％")
    #計算結果の保存
    st.session_state["d_kifukojyo_1"] = res_2_1  
    st.session_state["d_kifukojyo_2"] = res_2_2  
    #print(f"計算 寄付金控除実行額 市民税 res_2_1 =:{res_2_1}")
    #print(f"計算 寄付金控除実行額 県民税 res_2_2 =:{res_2_2}")

    return 'return zeigakukojyo'

def noufuszei():
#
#納付額（還付額）計算
#
    #所得割（算出所得割額-調整控除-税額控除(配当控除と寄付金控除)
    res_1_1 = ( st.session_state["gd_szei_1"]  - 
                st.session_state["d_tyoseikojyo_1"] - 
                st.session_state["d_haitokojyo_1"] - 
                st.session_state["d_kifukojyo_1"] )
    res_1_2 = ( st.session_state["gd_szei_2"] - 
                st.session_state["d_tyoseikojyo_2"] - 
                st.session_state["d_haitokojyo_2"] - 
                st.session_state["d_kifukojyo_2"] )

    if res_1_1 < 0 : res_1_1 = 0
    if res_1_2 < 0 : res_1_2 = 0
    if st.session_state["d_hikazei1"] == "非課税" : 
        res_1_1 = 0
        res_1_2 = 0

    #均等割
    if st.session_state["d_hikazei2"] == "非課税":
        res_2_1 = 0
        res_2_2 = 0
    else:
        res_2_1 = 3000
        res_2_2 = 2000

    #森林環境税
    if st.session_state["d_hikazei3"] == "非課税":
        res_3 = 0
    else:
        res_3 = 1000


    # ＊A 配当割額控除額・株式等譲渡所得割額控除額を市民税分と県民税分に分ける ( 源泉徴収税額 )
    res_4_1 = int (st.session_state["gd_gensentax"] * 3 / 5 )
    res_4_2 = st.session_state["gd_gensentax"] - res_4_1 

    # ＊B ( 所得割額 マイナス ＊A ) 
    res_5_1 = res_1_1 - res_4_1
    res_5_2 = res_1_2 - res_4_2
    # ＊B (-)の場合は所得割の還付   (+)の場合は所得割の納付( 納付の場合100円以下切捨て )
    if res_5_1 >=0:     res_5_1 = int( res_5_1 / 100 ) * 100
    if res_5_2 >=0:     res_5_2 = int( res_5_2 / 100 ) * 100

 
    #均等割を加えた市民税県民税合算の最終納付額（還付額）
    res_6 = res_5_1 + res_5_2 + res_2_1 + res_2_2 + res_3

   #計算結果の保存
    st.session_state["d_syotokuwari_1"] = res_1_1               
    st.session_state["d_syotokuwari_2"] = res_1_2
    st.session_state["d_kintowari_1"]   = res_2_1
    st.session_state["d_kintowari_2"]   = res_2_2
    st.session_state["d_kankyozei"]     = res_3
    st.session_state["d_warikojyo_1"]   = res_4_1
    st.session_state["d_warikojyo_2"]   = res_4_2
    st.session_state["gd_kakuteitax_1"] = res_5_1    
    st.session_state["gd_kakuteitax_2"] = res_5_2  
    st.session_state["gd_noufutax"]     = res_6


    #print(f"地方税 所得割 市民税額 res_1_1=:{res_1_1}")
    #print(f"地方税 所得割 県民税額 res_1_2=:{res_1_2}")
    #print(f"地方税 均等割 市民税額 res_2_1=:{res_2_1}")
    #print(f"地方税 均等割 県民税額 res_2_2=:{res_2_2}")
    #print(f"地方税 環境額 res_3=:{res_3}")
    #print(f"地方税 金融所得割額控除額 市民税額 res_4_1=:{res_4_1}")
    #print(f"地方税 金融所得割額控除額 県民税額 res_4_2=:{res_4_2}")
    #print(f"地方税 所得割 市民税額 確定税額 res_5_1=:{res_5_1}")
    #print(f"地方税 所得割 県民税額 確定税額 res_5_2=:{res_5_2}")
    #print(f"所得税 申告納税額 res_6=:{res_6}")
    
    return 'return noufuszei'


#地方税＿保険料控除　計算式1　(新保険料)
def keisansiki1(kval_1):
    kres_1 = 0

    match kval_1:
        case n if n <=12000:   kres_1 = kval_1
        case n if n <=32000:   kres_1 = math.ceil( kval_1 * 0.5 + 6000 )
        case n if n <=56000:   kres_1 = math.ceil( kval_1 * 0.25 + 14000 )
        case _:   kres_1 = 28000
    return kres_1

#地方税＿保険料控除　計算式2　(旧保険料)
def keisansiki2(kval_1):
    kres_1 = 0

    match kval_1:
        case n if n <=15000:   kres_1 = kval_1
        case n if n <=40000:   kres_1 = math.ceil( kval_1 * 0.5 + 7500 )
        case n if n <=70000:  kres_1 = math.ceil( kval_1 * 0.25 + 17500 )
        case _:  kres_1 = 35000
    return kres_1



#保険税(合計所得に対してかかる４月から翌年３月までの保険料)
def hokenzei(kval_1):
    #
    #保険計算応当日における年齢計算（何歳＋何ケ月）
    #
    # 加齢日が前日２４時基準(前日基準）)
    valw1 = tax_logic_s.nenreikeisan1( st.session_state["a_honnin_birthday"], "20260401", 2 )
    zenjitu_year = int( valw1 / 100 )
    zenjitu_month = valw1 - zenjitu_year * 100

    # 加齢日が誕生日当日基準（当日基準）
    valw1 = tax_logic_s.nenreikeisan2( st.session_state["a_honnin_birthday"], "20260401", 2 )
    tojitu_year = int( valw1 / 100 )
    tojitu_month = valw1 - tojitu_year * 100

    #
    #---------介護保険-----------(計算対象が zenjitu_year >= 64)
    #
    #  保険期間：4月から翌年3月　　
    #  保険開始：65歳の誕生日の前日を含む月の分から
    #  
    #  保険金額は合計所得による段階できまる（1～１３段階）
    #  ここでは一番下を段階６とする
    #  （段階１～５は、生活保護、非課税等の判断が必要のため）
    #
    valw1 = st.session_state["g_gokeisyotoku"] - 0

    if zenjitu_year >= 64:
        match valw1:
            case n if n < 1250000:  
                val_1 = 85500
            case n if n < 2000000: 
                val_1 = 94500
            case n if n < 3000000: 
                val_1 = 113500 
            case n if n < 5000000: 
                val_1 = 132400
            case n if n < 7000000: 
                val_1 = 143700
            case n if n < 10000000: 
                val_1 = 151300
            case n if n < 15000000: 
                val_1 = 174000 
            case _: 
                val_1 = 189100
    else:
        val_1 = 0

    #上限処理(上演オーバー額)
    val_1_over = 0

    #月割計算(本年度に65歳になる人、65歳の応答月から3月まで月割計算　前日基準で）
    val_1_tukiwari = 0
    val_1_tukisu   = 0
    if zenjitu_year >= 64:
        if zenjitu_year == 64:
            val_1_tukiwari = ( (val_1 - val_1_over) * zenjitu_month  / 12 )
            val_1_tukisu = zenjitu_month
        else:
            val_1_tukiwari = val_1 - val_1_over
            val_1_tukisu = 12
     
    #計算結果の保存
    st.session_state["h_kaigo_1"] = valw1              #介護保険_対象額
    st.session_state["h_kaigo_2"] = val_1              #介護保険_計算額
    st.session_state["h_kaigo_3"] = val_1_over         #介護保険_オーバー額
    st.session_state["h_kaigo_4_1"] = val_1_tukiwari   #介護保険_月割額
    st.session_state["h_kaigo_4_2"] = val_1_tukisu     #介護保険_月割月数


    #
    #---------国保-----------(計算対象が加入者 zenjitu_year <= 74)
    #
    #
    #  保険期間：4月から翌年3月
    #  国保の中身（以下の4つの課税額の合計）（さらに各々の課税額は、所得割＋均等割＋平等割額からなる）
    #       1．<基礎課税額>
    #       2．<後期高齢者支援金等課税額>
    #       3．<子供子育て支援納付金課税額>
    #       4．<介護納付金課税額>

    #  保険開始: 加入月から、ただし4．の介護納付金課税額は40歳の加齢月（前日基準）から
    #  保険終了: 75歳の加齢月（当日基準）の前月まで、
    #           ただし4．介護納付金課税額は65歳の加齢月（前日基準）の前月まで
    #

    valw1 = st.session_state["g_gokeisyotoku"] - 430000
    if valw1 < 0:    valw1 = 0 

    #基礎課税額               所得割:   val_2_1, 
    #                        均等割額：val_2_2, 平等割額: val_2_3
    #後期高齢者支援金等課税額   所得割:   val_3_1, 
    #                        均等割額：val_3_2, 平等割額: val_3_3
    #介護納付金課税額          所得割:   val_4_1, 
    #                        均等割額：val_4_2, 平等割額: val_4_3
    #子供子育て支援納付金課税額 所得割:   val_5_1, 
#                            均等割額：val_5_2, 平等割額: val_5_3


    if st.session_state["a_kokuho_1"] == "あり": 
        # 基礎課税額
        val_2_1 = int( valw1 * 0.079 / 100) * 100
        val_2_2 = 22700
        val_2_3 = 21400
    
        # 後期高齢者支援金等課税額
        val_3_1 = int( valw1 * 0.027 / 100) * 100
        val_3_2 = 8300
        val_3_3 = 6000

        # 介護納付金課税額
        val_4_1 = int( valw1 * 0.025 / 100) * 100
        val_4_2 = 7200
        val_4_3 = 6200

        # 子供子育て支援納付金課税額
        val_5_1 = int( valw1 * 0.0031 / 100) * 100
        val_5_2 = 1500
        val_5_3 = 800
    else:
        # 基礎課税額
        val_2_1 = 0
        val_2_2 = 0
        val_2_3 = 0
        # 後期高齢者支援金等課税額
        val_3_1 = 0
        val_3_2 = 0
        val_3_3 = 0
        # 介護納付金課税額
        val_4_1 = 0
        val_4_2 = 0
        val_4_3 = 0
        # 子供子育て支援納付金課税額
        val_5_1 = 0
        val_5_2 = 0
        val_5_3 = 0


    #上限処理(上演オーバー額)
    # 　基礎課税額上限 670000
    #   後期高齢者支援金等課税額上限 260000
    #   介護納付金課税額上限 170000
    #   子供子育て支援納付金課税額上限 30000
    val_2_over = 0 
    val_3_over = 0 
    val_4_over = 0 
    val_5_over = 0 
    
    val_2 = val_2_1 + val_2_2 + val_2_3
    val_3 = val_3_1 + val_3_2 + val_3_3
    val_4 = val_4_1 + val_4_2 + val_4_3
    val_5 = val_5_1 + val_5_2 + val_5_3

    if st.session_state["a_kokuho_1"] == "あり": 
        if val_2 > 670000:  val_2_over = val_2 -  670000 
        if val_3 > 260000:  val_3_over = val_3 -  260000 
        if val_4 > 170000:  val_4_over = val_4 -  170000 
        if val_5 > 30000:   val_5_over = val_5 -  30000 


    #介護納付金の月割計算（前日基準）
    val_4_tukiwari = 0
    val_4_tukisu   = 0
 
    if st.session_state["a_kokuho_1"] == "あり": 
        match zenjitu_year:
            case n if n < 39:  
                # 39歳未満は介護納付金課税額なし
                val_4_1 = 0
                val_4_2 = 0
                val_4_3 = 0
            
            case n if n == 39: 
                # 39歳は40歳の応答月より介護納付金課税額が発生(前日基準）)
                val_4_tukiwari = ( (val_4 - val_4_over) * zenjitu_month / 12 )
                val_4_tukisu = zenjitu_month

            case n if n == 64:
                # 64歳は65歳の応答月の前の月分まで（前日基準）
                val_4_tukiwari = ( (val_4 - val_4_over) * ( 12 - zenjitu_month ) / 12 )
                val_4_tukisu = 12 - zenjitu_month

            case n if n >= 65:
                # 65歳から介護保険制度に移行し介護給付金課税額はなし（前日基準）
                val_4_1 = 0
                val_4_2 = 0
                val_4_3 = 0
            case _: 
                val_4_tukiwari = val_4 - val_4_over
                val_4_tukisu = 12
            


    #介護納付金以外の月割計算（当日基準）
    #（基礎課税額,後期高齢者支援金等課税額,子供子育て支援納付金課税額）
    val_235_tukiwari = 0
    val_235_tukisu   = 0

    if st.session_state["a_kokuho_1"] == "あり": 
        match tojitu_year:
            # 74歳は75歳の応答月の前の月分まで（当日基準）
            case n if n == 74:
                val_235_tukiwari = ( (( val_2 + val_3 + val_5 ) - 
                    ( val_2_over + val_3_over + val_5_over )) * (12 - tojitu_month ) / 12 
                )
                val_235_tukisu = 12 - tojitu_month

            # 75歳の応答月より後期高齢者医療保険に移行し、国保分はなし（当日基準）
            case n if n >= 75:
                # 基礎課税額
                val_2_1 = 0
                val_2_2 = 0
                val_2_3 = 0
                # 後期高齢者支援金等課税額
                val_3_1 = 0
                val_3_2 = 0
                val_3_3 = 0
                # 子供子育て支援納付金課税額
                val_5_1 = 0
                val_5_2 = 0
                val_5_3 = 0
            case _: 
                val_235_tukiwari = (
                    ( val_2 + val_3 + val_5 ) - ( val_2_over + val_3_over + val_5_over )
                    )
                val_235_tukisu = 12


    #計算結果の保存
    st.session_state["h_kokuho_1"] = valw1   #国保_対象額
    st.session_state["h_kokuho_2_1_1"] = val_2_1   #国保_基礎課税額_所得割額
    st.session_state["h_kokuho_2_1_2"] = val_2_2   #国保_基礎課税額_均等割額
    st.session_state["h_kokuho_2_1_3"] = val_2_3   #国保_基礎課税額_平等割額
    st.session_state["h_kokuho_2_1"] = val_2       #国保_基礎課税額合計

    st.session_state["h_kokuho_2_2_1"] = val_3_1   #国保_後期高齢者支援金等課税額_所得割額
    st.session_state["h_kokuho_2_2_2"] = val_3_2   #国保_後期高齢者支援金等課税額_均等割額
    st.session_state["h_kokuho_2_2_3"] = val_3_3   #国保_後期高齢者支援金等課税額_平等割額
    st.session_state["h_kokuho_2_2"] = val_3       #国保_後期高齢者支援金等課税額合計

    st.session_state["h_kokuho_2_3_1"] = val_4_1   #国保_介護納付金課税額_所得割額
    st.session_state["h_kokuho_2_3_2"] = val_4_2   #国保_介護納付金課税額_均等割額
    st.session_state["h_kokuho_2_3_3"] = val_4_3   #国保_介護納付金課税額_平等割額
    st.session_state["h_kokuho_2_3"] = val_4       #国保_介護納付金課税額合計

    st.session_state["h_kokuho_2_4_1"] = val_5_1   #国保_子供子育て支援納付金課税額_所得割額
    st.session_state["h_kokuho_2_4_2"] = val_5_2   #国保_子供子育て支援納付金課税額_均等割額
    st.session_state["h_kokuho_2_4_3"] = val_5_3   #国保_子供子育て支援納付金課税額_平等割額
    st.session_state["h_kokuho_2_4"] = val_5       #国保_子供子育て支援納付金課税額合計
 
    st.session_state["h_kokuho_3_1"] = val_2_over  #国保_オーバー額_基礎課税額
    st.session_state["h_kokuho_3_2"] = val_3_over  #国保_オーバー額_後期高齢者支援金等課税額
    st.session_state["h_kokuho_3_3"] = val_4_over  #国保_オーバー額_介護納付金課税額
    st.session_state["h_kokuho_3_4"] = val_5_over  #国保_オーバー額_子供子育て支援納付金課税額
    st.session_state["h_kokuho_4_124_1"] = val_235_tukiwari   #国保_月割額_介護納付金以外
    st.session_state["h_kokuho_4_124_2"] = val_235_tukisu     #国保_月割月数_介護納付金以外
    st.session_state["h_kokuho_4_3_1"] = val_4_tukiwari       #国保_月割額_介護納付金
    st.session_state["h_kokuho_4_3_2"] = val_4_tukisu         #国保_月割月数_介護納付金
    
    #
    #---------後期高齢者医療制度-----------(計算対象が tojitu_year >= 74)
    #
    #  計算の基礎となる所得額に料率をかける所得割と均等割額がある保険
    #  保険期間：4月から翌年3月　　
    #  保険開始：75歳の誕生月分から(当日基準)
    #
    #   医療分  所得割: val_6_1, 均等割額：val_6_2
    #   子供分　所得割: val_7_1, 均等割額：val_7_2
    #

    valw1 = st.session_state["g_gokeisyotoku"] - 430000
    if valw1 < 0:    valw1 = 0 

    if tojitu_year >= 74:
        # 医療分
        val_6_1 = int ( valw1 * 0.0924 )
        val_6_2 = 49000
        # 子供分
        val_7_1 = int ( valw1 * 0.0025 )
        val_7_2 = 1400
    else:
        val_6_1 = 0
        val_6_2 = 0
        val_7_1 = 0
        val_7_2 = 0


    #上限処理(上演オーバー額)
    #   年間保険料上限(医療分＋子供分） 871000 
    val_6_over = 0 
    val_7_over = 0 

    val_6 = val_6_1 + val_6_2 
    val_7 = val_7_1 + val_7_2 

    if val_6  > 850000:  val_6_over = val_6 -  850000 
    if val_7  > 21000:   val_7_over = val_7 -  21000 
    
    #月割計算（当日基準）
    val_67_tukiwari = 0
    val_67_tukisu   = 0 

    if tojitu_year == 74:
        val_67_tukiwari = ( 
            int ((( val_6 - val_6_over ) * tojitu_month / 12 ) / 100 ) * 100 + 
            int ((( val_7 - val_7_over ) * tojitu_month / 12 ) / 100 ) * 100 
            )
        val_67_tukisu = tojitu_month
    else:
        if tojitu_year >= 75: 
            val_67_tukiwari = ( 
                int ((val_6 - val_6_over)/ 100 ) * 100 + 
                int (( val_7 - val_7_over)/ 100 ) * 100
            )
            val_67_tukisu = 12


    #計算結果の保存
    st.session_state["h_korei_1"] = valw1                 #後期高齢者医療制度_対象額
    st.session_state["h_korei_2_1"] = val_6_1 + val_6_2   #後期高齢者医療制度_計算額_医療分
    st.session_state["h_korei_2_2"] = val_7_1 + val_7_2   #後期高齢者医療制度_計算額_子供分
    st.session_state["h_korei_3_1"] = val_6_over          #後期高齢者医療制度_オーバー額_医療分
    st.session_state["h_korei_3_2"] = val_7_over          #後期高齢者医療制度_オーバー額_子供分
    st.session_state["h_korei_4_1"] = val_67_tukiwari     #後期高齢者医療制度_月割額
    st.session_state["h_korei_4_2"] = val_67_tukisu       #後期高齢者医療制度_月割月数

    #print(f"介護保険 対象額=:{st.session_state["h_kaigo_1"]}")
    #print(f"介護保険 計算額=:{st.session_state["h_kaigo_2"]}")
    #print(f"介護保険 オーバー=:{st.session_state["h_kaigo_3"]}")
    #print(f"介護保険 月割額=:{st.session_state["h_kaigo_4_1"]}")
    #print(f"介護保険 月数=:{st.session_state["h_kaigo_4_2"]}")

    #print(f"国保_対象額=:{st.session_state["h_kokuho_1"]}")
    #print(f"国保_基礎課税額 所得割額=:{st.session_state["h_kokuho_2_1_1"]}")
    #print(f"国保_基礎課税額 均等割額=:{st.session_state["h_kokuho_2_1_2"]}") 
    #print(f"国保_基礎課税額 平等割額=:{st.session_state["h_kokuho_2_1_3"]}")

    #print(f"国保_後期高齢者支援金等課税額 所得割額=:{st.session_state["h_kokuho_2_2_1"]}")
    #print(f"国保_後期高齢者支援金等課税額 均等割額=:{st.session_state["h_kokuho_2_2_2"]}") 
    #print(f"国保_後期高齢者支援金等課税額 平等割額=:{st.session_state["h_kokuho_2_2_3"]}")

    #print(f"国保_介護納付金課税額 所得割額=:{st.session_state["h_kokuho_2_3_1"]}")
    #print(f"国保_介護納付金課税額 均等割額=:{st.session_state["h_kokuho_2_3_2"]}") 
    #print(f"国保_介護納付金課税額 平等割額=:{st.session_state["h_kokuho_2_3_3"]}")

    #print(f"国保_子供子育て支援納付金課税額 所得割額=:{st.session_state["h_kokuho_2_4_1"]}")
    #print(f"国保_子供子育て支援納付金課税額 均等割額=:{st.session_state["h_kokuho_2_4_2"]}") 
    #print(f"国保_子供子育て支援納付金課税額 平等割額=:{st.session_state["h_kokuho_2_4_3"]}")

    #print(f"国保_オーバー分 基礎課税額=:{st.session_state["h_kokuho_3_1"]}")
    #print(f"国保_オーバー分 後期高齢者支援金等課税額=:{st.session_state["h_kokuho_3_2"]}") 
    #print(f"国保_オーバー分 介護納付金課税額=:{st.session_state["h_kokuho_3_3"]}")
    #print(f"国保_オーバー分 子供子育て支援納付金課税額=:{st.session_state["h_kokuho_3_3"]}")

    #print(f"国保_介護納付金以外 月割額=:{st.session_state["h_kokuho_4_124_1"]}")
    #print(f"国保_介護納付金以外 月数=:{st.session_state["h_kokuho_4_124_2"]}")
    #print(f"国保_介護納付金 月割額=:{st.session_state["h_kokuho_4_3_1"]}")
    #print(f"国保_介護納付金 月数=:{st.session_state["h_kokuho_4_3_2"]}")

    #print(f"後期高齢者医療制度 対象額=:{st.session_state["h_korei_1"]}") 
    #print(f"後期高齢者医療制度 計算額医療分=:{st.session_state["h_korei_2_1"]}")
    #print(f"後期高齢者医療制度 計算額子供分=:{st.session_state["h_korei_2_2"]}")
    #print(f"後期高齢者医療制度 オーバー医療分=:{st.session_state["h_korei_3_1"]}")
    #print(f"後期高齢者医療制度 オーバー子供分=:{st.session_state["h_korei_3_2"]}")
    #print(f"後期高齢者医療制度 月割額=:{st.session_state["h_korei_4_1"]}")
    #print(f"後期高齢者医療制度 月数=:{st.session_state["h_korei_4_2"]}")
    return 'return hokenzei'




    
 






 

    









 
