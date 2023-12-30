import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response=requests.get("https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies=[]
    recommended_movies_posters=[]
    for i in distances[1:6]:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters
movies_list=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_list)

similarity=pickle.load(open('similarity.pkl','rb'))

st.title("Film Tavsiye Sistemi")

movies_list=movies_list['title'].values


selected_movie_name=st.selectbox('Hangi Filmi Seçmek İstersiniz ?',
                    movies['title'].values)
if st.button('ÖNER'):
    st.subheader(f"'{selected_movie_name}' için önerilen filmler:")
    names, posters = recommend(selected_movie_name)
    columns = st.columns(5)
    for i in range(5):
        with columns[i]:
            st.text(names[i])
            st.image(posters[i])


def set_background(image_path):
    background_style = f"""
        <style>
        body {{
            background-image: url('{image_path}');
            background-size: cover;
        }}
        </style>
    """
    st.markdown(background_style, unsafe_allow_html=True)

background_image_path = "360_F_286323187_mDk3N4nGDaPkUmhNcdBe3RjSOfKqx4nZ.jpg"
set_background(background_image_path)

st.markdown(
        """
        <div class="footer">
            <div class="grid-container">
                <div class="grid-item">
                    <div class="name">Hasan Can Çelik</div>
                    <div class="links">
                        <a href="https://github.com/HasanCan6241" target="_blank">GitHub</a>
                        <a href="https://www.linkedin.com/in/hasan-can-%C3%A7elik-46950623b/" target="_blank">LinkedIn</a>
                        <a href="https://www.kaggle.com/hasancanelik" target="_blank">Kaggle</a>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
