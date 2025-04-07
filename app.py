import streamlit as st
import pandas as pd
import altair as alt
st.write("""
# My first app
# Hello *world!*
""")
if "hello" not in st.session_state:
    st.session_state.hello = False

if st.button("Say hello"):
    
    st.session_state.hello=True
if st.session_state.hello==True:
    st.write("Hello")
else:
    st.write("good")
st.markdown("# 不好")
df = pd.read_csv("data.csv")
df=df.head(10)
st.bar_chart(df.head(100),x='Sales Person',y="Boxes Shipped")
date = st.date_input("Pick a date")
df=df.set_index('Country')
#st.data_input
#st.write
#st.markdown
#st.bar_chart
#st.radio df.set_index("") st.multiselect("Note",list(df.index)) set one column of data as parameter
#data.sort_index(),data.T.reset_index()  #the condifferent motif in all SMILES 
pets=(1,2,3)
st.error(list(df.index).index("Australia"))
st.error(df.index)
pet = st.radio("Pick a pet",list(df.index),index=list(df.index).index("Australia"))
st.markdown(f"you choose {pet}")


@st.cache_data
def get_UN_data():
    AWS_BUCKET_URL = "https://streamlit-demo-data.s3-us-west-2.amazonaws.com"
    df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
    return df.set_index("Region")

try:
    df = get_UN_data()
    countries = st.multiselect(
        "Choose countries", list(df.index), ["China", "United States of America"]
    )
    if not countries:
        st.error("Please select at least one country.")
    else:
        data = df.loc[countries]
        st.error(data)
        data /= 1000000.0
        st.subheader("Gross agricultural production ($B)")
        st.dataframe(data.sort_index())

        data = data.T.reset_index()
        st.error(data)
        data = pd.melt(data, id_vars=["index"]).rename(
            columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
        )
        st.dataframe(data)
        chart = (
            alt.Chart(data)
            .mark_area(opacity=0.7)
            .encode(
                x="year:T",
                y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
                color="Region:N",
            )
        )
        st.altair_chart(chart, use_container_width=True)
except :
    st.error(f"This demo requires internet access. Connection error: ")
import streamlit as st
import pandas as pd
import altair as alt



import streamlit as st
import pandas as pd
import altair as alt

# 模拟数据：不同 SMILES 中 motif 不完全一致
data = pd.DataFrame({
    "SMILES": [
        "C1=CC=CC=C1", "C1=CC=CC=C1", "C1=CC=CC=C1",             # mol_1: A, B, C
        "C1CCCCC1", "C1CCCCC1",                                  # mol_2: B, D
        "CC(=O)OC1=CC=CC=C1C(=O)O", "CC(=O)OC1=CC=CC=C1C(=O)O",   # mol_3: A, E
        "CCN(CC)CC", "CCN(CC)CC", "CCN(CC)CC",                   # mol_4: B, C, F
        "C1CNCCC1", "C1CNCCC1",                                  # mol_5: A, F
        "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O", "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O"  # mol_6: D, E
    ],
    "Motif": [
        "A", "B", "C",
        "B", "D",
        "A", "E",
        "B", "C", "F",
        "A", "F",
        "D", "E"
    ],
    "Confidence": [
        0.92, 0.75, 0.65,
        0.80, 0.60,
        0.78, 0.68,
        0.85, 0.70, 0.55,
        0.73, 0.50,
        0.62, 0.67
    ]
})
# 所有 motif 列表
motif_list = sorted(data["Motif"].unique().tolist())

# 多选 motif（用户交互）
selected_motifs = st.multiselect("🎯 Select motifs to show", motif_list, default=motif_list)

# 过滤：只保留选中的 motif
filtered = data[data["Motif"].isin(selected_motifs)]

# 折线图 + 点图

import altair as alt

# 面积图（可带透明度）
area = alt.Chart(filtered).mark_area(opacity=0.3).encode(
    x=alt.X("SMILES:N", title="SMILES"),
    y=alt.Y("Confidence:Q", title="Confidence", scale=alt.Scale(domain=[0, 1])),
    color=alt.Color("Motif:N", legend=alt.Legend(title="Motif")),
    tooltip=["SMILES", "Motif", "Confidence"]
)

chart = area.properties(
    width=700,
    height=400,
    title="📊 Motif Confidence in SMILES (Area Chart)"
).configure_axisX(labelAngle=25)

st.altair_chart(chart, use_container_width=True)


