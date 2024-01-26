import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.title('Martins Dashboard')

uploaded_file = st.file_uploader("Wähle eine CSV- oder Excel-Datei", type=['csv', 'xlsx'])
if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)

    if st.checkbox('Zeige Rohdaten'):
        st.write(df)

    numeric_columns = df.select_dtypes(['number']).columns.tolist()

    if len(numeric_columns) >= 2:
        selected_columns = st.multiselect('Wähle zwei Spalten für das Dashboard', numeric_columns, default=numeric_columns[:2])
        if len(selected_columns) == 2:
            col1, col2 = selected_columns


            st.subheader('Streudiagramm')
            fig, ax = plt.subplots()
            ax.scatter(df[selected_columns[0]], df[selected_columns[1]])
            ax.set_xlabel(selected_columns[0])
            ax.set_ylabel(selected_columns[1])
            st.pyplot(fig)

            st.subheader('Linien-Diagramm')
            fig, ax = plt.subplots()
            ax.plot(df[selected_columns[0]], label=selected_columns[0])
            ax.plot(df[selected_columns[1]], label=selected_columns[1])
            ax.legend()
            st.pyplot(fig)

            st.subheader('Histogramme')
            fig, axs = plt.subplots(1, 2, figsize=(10, 5))
            axs[0].hist(df[selected_columns[0]], bins=20)
            axs[0].set_title(selected_columns[0])
            axs[1].hist(df[selected_columns[1]], bins=20)
            axs[1].set_title(selected_columns[1])
            st.pyplot(fig)

            st.subheader('Boxplots')
            fig, axs = plt.subplots(1, 2, figsize=(10, 5))
            sns.boxplot(y=df[selected_columns[0]], ax=axs[0])
            axs[0].set_title(selected_columns[0])
            sns.boxplot(y=df[selected_columns[1]], ax=axs[1])
            axs[1].set_title(selected_columns[1])
            st.pyplot(fig)

            st.subheader(f'Tortendiagramm für {col1}')
            bins = pd.cut(df[col1], bins=4)
            bin_counts = bins.value_counts()
            fig, ax = plt.subplots()
            ax.pie(bin_counts, labels=bin_counts.index, autopct='%1.1f%%', startangle=90)
            ax.axis(
                'equal')
            st.pyplot(fig)

            st.subheader('Dichtediagramm (KDE Plot)')
            fig, ax = plt.subplots()
            sns.kdeplot(data=df, x=col1, y=col2, ax=ax, cmap="Reds", shade=True)
            ax.set_title(f'Dichtediagramm von {col1} und {col2}')
            st.pyplot(fig)

            st.subheader('Hexbin Plot')
            fig, ax = plt.subplots()
            ax.hexbin(df[col1], df[col2], gridsize=30, cmap='Purples')
            ax.set_xlabel(col1)
            ax.set_ylabel(col2)
            plt.colorbar(ax.hexbin(df[col1], df[col2], gridsize=30, cmap='Purples'))
            st.pyplot(fig)

            st.subheader('Violin Plot')
            fig, ax = plt.subplots(1, 2, figsize=(12, 6))
            sns.violinplot(y=df[col1], ax=ax[0], inner='quartile')
            sns.violinplot(y=df[col2], ax=ax[1], inner='quartile')
            ax[0].set_title(f'Violin Plot von {col1}')
            ax[1].set_title(f'Violin Plot von {col2}')
            st.pyplot(fig)

        else:
            st.error('Bitte genau zwei Spalten auswählen.')
    else:
        st.error('Die CSV-Datei muss mindestens zwei numerische Spalten enthalten.')