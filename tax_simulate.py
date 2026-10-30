# tax_simulate.py

import streamlit as st
import importlib
#import datetime
import tax_logic_s 
import tax_logic_t 
import tax_csv_dialog

importlib.reload(tax_logic_s)
importlib.reload(tax_logic_t)
importlib.reload(tax_csv_dialog)

# --- タブのデザインをカスタマイズするCSS ---
st.markdown(
    """
    <style>
    /* 1. タブの並んでいる全体の背景と余白（角丸のグレーの枠にする場合） */
    div[data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #e9ecef;
    }

    /* 2. 各タブボタンの基本スタイル（非選択時） */
    button[data-baseweb="tab"] {
        height: 42px;
        background-color: #ffffff;
        border-radius: 6px;
        border: 1px solid #ced4da;
        color: #495057;
        font-weight: 500;
        padding: 0 20px;
        transition: all 0.2s ease;
    }

    /* 3. 選択されている（アクティブな）タブのスタイル */
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #0068c4 !important; /* 鮮やかな青色（お好みで変更可能） */
        color: #ffffff !important;            /* 文字色を白に */
        font-weight: bold !important;         /* 太字にする */
        border: 1px solid #00539f !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1); /* 軽く影をつけて浮き上がらせる */
    }

    /* 4. マウスを乗せたとき（ホバー時）のスタイル */
    button[data-baseweb="tab"]:hover {
        background-color: #e2e6ea;
        color: #212529;
    }
    
    /* 選択中にマウスを乗せたときは青を維持 */
    button[data-baseweb="tab"][aria-selected="true"]:hover {
        background-color: #00539f !important;
        color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
#-------------------------------------------------------------------

# --- st.text_inputの（全体の共通設定 ＋ 特定の項目だけの個別設定）をまとめたCSS 
st.markdown(
    """
    <style>
    /* ══════════════════════════════════════════════════════════
       1. 【全体用】すべての st.text_input に共通させたいデザイン
       ══════════════════════════════════════════════════════════ */
    
    /* (1). st.text_input の「ラベル（項目名）」の文字を大きく・太くする */
    .stTextInput label p {
        font-size: 16px !important;
    #    font-weight: bold !important;
        color: #0068c4 !important; /* ラベルの色（青系） */
    }

    /* (2). 通常の入力欄の中の文字サイズ */
    .stTextInput input {
        font-size: 16px !important;
    }

    /* (3). 【重要】計算結果などの「読み取り専用（disabled=True）」の入力欄 */
    .stTextInput input:disabled {
        background-color: #fffacd !important; /* 背景色：薄い黄色 */
        color: #d9534f !important;            /* 中の数字の色：赤系 */
        font-size: 16px !important;           /* 数字を大きく！ 20PX---->16PX*/
        font-weight: bold !important;         /* 太字にする！ */
        -webkit-text-fill-color: #d9534f !important; /* ブラウザによって色が消えるのを防ぐおまじない */
    }

    /* ══════════════════════════════════════════════════════════
       2. 【個別用】特定のラベル名を持つ st.text_input だけ変える設定
          ※ "合計税額 (円)" の部分をご自身のテキストボックスのラベル名に変更してください
       ══════════════════════════════════════════════════════════ */

    /* ① 指定したラベルの文字部分に背景色をつける */
    #div.stTextInput:has(input[aria-label="要納付額"]) label p {
    #    background-color: #e8f4fd !important; /* 薄い青の背景色 */
    #    padding: 4px 8px !important;         /* ラベル周りの余白 */
    #    border-radius: 4px !important;       /* 角を少し丸くする */
    #    color: #084298 !important;           /* 文字の色（濃い青） */
    #    display: inline-block;               /* 背景を文字の長さに合わせる */
    #}

    /* ② 指定したテキストエリアに枠線と背景をつける */
    div.stTextInput:has(input[aria-label="要納付額"]) input {
        border: 2px solid #d9534f !important; /* しっかりした赤い枠線 青(#0068c4)*/
        #background-color: #f8f9fa !important; /* テキストエリアの背景色 */
        font-weight: bold !important;         /* 太字にする */
    }
    div.stTextInput:has(input[aria-label="合 計 所 得 G10"]) input {
        border: 2px solid #d9534f !important; /* しっかりした赤い枠線 青(#0068c4)*/
        #background-color: #f8f9fa !important; /* テキストエリアの背景色 */
        font-weight: bold !important;         /* 太字にする */
    }
    div.stTextInput:has(input[aria-label="控除合計 J10"]) input {
        border: 2px solid #d9534f !important; /* しっかりした赤い枠線 青(#0068c4)*/
        #background-color: #f8f9fa !important; /* テキストエリアの背景色 */
        font-weight: bold !important;         /* 太字にする */
    }
    div.stTextInput:has(input[aria-label="総合課税所得 T1"]) input {
        border: 2px solid #d9534f !important; /* しっかりした赤い枠線 青(#0068c4)*/
        #background-color: #f8f9fa !important; /* テキストエリアの背景色 */
        font-weight: bold !important;         /* 太字にする */
    }
    div.stTextInput:has(input[aria-label="分離課税所得 T2"]) input {
        border: 2px solid #d9534f !important; /* しっかりした赤い枠線 青(#0068c4)*/
        #background-color: #f8f9fa !important; /* テキストエリアの背景色 */
        font-weight: bold !important;         /* 太字にする */
    }  
    div.stTextInput:has(input[aria-label="確定所得税 Z7"]) input {
        border: 2px solid #d9534f !important; /* しっかりした赤い枠線 青(#0068c4)*/
        #background-color: #f8f9fa !important; /* テキストエリアの背景色 */
        font-weight: bold !important;         /* 太字にする */
    }  
    div.stTextInput:has(input[aria-label="申告納付額 Z9(-は還付)"]) input {
        border: 2px solid #d9534f !important; /* しっかりした赤い枠線 青(#0068c4)*/
        #background-color: #f8f9fa !important; /* テキストエリアの背景色 */
        font-weight: bold !important;         /* 太字にする */
    }  
    div.stTextInput:has(input[aria-label="控除合計 J19"]) input {
        border: 2px solid #d9534f !important; /* しっかりした赤い枠線 青(#0068c4)*/
        #background-color: #f8f9fa !important; /* テキストエリアの背景色 */
        font-weight: bold !important;         /* 太字にする */
    }
    div.stTextInput:has(input[aria-label="総合課税所得 T11"]) input {
        border: 2px solid #d9534f !important; /* しっかりした赤い枠線 青(#0068c4)*/
        #background-color: #f8f9fa !important; /* テキストエリアの背景色 */
        font-weight: bold !important;         /* 太字にする */
    }
    div.stTextInput:has(input[aria-label="分離課税所得 T12"]) input {
        border: 2px solid #d9534f !important; /* しっかりした赤い枠線 青(#0068c4)*/
        #background-color: #f8f9fa !important; /* テキストエリアの背景色 */
        font-weight: bold !important;         /* 太字にする */
    }
    div.stTextInput:has(input[aria-label="確定所得割Z19"]) input {
        border: 2px solid #d9534f !important; /* しっかりした赤い枠線 青(#0068c4)*/
        #background-color: #f8f9fa !important; /* テキストエリアの背景色 */
        font-weight: bold !important;         /* 太字にする */
    }
    div.stTextInput:has(input[aria-label="確定所得割Z29"]) input {
        border: 2px solid #d9534f !important; /* しっかりした赤い枠線 青(#0068c4)*/
        #background-color: #f8f9fa !important; /* テキストエリアの背景色 */
        font-weight: bold !important;         /* 太字にする */
    }
    div.stTextInput:has(input[aria-label="申告納付額Z33(-は還付)"]) input {
        border: 2px solid #d9534f !important; /* しっかりした赤い枠線 青(#0068c4)*/
        #background-color: #f8f9fa !important; /* テキストエリアの背景色 */
        font-weight: bold !important;         /* 太字にする */
    }
  
    </style>
    """,
    unsafe_allow_html=True,
)

#--------------------------------------------------------------------

if "b_syotoku1" not in st.session_state:

#   変数_入力項目
    st.session_state["a_honnin_sex"] = " "
    st.session_state["a_honnin_birthday"] = " "
    st.session_state["a_honnin_kafu"] = " "
    st.session_state["a_honnin_syogai"] = " "
    st.session_state["a_honnin_haigu"] = " "

    st.session_state["a_haigu_birthday"] = " "
    st.session_state["a_haigu_syogai"] = " "
    st.session_state["a_haigu_syotoku"] = "0"
   
    st.session_state["a_kyuyo"] = "0"
    st.session_state["a_kyuyo_gen"] = "0"
    st.session_state["a_nenkin"] = "0" 
    st.session_state["a_nenkin_gen"] = "0"
    st.session_state["a_jigyo"] = "0"
    st.session_state["a_jigyo_cost"] = "0"

    for i in range(3):
        st.session_state[f"a_syokenname_{i}"] = " "
    
        st.session_state[f"a_jyoto_{i}"] = "0"
        st.session_state[f"a_jyotostax_{i}"] = "0"
        st.session_state[f"a_jyotottax_{i}"] = "0"
        st.session_state[f"a_jyotoselect_{i}"] = " "
    
        st.session_state[f"a_haitou4_{i}"] = "0" 
        st.session_state[f"a_haitou5_{i}"] = "0" 
        st.session_state[f"a_haitou6_{i}"] = "0" 
        st.session_state[f"a_haitou7_{i}"] = "0" 
        st.session_state[f"a_haitou8_{i}"] = "0" 
        st.session_state[f"a_haitou9stax_{i}"] = "0"
        st.session_state[f"a_haitou9ttax_{i}"] = "0"
        st.session_state[f"a_haitou9select_{i}"] = " "
        
        st.session_state[f"a_haitou10_{i}"] = "0"
        st.session_state[f"a_haitou11_{i}"] = "0"
        st.session_state[f"a_haitou12_{i}"] = "0"
        st.session_state[f"a_haitou13_{i}"] = "0"
        st.session_state[f"a_haitou14_{i}"] = "0"
        st.session_state[f"a_haitou15stax_{i}"] = "0"
        st.session_state[f"a_haitou15ttax_{i}"] = "0"
        st.session_state[f"a_haitou15select_{i}"] = " "
        st.session_state[f"g_haitou9_{i}"] = 0 
        st.session_state[f"g_haitou15_{i}"] = 0

    st.session_state["a_hoken13"] = "0"
    st.session_state["a_hoken15_1"] = "0"
    st.session_state["a_hoken15_2"] = "0"
    st.session_state["a_hoken15_3"] = "0"
    st.session_state["a_hoken15_4"] = "0"
    st.session_state["a_hoken15_5"] = "0"
    st.session_state["a_hoken16_1"] = "0"
    st.session_state["a_hoken16_2"] = "0"
    st.session_state["a_skojyo28_1"] = "0"
    st.session_state["a_skojyo28_2"] = "0"
    st.session_state["a_skojyo28_3"] = "0"
    st.session_state["a_skojyo28_4"] = "0"
    st.session_state["a_skojyo29"] = "0"  

    st.session_state["a_kokuho_1"] = " "
    st.session_state["a_kokuho_2"] = "0"  
    st.session_state["a_kokuho_3"] = " "
    st.session_state["a_kokuho_4"] = "0"  


#   変数_所得税額の計算項目
    st.session_state["b_honnin_age"] = 0
    st.session_state["b_haigu_age"] = 0

    st.session_state["b_syotoku1"] = 0
    st.session_state["b_syotoku6"] = 0
    st.session_state["b_syotoku6_tyosei"] = 0
    st.session_state["b_syotoku7"] = 0

    st.session_state["b_syotoku73"] = 0
    st.session_state["b_syotoku74"] = 0
    st.session_state["b_syotoku5"]  = 0
    st.session_state["b_haitokojyo_1"] = 0
    st.session_state["b_haitokojyo_2"] = 0
    st.session_state["b_haitokojyo_3"] = 0
    st.session_state["g_gensentax"] = 0
    st.session_state["gd_gensentax"] = 0
    st.session_state["g_sogosyotoku"] = 0
    st.session_state["g_bunrisyotoku"] = 0
    st.session_state["g_gokeisyotoku"] = 0

    st.session_state["b_skojyo13"] = 0
    st.session_state["b_skojyo15"] = 0
    st.session_state["b_skojyo16"] = 0
    st.session_state["b_skojyo17"] = 0
    st.session_state["b_skojyo19"] = 0
    st.session_state["b_kubun1"] = " "
    st.session_state["b_kubun2"] = " "
    st.session_state["b_skojyo21_kubun"] = " "
    st.session_state["b_skojyo21"] = 0
    st.session_state["b_skojyo25"] = 0
    st.session_state["b_skojyo28_kubun"] = " "
    st.session_state["b_skojyo28"] = 0
    st.session_state["b_skojyo29"] = 0
    st.session_state["g_syotokukojyo"] = 0

    st.session_state["b_kazei78"] = 0
    st.session_state["b_kazei81"] = 0
    st.session_state["b_kazei82"]  = 0

    st.session_state["b_szei86"] = 0
    st.session_state["b_szei89"] = 0
    st.session_state["b_szei90"]  = 0
    st.session_state["g_szei"] = 0

    st.session_state["b_haitokojyo"] = 0

    st.session_state["b_szei44"] = 0
    st.session_state["b_szei45"] = 0
    st.session_state["g_kakuteitax"] = 0
    st.session_state["g_noufutax"] = 0




#   変数_地方税額計算項目
    st.session_state["d_hikazei1"] = " "
    st.session_state["d_hikazei2"] = " "
    st.session_state["d_hikazei3"] = " "
    
    st.session_state["d_skojyo13"] = 0
    st.session_state["d_skojyo15"] = 0
    st.session_state["d_skojyo16"] = 0
    st.session_state["d_skojyo17"] = 0
    st.session_state["d_skojyo19"] = 0

    st.session_state["d_skojyo21"] = 0
    st.session_state["d_skojyo21_kubun"] = " "
    st.session_state["d_skojyo25"] = 0
    st.session_state["d_skojyo28"] = 0
    st.session_state["d_skojyo28_kubun"] = " "

    st.session_state["gd_syotokukojyo"] = 0
 
    st.session_state["d_kazei78"] = 0
    st.session_state["d_kazei81"] = 0
    st.session_state["d_kazei82"] = 0

    st.session_state["d_szei86_1"] = 0
    st.session_state["d_szei86_2"] = 0
    st.session_state["d_szei89&90_1"] = 0
    st.session_state["d_szei89&90_2"] = 0
    st.session_state["gd_szei_1"] = 0
    st.session_state["gd_szei_2"] = 0
 
    st.session_state["d_jinkjsagaku"] = 0
    st.session_state["d_tyoseikojyo_1"] = 0
    st.session_state["d_tyoseikojyo_2"] = 0
    st.session_state["d_haitokojyo_1"] = 0
    st.session_state["d_haitokojyo_2"] = 0

    st.session_state["d_kifukojyo_1"] = 0 
    st.session_state["d_kifukojyo_2"] = 0

    st.session_state["d_syotokuwari_1"] = 0
    st.session_state["d_syotokuwari_2"] = 0
    st.session_state["d_kintowari_1"] = 0
    st.session_state["d_kintowari_2"] = 0

    st.session_state["d_kankyozei"] = 0
    st.session_state["d_warikojyo_1"] = 0
    st.session_state["d_warikojyo_2"] = 0
    st.session_state["gd_kakuteitax_1"] = 0
    st.session_state["gd_kakuteitax_2"] = 0
    st.session_state["gd_noufutax"] = 0

    st.session_state["h_kokuho_1"] = 0
    st.session_state["h_kokuho_2_1"] = 0
    st.session_state["h_kokuho_2_2"] = 0
    st.session_state["h_kokuho_2_3"] = 0
    st.session_state["h_kokuho_2_4"] = 0
    st.session_state["h_kokuho_3_1"] = 0
    st.session_state["h_kokuho_3_2"] = 0
    st.session_state["h_kokuho_3_3"] = 0
    st.session_state["h_kokuho_3_4"] = 0
    st.session_state["h_kokuho_4_124_1"] = 0
    st.session_state["h_kokuho_4_124_2"] = 0
    st.session_state["h_kokuho_4_3_1"] = 0
    st.session_state["h_kokuho_4_3_2"] = 0
    st.session_state["h_kaigo_1"] = 0
    st.session_state["h_kaigo_2"] = 0
    st.session_state["h_kaigo_3"] = 0
    st.session_state["h_kaigo_4_1"] = 0
    st.session_state["h_kaigo_4_2"] = 0
    st.session_state["h_korei_1"] = 0
    st.session_state["h_korei_2_1"] = 0
    st.session_state["h_korei_2_2"] = 0
    st.session_state["h_korei_3_1"] = 0
    st.session_state["h_korei_3_2"] = 0
    st.session_state["h_korei_4_1"] = 0
    st.session_state["h_korei_4_2"] = 0

#print("init_val実行")


#   
#   入力された文字（全角やカンマ付き）を安全に数値に変換する関数
#   st.text_input、st.radio

#   def check_input()    整数値のチェックなし
#   def check_inputx()   整数値のチェックあり
#
def check_input(target_key):
    #
    #入力された文字（全角やカンマ付き）を安全に数値に変換する関数(整数値のチェックなし)
    #
    text_val = st.session_state[target_key]
    if not text_val:  # もし入力欄が空っぽ（Backspaceで全部消された）なら0にする
       st.session_state[target_key] = "0"
       return "0"
    try:
        # カンマ（半角・全角）を取り除く
        clean_text = text_val.replace(',', '').replace('，', '')
        # 整数に変換（全角数字も自動で半角になります）
        st.session_state[target_key] = str(int(clean_text))
    except ValueError:
        st.session_state[target_key] = "0"  # 万が一、あいうえお等の文字が入ったら0として扱う


def check_inputx(target_key, chk):
    #
    #入力された文字（全角やカンマ付き）を安全に数値に変換する関数(整数値のチェックあり)
    # chk="+"    プラスの整数のみ
    # chk="+-"   プラスマイナスの整数
    #
    text_val = st.session_state[target_key]
    if not text_val:  # もし入力欄が空っぽ（Backspaceで全部消された）なら0にする
       st.session_state[target_key] = "0"
       return "0"
    try:
        # カンマ（半角・全角）を取り除く
        clean_text = text_val.replace(',', '').replace('，', '')
        # 整数に変換（全角数字も自動で半角になります）
        clean_val = int(clean_text)
        # プラスの整数のみOKの場合のチェック
        if chk == "+":
            if clean_val < 0: clean_val = 0
        
        st.session_state[target_key] = str(clean_val)
    except ValueError:
        # 万が一、あいうえお等の文字が入ったら0として扱う
        # 小数点が含まれていたら0として扱う

        st.session_state[target_key] = "0" 

def haigu_init():
    if  st.session_state["a_honnin_haigu"] == "あり":
        if st.session_state["a_honnin_sex"] == "男": 
            st.session_state["a_haigu_sex"] = "女"
        else:
            st.session_state["a_haigu_sex"] = "男"
    else:
        st.session_state["a_haigu_sex"] = " " 
        st.session_state["a_haigu_birthday"] = " "
        st.session_state["b_haigu_age"] = " "
        st.session_state["a_haigu_syogai"] = " "  
        st.session_state["a_haigu_syotoku"] = "0"

#　
def keisan():
    #print(f"メイン  tax_logic_s: -----------開始")
    kval = tax_logic_s.nenreikeisan1(st.session_state["a_honnin_birthday"], "20251231", 1)
    st.session_state["b_honnin_age"] = kval

    if st.session_state["a_honnin_haigu"] == "あり":
        kval = tax_logic_s.nenreikeisan1(st.session_state["a_haigu_birthday"], "20251231", 2)
        st.session_state["b_haigu_age"] = kval


    
    k1 = tax_logic_s.syotokukingaku1()
        #print(f"メイン  tax_logic_s: {k1}")
    k1 = tax_logic_s.syotokukingaku2()
        #print(f"メイン  tax_logic_s: {k1}")
    k1 = tax_logic_s.syotokugoukei()
        #print(f"メイン  tax_logic_s: {k1}")
    k1 = tax_logic_s.syotokukojyo()
        #print(f"メイン  tax_logic_s: {k1}")
    k1 = tax_logic_s.kazeisyotoku()
        #print(f"メイン  tax_logic_s: {k1}")
    k1 = tax_logic_s.szeikeisan()
        #print(f"メイン  tax_logic_s: {k1}")    
    k1 = tax_logic_s.haitokojyo()
        #print(f"メイン  tax_logic_s: {k1}")
    k1 = tax_logic_s.noufuszei()
        #print(f"メイン  tax_logic_s: -----------終了")
        #print("-----------")
        #print(f"メイン  tax_logic_t: -----------開始")
    k1 = tax_logic_t.hikazeihantei()
        #print(f"メイン  tax_logic_t: {k1}")
    k1 = tax_logic_t.syotokukojyo()
        #print(f"メイン  tax_logic_t: {k1}")
    k1 = tax_logic_t.kazeisyotoku()
        #print(f"メイン  tax_logic_t: {k1}")
    k1 = tax_logic_t.szeikeisan()
        #print(f"メイン  tax_logic_t: {k1}")
    k1 = tax_logic_t.tyoseikojyo()
        #print(f"メイン  tax_logic_t: {k1}")
    k1 = tax_logic_t.zeigakukojyo()
        #print(f"メイン  tax_logic_t: {k1}")
    k1 = tax_logic_t.noufuszei()
        #print(f"メイン  tax_logic_t: {k1}")
    k1 = tax_logic_t.hokenzei(st.session_state["a_honnin_birthday"])
        #print(f"メイン  tax_logic_t: {k1}")
        #print(f"メイン  tax_logic_t: -----------終了")

    return "ok"


# セッションステートにログイン状態を保存
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔒 ログイン画面")
    #password = st.text_input("認証コードを入力してください", type="password")
    password = st.text_input("認証コードを入力してください")
    if st.button("ログイン"):
        # あらかじめ決めたパスワード（例: "family2026" など）と照合
        if password == "taxtest20261030":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("認証コードが違います。")
    st.stop()  # ログインするまでは以降のコードを実行しない


#
# ── ここから下が本来の税金計算アプリのコード ──
#


# サイドバーに免責事項を常に表示する
with st.sidebar:
    st.markdown("### 📝 このシュミレーターの対象")
    st.caption(
        "扶養者がいないか扶養者は配偶者のみで、年金、給与、金融所得と事業収入以外の所得がない方。"
        "特に、源泉徴収された金融所得があり、申告することで納税額及び保険の基礎となる合計所得を知りたい方です。"
    )        
    st.write("---")

    # このボタンを押すと CSV処理の別ウィンドウ（ダイアログ）が開きます
    if st.button("📁 CSVの入出力", key="btn1", use_container_width=True):
          tax_csv_dialog.show_csv_modal()

    resultx = st.button("計算（再計算）する", key="btn5",use_container_width=True, on_click = keisan)

    st.write("---")


    # 1. 免責事項
    st.markdown("### 📌 ご利用上の注意（免責事項）")
    st.caption(
        "本システムは個人の税額試算を補助するためのものであり、"
        "その正確性・完全性を完全に保証するものではありません。\n\n"
        "実際の申告にあたっては、必ずご自身の責任において"
        "税務署や専門家にご確認ください。"
    )

    st.markdown("---")  # 区切り線

    # 2. 著作権表示（Copyright）
    # ※ [あなたの名前やペンネーム] の部分はご自身の名前に書き換えてください
    st.markdown(
        "<p style='text-align: center; color: gray; font-size: 12px;'>"
        "© 2026 T.SAKUMA <br> "
        "All rights reserved. 無断転載を禁ずる"
        "</p>",
        unsafe_allow_html=True,
    )




# --- 0．ヘッダー & CSVポップアップ起動ボタン ---
st.caption("画面の日本語が不自然な場合は、ブラウザの自動翻訳機能を「オフ」にしてください。")

st.title("🧮 確定申告シミュレーター", anchor=False)

head_col1, head_col2,head_col3 = st.columns([1, 1, 2])
with head_col1:
    st.markdown("     ")
with head_col2:
    st.markdown("     ")
with head_col3:

    with st.popover("ℹ️ 確定申告シュミレーターの操作方法"):
         st.markdown("#### 📝 確定申告シュミレーターの操作方法")
         st.write("1、画面の流れに沿って、1、基本情報の入力　～　3、所得控除の入力　迄入力します。")
         st.write("2、入力待ちの項目は入力枠が赤色です。入力してTABキーを押すと次の項目に移動します。")
         st.write("3、入力が完了したら、左サイドバーの[計算（再計算）する]ボタンを押します。計算結果は＜＜計算結果のサマリー＞＞以降に表示されます。")
         st.write("4、入力を修正したら、必ず[計算（再計算）する]ボタンを押して再計算を実行して下さい。")
         st.write("5、入力内容を保存したい場合は、[ＣＳＶの入出力]ボタンを押し、[CSVダウンロード（保存）]タブを選択、[CSVファイルを保存]ボタンを押し入力内容を保存します。ここで保存されるのは、入力した項目のみで計算結果は保存されません。")
         st.write("6、保存したＣＳＶを取り込む場合は、[ＣＳＶの入出力]ボタンを押し、[CSVアップロード（読込）]タブを選択、[upload]ボタンを押し保存CSVファイルをを選択します。[データ取り込んで反映]ボタンをおします。反映後に必ず[計算（再計算）する]ボタンを押して再計算して下さい。")



# --- 1. 基本情報 ---
st.header("1. 基本情報の入力    2025年12月31日現在", anchor=False)
st.subheader("(1) 申告者本人", anchor=False)
kihon_col1,kihon_col2,kihon_col3,kihon_col4,kihon_col5,kihon_col6,kihon_col7 = st.columns([1,1.5,1,1,1.5,1,1])
with kihon_col1:
      st.radio("性別", ["男", "女"], key="a_honnin_sex")
with kihon_col2:
      st.text_input("生年月日(西暦8桁)", key="a_honnin_birthday", value=" ", 
        on_change=check_inputx, args=("a_honnin_birthday","+",)
    )
with kihon_col3:
      st.session_state["b_honnin_age"] = ( tax_logic_s.nenreikeisan1
        (st.session_state["a_honnin_birthday"], "20251231", 1)
      )
      st.metric(label="年齢", value=st.session_state["b_honnin_age"])
with kihon_col4:
      st.radio("寡婦該当", ["なし", "あり"], key="a_honnin_kafu")
with kihon_col5:
      st.radio("障害", ["なし", "障害者","特別障害者"], key="a_honnin_syogai")
with kihon_col6:
      st.radio("配偶者", ["なし", "あり"], key="a_honnin_haigu")
      haigu_init()
with kihon_col7:
      st.radio("国保計算", ["なし", "あり"], key="a_kokuho_1")      



st.subheader("(2) 配偶者", anchor=False)
kihon_col11,kihon_col12,kihon_col13,kihon_col14,kihon_col15 = st.columns([1,1.5,1,1.5,1.5])   
with kihon_col11:
    if st.session_state["a_honnin_haigu"] == "あり":
        st.metric(label="性別", value=st.session_state["a_haigu_sex"])   

with kihon_col12:
    if st.session_state["a_honnin_haigu"] == "あり":
        st.text_input("生年月日(西暦8桁)", key="a_haigu_birthday", value=" ", 
            on_change=check_inputx, args=("a_haigu_birthday","+",)
        )

with kihon_col13:
    if st.session_state["a_honnin_haigu"] == "あり":
        st.session_state["b_haigu_age"] = ( 
            tax_logic_s.nenreikeisan1(st.session_state["a_haigu_birthday"], "20251231", 1)
        )
        st.metric(label="年齢", value=st.session_state["b_haigu_age"])

with kihon_col14:
    if st.session_state["a_honnin_haigu"] == "あり":
      st.radio("障害", ["なし", "障害者","特別障害者","同居特別障害者"], key="a_haigu_syogai")

with kihon_col15:
    if st.session_state["a_honnin_haigu"] == "あり":
        st.text_input("合計所得金額の見積額", key="a_haigu_syotoku", value="0", 
            on_change=check_inputx, args=("a_haigu_syotoku","+")
        )
st.write("---")


# --- 2. 収入の入力 ---
st.header("2. 収入の入力 ( 給与、年金、事業、金融 )", anchor=False)
#
#
st.subheader("(1) 給与、年金、事業 ( 源泉徴収票、収支内訳書 )", anchor=False)
#st.subheader("収入内訳  ① 給与      ② 年金      ③ 副業等）", anchor=False)
incom_col1,incom_col2,incom_col3 = st.columns(3)
with incom_col1:
    st.text_input(
    "給与_支払金額", key="a_kyuyo", value="0", on_change=check_inputx, args=("a_kyuyo","+",)
    )
with incom_col2:
    st.text_input(
    "年金_支払金額", key="a_nenkin", value="0", on_change=check_inputx, args=("a_nenkin","+",)
    )
with incom_col3:
    st.text_input(
    "事業_収入", key="a_jigyo", value="0", on_change=check_inputx, args=("a_jigyo","+",)
        )

incom_col4,incom_col5,incom_col6 = st.columns(3)
with incom_col4:
    st.text_input(
    "給与_源泉徴収税額", key="a_kyuyo_gen", value="0", on_change=check_inputx, args=("a_kyuyo_gen","+",)
    )
with incom_col5:
    st.text_input(
    "年金_源泉徴収税額", key="a_nenkin_gen", value="0", on_change=check_inputx, args=("a_nenkin_gen","+",)
    )
with incom_col6:
    st.text_input(
    "事業_経費", key="a_jigyo_cost", value="342122", on_change=check_inputx, args=("a_jigyo_cost","+",)
    )        

#
st.subheader("(2) 金融所得（ 特定口座年間取引報告書 ）", anchor=False)
# 証券会社の入力データをPythonの裏側でまとめて保存するための「空のリスト」
#tabs1data = []

# 証券会社3社分のタブ（切り替え画面）を作成
tabs1 = st.tabs(["証券会社 1", "証券会社 2", "証券会社 3"])

# for文を使って、3つのタブの中に同じ入力画面を自動で作る
for i, tab in enumerate(tabs1):
    
    with tab:
        # 例：〇〇証券 などを入力する欄
        tabs1name = st.text_input(f"証券会社名（{i+1}社目）", placeholder="例：みずほ証券 など", key=f"a_syokenname_{i}")
        
        st.markdown("(1) 譲渡に係る年間取引損益及び源泉徴収税額等の入力")
        tabs1_col11,tabs1_col12,tabs1_col13,tabs1_col139 = st.columns(4)
        with tabs1_col11:
            st.text_input(
                "③差引金額の合計", 
                value="0", key=f"a_jyoto_{i}", 
                on_change=check_inputx, args=(f"a_jyoto_{i}","+-",)
                )
        with tabs1_col12:
            st.text_input(
                "源泉徴収税額(所得税)",
                value="0", key=f"a_jyotostax_{i}", 
                on_change=check_inputx, args=(f"a_jyotostax_{i}","+",)
        )
        with tabs1_col13:
            st.text_input(
                "譲渡所得割額(住民税)",
                value="0", key=f"a_jyotottax_{i}", 
                on_change=check_inputx, args=(f"a_jyotottax_{i}","+",)
            )
        with tabs1_col139:
            st.radio("申告方式",  ["申告しない", "申告分離課税"], key=f"a_jyotoselect_{i}")


        st.markdown("(2) 特定上場株式等の配当等（種類④～⑨）の入力")
        tabs1_col14,tabs1_col15,tabs1_col16,tabs1_col17,tabs1_col18 = st.columns(5)
        with tabs1_col14:
            st.text_input(
                "④配当等の額", 
                value="0", key=f"a_haitou4_{i}", 
                on_change=check_inputx, args=(f"a_haitou4_{i}","+-",)
            )
        with tabs1_col15:
            st.text_input(
                "⑤配当等の額",
                value="0", key=f"a_haitou5_{i}", 
                on_change=check_inputx, args=(f"a_haitou5_{i}","+-",)
            )
        with tabs1_col16:
            st.text_input(
                "⑥配当等の額",
                value="0", key=f"a_haitou6_{i}", 
                on_change=check_inputx, args=(f"a_haitou6_{i}","+-",)
            )
        with tabs1_col17:
            st.text_input(
                "⑦配当等の額",
                value="0", key=f"a_haitou7_{i}", 
                on_change=check_inputx, args=(f"a_haitou7_{i}","+-",)
            )
        with tabs1_col18:
            st.text_input(
                "⑧配当等の額",
                value="0", key=f"a_haitou8_{i}", 
                on_change=check_inputx, args=(f"a_haitou8_{i}","+-",)
            )

        tabs1_col19,tabs1_col20,tabs1_col21,tabs1_col219 = st.columns(4)
        with tabs1_col19:
            st.session_state[f"g_haitou9_{i}"] = ( 
                    int(st.session_state[f"a_haitou4_{i}"]) + 
                    int(st.session_state[f"a_haitou5_{i}"]) +
                    int(st.session_state[f"a_haitou6_{i}"]) +
                    int(st.session_state[f"a_haitou7_{i}"]) +
                    int(st.session_state[f"a_haitou8_{i}"]) 
            ) 
            val =  st.session_state[f"g_haitou9_{i}"]
            formatted_val = f"{val:,}"
            st.session_state[f"dspg_haitou9_{i}"] = formatted_val 
            st.text_input("⑨(④～⑧)の合計", disabled=True, key=f"dspg_haitou9_{i}" ) 
           
        with tabs1_col20:
            st.text_input(
                "⑨源泉徴収(所得税)",
                value="0", key=f"a_haitou9stax_{i}", 
                on_change=check_inputx, args=(f"a_haitou9stax_{i}","+",)
            )
        with tabs1_col21:
            st.text_input(
                "⑨配当割額(住民税)",
                value="0", key=f"a_haitou9ttax_{i}", 
                on_change=check_inputx, args=(f"a_haitou9ttax_{i}","+",)
            )
        with tabs1_col219:
            st.radio("申告方式 ", ["申告しない", "申告分離課税", "総合課税"], key=f"a_haitou9select_{i}")
    
        
        st.markdown("(3) 特定上場以外の配当（⑩～⑭）")
        tabs1_col22,tabs1_col23,tabs1_col24,tabs1_col25,tabs1_col26=st.columns(5)
        with tabs1_col22:
            st.text_input(
                "⑩配当等の額", 
                value="0", key=f"a_haitou10_{i}", 
                on_change=check_inputx, args=(f"a_haitou10_{i}","+-",)
            )
        with tabs1_col23:
            st.text_input(
                "⑪配当等の額", 
                value="0", key=f"a_haitou11_{i}", 
                on_change=check_inputx, args=(f"a_haitou11_{i}","+-",)
            )
        with tabs1_col24:
            st.text_input(
                "⑫配当等の額", 
                value="0", key=f"a_haitou12_{i}", 
                on_change=check_inputx, args=(f"a_haitou12_{i}","+-",)
            )
        with tabs1_col25:
            st.text_input(
                "⑬配当等の額", 
                value="0", key=f"a_haitou13_{i}", 
                on_change=check_inputx, args=(f"a_haitou13_{i}","+-",)
            )
        with tabs1_col26:
            st.text_input(
                "⑭配当等の額", 
                value="0", key=f"a_haitou14_{i}", 
                on_change=check_inputx, args=(f"a_haitou14_{i}","+-",)
            )

        tabs1_col27,tabs1_col28,tabs1_col29,tabs1_col299 = st.columns(4)
        with tabs1_col27:
            st.session_state[f"g_haitou15_{i}"] = ( 
                    int(st.session_state[f"a_haitou10_{i}"]) + 
                    int(st.session_state[f"a_haitou11_{i}"]) +
                    int(st.session_state[f"a_haitou12_{i}"]) +
                    int(st.session_state[f"a_haitou13_{i}"]) +
                    int(st.session_state[f"a_haitou14_{i}"]) 
            )
            val = st.session_state[f"g_haitou15_{i}"] 
            formatted_val = f"{val:,}"  
            st.session_state[f"dspg_haitou15_{i}"] = formatted_val 
            st.text_input("⑮(④～⑧)の合計", disabled=True, key=f"dspg_haitou15_{i}" ) 
 
        
        with tabs1_col28:
            st.text_input(
                "⑮源泉徴収(所得税)",
                value="0", key=f"a_haitou15stax_{i}", 
                on_change=check_inputx, args=(f"a_haitou15stax_{i}","+",)
            )
        with tabs1_col29:
            st.text_input(
                "⑮配当割額(住民税)",
                value="0", key=f"a_haitou15ttax_{i}", 
                on_change=check_inputx, args=(f"a_haitou15ttax_{i}","+",)
            )
        with tabs1_col299:
            st.radio("申告方式 ", ["申告しない", "申告分離課税"], key=f"a_haitou15select_{i}")
st.write("---")

# --- 所得控除の入力 ---
st.header("3. 所得控除の入力", anchor=False)

st.subheader("(社会,生命,地震)保険料、医療費控除、寄付金控除", anchor=False)
st.write("※給与や年金からの天引額と、本人が支払った保険料等の支払額を入力")

skojyo_col0,skojyo_col1,skojyo_col2,skojyo_col3,skojyo_col4,skojyo_col5 = st.columns(6)
with skojyo_col0:
    st.text_input(
    "社会保険料", key="a_hoken13", value="0", on_change=check_inputx, args=("a_hoken13","+",)
    )
with skojyo_col1:
    st.text_input(
    "新生命保険料", key="a_hoken15_1", value="0", on_change=check_inputx, args=("a_hoken15_1","+",)
    )
with skojyo_col2:
    st.text_input(
    "旧生命保険料", key="a_hoken15_2", value="0", on_change=check_inputx, args=("a_hoken15_2","+",)
    )
with skojyo_col3:
    st.text_input(
    "新個人年金", key="a_hoken15_3", value="0", on_change=check_inputx, args=("a_hoken15_3","+",)
    )
with skojyo_col4:
    st.text_input(
    "旧個人年金", key="a_hoken15_4", value="0", on_change=check_inputx, args=("a_hoken15_4","+",)
    )
with skojyo_col5:
    st.text_input(
    "介護医療", key="a_hoken15_5", value="0", on_change=check_inputx, args=("a_hoken15_5","+",)
    )

skojyo_col6,skojyo_col7,skojyo_col8,skojyo_col9,skojyo_col10,skojyo_col11,skojyo_col12 = st.columns(7)
with skojyo_col6:
    st.text_input(
    "地震保険料", key="a_hoken16_1", value="0", on_change=check_inputx, args=("a_hoken16_1","+",)
    )
with skojyo_col7:
    st.text_input(
    "旧長期損", key="a_hoken16_2", value="0", on_change=check_inputx, args=("a_hoken16_2","+",)
    )

with skojyo_col8:
    st.text_input(
    "医療費合計", key="a_skojyo28_1", value="0", on_change=check_inputx, args=("a_skojyo28_1","+",)
    )
with skojyo_col9:
    st.text_input(
    "医療費補填", key="a_skojyo28_2", value="0", on_change=check_inputx, args=("a_skojyo28_2","+",)
    )
with skojyo_col10:
    st.text_input(
    "セルメデ額", key="a_skojyo28_3", value="0", on_change=check_inputx, args=("a_skojyo28_3","+",)
    )
with skojyo_col11:
    st.text_input(
    "セル補填額", key="a_skojyo28_4", value="0", on_change=check_inputx, args=("a_skojyo28_4","+",)
    )
with skojyo_col12:
    st.text_input(
    "寄付金合計", key="a_skojyo29", value="0", on_change=check_inputx, args=("a_skojyo29","+",)
    )

st.write("---")

st.header("4. 計算（再計算）", anchor=False)

st.header("＜＜ 計算結果のサマリー ＞＞", anchor=False)
summ_col11,summ_col12,summ_col13,summ_col14,summ_col15,summ_col16 = st.columns([1,1,1,1,1,2])
with summ_col11:
    st.text_input("所得税 Z9", value=f"{st.session_state["g_noufutax"]:,}", disabled=True) 
with summ_col12:
    st.text_input("地方税 Z33", value=f"{st.session_state["gd_noufutax"]:,}", disabled=True) 
with summ_col13:
    st.text_input("国保概算 H11", value=f"{ (st.session_state["h_kokuho_4_124_1"] + 
        st.session_state["h_kokuho_4_3_1"] ):,}", disabled=True) 
with summ_col14:
    st.text_input("介護制度概算 H15", value=f"{st.session_state["h_kaigo_4_1"]:,}", disabled=True) 
with summ_col15:
    st.text_input("後期高齢概算 H20", value=f"{st.session_state["h_korei_4_1"]:,}", disabled=True) 
with summ_col16:
    formatted_val = f"{
        ( int(st.session_state["g_noufutax"]) +
          int(st.session_state["gd_noufutax"]) +
          int(st.session_state["h_kokuho_4_124_1"] + st.session_state["h_kokuho_4_3_1"]) +
          int(st.session_state["h_kaigo_4_1"]) +
          int(st.session_state["h_korei_4_1"])
        ):,}"
    st.text_input("要納付額(Z9+Z33+H11+H15+H20))", value=formatted_val, disabled=True) 

st.write("---")
st.write("---")

st.header("＜＜ 計算結果の詳細表示　＞＞", anchor=False) 
st.subheader("5. 合計所得の計算", anchor=False)

comp_col01,comp_col02,comp_col03,comp_col04,comp_col05,comp_col06,comp_col07 = st.columns(7)
with comp_col01:
    st.text_input("給与所得G1", value=f"{st.session_state["b_syotoku6"]:,}", disabled=True) 
with comp_col02:
    st.text_input("年金所得G2", value=f"{st.session_state["b_syotoku7"]:,}", disabled=True) 
with comp_col03:
    st.text_input("調整控除G3", value=f"{st.session_state["b_syotoku6_tyosei"]:,}", disabled=True) 
with comp_col04:
    st.text_input("事業所得G4", value=f"{st.session_state["b_syotoku1"]:,}", disabled=True) 
with comp_col05:
    st.text_input("配当所得G5", value=f"{st.session_state["b_syotoku5"]:,}", disabled=True) 
with comp_col06:
    st.text_input("譲渡所得G6", value=f"{st.session_state["b_syotoku73"]:,}", disabled=True) 
with comp_col07:
    st.text_input("配当所得G7", value=f"{st.session_state["b_syotoku74"]:,}", disabled=True) 

comp_col11,comp_col12,comp_col13,comp_col14,comp_col15 = st.columns(5)
with comp_col11:
    st.text_input("総合課税所得G8", value=f"{st.session_state["g_sogosyotoku"]:,}", disabled=True) 
with comp_col12:
    st.text_input("分離課税所得G9", value=f"{st.session_state["g_bunrisyotoku"]:,}", disabled=True) 
with comp_col13:
    st.text_input("合 計 所 得 G10", value=f"{st.session_state["g_gokeisyotoku"]:,}", disabled=True) 
with comp_col14:
    st.text_input("源泉_所得税G11", value=f"{st.session_state["g_gensentax"]:,}", disabled=True) 
with comp_col15:
    st.text_input("源泉_地方税G12", value=f"{st.session_state["gd_gensentax"]:,}", disabled=True) 

st.write("---")

st.subheader("6. 所得税計算", anchor=False)
st.subheader("(1) 所得控除", anchor=False)
comp_col21,comp_col22,comp_col23,comp_col24,comp_col25,comp_col26 = st.columns(6)
with comp_col21:
    st.text_input("社保控除J1", value=f"{st.session_state["b_skojyo13"]:,}", disabled=True) 
with comp_col22:
    st.text_input("生命保険J2", value=f"{st.session_state["b_skojyo15"]:,}", disabled=True) 
with comp_col23:
    st.text_input("地震保険J3", value=f"{st.session_state["b_skojyo16"]:,}", disabled=True) 
with comp_col24:
    st.text_input("寡婦控除J4", value=f"{st.session_state["b_skojyo17"]:,}", disabled=True) 
with comp_col25:
    st.text_input("障害者J5", value=f"{st.session_state["b_skojyo19"]:,}", disabled=True) 
with comp_col26:
    st.text_input("配偶者J6", value=f"{st.session_state["b_skojyo21"]:,}", disabled=True) 

comp_col27,comp_col28,comp_col29,comp_col30 = st.columns(4)
with comp_col27:
    st.text_input("基礎控除J7", value=f"{st.session_state["b_skojyo25"]:,}", disabled=True) 
with comp_col28:
    st.text_input("医療費J8", value=f"{st.session_state["b_skojyo28"]:,}", disabled=True) 
with comp_col29:
    st.text_input("寄付金J9", value=f"{st.session_state["b_skojyo29"]:,}", disabled=True) 
with comp_col30:
    st.text_input("控除合計 J10", value=f"{st.session_state["g_syotokukojyo"]:,}", disabled=True) 

st.subheader("(2) 課税所得", anchor=False)
comp_col31,comp_col32 = st.columns(2)
with comp_col31:
    st.text_input("総合課税所得 T1", value=f"{st.session_state["b_kazei78"]:,}", disabled=True) 
with comp_col32:
    st.text_input("分離課税所得 T2", 
    value=f"{st.session_state["b_kazei81"] + st.session_state["b_kazei82"]:,}", disabled=True) 

st.subheader("(3) 所得税", anchor=False)
comp_col33,comp_col34,comp_col35,comp_col36,comp_col37,comp_col38 = st.columns(6)
with comp_col33:
    st.text_input("所得税(総合課税)Z1", value=f"{st.session_state["b_szei86"]:,}", disabled=True) 
with comp_col34:
    st.text_input("所得税(分離課税)Z2", 
    value=f"{(st.session_state["b_szei89"] + st.session_state["b_szei90"]):,}", disabled=True) 
with comp_col35:
    st.text_input("所得税合計Z3（Z1+Z2）", value=f"{st.session_state["g_szei"]:,}", disabled=True) 
with comp_col36:
    st.text_input("配当控除Z4．．．", value=f"{st.session_state["b_haitokojyo"]:,}", disabled=True) 
with comp_col37:
    st.text_input("基準所得税額Z5．．．", value=f"{st.session_state["b_szei44"]:,}", disabled=True) 
with comp_col38:
    st.text_input("復興特別税Z6．．．", value=f"{st.session_state["b_szei45"]:,}", disabled=True) 


comp_col39,comp_col40,comp_col41 = st.columns(3)
with comp_col39:
    st.text_input("確定所得税 Z7", value=f"{st.session_state["g_kakuteitax"]:,}", disabled=True) 
with comp_col40:
    st.text_input("源泉_所得税 Z8", value=f"{st.session_state["g_gensentax"]:,}", disabled=True)     
with comp_col41:
    st.text_input("申告納付額 Z9(-は還付)", value=f"{st.session_state["g_noufutax"]:,}", disabled=True) 

st.write("---")

st.subheader("7. 地方税（市県民税）計算", anchor=False)
st.subheader("(1) 所得控除", anchor=False)
comp_col42,comp_col43,comp_col44,comp_col45,comp_col46,comp_col47 = st.columns(6)
with comp_col42:
    st.text_input("社保控除J11", value=f"{st.session_state["d_skojyo13"]:,}", disabled=True) 
with comp_col43:
    st.text_input("生命保険J12", value=f"{st.session_state["d_skojyo15"]:,}", disabled=True) 
with comp_col44:
    st.text_input("地震保険J13", value=f"{st.session_state["d_skojyo16"]:,}", disabled=True) 
with comp_col45:
    st.text_input("寡婦控除J14", value=f"{st.session_state["d_skojyo17"]:,}", disabled=True) 
with comp_col46:
    st.text_input("障害者J15", value=f"{st.session_state["d_skojyo19"]:,}", disabled=True) 
with comp_col47:
    st.text_input("配偶者J16", value=f"{st.session_state["d_skojyo21"]:,}", disabled=True) 

comp_col48,comp_col49,comp_col50 = st.columns(3)
with comp_col48:
    st.text_input("基礎控除J17", value=f"{st.session_state["d_skojyo25"]:,}", disabled=True) 
with comp_col49:
    st.text_input("医療費J18", value=f"{st.session_state["d_skojyo28"]:,}", disabled=True) 
with comp_col50:
    st.text_input("控除合計 J19", value=f"{st.session_state["gd_syotokukojyo"]:,}", disabled=True) 

st.subheader("(2) 課税所得", anchor=False)
comp_col51,comp_col52 = st.columns(2)
with comp_col51:
    st.text_input("総合課税所得 T11", value=f"{st.session_state["d_kazei78"]:,}", disabled=True) 
with comp_col52:
    st.text_input("分離課税所得 T12", 
    value=f"{(st.session_state["d_kazei81"]+st.session_state["d_kazei82"]):,}", disabled=True) 

st.subheader("(3) 所得割（市民税）", anchor=False)
comp_col61,comp_col62,comp_col63,comp_col64,comp_col65,comp_col66 = st.columns(6)
with comp_col61:
    st.text_input("所得割(総合課税)Z11", value=f"{st.session_state["d_szei86_1"]:,}", disabled=True) 
with comp_col62:
    st.text_input("所得割(分離課税)Z12", value=f"{st.session_state["d_szei89&90_1"]:,}", disabled=True) 
with comp_col63:
    st.text_input("所得割合計Z13", value=f"{st.session_state["gd_szei_1"]:,}", disabled=True) 
with comp_col64:
    st.text_input("調整控除Z14．．．", value=f"{st.session_state["d_tyoseikojyo_1"]:,}", disabled=True) 
with comp_col65:
    st.text_input("配当控除Z15．．．", value=f"{st.session_state["d_haitokojyo_1"]:,}", disabled=True) 
with comp_col66:
    st.text_input("寄付金控除Z16", value=f"{st.session_state["d_kifukojyo_1"]:,}", disabled=True) 

comp_col67,comp_col68,comp_col69 = st.columns(3)
with comp_col67:
    st.text_input("確定所得割Z17", value=f"{st.session_state["d_syotokuwari_1"]:,}", disabled=True) 
with comp_col68:
    st.text_input("配当割額Z18", value=f"{st.session_state["d_warikojyo_1"]:,}", disabled=True) 
with comp_col69:
    st.text_input("確定所得割Z19", value=f"{st.session_state["gd_kakuteitax_1"]:,}", disabled=True) 


st.subheader("(4) 所得割（県民税）", anchor=False)
comp_col71,comp_col72,comp_col73,comp_col74,comp_col75,comp_col76 = st.columns(6)
with comp_col71:
    st.text_input("所得割(総合課税)Z21", value=f"{st.session_state["d_szei86_2"]:,}", disabled=True) 
with comp_col72:
    st.text_input("所得割(分離)Z22", value=f"{st.session_state["d_szei89&90_2"]:,}", disabled=True) 
with comp_col73:
    st.text_input("所得割合計Z23", value=f"{st.session_state["gd_szei_2"]:,}", disabled=True) 
with comp_col74:
    st.text_input("調整控除Z24．．．", value=f"{st.session_state["d_tyoseikojyo_2"]:,}", disabled=True) 
with comp_col75:
    st.text_input("配当控除Z25．．．", value=f"{st.session_state["d_haitokojyo_2"]:,}", disabled=True) 
with comp_col76:
    st.text_input("寄付金控除Z26", value=f"{st.session_state["d_kifukojyo_2"]:,}", disabled=True) 

comp_col77,comp_col78,comp_col79 = st.columns(3)
with comp_col77:
    st.text_input("確定所得割Z27", value=f"{st.session_state["d_syotokuwari_2"]:,}", disabled=True) 
with comp_col78:
    st.text_input("配当割額Z28", value=f"{st.session_state["d_warikojyo_2"]:,}", disabled=True) 
with comp_col79:
    st.text_input("確定所得割Z29", value=f"{st.session_state["gd_kakuteitax_2"]:,}", disabled=True) 

st.subheader("(5) 均等割、市県民税", anchor=False)
comp_col81,comp_col82,comp_col83,comp_col84 = st.columns([1,1,1,1.5])
with comp_col81:
    st.text_input("均等割(市民税)Z30", value=f"{st.session_state["d_kintowari_1"]:,}", disabled=True) 
with comp_col82:
    st.text_input("均等割(県民税)Z31", value=f"{st.session_state["d_kintowari_2"]:,}", disabled=True) 
with comp_col83:
    st.text_input("森林環境税Z32", value=f"{st.session_state["d_kankyozei"]:,}", disabled=True) 
with comp_col84:
    st.text_input("申告納付額Z33(-は還付)", value=f"{st.session_state["gd_noufutax"]:,}", disabled=True) 

st.write("---")

subheader_col81,subheader_col82 = st.columns([1,1.5])
with subheader_col81:
    st.subheader("8. 概算保険料の計算", anchor=False)
with subheader_col82:
    with st.popover("ℹ️ なぜ保険料が概算なのか？必ずお読みください。"):

        st.write("＜保険料が概算の理由＞")
        st.write("①　3つの保険は全国一律ではありません。お住まいの地域により異なります。ここでの計算は、ある市町村の保険料率を使用して計算していますので、計算額は概算額（目安）です。ご注意ください。")

        st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;＜保険に適用される料率＞") 
        st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;国民健康保険（国保）と介護保険制度：市町村単位の料率が適用")  
        st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;後期高齢者医療制度　　　　　　　　：都道府県単位の料率が適用") 
        st.write("②　各保険には、一定の所得以下の世帯、本人及び同居家族の市民税の課税状況等により軽減措置がありますが、＊＊ここでは本人の年齢と合計所得のみを基に計算し、軽減措置を考慮してません。＊＊")
        st.write("①と②の理由により、保険料は概算（目安）です。正確な額は、お住まいの市町村でお聞き下さい。")
        st.write("計算で使用する保険料率は、ℹ️ 国民健康保険の計算式を見る、ℹ️ 介護保険制度の計算式を見る、ℹ️ 後期高齢者医療制度の計算式を見る　に記載しています。必ず確認してください。")

    
subheader_col83,subheader_col84 = st.columns([1.5,1])
with subheader_col83:
    st.subheader("(1) 国民健康保険（国保）", anchor=False)
with subheader_col84:
    with st.popover("ℹ️ 国民健康保険の計算式を見る"):
        st.markdown("#### 📝 シュミレーターの国保計算料率は以下のとおりです。")
        st.write("＊所得割対象額(A)＝合計所得G10 － ４３万円 ")
        st.write("＊計算された保険料には本人分(所得割＋均等割)の他に世帯割を含みます。")
        st.write("ー保険名ーーー所得割額(A)×N%ーー1人当り均等割ーー1世帯当り世帯割ーー上限ーー")
        
        st.write("①基礎課税額　　　　7.90%　　　　　　　22,700　　　　　　21,400　　　670,000") 
        st.write("②後期高齢者支援　　2.70%　　　　　　　8,300　　　　　　　6,000　　　260,000") 
        st.write("③介護納付金　　　　0.31%　　　　　　　1,500　　　　　　　800　　　　170,000")
        st.write("④子ども子育て支援　2.50%　　　　　　　7,200　　　　　　　6,200　　　　30,000") 

        st.write("国民健康保険は、①～④の保険税の合計です。①～④の各保険税は、所得割＋均等割＋世帯割を合計した金額です。")  
        st.write("国民健康保険は、75歳誕生日が属する月から後期高齢者医療制度へ移行します。")  
        st.write("③介護納付金は、40歳誕生日の前日が属する月から課税され、65歳誕生日の前日が属する月から介護保険制度へ移行します。")  
    
comp_col91,comp_col92,comp_col93,comp_col94,comp_col95,comp_col96 = st.columns(6)
with comp_col91:
    st.text_input("国保対象額H1", value=f"{st.session_state["h_kokuho_1"]:,}", disabled=True) 
with comp_col92:
    st.text_input("基礎課税額H2", value=f"{ (st.session_state["h_kokuho_2_1"] -
         st.session_state["h_kokuho_3_1"] ):,}", disabled=True) 
with comp_col93:
    st.text_input("後期高齢者支援H3", value=f"{ (st.session_state["h_kokuho_2_2"] -
         st.session_state["h_kokuho_3_2"] ):,}", disabled=True) 
with comp_col94:
    st.text_input("子ども子育て支援H4", value=f"{ (st.session_state["h_kokuho_2_4"] -
         st.session_state["h_kokuho_3_4"] ):,}", disabled=True) 
with comp_col95:
    val_1 = ( st.session_state["h_kokuho_2_1"] + st.session_state["h_kokuho_2_2"] + 
              st.session_state["h_kokuho_2_4"] - st.session_state["h_kokuho_3_1"] - 
              st.session_state["h_kokuho_3_2"] - st.session_state["h_kokuho_3_4"] )
    st.text_input("小計H5(H2+H3+H4)", value=f"{val_1:,}", disabled=True) 
with comp_col96:
    st.text_input("介護給付金H6", value=f"{ (st.session_state["h_kokuho_2_3"] - 
        st.session_state["h_kokuho_3_3"] ):,}", disabled=True)

comp_col97,comp_col98,comp_col99,comp_col100,comp_col101 = st.columns([1,1.5,1,1.5,2])
with comp_col97:
    st.text_input("月数H7", value=f"{str(st.session_state["h_kokuho_4_124_2"])}{" / 12"}", disabled=True) 
with comp_col98:
    st.text_input("月割額H8", value=f"{st.session_state["h_kokuho_4_124_1"]:,}", disabled=True) 
with comp_col99:
    st.text_input("介護月数H9", value=f"{str(st.session_state["h_kokuho_4_3_2"])}{" / 12"}", disabled=True) 
with comp_col100:
    st.text_input("介護月割額H10", value=f"{st.session_state["h_kokuho_4_3_1"]:,}", disabled=True) 
with comp_col101:
    st.text_input("国保概算額H11(H8+H10)", value=f"{ (st.session_state["h_kokuho_4_124_1"] + 
        st.session_state["h_kokuho_4_3_1"] ):,}", disabled=True) 


subheader_col85,subheader_col86 = st.columns([1.5,1])
with subheader_col85:
    st.subheader("(2) 介護保険制度", anchor=False)
with subheader_col86:
    with st.popover("ℹ️ 介護保険制度の計算式を見る"):
        st.markdown("#### 📝 シュミレーターの介護保険料率は以下のとおりです。")
        st.write("＊保険対象額(A)＝合計所得G10 ")
        st.write("所得に応じて所得段階がきまります。所得段階は13段階で、各段階ごとに保険料が決められています。")


        st.write("段階1～5は本人の合計所得の他に、生活保護該当有無、世帯全員の市民税課税非課税の条件が加わるため")
        st.write("＊＊このシュミレーターでは、一番下を6段階として介護保険料を計算します。")

        st.write("ー段階ーー本人市民税ーーー合計所得ーーーその他の条件ー保険料率ーーー保険料額年額ー") 
    
        st.write("　06段階　　　課税　　　125万未満　　　　　　　なし　　　　　1.13　　　　　85,500") 
        st.write("　07段階　　　課税　　　125万以上200万未満　　なし　　　　　1.25　　　　　94,500") 
        st.write("　08段階　　　課税　　　200万以上300万未満　　なし　　　　　1.50　　　　　113,500") 
        st.write("　09段階　　　課税　　　300万以上500万未満　　なし　　　　　1.75　　　　　132,400") 
        st.write("　10段階　　　課税　　　500万以上700万未満　　なし　　　　　1.90　　　　　143,700") 
        st.write("　11段階　　　課税　　　700万以上1000万未満　　なし　　　　　2.00　　　　　151,300") 
        st.write("　12段階　　　課税　　　1000万以上1500万未満　なし　　　　　2.30　　　　　174,000") 
        st.write("　13段階　　　課税　　　1500万以上　　　　　　なし　　　　　2.50　　　　　189,100") 

        st.write("(01段階------非課税------80万以下---------あり-------0.295---------21,600 )") 
        st.write("(02段階------非課税-----120万以下---------あり-------0.485---------36,700 )") 
        st.write("(03段階------非課税-----120万超え---------あり-------0.685---------51,900 )") 
        st.write("(04段階------非課税------80万以下---------あり-------0.885---------66,600 )") 
        st.write("(05段階------非課税------80万超え---------あり-------1.00----------75,600 )") 



comp_col102,comp_col103,comp_col104,comp_col105 = st.columns(4)
with comp_col102:
    st.text_input("介護対象額H12", value=f"{st.session_state["h_kaigo_1"]:,}", disabled=True) 
with comp_col103:
    st.text_input("保険料H13", value=f"{st.session_state["h_kaigo_2"]:,}", disabled=True) 
with comp_col104:
    st.text_input("月数H14", value=f"{str(st.session_state["h_kaigo_4_2"])}{" / 12"}", disabled=True) 
with comp_col105:
    st.text_input("月割額H15", value=f"{st.session_state["h_kaigo_4_1"]:,}", disabled=True) 


subheader_col87,subheader_col88 = st.columns([1.5,1])
with subheader_col87:
    st.subheader("(3) 後期高齢者医療制度", anchor=False)
with subheader_col88:
    with st.popover("ℹ️ 後期高齢者医療制度の計算式を見る"):
        st.markdown("#### 📝 シュミレーターの後期高齢者医療制度は以下のとおりです。")
        st.write("＊保険対象額(A)＝合計所得G10 － ４３万円")

        st.write("ー保険名ーーー所得割額(A)×N%ーー1人当り均等割ーーー上限ーー")
        
        st.write("①医療分　　　　9.24%　　　　　　　49,000　　　　　850,000") 
        st.write("②子ども分　　　0.25%　　　　　　　1,400　　　　　　21,000") 
    

        st.write("後期高齢者医療制度は、①～②の保険税の合計です。①～②の各保険税は、所得割＋均等割を合計した金額です。")  
        st.write("同一世帯内の被保険者と世帯主の所得に応じて均等割が軽減されます。正確な額は、市町村の窓口でお聞き下さい。") 

        st.write("75歳誕生日が属する月から後期高齢者医療制度へ移行します。")  




comp_col106,comp_col107,comp_col108,comp_col109,comp_col110 = st.columns(5)
with comp_col106:
    st.text_input("高齢対象額H16", value=f"{st.session_state["h_korei_1"]:,}", disabled=True) 
with comp_col107:
    st.text_input("医療分H17", value=f"{ (st.session_state["h_korei_2_1"] - 
        st.session_state["h_korei_3_1"] ):,}", disabled=True) 
with comp_col108:
    st.text_input("子供分H18", value=f"{ (st.session_state["h_korei_2_2"] -
        st.session_state["h_korei_3_2"] ):,}", disabled=True) 
with comp_col109:
    st.text_input("月数H19", value=f"{str(st.session_state["h_korei_4_2"])}{" / 12"}", disabled=True) 
with comp_col110:
    st.text_input("月割額H20", value=f"{st.session_state["h_korei_4_1"]:,}", disabled=True) 


