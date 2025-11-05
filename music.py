import requests
import os
import pandas as pd
from bs4 import BeautifulSoup as bs
import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
# Прямая ссылка на MP3-файл
def find_track(search):
    search = search.replace(' ', '%20')
    url = f'https://rus.hitmotop.com/search?q={search}'
    list = []
    try:
        page = requests.get(url)
    except:
        print("Страница недоступна!")
    soup = bs(page.text, "html.parser")
    tracks = soup.find("ul", class_="tracks__list")
    try:
        for track in tracks.find_all("li"):
            track_info = track.find("div",class_="track__info")
            track_name = track_info.find("div",class_="track__title").text.strip()
            track_desk = track_info.find("div",class_="track__desc").text
            track_time = track_info.find("div",class_="track__fulltime").text
            track_href = track_info.find("div",class_="track__info-r").find("a").get("href")
            print(track_name, track_desk, track_time, track_href)
            list.append([track_name, track_desk, track_time, track_href])
    except:
        print("Трек не найден!")
    return list
def download_music(url):
    url = 'https://rus.hitmotop.com/get/music/20170904/Mikhail_Krug_-_raer_48113874.mp3'

    try:
        # Скачиваем файл
        print("Начинаем загрузку трека...")
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Проверяем статус ответа

        # Создаем папку для загрузок
        os.makedirs('downloads', exist_ok=True)

        # Извлекаем название файла из URL
        filename = os.path.join('downloads', url.split('/')[-1])

        # Сохраняем файл с прогрессом
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0

        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        progress = (downloaded / total_size) * 100
                        print(f"Прогресс: {progress:.1f}%", end='\r')

        print(f"\nТрек успешно скачан: {filename}")
        print(f"Размер файла: {downloaded} байт")

    except Exception as e:
        print(f"Ошибка при скачивании: {e}")

#download_music("https://rus.hitmotop.com/get/music/20170904/Mikhail_Krug_-_raer_48113874.mp3")
st.set_page_config(page_title="Music Searcher", layout="wide")
st.title("🎵 Поиск и скачивание музыки")

# Поиск треков
search_query = st.text_input("Введите название трека для поиска:")
if st.button("Найти") and search_query:
    with st.spinner("Ищем треки..."):
        try:
            results = find_track(search_query)

            if results:
                st.success(f"Найдено треков: {len(results)}")

                # Выбор трека для скачивания
                track_names = [f"{row[0]} - {row[1]}" for row in results]
                selected_track = st.selectbox("Выберите трек для скачивания:", track_names)

                if selected_track:
                    track_index = track_names.index(selected_track)
                    download_url = results[track_index][3]
                    if st.button("Скачать выбранный трек"):
                        with st.spinner("Скачиваем..."):
                            try:
                                # Получаем бинарные данные трека
                                download_music(download_url)

                            except Exception as e:
                                st.error(f"Ошибка при скачивании: {str(e)}")
            else:
                st.warning("Ничего не найдено")

        except Exception as e:
            st.error(f"Ошибка при поиске: {str(e)}")

#streamlit run music.py