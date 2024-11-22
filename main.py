import os
import requests


def get_cat_images(api_key, limit=1, save_dir="img"):
    api_url = f"https://api.thecatapi.com/v1/images/search?limit={limit}"

    try:
        # Указываем заголовки с API-ключом
        headers = {"x-api-key": api_key}
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            # Получаем список изображений из ответа
            images = response.json()

            # Проверяем, существует ли папка, и создаём её, если необходимо
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            saved_images = []
            for img in images:
                # Получаем URL изображения
                image_url = img["url"]
                # Генерируем имя файла
                image_name = os.path.basename(image_url)
                image_path = os.path.join(save_dir, image_name)

                # Скачиваем изображение и сохраняем
                img_response = requests.get(image_url, stream=True)
                if img_response.status_code == 200:
                    with open(image_path, "wb") as file:
                        for chunk in img_response.iter_content(1024):
                            file.write(chunk)
                    saved_images.append(image_path)
                    print(f"Изображение сохранено: {image_path}")
                else:
                    print(f"Ошибка загрузки изображения: {image_url}")

            return saved_images

        else:
            print(f"Ошибка: статус-код {response.status_code}")
            return []

    except requests.RequestException as e:
        print(f"Произошла ошибка: {e}")
        return []


if __name__ == "__main__":
    # Укажите ваш API-ключ
    api_key = "live_iOASwwIOjqq1NE1pRJKUKyPeCBxlz5XE4NOcPgvHOtWuWXgimPtLWqHHn1Fi1m7L"

    # Получить и сохранить 5 изображений кошек
    saved_images = get_cat_images(api_key, limit=5)
    if saved_images:
        print("Сохранённые изображения:")
        for path in saved_images:
            print(path)
    else:
        print("Не удалось сохранить изображения.")
