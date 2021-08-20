from django.core.mail import send_mail


def send_activation_code(email, activation_code, status=None):
    if status == 'register':
        activation_url = f'http://localhost:8000/api/account/activate/{activation_code}'
        message = f"Поздравляем! Вы успешно зарегистрированы! Перейдите по ссылке для активации аккаунта: {activation_url}"

        send_mail(
            'Idea-X. Активация аккаунта',
            message,
            'admin.idea-x@gmail.com',
            [email, ],
            fail_silently=False
        )

    elif status == 'reset_password':
        send_mail(
            'Idea-X. Сброс пароля',
            f'Ваш код активации: {activation_code}',
            'admin.idea-x@gmail.com',
            [email, ],
            fail_silently=False,
        )