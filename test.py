import pytest
import os
from main import get_cat_images

def test_get_cat_images_success(mocker):

    # Мокируем ответ от requests.get
    mock_response = mocker.patch("requests.get")

    # Настраиваем успешный ответ от API
    mock_response.return_value.status_code = 200
    mock_response.return_value.json.return_value = [
        {"url": "https://cdn2.thecatapi.com/images/abc123.jpg"},
        {"url": "https://cdn2.thecatapi.com/images/xyz789.jpg"}
    ]

    # Настраиваем успешный ответ для скачивания изображения
    def mock_stream(*args, **kwargs):
        return b"mock image content"

    mock_response.return_value.iter_content = lambda chunk_size: [mock_stream()]

    # Вызываем функцию
    api_key = "fake_api_key"
    saved_images = get_cat_images(api_key, limit=2, save_dir="test_img")

    # Проверяем, что файлы сохранены с ожидаемыми именами
    assert len(saved_images) == 2
    assert os.path.join("test_img", "abc123.jpg") in saved_images
    assert os.path.join("test_img", "xyz789.jpg") in saved_images
