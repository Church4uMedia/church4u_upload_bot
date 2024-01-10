class L10n:

    start_message = (
        "{}, привет.\n\nЭто Church4u Youtube Uploader бот. Ты можешь с моей помощью загружать любое видео на Youtube"
        "По команде /help можно узать больше моих возможностей.\n\nСпасибо."
    )
    
    not_a_reply_msg = "Пожалуйста, \"Ответь\" (Reply) на сообщение с видеофайлом. В подписи к видео укажите его название."
    not_a_media_msg = "Не получается здесь найти видео. Пожалуйста, \"Ответь\" (Reply) на сообщение с видеофайлом. В подписи к видео укажите его название."
    not_a_valid_media_msg = "Формат видеосообщения не поддерживается ботом."
    not_a_title_msg = "Не получается найти название видео."

    processing = "Обработка....."
    
    downloading = "Загружаю медиафаил локально....."
    downloading_failed = "Загрузка завершилась с ошибкой!\n\nДетали ошибки: {}"
    downloading_success = "Загрузка локально завершена успешно!"
    downloading_report = "{}\n\n{}% готово.\n{} из {}\nСкорость: {} {}PS"

    uploading = "Загрузка в Youtube....."
    uploading_failed = "Загрузка в Youtube завершилась с ошибкой!\n\nДетали ошибки: {}"
    uploading_success = "Загрузка в Youtube завершена!\n\nСсылка на видео: [{}](https://youtu.be/{})"

    default_media_description = (
        "Оставайтесь на связи:\n"
        "YouTube: www.youtube.com/church4uby\n"
        "Facebook: www.facebook.com/brest.center.1\n"
        "Twitter: www.twitter.com/church4ubrest\n"
        "ВКонтакте: www.vk.com/church4u\n"
        "Instagram: www.instagram.com/church4u.by\n"
        "\n"
        "На канале не допускается ненормативная лексика, оскорбления, унижения личности и достоинства человека.\n"
    )
    default_media_tags = ["#church4u", "#art", "#handmade"]    

    cancel_button = "Отмена!"
    cancel_process_is_not_active = "Нет активных процессов загрузки!"
    cancel_will_be_cancelled = "Процесс скоро будет завершен!"