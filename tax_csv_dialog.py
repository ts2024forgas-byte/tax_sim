# tax_csv_dailog.py（CSVダイアログ）

import pandas as pd
import streamlit as st

# ==========================================
# 1. 保存・読込の対象とするキー一覧
# ==========================================
TARGET_KEYS = [
    "a_honnin_sex",
]
TARGET_KEYS.append("a_honnin_birthday")
TARGET_KEYS.append("a_honnin_kafu")
TARGET_KEYS.append("a_honnin_syogai")
TARGET_KEYS.append("a_honnin_haigu")
TARGET_KEYS.append("a_haigu_birthday")
TARGET_KEYS.append("a_haigu_syogai")
TARGET_KEYS.append("a_haigu_syotoku")
TARGET_KEYS.append("a_kyuyo")
TARGET_KEYS.append("a_kyuyo_gen")
TARGET_KEYS.append("a_nenkin")
TARGET_KEYS.append("a_nenkin_gen")
TARGET_KEYS.append("a_jigyo")
TARGET_KEYS.append("a_jigyo_cost")


for i in range(3):
    TARGET_KEYS.append(f"a_syokenname_{i}")
    TARGET_KEYS.append(f"a_jyoto_{i}")
    TARGET_KEYS.append(f"a_jyotostax_{i}")
    TARGET_KEYS.append(f"a_jyotottax_{i}")
    TARGET_KEYS.append(f"a_jyotoselect_{i}")
    TARGET_KEYS.append(f"a_haitou4_{i}") 
    TARGET_KEYS.append(f"a_haitou5_{i}")
    TARGET_KEYS.append(f"a_haitou6_{i}")
    TARGET_KEYS.append(f"a_haitou7_{i}")
    TARGET_KEYS.append(f"a_haitou8_{i}")
    TARGET_KEYS.append(f"a_haitou9stax_{i}")
    TARGET_KEYS.append(f"a_haitou9ttax_{i}")
    TARGET_KEYS.append(f"a_haitou9select_{i}")
    TARGET_KEYS.append(f"a_haitou10_{i}")
    TARGET_KEYS.append(f"a_haitou11_{i}")
    TARGET_KEYS.append(f"a_haitou12_{i}")
    TARGET_KEYS.append(f"a_haitou13_{i}")
    TARGET_KEYS.append(f"a_haitou14_{i}")
    TARGET_KEYS.append(f"a_haitou15stax_{i}")
    TARGET_KEYS.append(f"a_haitou15ttax_{i}")
    TARGET_KEYS.append(f"a_haitou15select_{i}")
       
TARGET_KEYS.append("a_hoken13")
TARGET_KEYS.append("a_hoken15_1")
TARGET_KEYS.append("a_hoken15_2")
TARGET_KEYS.append("a_hoken15_3")
TARGET_KEYS.append("a_hoken15_4")
TARGET_KEYS.append("a_hoken15_5")
TARGET_KEYS.append("a_hoken16_1")
TARGET_KEYS.append("a_hoken16_2")
TARGET_KEYS.append("a_skojyo28_1")
TARGET_KEYS.append("a_skojyo28_2")
TARGET_KEYS.append("a_skojyo28_3")
TARGET_KEYS.append("a_skojyo28_4")
TARGET_KEYS.append("a_skojyo29")  

TARGET_KEYS.append("a_kokuho_1")
TARGET_KEYS.append("a_kokuho_2") 
TARGET_KEYS.append("a_kokuho_3")
TARGET_KEYS.append("a_kokuho_4")




# ==========================================
# 1. CSV処理関数
# ==========================================


def export_to_csv(target_keys):
    """指定されたキーのデータを session_state から取得してCSVバイト列に変換"""
    export_data = {}
    for key in target_keys:
        export_data[key] = st.session_state.get(key, "")

    df = pd.DataFrame([export_data])
    # Excel等で開いた際の文字化けを防ぐため utf-8-sig を使用
    return df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")


def import_from_csv(uploaded_file, target_keys):
    """アップロードされたCSVから指定キーの値を session_state に復元"""
    try:
        df = pd.read_csv(uploaded_file, dtype=str)
        if not df.empty:
            first_row = df.iloc[0]
            for key in target_keys:
                if key in first_row:
                    st.session_state[key] = first_row[key]
            return True
    except Exception as e:
        st.error(f"CSVの読み込みに失敗しました: {e}")
        return False


# ==========================================
# 2. ポップアップ（ダイアログ）表示関数
# ==========================================
@st.dialog("📁 CSVデータの保存・復元")
#def show_csv_modal(target_keys):
def show_csv_modal():
    """メイン画面の上に別ウィンドウ風に浮き上がるCSV操作画面"""
    st.write(
        "現在の入力値をCSVファイルとして保存したり、保存データを読み復元できます。"
    )

    tab1, tab2 = st.tabs(["📥 CSVダウンロード（保存）", "📤 CSVアップロード（読込）"])

    with tab1:
        st.caption("現在の入力状態をCSVファイルに出力します。")
        csv_bytes = export_to_csv(TARGET_KEYS)
        st.download_button(
            label="CSVファイルを保存",
            data=csv_bytes,
            file_name="tax_data.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with tab2:
        st.caption("保存済みのCSVファイルを読み込みます。")
        uploaded_file = st.file_uploader(
            "ファイル選択", type=["csv"], label_visibility="collapsed"
        )

        if uploaded_file is not None:
            if st.button("データを取り込んで反映", use_container_width=True):
                if import_from_csv(uploaded_file, TARGET_KEYS):
                    st.success("データを読み込みました！")
                    st.rerun()  # 画面を再描画してメイン入力欄に即時反映